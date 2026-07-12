"""Frontmatter conformance and required-section checks against the type schema.

This module validates a parsed :class:`~knowledge.artifact_types.Artifact`
against the rules of its type, resolved from the single registry in
:mod:`knowledge.artifact_types`. It answers two questions:

* :func:`validate_frontmatter` — does the artifact's YAML frontmatter conform to
  the per-type schema? A conforming artifact carries every shared and
  type-additional required field, an id matching its type's pattern, and a
  status in its type's enum, and stores no projection-only field. A
  non-conforming artifact is reported with a :class:`ConformanceResult` whose
  :class:`Diagnostic` entries each name the specific missing field, offending
  value, or expected pattern.
* :func:`check_required_sections` — does the document's body carry every section
  in its type's required-section set? The set is resolved per type from the
  registry, so a pdr's set is never imposed on an intent-record. A document
  missing a required section is reported with a :class:`SectionCheckResult`
  naming the missing section.

Every diagnosis is specific: it never merely says "non-conforming", it names
*what* — the missing field, the offending value and its type's enum, or the
offending id and the expected pattern — so a caller can act on the report
without re-deriving the rule.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from knowledge.artifact_types import (
    SHARED_REQUIRED_FIELDS,
    STORED_PROJECTION_FIELDS,
    Artifact,
    artifact_type,
)

# Diagnostic codes. Named constants so callers select on a stable code rather
# than pattern-matching a human message.
MISSING_REQUIRED_FIELD = "missing-required-field"
MISSING_TYPE_FIELD = "missing-type-field"
UNRECOGNIZED_TYPE = "unrecognized-type"
UNRECOGNIZED_STATUS = "unrecognized-status"
ID_PATTERN_MISMATCH = "id-pattern-mismatch"
EMPTY_ANCHOR = "empty-anchor"
STORED_PROJECTION_FIELD = "stored-projection-field"

# The codes whose diagnostics denote a missing required field — the set
# :attr:`ConformanceResult.missing_fields` draws its field names from.
_MISSING_FIELD_CODES = frozenset({MISSING_REQUIRED_FIELD, MISSING_TYPE_FIELD})


@dataclass(frozen=True)
class Diagnostic:
    """One specific finding about why an artifact does or does not conform.

    ``code`` is the stable machine tag (one of the module-level code constants);
    ``message`` is the human-readable diagnosis that names the specific field,
    value, or pattern. ``field``, ``offending`` and ``expected`` carry the
    structured particulars a caller may want without parsing ``message``:

    * ``field`` — the frontmatter field the finding is about (e.g. ``updated``).
    * ``offending`` — the value that violated a rule (e.g. an unrecognized
      status or an id that failed its pattern).
    * ``expected`` — what was expected instead (e.g. the id pattern's example).
    """

    code: str
    message: str
    field: str | None = None
    offending: str | None = None
    expected: str | None = None


@dataclass(frozen=True)
class ConformanceResult:
    """The outcome of validating an artifact's frontmatter against its schema.

    ``diagnostics`` holds every finding, in check order. The result is
    **conforming** exactly when there are no diagnostics; :attr:`conforming` and
    :attr:`exit_code` surface that verdict for callers and a process exit
    respectively (``exit_code == 0`` when conforming, ``1`` otherwise).
    :attr:`missing_fields` names the required fields reported missing, and
    :attr:`messages` exposes the human diagnoses for reporting.
    """

    diagnostics: tuple[Diagnostic, ...]

    @property
    def conforming(self) -> bool:
        """Whether the artifact conforms (no diagnostics)."""
        return not self.diagnostics

    @property
    def exit_code(self) -> int:
        """A conventional exit status: ``0`` when conforming, ``1`` otherwise."""
        return 0 if self.conforming else 1

    @property
    def messages(self) -> tuple[str, ...]:
        """The human-readable diagnoses, in check order."""
        return tuple(d.message for d in self.diagnostics)

    @property
    def missing_fields(self) -> tuple[str, ...]:
        """The names of the required fields reported missing, in check order."""
        return tuple(
            d.field
            for d in self.diagnostics
            if d.code in _MISSING_FIELD_CODES and d.field is not None
        )

    def by_code(self, code: str) -> tuple[Diagnostic, ...]:
        """Return every diagnostic carrying ``code``."""
        return tuple(d for d in self.diagnostics if d.code == code)


def _is_present(frontmatter, key: str) -> bool:
    """Whether ``key`` is present with a non-``None`` value.

    A present-but-empty list still counts as present — the empty-anchor rule,
    not the missing-field rule, governs an empty required list.
    """
    return key in frontmatter and frontmatter.get(key) is not None


def validate_frontmatter(artifact: Artifact) -> ConformanceResult:
    """Validate ``artifact``'s frontmatter against its type's schema.

    The checks, in order:

    1. **Stored projection fields.** Any field in
       :data:`~knowledge.artifact_types.STORED_PROJECTION_FIELDS` (e.g.
       ``disclosure-level``) present in frontmatter is non-conforming: disclosure
       level is a projection the tool emits, never stored truth.
    2. **Type resolution.** A missing ``type`` field is a missing shared field;
       a ``type`` value outside the eight recognized types is an unrecognized
       type — reported, and type-specific checks are then skipped.
    3. **Shared required fields.** Every field in
       :data:`~knowledge.artifact_types.SHARED_REQUIRED_FIELDS` must be present.
    4. **Type-additional required fields**, then **non-empty anchor fields**
       (an adr's ``derives-from`` present but empty anchors to nothing).
    5. **Id pattern** and **status enum** for the resolved type.

    Returns a :class:`ConformanceResult`; a conforming artifact yields one with
    no diagnostics.
    """
    frontmatter = artifact.frontmatter
    diagnostics: list[Diagnostic] = []

    # 1. Stored projection fields must never appear in frontmatter.
    for forbidden in STORED_PROJECTION_FIELDS:
        if forbidden in frontmatter:
            diagnostics.append(
                Diagnostic(
                    code=STORED_PROJECTION_FIELD,
                    field=forbidden,
                    message=(
                        f"the frontmatter stores a '{forbidden}' field, but "
                        f"disclosure level is a projection emitted by the tool "
                        f"and is never a stored frontmatter field"
                    ),
                )
            )

    # 2. Resolve the type. A present-but-unrecognized type is reported and
    #    type-specific checks are skipped.
    type_value = frontmatter.get("type")
    atype = artifact_type(type_value) if isinstance(type_value, str) else None
    if _is_present(frontmatter, "type") and atype is None:
        diagnostics.append(
            Diagnostic(
                code=UNRECOGNIZED_TYPE,
                field="type",
                offending=str(type_value),
                message=(
                    f"the type value '{type_value}' is not one of the eight "
                    f"recognized artifact types"
                ),
            )
        )

    # 3. Shared required fields.
    for name in SHARED_REQUIRED_FIELDS:
        if not _is_present(frontmatter, name):
            diagnostics.append(
                Diagnostic(
                    code=MISSING_REQUIRED_FIELD,
                    field=name,
                    message=f"the required field '{name}' is missing from the frontmatter",
                )
            )

    # Type-specific checks only run against a resolved type.
    if atype is not None:
        # 4a. Type-additional required fields.
        for name in atype.extra_required_fields:
            if not _is_present(frontmatter, name):
                diagnostics.append(
                    Diagnostic(
                        code=MISSING_TYPE_FIELD,
                        field=name,
                        message=(
                            f"the type-required field '{name}' is missing from "
                            f"the frontmatter that a {atype.name} additionally requires"
                        ),
                    )
                )

        # 4b. Non-empty anchor fields: present but empty anchors to nothing.
        for name in atype.non_empty_fields:
            if _is_present(frontmatter, name) and not frontmatter.get(name):
                diagnostics.append(
                    Diagnostic(
                        code=EMPTY_ANCHOR,
                        field=name,
                        message=(
                            f"the '{name}' field is empty; an {atype.name} "
                            f"requires at least one anchor and this one anchors "
                            f"to no upstream artifact"
                        ),
                    )
                )

        # 5a. Id pattern.
        id_value = frontmatter.get("id")
        if _is_present(frontmatter, "id") and not re.fullmatch(
            atype.id_pattern, str(id_value)
        ):
            diagnostics.append(
                Diagnostic(
                    code=ID_PATTERN_MISMATCH,
                    field="id",
                    offending=str(id_value),
                    expected=atype.id_example,
                    message=(
                        f"the id '{id_value}' does not match the {atype.id_example} "
                        f"pattern its type requires"
                    ),
                )
            )

        # 5b. Status enum.
        status_value = frontmatter.get("status")
        if _is_present(frontmatter, "status") and status_value not in atype.statuses:
            diagnostics.append(
                Diagnostic(
                    code=UNRECOGNIZED_STATUS,
                    field="status",
                    offending=str(status_value),
                    message=(
                        f"the status value '{status_value}' is not a member of "
                        f"the {atype.name} status enum {list(atype.statuses)}"
                    ),
                )
            )

    return ConformanceResult(diagnostics=tuple(diagnostics))


@dataclass(frozen=True)
class SectionCheckResult:
    """The outcome of checking a document body against its required-section set.

    ``missing_sections`` names the required sections absent from the body, in the
    type's declared section order. The document is **conforming on body
    structure** exactly when none are missing; :attr:`conforming` and
    :attr:`exit_code` surface that verdict (``exit_code == 0`` when conforming).
    :attr:`messages` renders one human diagnosis per missing section for
    reporting.
    """

    missing_sections: tuple[str, ...]

    @property
    def conforming(self) -> bool:
        """Whether the body carries every required section."""
        return not self.missing_sections

    @property
    def exit_code(self) -> int:
        """A conventional exit status: ``0`` when conforming, ``1`` otherwise."""
        return 0 if self.conforming else 1

    @property
    def messages(self) -> tuple[str, ...]:
        """A human diagnosis naming each missing required section."""
        return tuple(
            f"the required section '{name}' is missing from the document body"
            for name in self.missing_sections
        )


def check_required_sections(artifact: Artifact) -> SectionCheckResult:
    """Check ``artifact``'s body against its type's required-section set.

    The required-section set is resolved per type from the single registry: the
    document's ``## `` section headings (see
    :attr:`~knowledge.artifact_types.Artifact.sections`) are compared against the
    resolved type's ``required_sections``, and any required section absent from
    the body is reported — in the type's declared section order — as missing.
    Because the set is resolved from the artifact's *own* type, a pdr's set is
    never imposed on an intent-record and vice versa.

    A document whose ``type`` does not resolve to a recognized type imposes no
    section set (that non-conformance is the frontmatter check's to report), so
    this returns a conforming result with no missing sections.
    """
    atype = artifact_type(artifact.type) if isinstance(artifact.type, str) else None
    if atype is None:
        return SectionCheckResult(missing_sections=())

    present = set(artifact.sections)
    missing = tuple(name for name in atype.required_sections if name not in present)
    return SectionCheckResult(missing_sections=missing)
