"""Step definitions for the frontmatter-conformance feature (12 scenarios).

Binds every scenario in ``frontmatter_conformance.feature`` and asserts each
Then/And leg against the :class:`ConformanceResult` returned by
``knowledge.schema.validate_frontmatter``.

RED leg: ``knowledge.schema`` does not yet exist, so ``validate_frontmatter`` is
imported inside the shared ``When`` step body — every scenario fails at that
step on the absent behaviour, not at collection time. The GREEN leg adds
``knowledge.schema`` and makes all twelve pass.

Fixtures are built in-process from a conforming baseline per type (rather than
from on-disk fixture files) so each Given states exactly the one deviation the
scenario is about.
"""

from __future__ import annotations

import pytest
from pytest_bdd import given, parsers, scenario, then, when

from knowledge.artifact_types import Artifact, artifact_type

FEATURE = "frontmatter_conformance.feature"


def _conforming_frontmatter(type_name: str) -> dict:
    """Build a fully conforming frontmatter mapping for ``type_name``.

    Every shared field is present and valid, the id matches the type's pattern,
    the status is a member of the type's enum, and every type-additional
    required field is present (non-empty where the type demands an anchor). Each
    Given then removes or mutates exactly one field.
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
        # Anchor fields carry a non-empty list; other extras a scalar.
        frontmatter[extra] = ["pdr-001"] if extra == "derives-from" else ["alice"]
    return frontmatter


@pytest.fixture
def context() -> dict:
    return {}


# --- Scenario bindings -------------------------------------------------------


@scenario(FEATURE, "a well-formed artifact passes frontmatter conformance")
def test_well_formed_conforms() -> None: ...


@scenario(
    FEATURE,
    "an artifact missing the required description field is reported non-conforming and names it",
)
def test_missing_description() -> None: ...


@scenario(
    FEATURE,
    "an artifact missing the required authors field is reported non-conforming and names it",
)
def test_missing_authors() -> None: ...


@scenario(
    FEATURE,
    "an artifact missing the required updated field is reported non-conforming and names it",
)
def test_missing_updated() -> None: ...


@scenario(
    FEATURE,
    "a status value outside the type's recognized enum is reported non-conforming and names the offending value",
)
def test_unrecognized_status() -> None: ...


@scenario(FEATURE, "an id that does not match the type's id pattern is reported non-conforming")
def test_id_pattern_mismatch() -> None: ...


@scenario(
    FEATURE,
    "an unrecognized type value is reported non-conforming and names the offending value",
)
def test_unrecognized_type() -> None: ...


@scenario(
    FEATURE,
    "an artifact missing a field its type additionally requires is reported non-conforming",
)
def test_missing_type_field_decision_makers() -> None: ...


@scenario(
    FEATURE,
    "a pdr omitting the required derives-from field is reported non-conforming and names it",
)
def test_missing_type_field_derives_from() -> None: ...


@scenario(
    FEATURE,
    "an adr whose derives-from list is empty is reported non-conforming for anchoring to nothing",
)
def test_adr_empty_anchor() -> None: ...


@scenario(FEATURE, "optional fields may be absent and the artifact still conforms")
def test_optional_absent_conforms() -> None: ...


@scenario(
    FEATURE,
    "disclosure level is a projection and is never a stored frontmatter field",
)
def test_stored_disclosure_level() -> None: ...


# --- Given steps -------------------------------------------------------------


@given(
    "an artifact whose frontmatter carries type, id, title, status, created, "
    "updated, authors and description"
)
def _base_conforming(context: dict) -> None:
    # Use pdr as the well-formed baseline: it exercises type-additional required
    # fields as well as the eight shared ones.
    context["frontmatter"] = _conforming_frontmatter("pdr")


@given("the id matches the id pattern its type requires")
def _id_matches(context: dict) -> None:
    atype = artifact_type(context["frontmatter"]["type"])
    import re

    assert re.fullmatch(atype.id_pattern, context["frontmatter"]["id"])


@given("the status value is a member of the enum its type recognizes")
def _status_in_enum(context: dict) -> None:
    atype = artifact_type(context["frontmatter"]["type"])
    assert context["frontmatter"]["status"] in atype.statuses


@given("it carries every field its type additionally requires")
def _carries_type_extras(context: dict) -> None:
    atype = artifact_type(context["frontmatter"]["type"])
    for extra in atype.extra_required_fields:
        assert extra in context["frontmatter"]


@given("an artifact whose frontmatter omits the required description field")
def _omit_description(context: dict) -> None:
    fm = _conforming_frontmatter("candidate")
    del fm["description"]
    context["frontmatter"] = fm


@given("an artifact whose frontmatter omits the required authors field")
def _omit_authors(context: dict) -> None:
    fm = _conforming_frontmatter("candidate")
    del fm["authors"]
    context["frontmatter"] = fm


@given("an artifact whose frontmatter carries created but omits the required updated field")
def _omit_updated(context: dict) -> None:
    fm = _conforming_frontmatter("candidate")
    assert "created" in fm
    del fm["updated"]
    context["frontmatter"] = fm


@given(parsers.parse('a candidate artifact whose frontmatter carries a status value of "{value}"'))
def _candidate_bad_status(context: dict, value: str) -> None:
    fm = _conforming_frontmatter("candidate")
    fm["status"] = value
    context["frontmatter"] = fm


@given(
    '"in-progress" is not a member of the candidate status enum exploring, '
    "shaped, briefed, parked or rejected"
)
def _in_progress_not_in_enum(context: dict) -> None:
    assert "in-progress" not in artifact_type("candidate").statuses


@given(
    parsers.parse(
        'a candidate artifact whose id is "{value}" rather than the cand-NNN '
        "pattern its type requires"
    )
)
def _candidate_bad_id(context: dict, value: str) -> None:
    fm = _conforming_frontmatter("candidate")
    fm["id"] = value
    context["frontmatter"] = fm


@given(parsers.parse('an artifact whose frontmatter carries a type value of "{value}"'))
def _artifact_bad_type(context: dict, value: str) -> None:
    fm = _conforming_frontmatter("candidate")
    fm["type"] = value
    context["frontmatter"] = fm


@given('"roadmap" is not one of the eight recognized artifact types')
def _roadmap_unrecognized(context: dict) -> None:
    from knowledge.artifact_types import RECOGNIZED_ARTIFACT_TYPES

    assert "roadmap" not in RECOGNIZED_ARTIFACT_TYPES


@given(
    "a pdr artifact whose frontmatter carries every shared required field but "
    "omits the decision-makers field its type additionally requires"
)
def _pdr_omit_decision_makers(context: dict) -> None:
    fm = _conforming_frontmatter("pdr")
    del fm["decision-makers"]
    context["frontmatter"] = fm


@given(
    "a pdr artifact whose frontmatter carries every shared required field but "
    "omits the derives-from field its type additionally requires"
)
def _pdr_omit_derives_from(context: dict) -> None:
    fm = _conforming_frontmatter("pdr")
    del fm["derives-from"]
    context["frontmatter"] = fm


@given("an adr artifact whose frontmatter carries a derives-from field whose value is an empty list")
def _adr_empty_derives_from(context: dict) -> None:
    fm = _conforming_frontmatter("adr")
    fm["derives-from"] = []
    context["frontmatter"] = fm


@given(
    "an artifact that carries every required field and a recognized status but "
    "omits the optional beads field"
)
def _conforming_without_beads(context: dict) -> None:
    fm = _conforming_frontmatter("candidate")
    assert "beads" not in fm
    context["frontmatter"] = fm


@given("an artifact whose frontmatter carries a stored disclosure-level field pinning its own tier")
def _stored_disclosure_level(context: dict) -> None:
    fm = _conforming_frontmatter("candidate")
    fm["disclosure-level"] = "L1"
    context["frontmatter"] = fm


# --- When step (shared) ------------------------------------------------------


@when("the knowledge context validates the artifact's frontmatter against the schema")
def _validate(context: dict) -> None:
    # Imported here so the RED commit fails on the absent behaviour rather than
    # at collection/import time.
    from knowledge.schema import validate_frontmatter

    artifact = Artifact(frontmatter=context["frontmatter"], body="")
    context["result"] = validate_frontmatter(artifact)


# --- Then steps --------------------------------------------------------------


@then("it reports the artifact as conforming")
def _is_conforming(context: dict) -> None:
    result = context["result"]
    assert result.conforming is True, f"expected conforming; diagnostics: {result.messages}"
    assert result.exit_code == 0


@then("it reports no missing required fields")
def _no_missing_fields(context: dict) -> None:
    assert context["result"].missing_fields == ()


@then("it reports the artifact as non-conforming")
def _is_non_conforming(context: dict) -> None:
    assert context["result"].conforming is False
    assert context["result"].exit_code != 0


@then(parsers.parse("the diagnosis names {field} as the missing required field"))
def _names_missing_required(context: dict, field: str) -> None:
    assert field in context["result"].missing_fields
    assert any(field in m for m in context["result"].messages)


@then(parsers.parse("the diagnosis names {field} as the missing type-required field"))
def _names_missing_type_required(context: dict, field: str) -> None:
    assert field in context["result"].missing_fields
    assert any(field in m for m in context["result"].messages)


@then("it reports the artifact as non-conforming for an unrecognized status")
def _non_conforming_status(context: dict) -> None:
    result = context["result"]
    assert result.conforming is False
    assert any(d.code == "unrecognized-status" for d in result.diagnostics)


@then(parsers.parse('the diagnosis names the offending value "{value}"'))
def _names_offending_value(context: dict, value: str) -> None:
    result = context["result"]
    assert any(d.offending == value for d in result.diagnostics)
    assert any(value in m for m in result.messages)


@then("it reports the artifact as non-conforming for an id that does not match its type pattern")
def _non_conforming_id(context: dict) -> None:
    result = context["result"]
    assert result.conforming is False
    assert any(d.code == "id-pattern-mismatch" for d in result.diagnostics)


@then("the diagnosis names the offending id and the expected pattern")
def _names_id_and_pattern(context: dict) -> None:
    result = context["result"]
    diag = next(d for d in result.diagnostics if d.code == "id-pattern-mismatch")
    assert diag.offending == "candidate-1"
    assert "cand-NNN" == diag.expected or "cand-NNN" in (diag.expected or "")
    assert "candidate-1" in diag.message and "cand-NNN" in diag.message


@then("it reports the artifact as non-conforming for an unrecognized type")
def _non_conforming_type(context: dict) -> None:
    result = context["result"]
    assert result.conforming is False
    assert any(d.code == "unrecognized-type" for d in result.diagnostics)


@then("the diagnosis names derives-from and states that an adr requires at least one anchor")
def _names_anchor_requirement(context: dict) -> None:
    result = context["result"]
    diag = next(d for d in result.diagnostics if d.code == "empty-anchor")
    assert diag.field == "derives-from"
    assert "derives-from" in diag.message
    assert "at least one anchor" in diag.message


@then("it reports the artifact as non-conforming for an adr that anchors to no upstream artifact")
def _non_conforming_anchor(context: dict) -> None:
    result = context["result"]
    assert result.conforming is False
    assert any(d.code == "empty-anchor" for d in result.diagnostics)


@then("it does not report the absent beads field as missing")
def _beads_not_missing(context: dict) -> None:
    assert "beads" not in context["result"].missing_fields


@then("it reports the artifact as non-conforming for storing a disclosure-level field")
def _non_conforming_disclosure(context: dict) -> None:
    result = context["result"]
    assert result.conforming is False
    assert any(d.code == "stored-projection-field" for d in result.diagnostics)


@then(
    "the diagnosis states that disclosure level is a projection emitted by the "
    "tool and is never a stored frontmatter field"
)
def _disclosure_message(context: dict) -> None:
    result = context["result"]
    diag = next(d for d in result.diagnostics if d.code == "stored-projection-field")
    assert diag.field == "disclosure-level"
    assert "projection" in diag.message
    assert "never a stored frontmatter field" in diag.message
