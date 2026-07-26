"""Step definitions for the per-type-body-sections feature (2 Scenario Outlines).

Binds both Scenario Outlines in ``per_type_body_sections.feature`` and asserts
each Then/And leg against the :class:`SectionCheckResult` returned by
``knowledge.schema.check_required_sections``. The Outlines are parameterized over
their Examples so every kind/section row is a distinct check:

* the missing-section Outline builds a body carrying every required section of
  the kind *except* the one the row names, and asserts the check reports the kind
  non-conforming and names that section as missing; and
* the full-set Outline builds a body carrying exactly the ``<sections>`` the row
  names and asserts the check reports the kind conforming on body structure with
  no missing section.

The required-section set for each kind is read from the single registry in
:mod:`knowledge.artifact_types`, so this test never re-spells a kind's sections
— it resolves them and drives the check the same way the required-section-sets
test does.
"""

from __future__ import annotations

import pytest
from pytest_bdd import scenario, given, then, when, parsers

from knowledge.artifact_types import Artifact, artifact_type

FEATURE = "per_type_body_sections.feature"


def _body_with_sections(section_names) -> str:
    """Render a Markdown body carrying each named section as a ``## `` heading."""
    return "\n".join(f"## {name}\nbody text for {name}\n" for name in section_names)


def _parse_section_list(prose: str) -> list[str]:
    """Parse a prose section list ("Context, Decision and Consequences") to names.

    The Examples spell the section set the way prose does — commas between all but
    the last pair, and an "and" before the final section. Normalizing the final
    " and " to a comma-separator lets a single split recover the exact section
    names, so the Given carries precisely the sections the row names.
    """
    normalized = prose.replace(" and ", ", ")
    return [part.strip() for part in normalized.split(",") if part.strip()]


@pytest.fixture
def context() -> dict:
    return {}


@scenario(
    FEATURE,
    "a document of its kind missing a required body section is reported "
    "non-conforming and names the section",
)
def test_missing_section_per_kind() -> None: ...


@scenario(
    FEATURE, "a document carrying its kind's full net-new required-section set passes"
)
def test_full_section_set_per_kind() -> None: ...


@given(
    parsers.parse(
        "a {kind} document whose body omits the {section} section its type's "
        "required-section set demands"
    )
)
def _kind_omits_section(context: dict, kind: str, section: str) -> None:
    atype = artifact_type(kind)
    assert atype is not None, f"unrecognized kind {kind!r}"
    assert section in atype.required_sections, (
        f"{section!r} is not in the {kind} required-section set "
        f"{atype.required_sections!r}"
    )
    present = [s for s in atype.required_sections if s != section]
    # Guard: the only omission is the section the row is about; every other
    # required section of the kind IS present.
    assert section not in present
    context["missing"] = section
    context["artifact"] = Artifact(
        frontmatter={"type": kind}, body=_body_with_sections(present)
    )


@given(parsers.parse("a {kind} document whose body carries {sections}"))
def _kind_carries_sections(context: dict, kind: str, sections: str) -> None:
    atype = artifact_type(kind)
    assert atype is not None, f"unrecognized kind {kind!r}"
    carried = _parse_section_list(sections)
    # Guard: the prose set the row names IS exactly the kind's full
    # required-section set — the Outline is the full-net-new-set case.
    assert tuple(carried) == atype.required_sections, (
        f"{kind} carries {carried!r} but its required-section set is "
        f"{atype.required_sections!r}"
    )
    context["artifact"] = Artifact(
        frontmatter={"type": kind}, body=_body_with_sections(carried)
    )


@when(
    "the knowledge context checks the document's body against its type's "
    "required-section set"
)
def _check_sections(context: dict) -> None:
    from knowledge.schema import check_required_sections

    context["result"] = check_required_sections(context["artifact"])


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


@then("it reports the document as conforming on body structure")
def _conforming_body(context: dict) -> None:
    result = context["result"]
    assert result.conforming is True, (
        f"expected conforming; missing: {result.missing_sections}"
    )
    assert result.exit_code == 0


@then("it names no missing required section")
def _no_missing_section(context: dict) -> None:
    assert context["result"].missing_sections == ()
