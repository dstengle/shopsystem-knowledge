"""Step definitions for the per-type derives-from optionality feature.

Binds the single Scenario Outline in ``per_type_derives_from.feature`` (three
Examples rows: intent-record, candidate, prioritization-record) and asserts
each Then/And leg against the :class:`ConformanceResult` returned by
``knowledge.schema.validate_frontmatter``.

This PINS the negative side of ADR-069's per-type schema realization: the three
discovery-first kinds do NOT carry ``derives-from`` in their
``extra_required_fields``, so an artifact of one of those kinds conforms when it
omits ``derives-from`` and the conformance check never reports ``derives-from``
as a missing required field. The fixture is built in-process from a conforming
baseline per kind (mirroring ``test_frontmatter_conformance.py``), stating the
one property the scenario is about — that no ``derives-from`` field is carried.
"""

from __future__ import annotations

import pytest
from pytest_bdd import given, parsers, scenario, then, when

from knowledge.artifact_types import Artifact, artifact_type

FEATURE = "per_type_derives_from.feature"


def _conforming_frontmatter(type_name: str) -> dict:
    """Build a fully conforming frontmatter mapping for ``type_name``.

    Every shared field is present and valid, the id matches the type's pattern,
    the status is a member of the type's enum, and every type-additional
    required field is present (non-empty where the type demands an anchor).
    """
    atype = artifact_type(type_name)
    assert atype is not None, f"{type_name} must be a recognized type"
    frontmatter: dict = {
        "type": type_name,
        "id": f"{atype.id_prefix}-001",
        "title": "A title",
        "status": atype.statuses[0],
        "created": "2026-01-01",
        "updated": "2026-01-02",
        "authors": ["alice"],
        "description": "A one-line description.",
    }
    for extra in atype.extra_required_fields:
        # Anchor fields carry a non-empty list; other extras a scalar list.
        frontmatter[extra] = ["pdr-001"] if extra == "derives-from" else ["alice"]
    return frontmatter


@pytest.fixture
def context() -> dict:
    return {}


# --- Scenario binding --------------------------------------------------------


@scenario(
    FEATURE,
    "a kind that does not schema-require derives-from conforms when the field is absent",
)
def test_per_type_derives_from_optional() -> None: ...


# --- Given step --------------------------------------------------------------


@given(
    parsers.parse(
        "a {kind} artifact that carries every field its type additionally "
        "requires but carries no derives-from field"
    )
)
def _artifact_without_derives_from(context: dict, kind: str) -> None:
    fm = _conforming_frontmatter(kind)
    # The kinds under test must not schema-require derives-from: the baseline
    # for such a kind carries no derives-from field, and this states the
    # scenario's one property explicitly.
    assert "derives-from" not in artifact_type(kind).extra_required_fields, (
        f"{kind} unexpectedly schema-requires derives-from"
    )
    fm.pop("derives-from", None)
    assert "derives-from" not in fm
    context["frontmatter"] = fm


# --- When step ---------------------------------------------------------------


@when("the knowledge context validates the artifact's frontmatter against the schema")
def _validate(context: dict) -> None:
    from knowledge.schema import validate_frontmatter

    artifact = Artifact(frontmatter=context["frontmatter"], body="")
    context["result"] = validate_frontmatter(artifact)


# --- Then steps --------------------------------------------------------------


@then("it reports the artifact as conforming")
def _is_conforming(context: dict) -> None:
    result = context["result"]
    assert result.conforming is True, f"expected conforming; diagnostics: {result.messages}"
    assert result.exit_code == 0


@then("it does not report derives-from as a missing required field")
def _derives_from_not_missing(context: dict) -> None:
    result = context["result"]
    assert "derives-from" not in result.missing_fields, (
        f"derives-from was wrongly reported missing; diagnostics: {result.messages}"
    )
