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
