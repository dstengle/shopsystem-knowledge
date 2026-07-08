"""The adversarial pass: a covered / contradicts / supersedes verdict per neighbour.

The authoring-time discovery pass (:mod:`knowledge.discovery`) surfaces the
existing decisions relevant to a draft. This module stands up the step that runs
next: the **adversarial pass**. Over a draft and the set of neighbours discovery
surfaced, it assigns EXACTLY ONE :class:`Verdict` per surfaced neighbour — is the
draft *covered by*, does it *contradict*, or does it *supersede* that neighbour —
and every verdict CITES the neighbour it is about BY ID. It is the primary
coherence mechanism (adversarial authoring), not a tier-3 formal-invariant check.

Two properties define the pass:

* **One cited verdict per surfaced neighbour.** The result carries exactly one
  :class:`Verdict` per neighbour, each citing a distinct ``neighbour_id``; the
  set of cited ids equals the set of surfaced neighbour ids. Nothing is dropped
  and nothing is double-cited.

* **Reasoned from decision text, no baseline.** Each verdict is derived
  deterministically from the neighbour's L0/L1 material (its verbatim L1 extract)
  and the draft's own decision text — with NO pre-encoded invariants or stored
  baselines, and WITHOUT re-loading the whole corpus (the pass takes the surfaced
  neighbours, never the sources).

Classification is explicit and deterministic so the downstream covered /
contradict / supersede case behaviours can each force one specific verdict. For a
neighbour, the pass looks at the draft's **span** — the draft sentences that
mention that neighbour's shared subject tokens (its ``overlap``) — and applies
this ordered ladder (first match wins):

1. **supersedes** — the span replaces the prior decision: it carries a
   *replacement* marker (e.g. ``replaces``, ``supersedes``, ``instead of``,
   ``no longer``, ``deprecate``). The draft withdraws the neighbour's decision.

2. the span makes a **parity claim** about the subject (e.g. ``unchanged``,
   ``keeps``, ``stays``, ``same``, ``preserve``, ``matches the existing``):

   a. **contradicts** — if the neighbour's own decision text is a *governed
      change* (its L1 extract carries a change marker such as ``change``,
      ``reduce``, ``invalidate``, ``no longer``, ``instead``). The parity claim
      is denied by the neighbour's governed change — established from the
      neighbour's decision text alone, with no stored baseline.

   b. **covered** — otherwise. The neighbour's decision is stable, so the draft's
      parity claim holds: the question is already decided the same way, and the
      draft is covered by the existing decision.

3. **covered** — the span *restates* the neighbour's decision: the neighbour's
   directive tokens are all present in the span (an implicit parity claim) and
   the neighbour is not a governed change.

4. **none** — the subjects overlap but none of the three relationships hold.

The three case fixtures land their verdict like so: put a **replacement** marker
in the draft sentence about the neighbour's subject for *supersedes*; make the
draft **claim parity** on a subject whose neighbour decision text is a **change**
for *contradicts*; make the draft **claim parity (or restate)** a subject whose
neighbour decision is **stable** for *covered*.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping

from knowledge.discovery import (
    DraftDecision,
    Neighbour,
    _topic_tokens,
    build_l0l1_index,
    run_authoring_discovery,
)


class VerdictKind(str, Enum):
    """The verdict the adversarial pass assigns to a surfaced neighbour.

    ``COVERED``/``CONTRADICTS``/``SUPERSEDES`` are the three coherence relations
    the pass answers; ``NONE`` is the neutral outcome for a neighbour that shares
    the draft's subject but stands in none of those three relations to it.
    """

    COVERED = "covered"
    CONTRADICTS = "contradicts"
    SUPERSEDES = "supersedes"
    NONE = "none"


# The draft withdraws/replaces the neighbour's prior decision on the subject.
_REPLACEMENT_MARKERS: tuple[str, ...] = (
    "replaces", "replace", "replacing", "supersede", "supersedes", "superseding",
    "instead of", "no longer", "deprecate", "deprecates", "retire", "retires",
)

# The draft claims the subject is unchanged / kept / matches the existing decision.
_PARITY_MARKERS: tuple[str, ...] = (
    "unchanged", "keeps", "keep", "keeping", "stays", "stay", "same",
    "preserve", "preserves", "preserving", "still", "continue", "continues",
    "matches", "matching", "as before", "parity",
)

# The neighbour's OWN decision text is a governed change to the subject surface.
_GOVERNED_CHANGE_MARKERS: tuple[str, ...] = (
    "change", "changes", "changed", "reduce", "reduces", "reduced",
    "increase", "increases", "increased", "invalidate", "invalidates",
    "no longer", "instead", "replace", "replaces", "drop", "drops", "differs",
)


def _sentences(text: str) -> tuple[str, ...]:
    """Split ``text`` into candidate sentences on newline and sentence punctuation.

    Deterministic and ambient-free — it reads only its argument. Empty fragments
    are dropped so a blank line or a trailing period contributes no span.
    """
    parts = re.split(r"[.\n]+", text)
    return tuple(part.strip() for part in parts if part.strip())


def _contains_marker(text_lower: str, markers: Iterable[str]) -> str | None:
    """Return the first marker in ``markers`` present in ``text_lower``, else None.

    Single-word markers match on token boundaries so ``change`` does not fire on
    ``unchanged``; multi-word markers (``no longer``) match as substrings.
    """
    for marker in markers:
        if " " in marker:
            if marker in text_lower:
                return marker
        elif re.search(rf"\b{re.escape(marker)}\b", text_lower):
            return marker
    return None


@dataclass(frozen=True)
class Verdict:
    """One adversarial verdict about the draft's relation to a surfaced neighbour.

    ``neighbour_id`` is the citation — the id of the neighbour this verdict is
    about. ``verdict`` is the :class:`VerdictKind`. The remaining fields are the
    explainable evidence the verdict was reasoned from: ``subject`` (the shared
    topic tokens establishing which governed surface it concerns), ``l1_extract``
    (the neighbour's verbatim L1 decision text — the cited material), ``rationale``
    (a human-readable explanation), and ``matched_markers`` (the decision-text
    markers that drove the classification). It carries no L2 body.
    """

    neighbour_id: str
    verdict: VerdictKind
    subject: tuple[str, ...]
    l1_extract: str
    rationale: str
    matched_markers: tuple[str, ...]


@dataclass(frozen=True)
class SupersedeEdge:
    """A typed supersede edge the draft owes to a prior decision it replaces.

    Named on top of a SUPERSEDES verdict: the draft being authored (``from_``)
    supersedes the prior decision (``to`` — the neighbour id the verdict cited),
    under the relation ``edge_type`` (the constant ``"supersedes"``). It is a
    thin, deterministic derivation from an existing SUPERSEDES verdict and the
    pass's draft id — it introduces NO new classification and reads no baseline.
    """

    from_: str
    to: str
    edge_type: str = "supersedes"


@dataclass(frozen=True)
class AdversarialResult:
    """The outcome of one adversarial pass: exactly one verdict per neighbour.

    ``verdicts`` holds one :class:`Verdict` per surfaced neighbour, in the order
    the neighbours were supplied. Each cites a distinct neighbour id, so the set
    of cited ids equals the set of surfaced neighbour ids. ``draft_id`` is the id
    of the draft the pass reasoned over — the ``from_`` endpoint of any supersede
    edge the draft owes (see :meth:`supersede_edges`).
    """

    verdicts: tuple[Verdict, ...]
    draft_id: str = ""

    def cited_ids(self) -> tuple[str, ...]:
        """Return the cited neighbour ids, in verdict order."""
        return tuple(verdict.neighbour_id for verdict in self.verdicts)

    def for_id(self, neighbour_id: str) -> Verdict:
        """Return the verdict citing ``neighbour_id``.

        Raises :class:`KeyError` if no verdict cites that id — the pass only ever
        cites surfaced neighbours, so an unknown id is a caller error.
        """
        for verdict in self.verdicts:
            if verdict.neighbour_id == neighbour_id:
                return verdict
        raise KeyError(neighbour_id)

    def supersede_edges(self) -> tuple[SupersedeEdge, ...]:
        """Return the typed supersede edges the draft owes, in verdict order.

        One :class:`SupersedeEdge` per SUPERSEDES verdict — nothing more. Each
        edge is derived deterministically from a SUPERSEDES verdict: it runs
        FROM the draft being authored (``draft_id``) TO the prior decision the
        verdict cited (``neighbour_id``), typed ``"supersedes"``. It names the
        edge the existing verdict already implies; it runs no new classification.
        """
        return tuple(
            SupersedeEdge(from_=self.draft_id, to=verdict.neighbour_id)
            for verdict in self.verdicts
            if verdict.verdict == VerdictKind.SUPERSEDES
        )


def _classify(draft: DraftDecision, neighbour: Neighbour) -> Verdict:
    """Classify the draft's relation to one surfaced ``neighbour``.

    The subject is the neighbour's ``overlap`` (the shared topic tokens discovery
    already computed). The draft's **span** is the union of the draft sentences
    that mention any subject token; markers are detected across that span. The
    ordered ladder in the module docstring decides the verdict. Deterministic:
    the function reads only the draft, the neighbour, and the module's marker
    tables — no wall clock, environment, or ambient state.
    """
    subject = neighbour.overlap
    subject_set = set(subject)

    draft_text = f"{draft.title}\n{draft.description}\n{draft.body}"
    span_sentences = [
        sentence
        for sentence in _sentences(draft_text)
        if _topic_tokens(sentence) & subject_set
    ]
    span = "\n".join(span_sentences)
    span_lower = span.lower()
    span_tokens = _topic_tokens(span)

    neighbour_lower = neighbour.l1_extract.lower()
    neighbour_directive = _topic_tokens(neighbour.l1_extract)
    neighbour_change = _contains_marker(neighbour_lower, _GOVERNED_CHANGE_MARKERS)

    replacement = _contains_marker(span_lower, _REPLACEMENT_MARKERS)
    parity = _contains_marker(span_lower, _PARITY_MARKERS)
    restates = bool(neighbour_directive) and neighbour_directive <= span_tokens

    if replacement is not None:
        kind = VerdictKind.SUPERSEDES
        markers = (replacement,)
        rationale = (
            f"the draft replaces {neighbour.id}'s decision on "
            f"{'/'.join(subject)} ('{replacement}')"
        )
    elif parity is not None:
        if neighbour_change is not None:
            kind = VerdictKind.CONTRADICTS
            markers = (parity, neighbour_change)
            rationale = (
                f"the draft claims parity on {'/'.join(subject)} ('{parity}'), but "
                f"{neighbour.id}'s decision is a governed change ('{neighbour_change}')"
            )
        else:
            kind = VerdictKind.COVERED
            markers = (parity,)
            rationale = (
                f"the draft claims parity on {'/'.join(subject)} ('{parity}') and "
                f"{neighbour.id}'s decision is stable — already decided the same way"
            )
    elif restates and neighbour_change is None:
        kind = VerdictKind.COVERED
        markers = ()
        rationale = (
            f"the draft restates {neighbour.id}'s decision on {'/'.join(subject)} "
            "— already decided the same way"
        )
    else:
        kind = VerdictKind.NONE
        markers = ()
        rationale = (
            f"the draft and {neighbour.id} share {'/'.join(subject)} but stand in "
            "no covered/contradicts/supersedes relation"
        )

    return Verdict(
        neighbour_id=neighbour.id,
        verdict=kind,
        subject=subject,
        l1_extract=neighbour.l1_extract,
        rationale=rationale,
        matched_markers=markers,
    )


def run_adversarial_pass(
    draft: DraftDecision, neighbours: Iterable[Neighbour]
) -> AdversarialResult:
    """Run the adversarial pass over ``draft`` against the surfaced ``neighbours``.

    For each surfaced neighbour the pass assigns exactly one :class:`Verdict` —
    covered / contradicts / supersedes / none — citing that neighbour BY ID and
    carrying the evidence it reasoned from (the shared subject and the neighbour's
    verbatim L1 extract). It consumes ONLY the draft and the neighbours (never the
    sources), so it structurally cannot re-load the whole corpus.

    Parameters
    ----------
    draft:
        The decision being authored.
    neighbours:
        The neighbours surfaced by :func:`knowledge.discovery.run_authoring_discovery`.

    Returns
    -------
    AdversarialResult
        One verdict per surfaced neighbour, in the order supplied; the set of
        cited ids equals the set of surfaced neighbour ids.
    """
    verdicts = tuple(_classify(draft, neighbour) for neighbour in neighbours)
    return AdversarialResult(verdicts=verdicts, draft_id=draft.id)


def authoring_time_review(
    sources: Mapping[str, str], draft: DraftDecision
) -> AdversarialResult:
    """Run the authoring-time review of ``draft`` over the ``sources`` corpus.

    A thin composition of the two existing passes — it introduces no new
    classification logic. It projects the source corpus down to its L0/L1 index
    (:func:`~knowledge.discovery.build_l0l1_index`), surfaces the neighbours
    relevant to the draft (:func:`~knowledge.discovery.run_authoring_discovery`),
    then runs the adversarial pass (:func:`run_adversarial_pass`) over the draft
    and those surfaced neighbours. The result carries exactly one verdict per
    surfaced neighbour, each citing that neighbour BY ID — so a draft that
    restates a stable existing decision the same way is flagged COVERED, citing
    the covering decision.

    Parameters
    ----------
    sources:
        The existing decision corpus — a mapping of document key to full source
        text (the shape :func:`build_l0l1_index` consumes).
    draft:
        The decision being authored.

    Returns
    -------
    AdversarialResult
        One verdict per surfaced neighbour, citing each by id.
    """
    index = build_l0l1_index(sources)
    discovery = run_authoring_discovery(index, draft)
    return run_adversarial_pass(draft, discovery.neighbours)
