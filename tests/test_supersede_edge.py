"""Step definitions for the supersede-edge outer-loop scenario.

Binds @scenario_hash:4f85b0b3af16073e — "a draft that replaces a prior decision
is flagged supersedes and names the supersede edge to write" — the supersedes
case of the adversarial pass carried one step further to NAME the typed edge the
draft owes.

A decision is being authored that REPLACES a prior accepted decision on a
question; the authoring-time flow surfaces the prior decision as a neighbour and
the adversarial pass flags the draft SUPERSEDES, citing the prior decision BY
ID. On top of that verdict the pass names the typed supersede EDGE the draft
owes: a "supersedes" edge from the draft to the prior decision, identified by
the prior decision's id.

The fixture is a single ACCEPTED decision (ADR-3201, a read-through cache) and a
draft that explicitly REPLACES it (a replacement marker referencing the shared
subject). By the existing classification ladder (a replacement marker fires the
SUPERSEDES branch first) this lands SUPERSEDES with NO change to the classifier
— the new behaviour is only the typed-edge naming derived on top of it.

The prior decision is surfaced by the real discovery pass and the supersedes
verdict is produced by the real adversarial pass, composed through the
authoring-time review entry point.

RED leg: the typed supersede-edge naming (``SupersedeEdge`` +
``AdversarialResult.supersede_edges``) does not yet exist, so it is imported
inside the ``Then`` step that asserts the edge — the scenario fails there on the
absent behaviour (ImportError), not at collection/import time.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from knowledge.discovery import DraftDecision

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "supersede_corpus"

PRIOR_ID = "ADR-3201"  # the accepted decision the draft replaces
DRAFT_ID = "DRAFT-write-through-cache"  # the draft doing the replacing


@pytest.fixture
def context() -> dict:
    return {}


@scenario(
    "supersede_edge.feature",
    "a draft that replaces a prior decision is flagged supersedes and names "
    "the supersede edge to write",
)
def test_supersede_edge() -> None:
    """Outer-loop binding; step bodies below carry the assertions."""


@given("an existing accepted decision on a question")
def _existing_accepted_decision(context: dict) -> None:
    # The raw source corpus: a single ACCEPTED decision that decides the cache
    # question. It becomes the prior decision the draft replaces.
    context["sources"] = {
        path.stem: path.read_text(encoding="utf-8")
        for path in sorted(FIXTURE_DIR.glob("*.md"))
    }


@given("a draft decision being authored that replaces that prior decision")
def _draft_replaces_prior(context: dict) -> None:
    # The draft explicitly REPLACES the accepted read-through cache decision — a
    # replacement marker over the shared subject, which the ladder resolves to
    # SUPERSEDES (the replacement branch fires first).
    context["draft"] = DraftDecision(
        id=DRAFT_ID,
        title="Write-through cache for the projection index",
        description="A draft that replaces the prior read-through cache decision.",
        body=(
            "## Decision\n\n"
            "This decision replaces the read-through cache for the projection "
            "index with a write-through cache answered from memory on a "
            "repeated lookup.\n"
        ),
    )


@when(
    "the knowledge context runs the authoring-time discovery pass over the draft"
)
def _run_authoring_time_review(context: dict) -> None:
    from knowledge.adversarial import VerdictKind, authoring_time_review

    context["VerdictKind"] = VerdictKind
    context["result"] = authoring_time_review(context["sources"], context["draft"])


@then("it flags the draft as superseding the prior decision")
def _flagged_supersedes(context: dict) -> None:
    result = context["result"]
    VerdictKind = context["VerdictKind"]

    # The prior decision was surfaced and it carries a verdict.
    assert PRIOR_ID in result.cited_ids(), (
        f"the prior decision {PRIOR_ID} must be surfaced and cited, got "
        f"{result.cited_ids()}"
    )

    verdict = result.for_id(PRIOR_ID)
    assert verdict.verdict == VerdictKind.SUPERSEDES, (
        f"the draft replaces {PRIOR_ID}'s decision, so it must be flagged "
        f"SUPERSEDES, got {verdict.verdict!r} ({verdict.rationale})"
    )


@then(
    "it names the typed supersede edge the draft owes to the prior decision by id"
)
def _names_typed_supersede_edge(context: dict) -> None:
    # Imported HERE (not at module top): the RED commit fails at this step on the
    # absent typed supersede-edge naming, not at collection time.
    from knowledge.adversarial import SupersedeEdge

    result = context["result"]
    draft = context["draft"]

    # The pass names exactly the supersede edges owed — one per SUPERSEDES
    # verdict — and each is a typed SupersedeEdge instance.
    edges = result.supersede_edges()
    assert edges, "the pass must name the supersede edge the draft owes"
    assert all(isinstance(edge, SupersedeEdge) for edge in edges), (
        f"every named edge must be a typed SupersedeEdge, got {edges!r}"
    )

    # The edge the draft owes to the prior decision, keyed BY the prior id.
    owed = next((edge for edge in edges if edge.to == PRIOR_ID), None)
    assert owed is not None, (
        f"the pass must name the supersede edge owed to {PRIOR_ID} by id, got "
        f"targets {[edge.to for edge in edges]}"
    )

    # It is TYPED "supersedes"...
    assert owed.edge_type == "supersedes", (
        f"the owed edge must be typed 'supersedes', got {owed.edge_type!r}"
    )
    # ...runs FROM the draft being authored...
    assert owed.from_ == DRAFT_ID, (
        f"the owed edge must run from the draft {DRAFT_ID}, got {owed.from_!r}"
    )
    # ...and targets the prior decision BY ID.
    assert owed.to == PRIOR_ID, (
        f"the owed edge must target the prior decision {PRIOR_ID} by id, got "
        f"{owed.to!r}"
    )
