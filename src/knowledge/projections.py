"""Single-source projection generation.

The public entry point is :func:`generate_projections`, which turns one source
decision document (YAML frontmatter + Markdown body) into the full set of
architecture-decision projections:

* an **L0 card** carrying the ``id``, ``title``, ``status`` and ``description``
  drawn from the frontmatter;
* an **L1 extract** carrying the verbatim text of the recognized decision
  section from the body;
* an **L2 projection** that is the source document itself;
* a **machine index entry** and a **human index entry**, both derived from the
  same frontmatter.

No projection introduces a fact that is not present in the single source, and
generation is deterministic: it reads only ``source`` and emits no timestamps,
hostnames, or absolute paths.

Generation is **convention-gated**: a document whose body carries none of the
:data:`RECOGNIZED_DECISION_HEADINGS` is reported as non-conforming — via
:class:`NonConformingDocumentError` — rather than projected into a bundle with a
silently empty L1 extract. Later sub-issues (byte-stability, idempotent regen,
kind-parameterized accessor) extend this module, so frontmatter parsing and
recognized-heading detection are factored into the named helpers
:func:`parse_frontmatter`, :data:`RECOGNIZED_DECISION_HEADINGS`,
:func:`has_recognized_decision_heading`, and :func:`extract_decision_section`.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

# The set of Markdown section headings recognized as the decision section whose
# body becomes the L1 extract. Factored into a named constant so the
# convention-gating sub-issue can reuse (and extend) exactly this set rather
# than duplicating the recognition rule.
RECOGNIZED_DECISION_HEADINGS: tuple[str, ...] = (
    "## Decision",
    "## Decision Outcome",
)

# The frontmatter delimiter line (YAML front matter fence).
_FRONTMATTER_FENCE = "---"


class NonConformingDocumentError(ValueError):
    """A source document lacks a recognized decision-section heading.

    Convention-gating (this sub-issue): rather than silently emitting an empty
    L1 extract, :func:`generate_projections` refuses to project a document whose
    body carries none of the headings in :data:`RECOGNIZED_DECISION_HEADINGS`
    and reports it as non-conforming, naming the missing convention.

    The error carries the offending document's ``document_id`` (drawn from the
    frontmatter ``id``, or ``None`` when absent) and a human-readable
    ``reason`` so later sub-issues — notably the kind-parameterized accessor —
    can surface *which* document was rejected and *why* without re-deriving the
    recognition rule.
    """

    def __init__(self, document_id: str | None) -> None:
        self.document_id = document_id
        self.reason = "lacks a recognized decision heading"
        which = document_id if document_id else "<unknown id>"
        super().__init__(
            f"document {which} is non-conforming: it {self.reason}; its body "
            f"carries none of the recognized decision headings "
            f"{list(RECOGNIZED_DECISION_HEADINGS)}"
        )


@dataclass(frozen=True)
class L0Card:
    """The L0 card: the machine-truth fields drawn verbatim from frontmatter."""

    id: str
    title: str
    status: str
    description: str


@dataclass(frozen=True)
class L1Extract:
    """The L1 extract: the verbatim body of the recognized decision section."""

    text: str


@dataclass(frozen=True)
class ProjectionBundle:
    """The full set of projections generated from one source document."""

    l0: L0Card
    l1: L1Extract
    l2: str
    machine_index_entry: Mapping[str, str]
    human_index_entry: str


def parse_frontmatter(source: str) -> dict[str, str]:
    """Parse the leading YAML frontmatter block into a ``key -> value`` map.

    Only the simple ``key: value`` frontmatter this context authors is
    supported. Each returned value is the verbatim text that appears in
    ``source`` (leading/trailing whitespace around the value trimmed), so every
    parsed fact is a substring of the source document — the no-new-facts
    invariant holds by construction.

    Parameters
    ----------
    source:
        The full source document, opening with a ``---`` frontmatter fence.

    Returns
    -------
    dict[str, str]
        The parsed frontmatter fields.
    """
    lines = source.splitlines()
    if not lines or lines[0].strip() != _FRONTMATTER_FENCE:
        return {}

    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == _FRONTMATTER_FENCE:
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def _recognized_decision_heading_index(lines: list[str]) -> int | None:
    """Return the index of the first recognized decision heading, or ``None``.

    The single scan for a recognized heading lives here so both the
    convention-gate (:func:`has_recognized_decision_heading`) and the extractor
    (:func:`extract_decision_section`) consult exactly the same recognition
    rule — the set named in :data:`RECOGNIZED_DECISION_HEADINGS` — without
    duplicating it.
    """
    for index, line in enumerate(lines):
        if line.strip() in RECOGNIZED_DECISION_HEADINGS:
            return index
    return None


def has_recognized_decision_heading(source: str) -> bool:
    """Return whether ``source``'s body carries a recognized decision heading.

    This is the convention-gate predicate: it reuses the recognition rule in
    :data:`RECOGNIZED_DECISION_HEADINGS` (via
    :func:`_recognized_decision_heading_index`) rather than re-deriving it, so a
    document is conforming exactly when it carries one of those headings.
    """
    return _recognized_decision_heading_index(source.splitlines()) is not None


def extract_decision_section(source: str) -> str:
    """Return the verbatim body text of the recognized decision section.

    The body runs from the first recognized decision heading (see
    :data:`RECOGNIZED_DECISION_HEADINGS`) up to — but not including — the next
    Markdown heading, so a following section such as ``## Consequences`` never
    bleeds into the extract. The returned text is a verbatim substring of
    ``source`` with surrounding blank lines trimmed.

    Parameters
    ----------
    source:
        The full source document.

    Returns
    -------
    str
        The verbatim decision-section body, or ``""`` if no recognized decision
        heading is present.
    """
    lines = source.splitlines(keepends=True)

    heading_index = _recognized_decision_heading_index(lines)
    if heading_index is None:
        return ""
    start = heading_index + 1

    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].lstrip().startswith("#"):
            end = index
            break

    return "".join(lines[start:end]).strip()


def _render_machine_index_entry(frontmatter: Mapping[str, str]) -> dict[str, str]:
    """Build the structured machine index entry from the frontmatter facts."""
    return {
        "id": frontmatter["id"],
        "title": frontmatter["title"],
        "status": frontmatter["status"],
    }


def _render_human_index_entry(frontmatter: Mapping[str, str]) -> str:
    """Render the human-readable index line from the frontmatter facts.

    The line surfaces the id, title and status and adds only punctuation and
    whitespace glue — no alphabetic content beyond the rendered facts — so it
    introduces no fact absent from the source.
    """
    return f"{frontmatter['id']}: {frontmatter['title']} [{frontmatter['status']}]"


def generate_projections(source: str) -> ProjectionBundle:
    """Generate the architecture-decision projections from a single source.

    Parameters
    ----------
    source:
        The full text of one source decision document: YAML frontmatter
        (``id``, ``title``, ``status``, ``description``) followed by a Markdown
        body carrying a recognized decision section heading.

    Returns
    -------
    ProjectionBundle
        A bundle exposing ``l0`` (id/title/status/description card), ``l1``
        (verbatim recognized-decision-section extract), ``l2`` (the source
        document itself), ``machine_index_entry`` and ``human_index_entry`` —
        all derived from the single source, introducing no fact absent from it.
    """
    frontmatter = parse_frontmatter(source)

    # Convention-gate: a document whose body carries none of the recognized
    # decision headings is reported as non-conforming rather than projected into
    # a bundle with a silently empty L1 extract.
    if not has_recognized_decision_heading(source):
        raise NonConformingDocumentError(document_id=frontmatter.get("id"))

    l0 = L0Card(
        id=frontmatter["id"],
        title=frontmatter["title"],
        status=frontmatter["status"],
        description=frontmatter["description"],
    )
    l1 = L1Extract(text=extract_decision_section(source))

    return ProjectionBundle(
        l0=l0,
        l1=l1,
        l2=source,
        machine_index_entry=_render_machine_index_entry(frontmatter),
        human_index_entry=_render_human_index_entry(frontmatter),
    )


# --- Corpus-level generation -------------------------------------------------
#
# The single-source :func:`generate_projections` above turns one document into a
# structured :class:`ProjectionBundle`. Corpus-level generation lifts that to a
# fixed set of documents and *serializes* every projection tier and both index
# entries into a deterministic **byte manifest**: a mapping of relative output
# path to the exact bytes that path should carry.
#
# The manifest is the pure, filesystem-free artifact later sub-issues build on:
# the idempotent-regen sub-issue writes each ``path -> bytes`` pair to disk and
# adds a check mode that compares the on-disk bytes against a freshly generated
# manifest, and the kind-parameterized accessor selects manifest entries by
# their leading ``kind/`` path segment. Because generation reads only the source
# corpus — never the wall clock, the environment, the hostname, or the current
# working directory — and every embedded path is relative, two regenerations of
# the same corpus on different hosts at different times are byte-for-byte
# identical.

# The manifest path segment naming each projection kind. Kept as named
# constants so the kind-parameterized accessor selects by exactly these
# segments rather than re-deriving the layout.
CORPUS_KIND_SEGMENTS: tuple[str, ...] = ("l0", "l1", "l2", "index")


def _serialize_json(payload: object) -> bytes:
    """Serialize ``payload`` to canonical, ambient-free JSON bytes.

    ``sort_keys`` makes key order independent of insertion order, ``ensure_ascii``
    keeps the byte encoding independent of locale, and the fixed indent plus a
    single trailing newline make the byte layout fully determined by the payload
    — no timestamp, hostname, or path is introduced.
    """
    text = json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True)
    return (text + "\n").encode("utf-8")


def _serialize_text(text: str) -> bytes:
    """Serialize a text tier to bytes with a single normalized trailing newline."""
    return (text.rstrip("\n") + "\n").encode("utf-8")


def generate_corpus(sources: Mapping[str, str]) -> dict[str, bytes]:
    """Generate the full projection set and index for a corpus as a byte manifest.

    Parameters
    ----------
    sources:
        A mapping of document id to that document's full source text. The corpus
        is the single source of truth; nothing else is read.

    Returns
    -------
    dict[str, bytes]
        An ordered manifest mapping each relative output path to the exact bytes
        that path should carry. Documents are visited in sorted id order, so the
        manifest's path order — and therefore its serialized form — is stable.
        Per document ``doc_id`` the manifest carries ``l0/<doc_id>.json`` (the
        card), ``l1/<doc_id>.md`` (the verbatim extract) and ``l2/<doc_id>.md``
        (the source), plus corpus-wide ``index/machine.json`` and
        ``index/human.md`` entries covering every document in sorted id order.

    Determinism
    -----------
    The manifest is a pure function of ``sources``: it embeds no timestamp, no
    hostname, and no absolute filesystem path, and every manifest key is a
    relative path. Two calls with the same corpus produce byte-for-byte
    identical manifests regardless of host, time, environment, or working
    directory.
    """
    ordered_ids = sorted(sources)

    manifest: dict[str, bytes] = {}
    bundles: dict[str, ProjectionBundle] = {}
    for doc_id in ordered_ids:
        bundle = generate_projections(sources[doc_id])
        bundles[doc_id] = bundle
        manifest[f"l0/{doc_id}.json"] = _serialize_json(
            {
                "id": bundle.l0.id,
                "title": bundle.l0.title,
                "status": bundle.l0.status,
                "description": bundle.l0.description,
            }
        )
        manifest[f"l1/{doc_id}.md"] = _serialize_text(bundle.l1.text)
        manifest[f"l2/{doc_id}.md"] = _serialize_text(bundle.l2)

    manifest["index/machine.json"] = _serialize_json(
        [dict(bundles[doc_id].machine_index_entry) for doc_id in ordered_ids]
    )
    manifest["index/human.md"] = _serialize_text(
        "\n".join(bundles[doc_id].human_index_entry for doc_id in ordered_ids)
    )

    return manifest


# --- Filesystem materialization and check mode -------------------------------
#
# ``generate_corpus`` above is a *pure* ``path -> bytes`` manifest: it touches no
# filesystem. This section lifts that manifest onto disk and back.
#
# ``write_corpus`` materializes the manifest under an output directory, rewriting
# only the files whose on-disk bytes differ from the manifest. Because generation
# is deterministic, regenerating over an unchanged source produces a manifest
# byte-identical to what is already on disk, so *no* file is rewritten and the
# reported changed set is empty — regeneration is idempotent.
#
# ``check_corpus`` compares a freshly generated manifest against the on-disk
# outputs without writing anything, reporting the drifted paths (and a
# conventional non-zero exit status) when the outputs are stale, or no drift and
# a success exit status when they are already current.


@dataclass(frozen=True)
class WriteResult:
    """The outcome of materializing a corpus manifest under an output directory.

    ``changed_paths`` holds the relative manifest paths whose on-disk bytes were
    (re)written because they differed from the freshly generated manifest — an
    empty tuple means the outputs already matched the source and nothing was
    rewritten. Comparing desired manifest bytes to on-disk bytes and rewriting
    only the differing files is what makes regeneration over an unchanged source
    write zero changed bytes.
    """

    changed_paths: tuple[str, ...]

    @property
    def changed_count(self) -> int:
        """The number of files (re)written — zero on an idempotent regeneration."""
        return len(self.changed_paths)


@dataclass(frozen=True)
class CheckResult:
    """The outcome of checking on-disk outputs against a freshly generated manifest.

    ``drift`` holds the relative manifest paths whose on-disk bytes differ from
    (or are missing against) the freshly generated manifest. ``has_drift`` and
    ``exit_code`` surface the same fact for callers and a process exit
    respectively: clean outputs yield ``drift == ()``, ``has_drift is False`` and
    ``exit_code == 0`` (a success status).
    """

    drift: tuple[str, ...]

    @property
    def has_drift(self) -> bool:
        """Whether any on-disk output has drifted from the manifest."""
        return bool(self.drift)

    @property
    def exit_code(self) -> int:
        """A conventional process exit status: ``0`` when clean, ``1`` on drift."""
        return 1 if self.drift else 0


def write_corpus(sources: Mapping[str, str], out_dir: str | os.PathLike[str]) -> WriteResult:
    """Materialize the corpus manifest under ``out_dir``, rewriting only drift.

    The manifest from :func:`generate_corpus` is written path-by-path under
    ``out_dir``. A file is (re)written only when its on-disk bytes differ from
    the manifest's bytes (or the file is absent); a file whose bytes already
    match is left untouched — its mtime does not change. Because generation is
    deterministic, a regeneration over an unchanged source yields a manifest
    byte-identical to what is already on disk, so no file is rewritten and the
    returned :class:`WriteResult` reports an empty ``changed_paths`` — the
    "writes zero changed bytes" idempotence property.

    Parameters
    ----------
    sources:
        A mapping of document id to full source text — the single source of
        truth passed straight through to :func:`generate_corpus`.
    out_dir:
        The output directory under which the manifest's relative paths are
        materialized. It (and any needed parent directories) are created as
        required. Only relative manifest paths are ever joined onto it.

    Returns
    -------
    WriteResult
        Carrying the relative paths that were (re)written, in manifest order.
    """
    base = Path(out_dir)
    manifest = generate_corpus(sources)

    changed: list[str] = []
    for rel_path, data in manifest.items():
        target = base / rel_path
        if target.exists() and target.read_bytes() == data:
            # Already current: leave the file (and its mtime) untouched.
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        changed.append(rel_path)

    return WriteResult(changed_paths=tuple(changed))


def check_corpus(sources: Mapping[str, str], out_dir: str | os.PathLike[str]) -> CheckResult:
    """Check the on-disk outputs under ``out_dir`` against a fresh manifest.

    A freshly generated manifest (see :func:`generate_corpus`) is compared
    path-by-path against the bytes on disk under ``out_dir`` **without writing
    anything**. A path drifts when its on-disk file is absent or its bytes differ
    from the manifest. Over an unchanged source that has already been written,
    every path matches, so the returned :class:`CheckResult` reports no drift and
    a success exit status (``exit_code == 0``).

    Parameters
    ----------
    sources:
        The corpus source mapping, passed straight through to
        :func:`generate_corpus`.
    out_dir:
        The output directory whose materialized outputs are checked.

    Returns
    -------
    CheckResult
        Carrying the drifted relative paths (empty when the outputs are current),
        in manifest order.
    """
    base = Path(out_dir)
    manifest = generate_corpus(sources)

    drift: list[str] = []
    for rel_path, data in manifest.items():
        target = base / rel_path
        if not target.exists() or target.read_bytes() != data:
            drift.append(rel_path)

    return CheckResult(drift=tuple(drift))


# --- Kind-parameterized accessor and registry --------------------------------
#
# Everything above turns *one kind's* source corpus into a byte manifest. This
# section lifts that behind a single accessor that is parameterized by document
# *kind*: a kind (for example the architecture-decision kind) is registered
# against its source corpus, and callers reach a kind's projections only through
# :meth:`KnowledgeContext.projections_for`.
#
# The accessor refuses an unregistered kind: requesting a kind that was never
# registered returns a definite kind-not-registered result
# (:class:`KindProjections` with ``registered is False`` and ``projections is
# None``) rather than silently defaulting to some other kind's corpus. Because
# the not-registered result carries no projections at all, an unregistered kind
# can never be mistaken for — or default to — the architecture-decision corpus.

# The kind under which this context's architecture-decision corpus is
# registered. Named as a constant so callers select by exactly this kind rather
# than re-spelling the string. The authoring-discovery family reaches the
# architecture-decision corpus/index through
# ``KnowledgeContext.projections_for(ARCHITECTURE_DECISION_KIND)``.
ARCHITECTURE_DECISION_KIND = "architecture-decision"


@dataclass(frozen=True)
class KindProjections:
    """The result of requesting projections for a document kind.

    This is the single return shape of :meth:`KnowledgeContext.projections_for`,
    uniform across both the registered and the unregistered case so callers
    distinguish them on ``registered`` rather than on the return *type*:

    * **Registered kind** — ``registered is True`` and ``projections`` is that
      kind's corpus byte manifest (the ``path -> bytes`` mapping
      :func:`generate_corpus` builds for the kind's registered source corpus).
    * **Unregistered kind** — ``registered is False`` and ``projections is
      None``. This is the *definite kind-not-registered result*: it carries no
      projections at all, so it can never be mistaken for, or default to, any
      registered kind's corpus.

    ``kind`` always echoes the requested kind, so a caller can surface *which*
    kind was requested without re-threading it.
    """

    kind: str
    registered: bool
    projections: dict[str, bytes] | None


class KnowledgeContext:
    """A registry of document kinds mapping each to its corpus, plus the accessor.

    A kind is made known by :meth:`register`, which binds the kind to its source
    corpus (a ``doc_id -> source text`` mapping). :meth:`projections_for` is the
    kind-parameterized accessor: it returns the registered kind's corpus
    projections, or — for a kind that was never registered — a definite
    kind-not-registered result rather than defaulting to another kind's corpus.

    "No other kind registered" is a real, observable precondition: a fresh
    context has :meth:`registered_kinds` empty, and each :meth:`register` adds
    exactly one kind.
    """

    def __init__(self) -> None:
        # kind -> that kind's source corpus (doc_id -> source text).
        self._corpora: dict[str, Mapping[str, str]] = {}

    def register(self, kind: str, sources: Mapping[str, str]) -> None:
        """Register ``kind`` against its source corpus ``sources``.

        Binds ``kind`` to the corpus its projections are generated from. Only a
        registered kind is served projections by :meth:`projections_for`; a kind
        that is never registered stays unknown to the accessor.
        """
        self._corpora[kind] = sources

    def registered_kinds(self) -> tuple[str, ...]:
        """Return the registered kinds in sorted order (empty when none)."""
        return tuple(sorted(self._corpora))

    def projections_for(self, kind: str) -> KindProjections:
        """Return the projections for ``kind`` — the kind-parameterized accessor.

        For a **registered** kind, returns a :class:`KindProjections` with
        ``registered is True`` whose ``projections`` is that kind's corpus byte
        manifest (see :func:`generate_corpus`). For an **unregistered** kind,
        returns a :class:`KindProjections` with ``registered is False`` and
        ``projections is None`` — a definite kind-not-registered result that
        does not default to any other kind's corpus.
        """
        if kind not in self._corpora:
            return KindProjections(kind=kind, registered=False, projections=None)
        return KindProjections(
            kind=kind,
            registered=True,
            projections=generate_corpus(self._corpora[kind]),
        )
