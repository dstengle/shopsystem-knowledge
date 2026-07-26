"""The additive-discipline check over the per-type typedef set.

The base schema governs the shared frontmatter fields every artifact carries
(:data:`~knowledge.artifact_types.SHARED_REQUIRED_FIELDS`) plus the
base-governed optionals — ``distribution`` (governed by ``DISTRIBUTION_ENUM``
in :mod:`knowledge.schema`) and the
:data:`~knowledge.schema.RECOGNIZED_OPTIONAL_FIELDS` (``tags``,
``external-references``). A per-type typedef must state ONLY its per-type
deltas: its own required body sections, its status enum, and its edge
participation (the extra/non-empty required fields it adds). It must not
re-declare a field the base schema already governs.

This module runs an **additive-discipline** check over the per-type typedef
*set* (not an artifact corpus): for each :class:`~knowledge.artifact_types.ArtifactType`,
it inspects the union of the type's ``extra_required_fields`` and
``non_empty_fields`` for any name intersecting the base-governed set. Each such
re-declaration draws one ``base-field-redeclaration`` finding naming the typedef
and the re-declared field, carrying a remediation to remove the re-declared base
field and inherit it from the base schema. Legitimate per-type deltas
(``required_sections``, ``statuses``, edge fields such as ``derives-from`` or
``incorporates``) are not base-governed and draw no finding.

The finding reuses :class:`~knowledge.coherence.Finding` with
:attr:`~knowledge.coherence.Severity.BLOCKING`, so a
:class:`~knowledge.coherence.CoherenceReport` folded over the findings exits
non-zero when any typedef re-declares a base field.
"""

from __future__ import annotations

from knowledge.artifact_types import SHARED_REQUIRED_FIELDS, ArtifactType
from knowledge.coherence import Finding, Severity
from knowledge.schema import RECOGNIZED_OPTIONAL_FIELDS

CHECK_ID = "base-field-redeclaration"
CHECK_NAME = "per-type typedef re-declares a base-governed field"

# The fields the base schema already governs. A per-type typedef re-declaring
# any of these is a base-field-redeclaration defect. This is the shared required
# set, plus ``distribution`` (governed via DISTRIBUTION_ENUM in the schema, but
# not part of RECOGNIZED_OPTIONAL_FIELDS), plus the recognized optionals.
BASE_GOVERNED_FIELDS: frozenset[str] = (
    frozenset(SHARED_REQUIRED_FIELDS)
    | {"distribution"}
    | frozenset(RECOGNIZED_OPTIONAL_FIELDS)
)


def check_additive_discipline(typedefs) -> list[Finding]:
    """Flag any per-type typedef that re-declares a base-governed field.

    Ranges over ``typedefs`` (an iterable of
    :class:`~knowledge.artifact_types.ArtifactType`). For each typedef, the union
    of its ``extra_required_fields`` and ``non_empty_fields`` is intersected with
    :data:`BASE_GOVERNED_FIELDS`; every re-declared base field draws one
    ``base-field-redeclaration`` :class:`~knowledge.coherence.Finding` naming the
    typedef and the field, in typedef-then-field report order. A typedef stating
    only its per-type deltas draws no finding.
    """
    findings: list[Finding] = []
    for atype in typedefs:
        declared = tuple(atype.extra_required_fields) + tuple(atype.non_empty_fields)
        seen: set[str] = set()
        for field_name in declared:
            if field_name in seen:
                continue
            seen.add(field_name)
            if field_name not in BASE_GOVERNED_FIELDS:
                continue
            findings.append(
                Finding(
                    check_id=CHECK_ID,
                    check_name=CHECK_NAME,
                    severity=Severity.BLOCKING,
                    subjects=(atype.name,),
                    message=(
                        f"typedef '{atype.name}' re-declares the base-governed field "
                        f"'{field_name}' that the base schema already governs"
                    ),
                    remediation=(
                        f"remove the re-declared base field '{field_name}' from "
                        f"typedef '{atype.name}' and inherit it from the base schema"
                    ),
                )
            )
    return findings


__all__ = [
    "BASE_GOVERNED_FIELDS",
    "CHECK_ID",
    "CHECK_NAME",
    "check_additive_discipline",
]
