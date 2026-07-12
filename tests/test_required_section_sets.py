"""Step definitions for the required-section-sets feature (3 scenarios).

Binds every scenario in ``required_section_sets.feature`` and asserts each
Then/And leg against the :class:`SectionCheckResult` returned by
``knowledge.schema.check_required_sections``.

RED leg: ``check_required_sections`` does not yet exist, so it is imported inside
the shared ``When`` step body — each scenario fails there on the absent
behaviour, not at collection time. The GREEN leg adds it and makes all three
pass.

Document bodies are built in-process from a type's declared required-section set
so a Given states exactly which section is present or omitted, and the resolve
-per-type scenario is genuinely a different set for a different type.
"""

from __future__ import annotations

import pytest
from pytest_bdd import scenario, given, then, when

from knowledge.artifact_types import Artifact, artifact_type

FEATURE = "required_section_sets.feature"


def _body_with_sections(section_names) -> str:
    """Render a Markdown body carrying each named section as a ``## `` heading."""
    return "\n".join(f"## {name}\nbody text for {name}\n" for name in section_names)


@pytest.fixture
def context() -> dict:
    return {}


@scenario(
    FEATURE,
    "a document missing a required body section is reported non-conforming and names the section",
)
def test_missing_section() -> None: ...


@scenario(FEATURE, "a document carrying its type's full required-section set passes")
def test_full_section_set_passes() -> None: ...


@scenario(FEATURE, "the required-section set is resolved per type")
def test_section_set_resolved_per_type() -> None: ...


@given(
    "a pdr document whose body omits the Options considered section its type's "
    "required-section set demands"
)
def _pdr_missing_options(context: dict) -> None:
    pdr = artifact_type("pdr")
    assert "Options considered" in pdr.required_sections
    present = [s for s in pdr.required_sections if s != "Options considered"]
    # Guard: every other required section IS present, so the only omission is
    # the one the scenario is about.
    assert present and "Options considered" not in present
    context["artifact"] = Artifact(frontmatter={"type": "pdr"}, body=_body_with_sections(present))


@given("a pdr document whose body carries every section in its type's required-section set")
def _pdr_full_set(context: dict) -> None:
    pdr = artifact_type("pdr")
    context["artifact"] = Artifact(
        frontmatter={"type": "pdr"}, body=_body_with_sections(pdr.required_sections)
    )


@given(
    "an intent-record document whose body omits a section that the pdr "
    "required-section set demands but that the intent-record required-section "
    "set does not"
)
def _intent_omits_pdr_section(context: dict) -> None:
    pdr = artifact_type("pdr")
    intent = artifact_type("intent-record")
    # "Options considered" is demanded by pdr but not by intent-record.
    assert "Options considered" in pdr.required_sections
    assert "Options considered" not in intent.required_sections
    # The intent-record body carries its own full set but not the pdr-only one.
    body = _body_with_sections(intent.required_sections)
    assert "Options considered" not in body
    context["artifact"] = Artifact(frontmatter={"type": "intent-record"}, body=body)


@when("the knowledge context checks the document's body against its type's required-section set")
def _check_sections(context: dict) -> None:
    from knowledge.schema import check_required_sections

    context["result"] = check_required_sections(context["artifact"])


@then("it reports the document as non-conforming for a missing required section")
def _non_conforming_body(context: dict) -> None:
    result = context["result"]
    assert result.conforming is False
    assert result.exit_code != 0


@then("the diagnosis names Options considered as the missing section")
def _names_missing_section(context: dict) -> None:
    result = context["result"]
    assert "Options considered" in result.missing_sections
    assert any("Options considered" in m for m in result.messages)


@then("it reports the document as conforming on body structure")
def _conforming_body(context: dict) -> None:
    result = context["result"]
    assert result.conforming is True, f"expected conforming; missing: {result.missing_sections}"
    assert result.exit_code == 0


@then("it names no missing required section")
def _no_missing_section(context: dict) -> None:
    assert context["result"].missing_sections == ()


@then("it reports the intent-record as conforming on body structure")
def _intent_conforming(context: dict) -> None:
    assert context["result"].conforming is True


@then("it does not impose the pdr section set on the intent-record")
def _no_pdr_imposition(context: dict) -> None:
    # The pdr-only "Options considered" section is not reported missing on an
    # intent-record: the required-section set is resolved per type.
    assert "Options considered" not in context["result"].missing_sections
