"""Step definitions for the single-source projection-extension scenarios.

Binds two outer-loop scenarios of ``single_source_projections_full.feature``:

* @scenario_hash:a6b4bc6d9efd5377 — "L0/L1/L2 projections and the index are
  generated from the single source document" — asserting every projection tier,
  both index entries, and the no-new-facts invariant against the
  :class:`~knowledge.projections.ProjectionBundle` that
  ``generate_projections`` returns; and
* @scenario_hash:b04360552695af7c — "L1 extraction is convention-gated and a
  document lacking a recognized decision heading is reported non-conforming" —
  asserting that a document carrying none of the recognized decision headings is
  reported as non-conforming rather than projected into a silently empty L1
  extract.

Both scenarios bind the *already-generalized* ``generate_projections`` surface
(the "decision projections" phrasing), pinning the behaviour these hashes
require against the single-source generator and its convention gate.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from knowledge.projections import generate_projections

FEATURE = "single_source_projections_full.feature"
FIXTURES = Path(__file__).parent / "fixtures"
CONFORMING_FIXTURE = FIXTURES / "adr_0007_single_source.md"
NON_CONFORMING_FIXTURE = FIXTURES / "adr_0011_no_decision_heading.md"

# The machine-truth facts that live in the conforming fixture's YAML
# frontmatter. Every projection must draw only from these.
FM_ID = "ADR-0007"
FM_TITLE = "Adopt single-source projection generation"
FM_STATUS = "accepted"
FM_DESCRIPTION = (
    "All projection tiers are generated deterministically from one source "
    "document."
)

# The recognized decision-section headings the knowledge context gates on. The
# non-conforming fixture carries none of these in its body.
RECOGNIZED_HEADINGS = ("## Decision", "## Decision Outcome")


@pytest.fixture
def context() -> dict:
    return {}


# --- Scenario bindings -------------------------------------------------------


@scenario(
    FEATURE,
    "L0/L1/L2 projections and the index are generated from the single source document",
)
def test_projections_from_single_source() -> None:
    """Outer-loop binding; step bodies below carry the assertions."""


@scenario(
    FEATURE,
    "L1 extraction is convention-gated and a document lacking a recognized "
    "decision heading is reported non-conforming",
)
def test_convention_gated_non_conforming() -> None:
    """Outer-loop binding; step bodies below carry the assertions."""


# --- Given steps -------------------------------------------------------------


@given(
    "a decision document whose only machine truth lives in its YAML frontmatter "
    "and whose body carries a recognized decision section"
)
def _conforming_document(context: dict) -> None:
    source = CONFORMING_FIXTURE.read_text(encoding="utf-8")
    # Guard the fixture's own preconditions so a later edit cannot silently
    # weaken the scenario.
    assert source.startswith("---\n"), "fixture must open with YAML frontmatter"
    assert "## Decision" in source, "fixture body must carry a recognized decision section"
    for fact in (FM_ID, FM_TITLE, FM_STATUS, FM_DESCRIPTION):
        assert fact in source, f"frontmatter fact {fact!r} must appear in the source"
    context["source"] = source


@given("a decision document whose body carries none of the recognized decision headings")
def _non_conforming_document(context: dict) -> None:
    source = NON_CONFORMING_FIXTURE.read_text(encoding="utf-8")
    assert source.startswith("---\n"), "fixture must open with YAML frontmatter"
    for heading in RECOGNIZED_HEADINGS:
        assert heading not in source, (
            f"fixture body must carry none of the recognized decision headings; "
            f"found {heading!r}"
        )
    context["source"] = source


# --- When steps --------------------------------------------------------------


@when("the knowledge context generates the decision projections from that single source")
def _generate_from_single_source(context: dict) -> None:
    context["projections"] = generate_projections(context["source"])


@when("the knowledge context generates the decision projections")
def _generate_capturing_error(context: dict) -> None:
    # Capture either outcome so the Then/And legs assert on the reported result.
    try:
        context["bundle"] = generate_projections(context["source"])
        context["error"] = None
    except Exception as exc:  # noqa: BLE001 - the scenario asserts on the report
        context["bundle"] = None
        context["error"] = exc


# --- Then steps: full projection set -----------------------------------------


@then(
    "it emits an L0 card carrying the id, title, status and description drawn "
    "from the frontmatter"
)
def _l0_card(context: dict) -> None:
    l0 = context["projections"].l0
    assert l0.id == FM_ID
    assert l0.title == FM_TITLE
    assert l0.status == FM_STATUS
    assert l0.description == FM_DESCRIPTION


@then(
    "it emits an L1 extract carrying the verbatim text of the recognized "
    "decision section"
)
def _l1_extract(context: dict) -> None:
    source = context["source"]
    l1 = context["projections"].l1
    # Verbatim: the extract text appears exactly in the source document.
    assert l1.text in source
    # It captured the decision section's body...
    assert "Generate the L0 card" in l1.text
    # ...and stopped at the section boundary.
    assert "## Consequences" not in l1.text


@then("it emits an L2 projection that is the source document itself")
def _l2_projection(context: dict) -> None:
    assert context["projections"].l2 == context["source"]


@then(
    "it emits a machine index entry and a human index entry for that document, "
    "both derived from the same frontmatter"
)
def _index_entries(context: dict) -> None:
    projections = context["projections"]
    machine = projections.machine_index_entry
    human = projections.human_index_entry

    assert machine["id"] == FM_ID
    assert machine["title"] == FM_TITLE
    assert machine["status"] == FM_STATUS

    assert isinstance(human, str)
    assert FM_ID in human
    assert FM_TITLE in human
    assert FM_STATUS in human


@then("no projection introduces any fact that is not present in the single source")
def _no_new_facts(context: dict) -> None:
    source = context["source"]
    projections = context["projections"]
    l0 = projections.l0

    for value in (l0.id, l0.title, l0.status, l0.description):
        assert value in source, f"L0 fact {value!r} absent from source"

    assert projections.l1.text in source
    assert projections.l2 == source

    machine = projections.machine_index_entry
    for value in (machine["id"], machine["title"], machine["status"]):
        assert value in source, f"machine index fact {value!r} absent from source"

    residual = projections.human_index_entry
    for value in (FM_ID, FM_TITLE, FM_STATUS, FM_DESCRIPTION):
        residual = residual.replace(value, " ")
    leftover_letters = [ch for ch in residual if ch.isalpha()]
    assert not leftover_letters, (
        "human index entry introduced non-frontmatter facts: "
        f"{''.join(leftover_letters)!r}"
    )


# --- Then steps: convention gate ---------------------------------------------


@then("it reports that document as non-conforming for lacking a recognized decision heading")
def _reports_non_conforming(context: dict) -> None:
    error = context["error"]
    assert error is not None, (
        "generation must report the document as non-conforming, not return a "
        "projection bundle silently"
    )
    assert type(error).__name__ == "NonConformingDocumentError", (
        f"expected a NonConformingDocumentError report, got {type(error).__name__}"
    )
    assert "recognized decision heading" in str(error).lower(), (
        f"report must name the missing recognized decision heading; got {str(error)!r}"
    )


@then("it does not emit a silently empty L1 extract for that document")
def _no_silently_empty_l1(context: dict) -> None:
    bundle = context["bundle"]
    assert bundle is None, (
        "generation must not emit a projection bundle carrying a silently empty "
        "L1 extract for a non-conforming document"
    )
