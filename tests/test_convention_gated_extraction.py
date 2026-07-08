"""Step definitions for the convention-gated L1 extraction outer-loop scenario.

Binds @scenario_hash:dbd9846f04d8e22b — "L1 extraction is convention-gated and
a document lacking a recognized decision heading is reported non-conforming" —
and asserts both Then/And legs:

* the document is *reported* as non-conforming, naming the missing recognized
  decision heading as the reason, and
* generation does **not** emit a silently empty L1 extract for that document.

RED leg: today ``generate_projections`` silently returns a bundle whose
``l1.text`` is ``""`` for a document lacking a recognized decision heading, so
the "reports as non-conforming" leg fails for the right reason (the
convention-gating behaviour is absent). The GREEN leg makes both legs pass.

The step bodies deliberately reference the non-conforming error by
``type(...).__name__`` rather than importing it at module top: the same test
file is committed at RED (before the symbol exists) and must fail on behaviour,
not on a collection/import error.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from knowledge.projections import generate_projections

FIXTURE = Path(__file__).parent / "fixtures" / "adr_0011_no_decision_heading.md"

# The recognized decision-section headings the knowledge context gates on. The
# non-conforming fixture carries none of these in its body.
RECOGNIZED_HEADINGS = ("## Decision", "## Decision Outcome")


@pytest.fixture
def context() -> dict:
    return {}


@scenario(
    "single_source_projection.feature",
    "L1 extraction is convention-gated and a document lacking a recognized "
    "decision heading is reported non-conforming",
)
def test_convention_gated_extraction() -> None:
    """Outer-loop binding; step bodies below carry the assertions."""


@given("a decision document whose body carries none of the recognized decision headings")
def _non_conforming_document(context: dict) -> None:
    source = FIXTURE.read_text(encoding="utf-8")
    # Guard the fixture's own preconditions so a later fixture edit cannot
    # silently weaken the scenario: it must have frontmatter, and its body must
    # carry none of the recognized decision headings.
    assert source.startswith("---\n"), "fixture must open with YAML frontmatter"
    for heading in RECOGNIZED_HEADINGS:
        assert heading not in source, (
            f"fixture body must carry none of the recognized decision headings; "
            f"found {heading!r}"
        )
    context["source"] = source


@when("the knowledge context generates the architecture-decision projections")
def _generate(context: dict) -> None:
    # Capture either outcome without failing here, so the Then/And legs can
    # assert on the reported result.
    try:
        context["bundle"] = generate_projections(context["source"])
        context["error"] = None
    except Exception as exc:  # noqa: BLE001 - the scenario asserts on the report
        context["bundle"] = None
        context["error"] = exc


@then("it reports that document as non-conforming for lacking a recognized decision heading")
def _reports_non_conforming(context: dict) -> None:
    error = context["error"]
    # Non-conformance must be reported explicitly — not swallowed into a bundle.
    assert error is not None, (
        "generation must report the document as non-conforming, not return "
        "a projection bundle silently"
    )
    assert type(error).__name__ == "NonConformingDocumentError", (
        f"expected a NonConformingDocumentError report, got {type(error).__name__}"
    )
    # The report must name the missing recognized decision heading as the reason.
    assert "recognized decision heading" in str(error).lower(), (
        f"report must name the missing recognized decision heading; got {str(error)!r}"
    )


@then("it does not emit a silently empty L1 extract for that document")
def _no_silently_empty_l1(context: dict) -> None:
    bundle = context["bundle"]
    # If a bundle came back at all, it must not carry a silently empty L1
    # extract — but the convention-gated behaviour is to report non-conformance
    # instead of producing any bundle for this document.
    assert bundle is None, (
        "generation must not emit a projection bundle carrying a silently empty "
        "L1 extract for a non-conforming document"
    )
