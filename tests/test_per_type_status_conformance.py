"""Step definitions for the per-type status enum conformance feature.

Binds the two Scenario Outlines in ``per_type_status_conformance.feature``,
which pin that ``knowledge.schema.validate_frontmatter`` resolves each
artifact's status enum from its *own* type in the single registry: a status
inside its kind's enum conforms, and a status outside it is reported
non-conforming for an unrecognized status naming the offending value.

This mirrors the fixture pattern in ``test_frontmatter_conformance.py``: a
fully conforming frontmatter is built in-process per kind so the only variable
under test is the ``status`` value each Examples row supplies. Ids are built to
match each type's id pattern (the session-record's date-plus-letter id, the
others' ``<prefix>-NNN``) so that — apart from the status — nothing else in the
frontmatter draws a diagnostic and the conforming rows are genuinely conforming.
"""

from __future__ import annotations

import pytest
from pytest_bdd import given, parsers, scenario, then, when

from knowledge.artifact_types import Artifact, artifact_type

FEATURE = "per_type_status_conformance.feature"

# A valid id per kind, matching that type's id pattern. Every kind but
# session-record uses the default ``<prefix>-NNN`` form; session-record is named
# by the day it happened (``sess-YYYY-MM-DD-x``).
_VALID_IDS: dict[str, str] = {
    "adr": "adr-001",
    "pdr": "pdr-001",
    "brief": "brief-001",
    "session-record": "sess-2026-07-16-a",
    "prioritization-record": "prio-001",
}


def _conforming_frontmatter(kind: str, status: str) -> dict:
    """Build a fully conforming frontmatter for ``kind`` carrying ``status``.

    Every shared field is present and valid, the id matches the kind's pattern,
    and every type-additional required field is present (non-empty where the
    kind demands an anchor). The only field a scenario varies is ``status``, so
    a diagnosis — when one appears — is attributable to the status alone.
    """
    atype = artifact_type(kind)
    assert atype is not None, f"{kind} must be a recognized type"
    frontmatter: dict = {
        "type": kind,
        "id": _VALID_IDS[kind],
        "title": "A title",
        "status": status,
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


# --- Scenario bindings -------------------------------------------------------


@scenario(FEATURE, "a status value inside its kind's enum conforms")
def test_status_inside_enum_conforms() -> None: ...


@scenario(
    FEATURE,
    "a status value outside its kind's enum is reported non-conforming and names the offending value",
)
def test_status_outside_enum_non_conforming() -> None: ...


# --- Given steps -------------------------------------------------------------


@given(
    parsers.parse('a {kind} artifact whose frontmatter carries a status value of "{status}"')
)
def _kind_artifact_with_status(context: dict, kind: str, status: str) -> None:
    context["frontmatter"] = _conforming_frontmatter(kind, status)


@given(parsers.parse('"{status}" is a member of the {kind} status enum'))
def _status_is_member(context: dict, status: str, kind: str) -> None:
    atype = artifact_type(kind)
    assert atype is not None
    assert status in atype.statuses, (
        f"'{status}' is expected to be a member of the {kind} status enum {atype.statuses!r}"
    )


@given(parsers.parse('"{status}" is not a member of the {kind} status enum'))
def _status_is_not_member(context: dict, status: str, kind: str) -> None:
    atype = artifact_type(kind)
    assert atype is not None
    assert status not in atype.statuses, (
        f"'{status}' is expected NOT to be a member of the {kind} status enum {atype.statuses!r}"
    )


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


@then("it does not report an unrecognized-status diagnosis")
def _no_unrecognized_status(context: dict) -> None:
    result = context["result"]
    assert not any(d.code == "unrecognized-status" for d in result.diagnostics), (
        f"a member status was wrongly flagged unrecognized; diagnostics: {result.messages}"
    )


@then("it reports the artifact as non-conforming for an unrecognized status")
def _non_conforming_status(context: dict) -> None:
    result = context["result"]
    assert result.conforming is False
    assert result.exit_code != 0
    assert any(d.code == "unrecognized-status" for d in result.diagnostics), (
        f"expected an unrecognized-status diagnosis; diagnostics: {result.messages}"
    )


@then(parsers.parse('the diagnosis names the offending value "{value}"'))
def _names_offending_value(context: dict, value: str) -> None:
    result = context["result"]
    assert any(
        d.code == "unrecognized-status" and d.offending == value for d in result.diagnostics
    ), f"no unrecognized-status diagnosis named the offending value '{value}': {result.messages}"
    assert any(value in m for m in result.messages)
