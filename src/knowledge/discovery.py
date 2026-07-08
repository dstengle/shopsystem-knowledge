"""Authoring-time discovery of relevant neighbours via the L0/L1 index.

This module stands up the **authoring-time discovery pass**: when a decision is
being authored, the knowledge context surfaces the existing decisions relevant
to the draft so a coherence pass can reason about them. It is the FIRST
behaviour of the authoring-discovery family and the primary coherence mechanism
the verdict / covered / contradict / supersede passes build on.

Two properties define the pass, and both are observable:

* **Relevant subset, named by id.** Given the existing corpus and a draft on a
  topic that overlaps only a *subset* of it, :func:`run_authoring_discovery`
  surfaces exactly that subset — each neighbour named by id — and excludes a
  decision whose topic does not overlap the draft. Relevance is a simple,
  deterministic, explainable overlap signal: the shared topic tokens between the
  draft and each candidate's L0/L1 material (no ML, no ambient state). Every
  surfaced :class:`Neighbour` carries the ``overlap`` tokens that explain *why*
  it is relevant.

* **Index-not-whole-corpus.** The pass selects neighbours from the **L0/L1
  index** — each existing decision's L0 card and L1 extract — rather than
  loading the whole corpus (the L2 bodies) into the pass. :class:`L0L1Index` is
  the boundary that drops L2: :func:`build_l0l1_index` projects the source
  corpus down to L0 cards + L1 extracts, and :func:`run_authoring_discovery`
  consumes only that index and the draft. Neither the index entries nor the
  surfaced neighbours carry an L2 body, so the pass structurally cannot reach a
  whole-corpus body.

Each surfaced neighbour still carries enough — its id, its L0 card, and its
verbatim L1 extract — for a downstream adversarial pass (the verdict sub-issue)
to attach a covered / contradicts / supersedes verdict citing the neighbour by
id, WITHOUT re-loading the whole corpus.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping

from knowledge.projections import L0Card, generate_projections

# Topic tokens are lowercase alphanumeric runs. Generic English glue and a few
# ADR-boilerplate words are dropped so relevance turns on shared *topic* words
# rather than on structural filler every decision carries. The set is small and
# explicit — the overlap signal must stay deterministic and explainable.
_STOPWORDS: frozenset[str] = frozenset(
    {
        "a", "an", "and", "are", "as", "at", "be", "between", "by", "does",
        "every", "first", "for", "from", "in", "into", "is", "it", "its", "not",
        "of", "on", "onto", "or", "over", "rather", "so", "than", "that", "the",
        "then", "there", "these", "this", "to", "up", "was", "which", "with",
        # ADR-structural boilerplate that carries no topic signal:
        "decision", "consequences", "adopt", "keep",
    }
)


def _topic_tokens(text: str) -> frozenset[str]:
    """Return the set of topic tokens in ``text``.

    Tokens are lowercase alphanumeric runs of length >= 2 with the stopwords in
    :data:`_STOPWORDS` removed. The function reads only its argument — no wall
    clock, environment, or ambient state — so the overlap signal is
    deterministic.
    """
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return frozenset(t for t in tokens if len(t) >= 2 and t not in _STOPWORDS)


@dataclass(frozen=True)
class DraftDecision:
    """A decision being authored, before it enters the corpus.

    The draft carries the same authored fields a source document would — an
    ``id`` (a provisional handle), a ``title`` and ``description`` (its L0-level
    facts), and a ``body`` (its decision prose). The discovery pass reads the
    draft's ``title``, ``description`` and ``body`` as the topic material it
    matches against the L0/L1 index.
    """

    id: str
    title: str
    description: str
    body: str

    def topic_tokens(self) -> frozenset[str]:
        """Return the draft's topic tokens (title + description + body)."""
        return _topic_tokens(f"{self.title}\n{self.description}\n{self.body}")


@dataclass(frozen=True)
class L0L1IndexEntry:
    """One existing decision's L0 card + L1 extract — and pointedly NO L2 body.

    This is the unit the discovery pass selects on. It carries the ``id`` (drawn
    from the L0 card), the :class:`~knowledge.projections.L0Card` itself, and the
    verbatim ``l1_extract`` text. It deliberately exposes no L2 attribute: the
    whole-corpus body is dropped at :func:`build_l0l1_index`, so it can never be
    reached through an index entry.
    """

    id: str
    l0: L0Card
    l1_extract: str

    def topic_tokens(self) -> frozenset[str]:
        """Return this entry's topic tokens (L0 title + description + L1 extract)."""
        return _topic_tokens(
            f"{self.l0.title}\n{self.l0.description}\n{self.l1_extract}"
        )


@dataclass(frozen=True)
class L0L1Index:
    """The L0/L1 index: every existing decision's L0 card + L1 extract.

    This is the whole input the discovery pass reads besides the draft. Because
    it holds only :class:`L0L1IndexEntry` values — L0 cards and L1 extracts, no
    L2 bodies — the pass that consumes it structurally cannot load the whole
    corpus. Entries are held in sorted id order for a deterministic scan.
    """

    entries: tuple[L0L1IndexEntry, ...]

    def ids(self) -> tuple[str, ...]:
        """Return the indexed decision ids, in the index's sorted order."""
        return tuple(entry.id for entry in self.entries)


@dataclass(frozen=True)
class Neighbour:
    """An existing decision surfaced as relevant to the draft, named by id.

    Carries exactly what a downstream adversarial pass needs to cite it BY ID
    without re-loading the whole corpus: its ``id``, its
    :class:`~knowledge.projections.L0Card`, and its verbatim ``l1_extract``. The
    ``overlap`` tuple is the explainable relevance signal — the shared topic
    tokens between the draft and this neighbour's L0/L1 material — and ``score``
    is their count. It carries no L2 body.
    """

    id: str
    l0: L0Card
    l1_extract: str
    overlap: tuple[str, ...]
    score: int


@dataclass(frozen=True)
class DiscoveryResult:
    """The outcome of one authoring-time discovery pass over a draft.

    ``neighbours`` holds the surfaced existing decisions relevant to the draft,
    ordered by descending relevance ``score`` then by ``id`` — a total,
    deterministic order. An empty tuple means nothing in the corpus overlapped
    the draft's topic.
    """

    neighbours: tuple[Neighbour, ...]

    def ids(self) -> tuple[str, ...]:
        """Return the surfaced neighbour ids in surfaced (relevance) order."""
        return tuple(neighbour.id for neighbour in self.neighbours)


def build_l0l1_index(sources: Mapping[str, str]) -> L0L1Index:
    """Project a source corpus down to its L0/L1 index — dropping the L2 bodies.

    Each source is run through :func:`~knowledge.projections.generate_projections`
    and only its L0 card and L1 extract are retained; the L2 body is discarded.
    The returned :class:`L0L1Index` is therefore the corpus's L0/L1 material and
    nothing more — the boundary that lets the discovery pass select neighbours
    from L0/L1 without ever holding the whole corpus.

    Parameters
    ----------
    sources:
        A mapping of document key to that document's full source text — the same
        corpus shape the projection generator consumes.

    Returns
    -------
    L0L1Index
        Entries in sorted id order, each carrying an id + L0 card + L1 extract.
    """
    entries: list[L0L1IndexEntry] = []
    for source in sources.values():
        bundle = generate_projections(source)
        entries.append(
            L0L1IndexEntry(
                id=bundle.l0.id,
                l0=bundle.l0,
                l1_extract=bundle.l1.text,
            )
        )
    entries.sort(key=lambda entry: entry.id)
    return L0L1Index(entries=tuple(entries))


def run_authoring_discovery(index: L0L1Index, draft: DraftDecision) -> DiscoveryResult:
    """Run the authoring-time discovery pass over ``draft`` against ``index``.

    The pass consumes ONLY the L0/L1 ``index`` and the ``draft`` — it takes no
    corpus/sources parameter, so it structurally cannot load the whole corpus
    into the pass. For each index entry it computes the shared topic tokens
    between the draft and the entry's L0/L1 material; an entry with at least one
    shared token is surfaced as a :class:`Neighbour` carrying that overlap. A
    decision whose topic does not overlap the draft is not surfaced.

    Neighbours are returned ordered by descending overlap ``score`` then by
    ``id`` — a deterministic, ambient-free order.

    Parameters
    ----------
    index:
        The L0/L1 index of existing decisions (see :func:`build_l0l1_index`).
    draft:
        The decision being authored.

    Returns
    -------
    DiscoveryResult
        The surfaced neighbours, each named by id and carrying its L0 card, its
        verbatim L1 extract, and the explainable overlap signal.
    """
    draft_tokens = draft.topic_tokens()

    neighbours: list[Neighbour] = []
    for entry in index.entries:
        shared = draft_tokens & entry.topic_tokens()
        if not shared:
            continue
        overlap = tuple(sorted(shared))
        neighbours.append(
            Neighbour(
                id=entry.id,
                l0=entry.l0,
                l1_extract=entry.l1_extract,
                overlap=overlap,
                score=len(overlap),
            )
        )

    neighbours.sort(key=lambda neighbour: (-neighbour.score, neighbour.id))
    return DiscoveryResult(neighbours=tuple(neighbours))
