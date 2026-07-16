"""Step definitions for the real-practice typedef corrections feature (19 scenarios).

Binds every scenario in ``typedef_real_practice_corrections.feature`` and
asserts each Then/And leg against the single-sourced typedef registry
(:mod:`knowledge.artifact_types`), the format generator
(:mod:`knowledge.typedefs`), and the conformance checks
(:mod:`knowledge.schema`).

The three corrected typedefs — intent-record, candidate and session-record —
each drive their generated template sections/order, the generated schema
fragment's status enum and id pattern, and the body/frontmatter conformance
checks. Because each type is single-sourced by its typedef, the assertions here
read the GENERATED output (template bytes, schema-fragment bytes) and the
conformance results rather than re-spelling the rules.

Documents and frontmatter are built in-process from the section/status/id shapes
each scenario names (not from on-disk fixtures) so each Given states exactly the
one deviation under test. The "N independently-authored instances" clauses are
rationale for why the corrected shape is the real-practice one; the testable
assertions are on the generator output and the conformance verdicts.
"""

from __future__ import annotations

import json
import re

import pytest
from pytest_bdd import given, parsers, scenario, then, when

from knowledge.artifact_types import Artifact, artifact_type
from knowledge.schema import (
    ID_PATTERN_MISMATCH,
    UNRECOGNIZED_STATUS,
    check_required_sections,
    validate_frontmatter,
)
from knowledge.typedefs import generate_typedef_format

FEATURE = "typedef_real_practice_corrections.feature"


# --- Helpers -----------------------------------------------------------------


def _body_with_sections(names) -> str:
    """Render a Markdown body carrying each named section as a ``## `` heading."""
    return "\n".join(f"## {name}\nbody text for {name}\n" for name in names)


def _template_sections(type_name: str) -> tuple[str, ...]:
    """The ``## `` section headings the generated template for a type declares."""
    text = generate_typedef_format(artifact_type(type_name)).template.data.decode("utf-8")
    return tuple(
        line[3:].strip() for line in text.splitlines() if line.startswith("## ")
    )


def _fragment(type_name: str) -> dict:
    """The generated schema fragment for a type, parsed from its JSON bytes."""
    data = generate_typedef_format(artifact_type(type_name)).schema_fragment.data
    return json.loads(data.decode("utf-8"))


def _full_frontmatter(type_name: str, *, id_value: str, status_value: str) -> dict:
    """A frontmatter mapping conforming on every axis except the one under test.

    Every shared field is present, each type-additional required field is
    present, and ``id``/``status`` are set to the scenario's values — so the only
    conformance verdict that can move is the id-pattern or status-enum leg the
    scenario is about.
    """
    atype = artifact_type(type_name)
    frontmatter: dict = {
        "type": type_name,
        "id": id_value,
        "title": "A title",
        "status": status_value,
        "created": "2026-01-01",
        "updated": "2026-01-02",
        "authors": ["alice"],
        "description": "A one-line description.",
    }
    for extra in atype.extra_required_fields:
        frontmatter[extra] = ["pdr-001"] if extra == "derives-from" else []
    return frontmatter


@pytest.fixture
def context() -> dict:
    return {}


# =============================================================================
# Behavior A — intent-record requires its 8 real-practice body sections in order
# =============================================================================

INTENT_SECTIONS = (
    "Verbatim anchors",
    "The goal behind the ask",
    "Who it serves",
    "Constraints",
    "Non-goals",
    "Appetite signal",
    "Failure conditions",
    "Open threads",
)


@scenario(FEATURE, "the intent-record typedef requires each of the 8 real-practice body sections")
def test_intent_eight_sections() -> None: ...


@scenario(FEATURE, "the intent-record typedef positions Verbatim anchors first, immediately after the title")
def test_intent_section_order() -> None: ...


@scenario(FEATURE, "an intent-record document missing a required section is reported non-conforming and names it")
def test_intent_missing_section() -> None: ...


@scenario(FEATURE, "an intent-record document carrying its type's full 8-section required set passes")
def test_intent_full_section_set() -> None: ...


@given(
    'the intent-record typedef, whose generated template today declares only "Intent" '
    'and "Signals of success", sections no real instance has ever used'
)
def _intent_typedef_old_sections(context: dict) -> None:
    context["type"] = "intent-record"


@given(
    parsers.parse(
        "7 independently-authored intent-record instances (intent-001 through "
        'intent-007) that instead consistently carry "{section}" as a body section'
    )
)
def _intent_instances_carry_section(context: dict, section: str) -> None:
    # Rationale for why the corrected section set is real practice; the testable
    # assertion is on the generated template, checked in the Then leg.
    context.setdefault("type", "intent-record")


@given(
    "the intent-record typedef's real-practice section order: Verbatim anchors, "
    "The goal behind the ask, Who it serves, Constraints, Non-goals, Appetite "
    "signal, Failure conditions, Open threads"
)
def _intent_real_order(context: dict) -> None:
    context["type"] = "intent-record"


@given(
    "an intent-record document whose body carries every section in its type's "
    "required-section set except Failure conditions"
)
def _intent_missing_failure_conditions(context: dict) -> None:
    present = [s for s in INTENT_SECTIONS if s != "Failure conditions"]
    context["artifact"] = Artifact(
        frontmatter={"type": "intent-record"}, body=_body_with_sections(present)
    )


@given(
    "an intent-record document whose body carries Verbatim anchors, The goal behind "
    "the ask, Who it serves, Constraints, Non-goals, Appetite signal, Failure "
    "conditions and Open threads"
)
def _intent_full_body(context: dict) -> None:
    context["artifact"] = Artifact(
        frontmatter={"type": "intent-record"}, body=_body_with_sections(INTENT_SECTIONS)
    )


@when("the knowledge context runs the format generator over the intent-record typedef")
def _generate_intent(context: dict) -> None:
    context["type"] = "intent-record"


@then(parsers.parse('the generated intent-record template declares "{section}" as a required body section'))
def _intent_template_declares_section(section: str) -> None:
    assert section in _template_sections("intent-record"), (
        f"generated intent-record template does not declare section {section!r}; "
        f"has {_template_sections('intent-record')}"
    )


@then(
    "the generated intent-record template positions Verbatim anchors immediately "
    "after the title and before The goal behind the ask"
)
def _intent_verbatim_first() -> None:
    sections = _template_sections("intent-record")
    assert sections[0] == "Verbatim anchors", f"first section is {sections[:1]}"
    assert sections[1] == "The goal behind the ask", f"second section is {sections[1:2]}"


@then(
    "the remaining sections appear in the order Who it serves, Constraints, "
    "Non-goals, Appetite signal, Failure conditions, Open threads"
)
def _intent_remaining_order() -> None:
    sections = _template_sections("intent-record")
    assert sections[2:] == (
        "Who it serves",
        "Constraints",
        "Non-goals",
        "Appetite signal",
        "Failure conditions",
        "Open threads",
    ), f"remaining order is {sections[2:]}"


# --- Shared body-section When / Then legs (first defined here) ---------------


@when("the knowledge context checks the document's body against its type's required-section set")
def _check_sections(context: dict) -> None:
    context["section_result"] = check_required_sections(context["artifact"])


@then("it reports the document as non-conforming for a missing required section")
def _body_non_conforming(context: dict) -> None:
    result = context["section_result"]
    assert result.conforming is False
    assert result.exit_code != 0


@then("it reports the document as conforming on body structure")
def _body_conforming(context: dict) -> None:
    result = context["section_result"]
    assert result.conforming is True, f"missing: {result.missing_sections}"
    assert result.exit_code == 0


@then("it names no missing required section")
def _body_no_missing(context: dict) -> None:
    assert context["section_result"].missing_sections == ()


@then(parsers.parse("the diagnosis names {section} as the missing section"))
def _body_names_missing(context: dict, section: str) -> None:
    result = context["section_result"]
    assert section in result.missing_sections, (
        f"{section!r} not in missing {result.missing_sections}"
    )
    assert any(section in m for m in result.messages)


# --- Shared frontmatter-validate When / Then legs (first defined here) -------


@when("the knowledge context validates the artifact's frontmatter against the schema")
def _validate_frontmatter(context: dict) -> None:
    context["fm_result"] = validate_frontmatter(context["artifact"])


@then("it reports the artifact as conforming")
def _fm_conforming(context: dict) -> None:
    result = context["fm_result"]
    assert result.conforming is True, f"diagnostics: {result.messages}"
    assert result.exit_code == 0


@then("it does not report an unrecognized-status diagnosis")
def _fm_no_unrecognized_status(context: dict) -> None:
    assert context["fm_result"].by_code(UNRECOGNIZED_STATUS) == ()


@then("it reports the artifact as non-conforming for an unrecognized status")
def _fm_unrecognized_status(context: dict) -> None:
    result = context["fm_result"]
    assert result.conforming is False
    assert result.by_code(UNRECOGNIZED_STATUS), "expected an unrecognized-status diagnostic"


@then(parsers.parse('the diagnosis names the offending value "{value}"'))
def _fm_names_offending_status(context: dict, value: str) -> None:
    diags = context["fm_result"].by_code(UNRECOGNIZED_STATUS)
    assert any(d.offending == value for d in diags), (
        f"no unrecognized-status diagnostic names {value!r}: {[d.offending for d in diags]}"
    )
    assert any(value in d.message for d in diags)


# =============================================================================
# Behavior B — intent-record status enum is exactly "recorded"
# =============================================================================


@scenario(FEATURE, '"recorded" is a valid intent-record status value, matching every real instance')
def test_intent_recorded_valid() -> None: ...


@scenario(FEATURE, 'the intent-record status enum is exactly the single real-practice value "recorded"')
def test_intent_enum_exactly_recorded() -> None: ...


@scenario(
    FEATURE,
    "an intent-record artifact carrying a status value outside the real enum is "
    "reported non-conforming and names the offending value",
)
def test_intent_draft_non_conforming() -> None: ...


@given('an intent-record artifact whose frontmatter carries a status value of "recorded"')
def _intent_status_recorded(context: dict) -> None:
    context["artifact"] = Artifact(
        frontmatter=_full_frontmatter("intent-record", id_value="intent-001", status_value="recorded")
    )


@given(
    "the intent-record typedef, whose currently generated status enum is draft, "
    "active, fulfilled or abandoned — a set no real intent-record instance has "
    "ever used"
)
def _intent_typedef_old_enum(context: dict) -> None:
    context["type"] = "intent-record"


@given(
    "7 independently-authored intent-record instances (intent-001 through "
    'intent-007), each carrying status "recorded" and none carrying draft, active, '
    "fulfilled or abandoned"
)
def _intent_instances_recorded(context: dict) -> None:
    context.setdefault("type", "intent-record")


@then('the generated schema fragment\'s status enum for intent-record contains exactly one value, "recorded"')
def _intent_enum_exactly_recorded() -> None:
    assert _fragment("intent-record")["statuses"] == ["recorded"]


@then('none of "draft", "active", "fulfilled" or "abandoned" is a member of the generated status enum')
def _intent_enum_excludes_old() -> None:
    statuses = set(_fragment("intent-record")["statuses"])
    assert statuses.isdisjoint({"draft", "active", "fulfilled", "abandoned"})


@given('an intent-record artifact whose frontmatter carries a status value of "draft"')
def _intent_status_draft(context: dict) -> None:
    context["artifact"] = Artifact(
        frontmatter=_full_frontmatter("intent-record", id_value="intent-001", status_value="draft")
    )


@given('"draft" is not a member of the intent-record status enum recorded')
def _draft_not_in_recorded(context: dict) -> None:
    # Rationale; the assertion is on the validation verdict in the Then leg.
    pass


# =============================================================================
# Behavior C — candidate requires its 9 real-practice narrative body sections
# =============================================================================

CANDIDATE_SECTIONS = (
    "Verbatim anchors",
    "Problem",
    "Appetite",
    "Solution sketch",
    "Rabbit holes",
    "No-gos",
    "Evidence / experiments",
    "Resolution",
    "Changelog",
)


@scenario(FEATURE, "the candidate typedef requires each of the real-practice narrative body sections beyond Verbatim anchors")
def test_candidate_narrative_sections() -> None: ...


@scenario(FEATURE, "the candidate typedef's narrative sections follow real practice's order, immediately after Verbatim anchors")
def test_candidate_section_order() -> None: ...


@scenario(FEATURE, "a candidate document missing the Resolution section is reported non-conforming and names it")
def test_candidate_missing_resolution() -> None: ...


@scenario(FEATURE, "a candidate document carrying its full 9-section required set passes")
def test_candidate_full_section_set() -> None: ...


@given(
    'the candidate typedef, whose generated template today declares only "Context" '
    'and "Open questions", sections no real instance has ever used'
)
def _candidate_typedef_old_sections(context: dict) -> None:
    context["type"] = "candidate"


@given(
    parsers.parse(
        "5 independently-authored candidate instances (cand-001 through cand-005) "
        'that instead consistently carry "{section}" as a body section'
    )
)
def _candidate_instances_carry_section(context: dict, section: str) -> None:
    context.setdefault("type", "candidate")


@given(
    "the candidate typedef's real-practice section order: Verbatim anchors, "
    "Problem, Appetite, Solution sketch, Rabbit holes, No-gos, Evidence / "
    "experiments, Resolution, Changelog"
)
def _candidate_real_order(context: dict) -> None:
    context["type"] = "candidate"


@when("the knowledge context runs the format generator over the candidate typedef")
def _generate_candidate(context: dict) -> None:
    context["type"] = "candidate"


@then(parsers.parse('the generated candidate template declares "{section}" as a required body section'))
def _candidate_template_declares_section(section: str) -> None:
    assert section in _template_sections("candidate"), (
        f"generated candidate template does not declare section {section!r}; "
        f"has {_template_sections('candidate')}"
    )


@then("the generated candidate template positions Problem immediately after Verbatim anchors")
def _candidate_problem_after_verbatim() -> None:
    sections = _template_sections("candidate")
    assert sections[0] == "Verbatim anchors", f"first section is {sections[:1]}"
    assert sections[1] == "Problem", f"second section is {sections[1:2]}"


@then(
    "the remaining sections appear in the order Appetite, Solution sketch, Rabbit "
    "holes, No-gos, Evidence / experiments, Resolution, Changelog"
)
def _candidate_remaining_order() -> None:
    sections = _template_sections("candidate")
    assert sections[2:] == (
        "Appetite",
        "Solution sketch",
        "Rabbit holes",
        "No-gos",
        "Evidence / experiments",
        "Resolution",
        "Changelog",
    ), f"remaining order is {sections[2:]}"


@given(
    "a candidate document whose body carries Verbatim anchors, Problem, Appetite, "
    "Solution sketch, Rabbit holes, No-gos and Evidence / experiments but omits "
    "Resolution"
)
def _candidate_missing_resolution(context: dict) -> None:
    present = [s for s in CANDIDATE_SECTIONS if s not in ("Resolution", "Changelog")]
    context["artifact"] = Artifact(
        frontmatter={"type": "candidate"}, body=_body_with_sections(present)
    )


@given(
    "a candidate document whose body carries Verbatim anchors, Problem, Appetite, "
    "Solution sketch, Rabbit holes, No-gos, Evidence / experiments, Resolution and "
    "Changelog"
)
def _candidate_full_body(context: dict) -> None:
    context["artifact"] = Artifact(
        frontmatter={"type": "candidate"}, body=_body_with_sections(CANDIDATE_SECTIONS)
    )


# =============================================================================
# Behavior D — candidate status enum includes committed
# =============================================================================


@scenario(FEATURE, "the candidate typedef's generated status enum includes committed, the value cand-005 uses")
def test_candidate_enum_includes_committed() -> None: ...


@scenario(FEATURE, "a candidate artifact carrying status committed passes frontmatter conformance")
def test_candidate_committed_conforms() -> None: ...


@scenario(
    FEATURE,
    "a status value outside the type's recognized enum is reported non-conforming "
    "and names the offending value",
)
def test_candidate_in_progress_non_conforming() -> None: ...


@given(
    "the candidate typedef, whose currently generated status enum is exploring, "
    "shaped, briefed, parked or rejected — a set that omits committed, the value "
    "cand-005's ratification uses"
)
def _candidate_typedef_old_enum(context: dict) -> None:
    context["type"] = "candidate"


@given(
    "5 independently-authored candidate instances, four (cand-001 through cand-004) "
    "carrying status shaped and one (cand-005) carrying status committed once the "
    "product authority ratified it"
)
def _candidate_instances_committed(context: dict) -> None:
    context.setdefault("type", "candidate")


@then("the generated schema fragment's status enum for candidate is exploring, shaped, briefed, committed, parked and rejected")
def _candidate_enum_full() -> None:
    assert _fragment("candidate")["statuses"] == [
        "exploring",
        "shaped",
        "briefed",
        "committed",
        "parked",
        "rejected",
    ]


@then("committed is a member of the generated status enum")
def _candidate_enum_has_committed() -> None:
    assert "committed" in _fragment("candidate")["statuses"]


@given('a candidate artifact whose frontmatter carries a status value of "committed"')
def _candidate_status_committed(context: dict) -> None:
    context["artifact"] = Artifact(
        frontmatter=_full_frontmatter("candidate", id_value="cand-001", status_value="committed")
    )


@given('a candidate artifact whose frontmatter carries a status value of "in-progress"')
def _candidate_status_in_progress(context: dict) -> None:
    context["artifact"] = Artifact(
        frontmatter=_full_frontmatter("candidate", id_value="cand-001", status_value="in-progress")
    )


@given('"in-progress" is not a member of the candidate status enum exploring, shaped, briefed, committed, parked or rejected')
def _in_progress_not_in_enum(context: dict) -> None:
    # Rationale; the assertion is on the validation verdict in the Then leg.
    pass


# =============================================================================
# Behavior E — session-record requires Outcome and Open threads body sections
# =============================================================================


@scenario(FEATURE, "the session-record typedef requires an Outcome section and an Open threads section, not Summary and Outcomes")
def test_session_sections() -> None: ...


@scenario(FEATURE, "a session-record document missing the Open threads section is reported non-conforming and names it")
def test_session_missing_open_threads() -> None: ...


@scenario(FEATURE, "a session-record document carrying Outcome and Open threads passes conformance")
def test_session_full_section_set() -> None: ...


@given(
    'the session-record typedef, whose currently generated template declares "Summary" '
    'and "Outcomes" as its two body sections, headings no real instance has ever used'
)
def _session_typedef_old_sections(context: dict) -> None:
    context["type"] = "session-record"


@given(
    "5 independently-authored session-record instances that instead consistently "
    'carry "Outcome" and "Open threads" as their two body sections'
)
def _session_instances_carry_sections(context: dict) -> None:
    context.setdefault("type", "session-record")


@when("the knowledge context runs the format generator over the session-record typedef")
def _generate_session(context: dict) -> None:
    context["type"] = "session-record"


@then("the generated session-record template declares Outcome and Open threads as its required body sections")
def _session_template_declares_sections() -> None:
    sections = _template_sections("session-record")
    assert "Outcome" in sections, f"template sections are {sections}"
    assert "Open threads" in sections, f"template sections are {sections}"


@then("it does not declare Summary or Outcomes as required body sections")
def _session_template_omits_old() -> None:
    sections = _template_sections("session-record")
    assert "Summary" not in sections, f"template still declares Summary: {sections}"
    assert "Outcomes" not in sections, f"template still declares Outcomes: {sections}"


@given(
    "a session-record document whose body carries Outcome but omits the Open threads "
    "section its type's required-section set now demands"
)
def _session_missing_open_threads(context: dict) -> None:
    context["artifact"] = Artifact(
        frontmatter={"type": "session-record"}, body=_body_with_sections(["Outcome"])
    )


@given(
    "a session-record document whose body carries Outcome and Open threads, its "
    "type's full required-section set"
)
def _session_full_body(context: dict) -> None:
    context["artifact"] = Artifact(
        frontmatter={"type": "session-record"},
        body=_body_with_sections(["Outcome", "Open threads"]),
    )
