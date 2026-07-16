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

import pytest
from pytest_bdd import given, parsers, scenario, then, when

# The literal on-disk path the validate scenarios name.
ARTIFACT_PATH = "/tmp/example-artifact.md"


@pytest.fixture
def context() -> dict:
    return {}


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


# --- Given -------------------------------------------------------------------


@given('the installed "shop-knowledge" distribution')
def _installed_distribution(context: dict) -> None:
    # The distribution provides its command-line entry point; importing it is
    # what "installed" means for the in-process driver.
    from knowledge.cli import main

    context["main"] = main


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
