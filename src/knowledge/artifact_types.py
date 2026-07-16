"""The artifact type system: the eight recognized types and the parsed artifact.

This module is the **single, well-documented registry** the whole knowledge
context resolves an artifact's type rules through. Wave A's frontmatter
conformance check (:mod:`knowledge.schema`), its required-section check
(also :mod:`knowledge.schema`), and its typedef drift check
(:mod:`knowledge.typedefs`) all read the per-type rules from here rather than
re-spelling them, and the later coherence-gate and digest waves reuse the same
registry. There is exactly one place a type's id pattern, status enum,
type-additional required fields, non-empty anchor fields, and required body
sections are defined: the :data:`ARTIFACT_TYPES` table below.

The context recognizes **exactly eight artifact types**. Every artifact shares
the eight :data:`SHARED_REQUIRED_FIELDS` frontmatter fields; each type then adds
its own id pattern, status enum, and any type-additional required fields.
``disclosure-level`` is deliberately **not** a stored field — disclosure level
is a projection the tool emits, never frontmatter truth — so it is listed in
:data:`STORED_PROJECTION_FIELDS` and its presence in frontmatter is a
conformance error (see :mod:`knowledge.schema`).

Parsing is deterministic and ambient-free: :func:`parse_artifact` reads only the
source text — no wall clock, hostname, or filesystem path enters an
:class:`Artifact`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Mapping

import yaml

# The frontmatter fields every artifact must carry, regardless of type. Kept as
# a single named tuple so the conformance check reads the shared requirement
# from exactly one place.
SHARED_REQUIRED_FIELDS: tuple[str, ...] = (
    "type",
    "id",
    "title",
    "status",
    "created",
    "updated",
    "authors",
    "description",
)

# Fields that must NEVER appear in stored frontmatter because they are
# projections the tool emits, not source truth. ``disclosure-level`` is the
# canonical example: an artifact's disclosure tier is computed and projected,
# never pinned in the document itself, so storing it is a conformance error.
STORED_PROJECTION_FIELDS: tuple[str, ...] = ("disclosure-level",)

# The YAML frontmatter fence.
_FRONTMATTER_FENCE = "---"


@dataclass(frozen=True)
class ArtifactType:
    """The rules that define one recognized artifact type.

    A single :class:`ArtifactType` is the whole truth about a type: its id
    pattern, the status values it recognizes, the frontmatter fields it requires
    beyond the shared set, which of those must carry a non-empty anchor, and the
    body sections its documents must contain. Every downstream check resolves a
    type to one of these and reads the rule it needs — nothing re-derives a
    type's rules elsewhere.

    Attributes
    ----------
    name:
        The type's frontmatter ``type`` value (e.g. ``"adr"``).
    id_prefix:
        The literal id prefix (e.g. ``"adr"``) an id of this type carries.
    id_pattern:
        An anchored regular expression an id of this type must fully match
        (e.g. ``r"cand-\\d{3,}"``).
    id_example:
        A human-facing rendering of the id pattern (e.g. ``"cand-NNN"``) named
        in a non-conformance diagnosis.
    statuses:
        The status enum this type recognizes; a status outside it is
        non-conforming.
    extra_required_fields:
        The frontmatter fields required *in addition to* the shared set.
    non_empty_fields:
        Required fields whose value must be a non-empty list — a present but
        empty value is non-conforming (e.g. an adr's ``derives-from`` anchoring
        to nothing).
    required_sections:
        The body section headings a document of this type must carry.
    document_shape:
        The document shape the typedef generates. ``"instance"`` (the default)
        is an append-only record — each artifact of the type is a new numbered
        instance. ``"living"`` is a single stewarded document revised in place
        (e.g. ``current-state``), whose generated template carries its
        accumulating list fields (such as ``incorporates``) as YAML lists rather
        than as a fresh numbered instance. The generator reads this to shape the
        template and encodes it in the schema fragment, so the living-vs-instance
        distinction is single-sourced from the typedef.
    """

    name: str
    id_prefix: str
    id_pattern: str
    id_example: str
    statuses: tuple[str, ...]
    extra_required_fields: tuple[str, ...] = ()
    non_empty_fields: tuple[str, ...] = ()
    required_sections: tuple[str, ...] = ()
    document_shape: str = "instance"

    @property
    def all_required_fields(self) -> tuple[str, ...]:
        """The full required-field set: the shared fields plus this type's own."""
        return SHARED_REQUIRED_FIELDS + self.extra_required_fields


def _pattern(prefix: str) -> str:
    """Build the anchored ``prefix-NNN`` id pattern (at least three digits)."""
    return rf"{re.escape(prefix)}-\d{{3,}}"


# The eight recognized artifact types of the discovery-first knowledge context,
# following the decision pipeline from an early exploration through to the living
# record of settled decisions (PDR-032 kind->type / ADR-059):
#
#   intent-record      — a captured statement of intent and its success signals.
#   candidate          — an idea under exploration, not yet committed to.
#   session-record     — a record of a working session and the work it produced
#                        or revised.
#   prioritization-record — a record of how work was ranked and why.
#   brief              — a shaped brief handed on for a decision.
#   pdr                — a product decision record: the decision-makers weigh
#                        options and derive a decision from upstream artifacts.
#   adr                — an architecture decision record anchored to (deriving
#                        from) at least one upstream artifact.
#   current-state      — the single living stewarded document that incorporates
#                        the settled decisions (see :mod:`knowledge.typedefs`).
#
# ``roadmap`` is intentionally absent: it is not one of the eight recognized
# types, so a document typed ``roadmap`` is non-conforming.
_ARTIFACT_TYPE_LIST: tuple[ArtifactType, ...] = (
    ArtifactType(
        name="intent-record",
        id_prefix="intent",
        id_pattern=_pattern("intent"),
        id_example="intent-NNN",
        statuses=("draft", "active", "fulfilled", "abandoned"),
        required_sections=(
            "Verbatim anchors",
            "The goal behind the ask",
            "Who it serves",
            "Constraints",
            "Non-goals",
            "Appetite signal",
            "Failure conditions",
            "Open threads",
        ),
    ),
    ArtifactType(
        name="candidate",
        id_prefix="cand",
        id_pattern=_pattern("cand"),
        id_example="cand-NNN",
        statuses=("exploring", "shaped", "briefed", "parked", "rejected"),
        required_sections=("Context", "Open questions"),
    ),
    ArtifactType(
        name="session-record",
        id_prefix="session",
        id_pattern=_pattern("session"),
        id_example="session-NNN",
        statuses=("open", "closed"),
        extra_required_fields=("produced", "revised"),
        required_sections=("Summary", "Outcomes"),
    ),
    ArtifactType(
        name="prioritization-record",
        id_prefix="prio",
        id_pattern=_pattern("prio"),
        id_example="prio-NNN",
        statuses=("draft", "active", "superseded"),
        required_sections=("Ranking", "Rationale"),
    ),
    ArtifactType(
        name="brief",
        id_prefix="brief",
        id_pattern=_pattern("brief"),
        id_example="brief-NNN",
        statuses=("draft", "ready", "delivered", "withdrawn"),
        extra_required_fields=("derives-from",),
        required_sections=("Summary", "Scope"),
    ),
    ArtifactType(
        name="pdr",
        id_prefix="pdr",
        id_pattern=_pattern("pdr"),
        id_example="pdr-NNN",
        statuses=("proposed", "accepted", "superseded", "rejected"),
        extra_required_fields=("decision-makers", "derives-from"),
        required_sections=("Context", "Options considered", "Decision", "Consequences"),
    ),
    ArtifactType(
        name="adr",
        id_prefix="adr",
        id_pattern=_pattern("adr"),
        id_example="adr-NNN",
        statuses=("proposed", "accepted", "superseded", "rejected"),
        extra_required_fields=("derives-from",),
        non_empty_fields=("derives-from",),
        required_sections=("Context", "Decision", "Consequences"),
    ),
    ArtifactType(
        name="current-state",
        id_prefix="current-state",
        id_pattern=_pattern("current-state"),
        id_example="current-state-NNN",
        statuses=("current", "superseded"),
        extra_required_fields=("incorporates",),
        required_sections=("Current decisions", "Stewardship"),
        document_shape="living",
    ),
)

# The registry: type name -> its rules. This mapping is the single source of
# truth every downstream check resolves a type through.
ARTIFACT_TYPES: Mapping[str, ArtifactType] = {
    atype.name: atype for atype in _ARTIFACT_TYPE_LIST
}

# The eight recognized type names, in pipeline order. A ``type`` value outside
# this tuple is unrecognized and therefore non-conforming.
RECOGNIZED_ARTIFACT_TYPES: tuple[str, ...] = tuple(
    atype.name for atype in _ARTIFACT_TYPE_LIST
)


def artifact_type(name: str) -> ArtifactType | None:
    """Resolve a type name to its :class:`ArtifactType`, or ``None`` if unknown.

    Returning ``None`` — rather than defaulting to some other type — is what
    lets the conformance check report an unrecognized type as non-conforming
    instead of silently validating it against the wrong rules.
    """
    return ARTIFACT_TYPES.get(name)


@dataclass(frozen=True)
class Artifact:
    """A parsed artifact: its frontmatter facts and its Markdown body.

    An :class:`Artifact` is the structured form every check operates on. The
    ``type``/``id``/``status``/``title`` accessors surface the shared frontmatter
    facts (``None`` when absent, so a missing field is observable rather than a
    ``KeyError``), ``frontmatter`` exposes the full parsed mapping (list-valued
    fields such as ``authors`` and ``derives-from`` stay lists), and
    :attr:`sections` names the body's ``##`` section headings in document order.
    """

    frontmatter: Mapping[str, object] = field(default_factory=dict)
    body: str = ""

    def _get(self, key: str) -> object | None:
        return self.frontmatter.get(key)

    @property
    def type(self) -> object | None:
        """The frontmatter ``type`` value, or ``None`` when absent."""
        return self._get("type")

    @property
    def id(self) -> object | None:
        """The frontmatter ``id`` value, or ``None`` when absent."""
        return self._get("id")

    @property
    def status(self) -> object | None:
        """The frontmatter ``status`` value, or ``None`` when absent."""
        return self._get("status")

    @property
    def title(self) -> object | None:
        """The frontmatter ``title`` value, or ``None`` when absent."""
        return self._get("title")

    @property
    def sections(self) -> tuple[str, ...]:
        """The body's ``## `` section heading texts, in document order.

        Only level-two (``## ``) headings are treated as sections; the heading
        text (with the ``## `` marker and surrounding whitespace stripped) is
        the section name a required-section check matches against.
        """
        names: list[str] = []
        for line in self.body.splitlines():
            stripped = line.strip()
            if stripped.startswith("## "):
                names.append(stripped[3:].strip())
        return tuple(names)


def parse_artifact(source: str) -> Artifact:
    """Parse one source document into a structured :class:`Artifact`.

    The document opens with a ``---`` YAML frontmatter fence, a YAML block, a
    closing ``---`` fence, and then the Markdown body. The frontmatter is parsed
    with a real YAML loader so list-valued fields (``authors``, ``derives-from``)
    and empty lists (``derives-from: []``) round-trip as lists rather than being
    flattened to strings — the empty-anchor conformance rule depends on telling
    an empty list apart from a present scalar.

    Parsing reads only ``source``; it introduces no timestamp, hostname, or
    filesystem path.

    Parameters
    ----------
    source:
        The full source document text.

    Returns
    -------
    Artifact
        The parsed frontmatter mapping and the Markdown body. A document without
        a leading frontmatter fence yields an :class:`Artifact` with empty
        frontmatter and the whole text as its body.
    """
    lines = source.splitlines(keepends=True)
    if not lines or lines[0].strip() != _FRONTMATTER_FENCE:
        return Artifact(frontmatter={}, body=source)

    # Find the closing fence.
    end_index: int | None = None
    for index in range(1, len(lines)):
        if lines[index].strip() == _FRONTMATTER_FENCE:
            end_index = index
            break
    if end_index is None:
        # No closing fence: treat the whole thing as body with no frontmatter.
        return Artifact(frontmatter={}, body=source)

    frontmatter_text = "".join(lines[1:end_index])
    body = "".join(lines[end_index + 1 :])

    loaded = yaml.safe_load(frontmatter_text) if frontmatter_text.strip() else {}
    frontmatter: dict[str, object] = dict(loaded) if isinstance(loaded, dict) else {}

    return Artifact(frontmatter=frontmatter, body=body)
