"""Step definitions for the shop-knowledge CLI distribution feature.

Binds the pinned scenarios in ``shop_knowledge_cli.feature``. The CLI is
exercised **in-process**: each scenario drives ``knowledge.cli.main`` with an
explicit argv and captures the exit code plus the raw stdout/stderr bytes it
writes, so the byte-for-byte template/schema assertions compare against exactly
the bytes the underlying ``render_template`` / ``render_schema_fragment``
generators produce. A single ``When I run "shop-knowledge ..."`` step captures
the whole command string and splits it into argv, so ``template``, ``schema``,
``validate`` and the reject cases all route through one binding without step
ambiguity.
"""

from __future__ import annotations

import io
from pathlib import Path

import pytest
import yaml
from pytest_bdd import given, parsers, scenario, then, when

# The literal on-disk path the validate scenarios name.
ARTIFACT_PATH = "/tmp/example-artifact.md"


@pytest.fixture
def context() -> dict:
    return {}


# --- Document builder for the validate scenarios ----------------------------


def _write_document(atype, *, omit_fields=(), omit_sections=(), override=None) -> str:
    """Render and write a document of ``atype`` to the literal artifact path.

    The document is conforming by construction — every shared and type-additional
    required field present (with an id matching the type's pattern, a status in
    its enum, non-empty anchors), and every required section in the body — except
    for the fields in ``omit_fields``, the sections in ``omit_sections``, and any
    ``override`` frontmatter values. That lets each scenario introduce exactly the
    violation(s) it exercises and nothing else.
    """
    frontmatter: dict[str, object] = {
        "type": atype.name,
        "id": atype.id_example.replace("NNN", "001"),
        "title": "Example artifact",
        "status": atype.statuses[0],
        "created": "2026-01-01",
        "updated": "2026-01-02",
        "authors": ["someone"],
        "description": "An example artifact for validation.",
    }
    for name in atype.extra_required_fields:
        frontmatter[name] = ["anchor-001"]
    if override:
        frontmatter.update(override)
    for name in omit_fields:
        frontmatter.pop(name, None)

    fm_text = yaml.safe_dump(frontmatter, sort_keys=False)
    body_lines: list[str] = []
    for section in atype.required_sections:
        if section in omit_sections:
            continue
        body_lines += [f"## {section}", "", "Content.", ""]
    source = "---\n" + fm_text + "---\n\n" + "\n".join(body_lines) + "\n"
    Path(ARTIFACT_PATH).write_text(source, encoding="utf-8")
    return source


# --- Scenario bindings -------------------------------------------------------


@scenario(
    "shop_knowledge_cli.feature",
    '"shop-knowledge template" prints the canonical authoring template for a recognized artifact type',
)
def test_template_recognized() -> None: ...


@scenario(
    "shop_knowledge_cli.feature",
    '"shop-knowledge schema" prints the canonical JSON Schema fragment for a recognized artifact type',
)
def test_schema_recognized() -> None: ...


@scenario(
    "shop_knowledge_cli.feature",
    '"shop-knowledge template" and "shop-knowledge schema" both reject an unrecognized artifact type and name the offending value',
)
def test_reject_unrecognized() -> None: ...


@scenario(
    "shop_knowledge_cli.feature",
    '"shop-knowledge validate" reports a conforming document as conforming',
)
def test_validate_conforming() -> None: ...


@scenario(
    "shop_knowledge_cli.feature",
    '"shop-knowledge validate" on a document missing a required frontmatter field '
    "reports the same named diagnosis the internal frontmatter check produces",
)
def test_validate_missing_field() -> None: ...


@scenario(
    "shop_knowledge_cli.feature",
    '"shop-knowledge validate" on a document whose frontmatter omits or misdeclares '
    "the type field reports that specific diagnosis rather than skipping validation",
)
def test_validate_missing_type() -> None: ...


# --- Given -------------------------------------------------------------------


@given('the installed "shop-knowledge" distribution')
def _installed_distribution(context: dict) -> None:
    # The distribution provides its command-line entry point; importing it is
    # what "installed" means for the in-process driver.
    from knowledge.cli import main

    context["main"] = main


# --- Given: validate documents ----------------------------------------------
#
# The validate scenarios all build a candidate document (shared frontmatter set
# plus the Context / Open questions section pair) and introduce exactly the
# violation each scenario names.


def _base_type():
    from knowledge.artifact_types import artifact_type

    atype = artifact_type("candidate")
    assert atype is not None
    return atype


@given(
    parsers.re(
        r'a document on disk at "[^"]+" whose frontmatter declares a recognized "type" '
        r"and satisfies every frontmatter-required field, id pattern, and status enum for that type"
    )
)
def _doc_conforming_frontmatter(context: dict) -> None:
    atype = _base_type()
    context["atype"] = atype
    # Conforming frontmatter written first; the body-section given completes it.
    _write_document(atype, omit_sections=atype.required_sections)


@given(
    parsers.re(r"the document's body carries every section its type's required-section set demands")
)
def _doc_has_all_sections(context: dict) -> None:
    _write_document(context["atype"])


@given(parsers.re(r"a document on disk at \"[^\"]+\" whose frontmatter omits a field its recognized type requires"))
def _doc_missing_field(context: dict) -> None:
    atype = _base_type()
    context["atype"] = atype
    context["missing_field"] = "description"
    # A single shared required field is omitted; every section is present, so the
    # missing field is the document's only violation.
    context["source"] = _write_document(atype, omit_fields=["description"])


@given(
    parsers.re(
        r"a document on disk at \"[^\"]+\" whose frontmatter omits the \"type\" field, "
        r"or declares a \"type\" value outside the eight recognized artifact types"
    )
)
def _doc_missing_type(context: dict) -> None:
    atype = _base_type()
    context["atype"] = atype
    # Omit the type field entirely: the document has no determinable type.
    context["source"] = _write_document(atype, omit_fields=["type"])


# --- When --------------------------------------------------------------------


@when(parsers.re(r'I run "shop-knowledge (?P<cmd>[^"]+)"'))
def _run_shop_knowledge(context: dict, cmd: str) -> None:
    from knowledge.cli import main

    argv = cmd.split()
    out, err = io.BytesIO(), io.BytesIO()
    rc = main(argv, stdout=out, stderr=err)
    context["exit"] = rc
    context["stdout"] = out.getvalue()
    context["stderr"] = err.getvalue()


# --- Then: exit codes and stderr --------------------------------------------


@then("the exit code is 0")
def _exit_zero(context: dict) -> None:
    assert context["exit"] == 0, f"expected exit 0, got {context['exit']}"


@then("the exit code is non-zero")
def _exit_nonzero(context: dict) -> None:
    assert context["exit"] != 0, "expected a non-zero exit code"


@then("stderr is empty")
def _stderr_empty(context: dict) -> None:
    assert context["stderr"] == b"", f"expected empty stderr, got {context['stderr']!r}"


# --- Then: template byte-for-byte -------------------------------------------


@then(parsers.re(r'stdout is the "(?P<type_name>[^"]+)" typedef\'s generated template byte-for-byte'))
def _stdout_is_template(context: dict, type_name: str) -> None:
    from knowledge.artifact_types import artifact_type
    from knowledge.typedefs import render_template

    expected = render_template(artifact_type(type_name))
    assert context["stdout"] == expected, "stdout is not the generated template byte-for-byte"


@then(parsers.re(r'stdout is the "(?P<type_name>[^"]+)" typedef\'s generated schema fragment byte-for-byte'))
def _stdout_is_schema(context: dict, type_name: str) -> None:
    from knowledge.artifact_types import artifact_type
    from knowledge.typedefs import render_schema_fragment

    expected = render_schema_fragment(artifact_type(type_name))
    assert context["stdout"] == expected, "stdout is not the generated schema fragment byte-for-byte"


# --- Then: reject unrecognized type -----------------------------------------


@then(parsers.re(r'stderr names "(?P<offending>[^"]+)" as an unrecognized artifact type'))
def _stderr_names_offending(context: dict, offending: str) -> None:
    stderr = context["stderr"].decode("utf-8")
    assert offending in stderr, f"stderr does not name the offending value {offending!r}"


@then("stderr lists the eight recognized artifact types")
def _stderr_lists_eight_types(context: dict) -> None:
    from knowledge.artifact_types import RECOGNIZED_ARTIFACT_TYPES

    stderr = context["stderr"].decode("utf-8")
    assert len(RECOGNIZED_ARTIFACT_TYPES) == 8
    for type_name in RECOGNIZED_ARTIFACT_TYPES:
        assert type_name in stderr, f"stderr does not list recognized type {type_name!r}"


# --- Then: validate reporting -----------------------------------------------


def _stdout_text(context: dict) -> str:
    return context["stdout"].decode("utf-8")


@then("stdout reports the document as conforming")
def _reports_conforming(context: dict) -> None:
    text = _stdout_text(context)
    assert "non-conforming" not in text, f"expected a conforming report, got: {text!r}"
    assert "conforming" in text, f"stdout does not report the document conforming: {text!r}"


@then("stdout names no violation")
def _names_no_violation(context: dict) -> None:
    text = _stdout_text(context)
    assert "- " not in text, f"a conforming report should name no violation, got: {text!r}"


@then("stdout reports the document as non-conforming")
def _reports_non_conforming(context: dict) -> None:
    text = _stdout_text(context)
    assert "non-conforming" in text, f"stdout does not report the document non-conforming: {text!r}"


@then("stdout names the missing required field by its field name")
def _names_missing_field(context: dict) -> None:
    from knowledge.artifact_types import parse_artifact
    from knowledge.schema import validate_frontmatter

    field = context["missing_field"]
    text = _stdout_text(context)
    # The CLI names the field the internal frontmatter check reports missing.
    internal = validate_frontmatter(parse_artifact(context["source"]))
    assert field in internal.missing_fields, "the internal check did not report this field missing"
    assert field in text, f"stdout does not name the missing field {field!r}: {text!r}"


@then("stdout reports the document as non-conforming for a missing or unrecognized type")
def _reports_non_conforming_type(context: dict) -> None:
    text = _stdout_text(context)
    assert "non-conforming" in text, f"stdout does not report non-conforming: {text!r}"
    assert "type" in text, f"stdout does not name the type problem: {text!r}"


@then("stdout does not silently skip validation for lack of a determinable type")
def _does_not_skip_type(context: dict) -> None:
    from knowledge.artifact_types import parse_artifact
    from knowledge.schema import validate_frontmatter

    text = _stdout_text(context)
    # The internal frontmatter check produces a specific type diagnosis; the CLI
    # surfaces it rather than passing the document or emitting nothing.
    internal = validate_frontmatter(parse_artifact(context["source"]))
    assert not internal.conforming, "the internal check unexpectedly conformed"
    assert context["exit"] != 0, "validation was silently skipped (clean exit)"
    assert any(message in text for message in internal.messages), (
        f"stdout does not surface the internal type diagnosis: {text!r}"
    )
