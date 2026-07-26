"""Step definitions for the current-state versioned-schema feature (7 scenarios).

Pins the versioned current-state schema the type system enforces under
ADR-069 D7: current-state is a numbered append-only instance whose id matches
the ``current-state-NNN`` pattern, whose status is a member of the versioned
enum ``current`` or ``superseded``, whose frontmatter additionally requires an
``incorporates`` list, and whose body carries the ``Current decisions`` and
``Stewardship`` required sections.

These scenarios PIN already-realized behaviour: current-state's typedef is
already a versioned instance (id pattern, status enum, extra-required
``incorporates``, and required-section set), so binding them against the
existing ``knowledge.schema`` checks passes on arrival. The frontmatter
scenarios assert against the :class:`ConformanceResult` from
``validate_frontmatter``; the body scenarios assert against the
:class:`SectionCheckResult` from ``check_required_sections``.

Fixtures are built in-process from a conforming current-state baseline so each
Given states exactly the one deviation the scenario is about.
"""

from __future__ import annotations

import re

import pytest
from pytest_bdd import given, parsers, scenario, then, when

from knowledge.artifact_types import Artifact, artifact_type

FEATURE = "current_state_versioned_schema.feature"


def _conforming_frontmatter() -> dict:
    """Build a fully conforming current-state frontmatter mapping.

    Every shared field is present and valid, the id matches the
    ``current-state-NNN`` pattern, the status is a member of the type's enum,
    and the type-additional ``incorporates`` field is present as a non-empty
    list. Each Given then removes or mutates exactly one field.
    """
    atype = artifact_type("current-state")
    assert atype is not None, "current-state must be a recognized type"
    frontmatter: dict = {
        "type": "current-state",
        "id": f"{atype.id_prefix}-001",
        "title": "A snapshot title",
        "status": atype.statuses[0],
        "created": "2026-01-01",
        "updated": "2026-01-02",
        "authors": ["alice"],
        "description": "A one-line description.",
        "incorporates": ["adr-069", "pdr-032"],
    }
    return frontmatter


def _body_with_sections(section_names) -> str:
    """Render a Markdown body carrying each named section as a ``## `` heading."""
    return "\n".join(f"## {name}\nbody text for {name}\n" for name in section_names)


@pytest.fixture
def context() -> dict:
    return {}


# --- Scenario bindings -------------------------------------------------------


@scenario(
    FEATURE,
    "a versioned current-state instance with a current-state-NNN id and status current conforms",
)
def test_versioned_instance_conforms() -> None: ...


@scenario(FEATURE, "each value of the current-state versioned status enum conforms")
def test_versioned_status_enum_conforms() -> None: ...


@scenario(
    FEATURE,
    "the singleton status live is reported non-conforming against the versioned current or superseded enum",
)
def test_singleton_status_live_non_conforming() -> None: ...


@scenario(
    FEATURE,
    "a bare current-state id is reported non-conforming against the versioned current-state-NNN pattern",
)
def test_bare_id_non_conforming() -> None: ...


@scenario(
    FEATURE,
    "a current-state document carrying Current decisions and Stewardship passes body conformance",
)
def test_body_full_set_conforms() -> None: ...


@scenario(
    FEATURE,
    "a current-state document missing the Stewardship section is reported non-conforming and names it",
)
def test_body_missing_stewardship() -> None: ...


@scenario(
    FEATURE,
    "a current-state artifact omitting the required incorporates field is reported non-conforming and names it",
)
def test_omits_incorporates() -> None: ...


# --- Given steps -------------------------------------------------------------


@given(
    parsers.parse(
        'a current-state artifact whose id is "{id_value}" and whose status is "{status}"'
    )
)
def _artifact_with_id_and_status(context: dict, id_value: str, status: str) -> None:
    fm = _conforming_frontmatter()
    fm["id"] = id_value
    fm["status"] = status
    context["frontmatter"] = fm


@given("it carries an incorporates list naming the accepted decisions the snapshot reflects")
def _carries_incorporates(context: dict) -> None:
    fm = context["frontmatter"]
    assert "incorporates" in fm and fm["incorporates"], (
        "the current-state baseline must carry a non-empty incorporates list"
    )
    # incorporates is a type-additional required field for current-state.
    assert "incorporates" in artifact_type("current-state").extra_required_fields


@given(
    parsers.parse(
        'a current-state artifact whose frontmatter carries a status value of "{value}"'
    )
)
def _artifact_bad_or_enum_status(context: dict, value: str) -> None:
    fm = _conforming_frontmatter()
    fm["status"] = value
    context["frontmatter"] = fm


@given(
    parsers.parse(
        '"{value}" is a member of the current-state status enum current or superseded'
    )
)
def _value_in_status_enum(context: dict, value: str) -> None:
    assert value in artifact_type("current-state").statuses, (
        f"'{value}' is not a member of the current-state status enum "
        f"{artifact_type('current-state').statuses!r}"
    )


@given(
    parsers.parse(
        '"{value}" is not a member of the current-state status enum current or superseded'
    )
)
def _value_not_in_status_enum(context: dict, value: str) -> None:
    assert value not in artifact_type("current-state").statuses, (
        f"'{value}' is unexpectedly a member of the current-state status enum "
        f"{artifact_type('current-state').statuses!r}"
    )


@given(
    parsers.parse(
        'a current-state artifact whose id is "{value}" rather than the '
        "current-state-NNN pattern its type now requires"
    )
)
def _artifact_bad_id(context: dict, value: str) -> None:
    fm = _conforming_frontmatter()
    fm["id"] = value
    context["frontmatter"] = fm


@given(
    "a current-state document whose body carries Current decisions and "
    "Stewardship, its type's required-section set"
)
def _body_full_set(context: dict) -> None:
    atype = artifact_type("current-state")
    assert set(atype.required_sections) == {"Current decisions", "Stewardship"}
    context["artifact"] = Artifact(
        frontmatter={"type": "current-state"},
        body=_body_with_sections(atype.required_sections),
    )


@given(
    "a current-state document whose body carries Current decisions but omits "
    "the Stewardship section its type's required-section set demands"
)
def _body_omits_stewardship(context: dict) -> None:
    atype = artifact_type("current-state")
    assert "Stewardship" in atype.required_sections
    present = [s for s in atype.required_sections if s != "Stewardship"]
    assert present and "Stewardship" not in present
    context["artifact"] = Artifact(
        frontmatter={"type": "current-state"},
        body=_body_with_sections(present),
    )


@given(
    "a current-state artifact whose frontmatter carries every shared required "
    "field but omits the incorporates field its type additionally requires"
)
def _omits_incorporates(context: dict) -> None:
    fm = _conforming_frontmatter()
    del fm["incorporates"]
    context["frontmatter"] = fm


# --- When steps --------------------------------------------------------------


@when("the knowledge context validates the artifact's frontmatter against the schema")
def _validate(context: dict) -> None:
    from knowledge.schema import validate_frontmatter

    artifact = Artifact(frontmatter=context["frontmatter"], body="")
    context["result"] = validate_frontmatter(artifact)


@when("the knowledge context checks the document's body against its type's required-section set")
def _check_sections(context: dict) -> None:
    from knowledge.schema import check_required_sections

    context["result"] = check_required_sections(context["artifact"])


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


@then("it reports the artifact as non-conforming")
def _is_non_conforming(context: dict) -> None:
    result = context["result"]
    assert result.conforming is False
    assert result.exit_code != 0


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


@then("the diagnosis names the offending id and the expected current-state-NNN pattern")
def _names_id_and_pattern(context: dict) -> None:
    result = context["result"]
    diag = next(d for d in result.diagnostics if d.code == "id-pattern-mismatch")
    assert diag.offending == "current-state"
    assert "current-state-NNN" in (diag.expected or "")
    assert "current-state" in diag.message and "current-state-NNN" in diag.message


@then(parsers.parse("the diagnosis names {field} as the missing type-required field"))
def _names_missing_type_required(context: dict, field: str) -> None:
    result = context["result"]
    assert field in result.missing_fields
    assert any(field in m for m in result.messages)


@then("it reports the document as conforming on body structure")
def _conforming_body(context: dict) -> None:
    result = context["result"]
    assert result.conforming is True, f"expected conforming; missing: {result.missing_sections}"
    assert result.exit_code == 0


@then("it names no missing required section")
def _no_missing_section(context: dict) -> None:
    assert context["result"].missing_sections == ()


@then("it reports the document as non-conforming for a missing required section")
def _non_conforming_body(context: dict) -> None:
    result = context["result"]
    assert result.conforming is False
    assert result.exit_code != 0


@then(parsers.parse("the diagnosis names {section} as the missing section"))
def _names_missing_section(context: dict, section: str) -> None:
    result = context["result"]
    assert section in result.missing_sections
    assert any(section in m for m in result.messages)
