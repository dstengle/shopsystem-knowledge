"""Step definitions for the single-source projection outer-loop scenario.

Binds @scenario_hash:d121b489919c177e — "L0/L1/L2 projections and the index
are generated from the single source document" — and asserts every Then/And
leg: the L0 card fields, the verbatim L1 extract, L2 == source, the machine and
human index entries derived from the same frontmatter, and the no-new-facts
invariant.

RED leg: ``generate_projections`` raises ``NotImplementedError`` at the When
step, so the scenario fails for the right reason (behaviour unimplemented),
not a collection/import error. The GREEN leg makes the assertions below pass.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from knowledge.projections import generate_projections

FIXTURE = Path(__file__).parent / "fixtures" / "adr_0007_single_source.md"

# The machine-truth facts that live in the fixture's YAML frontmatter. Every
# projection must draw only from these; none may introduce a fact absent from
# the source document.
FM_ID = "ADR-0007"
FM_TITLE = "Adopt single-source projection generation"
FM_STATUS = "accepted"
FM_DESCRIPTION = (
    "All projection tiers are generated deterministically from one source "
    "document."
)


@pytest.fixture
def context() -> dict:
    return {}


@scenario(
    "single_source_projection.feature",
    "L0/L1/L2 projections and the index are generated from the single source document",
)
def test_single_source_projection() -> None:
    """Outer-loop binding; step bodies below carry the assertions."""


@given(
    "a decision document whose only machine truth lives in its YAML frontmatter "
    "and whose body carries a recognized decision section"
)
def _source_document(context: dict) -> None:
    source = FIXTURE.read_text(encoding="utf-8")
    # Guard the fixture's own preconditions so a later fixture edit cannot
    # silently weaken the scenario.
    assert source.startswith("---\n"), "fixture must open with YAML frontmatter"
    assert "## Decision" in source, "fixture body must carry a recognized decision section"
    for fact in (FM_ID, FM_TITLE, FM_STATUS, FM_DESCRIPTION):
        assert fact in source, f"frontmatter fact {fact!r} must appear in the source"
    context["source"] = source


@when(
    "the knowledge context generates the architecture-decision projections "
    "from that single source"
)
def _generate(context: dict) -> None:
    context["projections"] = generate_projections(context["source"])


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
    # ...and stopped at the section boundary — it did not bleed the following
    # Consequences section into the extract.
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

    # The machine index entry is structured and derived from the frontmatter.
    assert machine["id"] == FM_ID
    assert machine["title"] == FM_TITLE
    assert machine["status"] == FM_STATUS

    # The human index entry is a rendered line that surfaces the same facts.
    assert isinstance(human, str)
    assert FM_ID in human
    assert FM_TITLE in human
    assert FM_STATUS in human


@then("no projection introduces any fact that is not present in the single source")
def _no_new_facts(context: dict) -> None:
    source = context["source"]
    projections = context["projections"]
    l0 = projections.l0

    # Every fact-bearing field of every structured projection is a verbatim
    # substring of the single source document.
    for value in (l0.id, l0.title, l0.status, l0.description):
        assert value in source, f"L0 fact {value!r} absent from source"

    assert projections.l1.text in source
    assert projections.l2 == source

    machine = projections.machine_index_entry
    for value in (machine["id"], machine["title"], machine["status"]):
        assert value in source, f"machine index fact {value!r} absent from source"

    # The human index entry may add formatting glue (punctuation/whitespace)
    # but must introduce no alphabetic fact beyond the frontmatter values it
    # renders. Strip the known frontmatter facts and assert no residual
    # letters remain.
    residual = projections.human_index_entry
    for value in (FM_ID, FM_TITLE, FM_STATUS, FM_DESCRIPTION):
        residual = residual.replace(value, " ")
    leftover_letters = [ch for ch in residual if ch.isalpha()]
    assert not leftover_letters, (
        "human index entry introduced non-frontmatter facts: "
        f"{''.join(leftover_letters)!r}"
    )
