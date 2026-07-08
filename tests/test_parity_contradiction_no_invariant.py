"""Step definitions for the parity-contradiction keystone outer-loop scenario.

Binds @scenario_hash:f77904953e96124e — "a parity claim contradicted by a
neighbour's governed change is caught with no pre-encoded invariant" — the
tier-3-OPT-IN keystone of the adversarial pass.

A decision is being authored that claims PARITY (an unchanged interface) over a
governed surface whose EXISTING decision text is itself a governed CHANGE. The
corpus registers NO invariants and NO baselines — there is no invariant/baseline
registry in play at all. The PRIMARY mechanism (the adversarial authoring pass
reasoning over the neighbour's live L1 decision text) catches the contradiction
and cites the neighbour BY ID, with the tier-3 formal-invariant check strictly
OPT-IN, never required.

The fixture is a single ACCEPTED decision (ADR-4001) whose L1 decision text
CHANGES the default pagination page size — it carries a governed-change marker —
and a draft that claims that same surface stays unchanged (a parity claim that
is therefore denied). By the existing classification ladder (a parity claim over
a neighbour whose decision text is a governed change) this lands CONTRADICTS with
no change to the classifier.

"No pre-encoded invariant or baseline required" is made OBSERVABLE three ways:

  1. The verdict's cited evidence is the neighbour's own decision text — the
     matched governed-change marker is drawn from, and verbatim-present in, the
     neighbour's L1 extract (not a stored baseline).
  2. ``run_adversarial_pass`` structurally consumes only ``(draft, neighbours)``
     and ``authoring_time_review`` only ``(sources, draft)`` — neither takes an
     invariants/baselines/registry parameter, so no such registry can be fed in.
  3. The ``knowledge.adversarial`` module exposes no invariant/baseline registry
     symbol at all — there is nothing to register against.

The contradicted neighbour is surfaced by the real discovery pass and the
contradicts verdict is produced by the real adversarial pass, composed through
the authoring-time review entry point.

RED leg: the keystone binding fails on the CONTRADICTS assertion until the GREEN
fixture/wiring is in place; the imports resolve against the existing module.
"""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from knowledge.discovery import DraftDecision

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "parity_contradiction_corpus"

# The single accepted decision whose decision text is a governed change; the
# draft's parity claim over this same surface is what the pass must contradict.
CHANGED_ID = "ADR-4001"


@pytest.fixture
def context() -> dict:
    return {}


@scenario(
    "parity_contradiction_no_invariant.feature",
    "a parity claim contradicted by a neighbour's governed change is caught "
    "with no pre-encoded invariant",
)
def test_parity_contradiction_no_invariant() -> None:
    """Outer-loop binding; step bodies below carry the assertions."""


@given("an existing decision whose decision text changes a governed interface")
def _existing_governed_change(context: dict) -> None:
    # The raw source corpus: a single ACCEPTED decision whose L1 decision text
    # CHANGES the default pagination page size — a governed change on that
    # surface. It becomes the neighbour the draft's parity claim is measured
    # against.
    context["sources"] = {
        path.stem: path.read_text(encoding="utf-8")
        for path in sorted(FIXTURE_DIR.glob("*.md"))
    }


@given(
    "a draft decision being authored that claims parity or an unchanged "
    "interface over that same surface"
)
def _draft_claims_parity(context: dict) -> None:
    # The draft claims the same pagination page-size surface stays UNCHANGED — a
    # parity claim over a neighbour whose decision text changed it, which the
    # ladder resolves to CONTRADICTS.
    context["draft"] = DraftDecision(
        id="DRAFT-pagination-parity",
        title="Pagination page size for the projection service",
        description="A draft that keeps the pagination page size unchanged.",
        body=(
            "## Decision\n\n"
            "The pagination page size stays unchanged at the current default "
            "for every response.\n"
        ),
    )


@given("the corpus carries no registered invariants and no registered baselines")
def _no_invariants_no_baselines(context: dict) -> None:
    # OBSERVABLE (part 1 of the no-registry proof): the corpus is a plain set of
    # decision sources — there is no invariant/baseline registry in play at all.
    # The adversarial-pass entry points structurally cannot be handed one, and
    # the module exposes no registry to register against. Asserted here so the
    # precondition ("no registered invariants and no registered baselines") is
    # a checked fact, not an unstated assumption.
    from knowledge import adversarial
    from knowledge.adversarial import authoring_time_review, run_adversarial_pass

    # (a) The adversarial pass consumes ONLY (draft, neighbours) — no invariants
    # or baselines parameter can be supplied to it.
    pass_params = list(inspect.signature(run_adversarial_pass).parameters)
    assert pass_params == ["draft", "neighbours"], (
        "run_adversarial_pass must consume exactly (draft, neighbours); an "
        "invariant/baseline/registry parameter would let a pre-encoded baseline "
        f"drive the verdict, got {pass_params}"
    )

    # (b) The authoring-time entry point consumes ONLY (sources, draft) — again,
    # no invariant/baseline registry parameter.
    review_params = list(inspect.signature(authoring_time_review).parameters)
    assert review_params == ["sources", "draft"], (
        "authoring_time_review must consume exactly (sources, draft); an "
        "invariant/baseline/registry parameter would introduce a pre-encoded "
        f"baseline mechanism, got {review_params}"
    )

    # (c) The module exposes NO invariant/baseline registry symbol at all — there
    # is nothing to register against, so the verdict cannot come from one.
    registry_names = [
        name
        for name in dir(adversarial)
        if ("invariant" in name.lower() or "baseline" in name.lower())
    ]
    assert registry_names == [], (
        "the adversarial module must expose no invariant/baseline registry "
        f"symbol; the pass reasons from decision text alone, got {registry_names}"
    )


@when(
    "the knowledge context runs the adversarial pass over the draft against "
    "that neighbour"
)
def _run_adversarial_pass(context: dict) -> None:
    from knowledge.adversarial import VerdictKind, authoring_time_review

    context["VerdictKind"] = VerdictKind
    context["result"] = authoring_time_review(context["sources"], context["draft"])


@then(
    "it flags the draft as contradicting the neighbour on the basis of the "
    "neighbour's decision text"
)
def _flagged_contradicts_from_decision_text(context: dict) -> None:
    result = context["result"]
    VerdictKind = context["VerdictKind"]

    # The changed decision was surfaced and carries a verdict.
    assert CHANGED_ID in result.cited_ids(), (
        f"the changed decision {CHANGED_ID} must be surfaced and cited, got "
        f"{result.cited_ids()}"
    )

    verdict = result.for_id(CHANGED_ID)
    assert verdict.verdict == VerdictKind.CONTRADICTS, (
        f"the draft claims parity over {CHANGED_ID}'s governed change, so it must "
        f"be flagged CONTRADICTS, got {verdict.verdict!r} ({verdict.rationale})"
    )

    # ON THE BASIS OF the neighbour's decision text: the evidence the verdict was
    # reasoned from is the neighbour's own L1 decision text — the matched
    # governed-change marker is drawn from, and verbatim-present in, that extract.
    # This is the no-baseline proof at the verdict level: the contradiction is
    # established from the neighbour's live decision text, not a stored baseline.
    assert verdict.l1_extract, (
        "the contradicts verdict must carry the neighbour's verbatim L1 decision "
        "text as the cited evidence it reasoned over"
    )
    change_markers = [
        marker for marker in verdict.matched_markers if marker in verdict.l1_extract.lower()
    ]
    assert change_markers, (
        "the contradiction must be established from a governed-change marker "
        "present in the neighbour's OWN decision text (not a stored baseline); "
        f"matched_markers={verdict.matched_markers!r} l1_extract="
        f"{verdict.l1_extract!r}"
    )


@then("it cites the contradicted neighbour by id")
def _cites_contradicted_by_id(context: dict) -> None:
    result = context["result"]
    verdict = result.for_id(CHANGED_ID)

    assert verdict.neighbour_id == CHANGED_ID, (
        f"the contradicts verdict must cite {CHANGED_ID} by id, got "
        f"{verdict.neighbour_id!r}"
    )
    assert verdict.subject, (
        "the contradicts verdict must carry the shared subject tokens that "
        "explain which governed surface the contradiction is about"
    )


@then(
    "it produces this verdict without requiring any pre-encoded invariant or "
    "baseline to be registered"
)
def _no_pre_encoded_invariant_required(context: dict) -> None:
    # OBSERVABLE (part 2 of the no-registry proof): the verdict was produced by a
    # composition — authoring_time_review -> run_adversarial_pass — that took ONLY
    # the plain source corpus and the draft. No invariant or baseline was, or
    # could be, registered: the entry points expose no such parameter, and the
    # module exposes no registry symbol. Re-assert the structural facts at the
    # point the verdict is claimed so the "not required" property travels with the
    # verdict itself, not just the precondition step.
    from knowledge import adversarial
    from knowledge.adversarial import authoring_time_review, run_adversarial_pass

    assert list(inspect.signature(run_adversarial_pass).parameters) == [
        "draft",
        "neighbours",
    ]
    assert list(inspect.signature(authoring_time_review).parameters) == [
        "sources",
        "draft",
    ]
    assert not [
        name
        for name in dir(adversarial)
        if ("invariant" in name.lower() or "baseline" in name.lower())
    ], "the verdict must be reachable with no invariant/baseline registry present"

    # And the verdict is a real CONTRADICTS reached through that registry-free
    # composition — the tier-3 formal-invariant check was strictly OPT-IN here.
    verdict = context["result"].for_id(CHANGED_ID)
    assert verdict.verdict == context["VerdictKind"].CONTRADICTS
