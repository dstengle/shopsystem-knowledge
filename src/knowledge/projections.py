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

from dataclasses import dataclass
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
