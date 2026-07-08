"""Step definitions for the adversarial-pass outer-loop scenario.

Binds @scenario_hash:bea7c4aa89633418 — "the discovery pass answers covered,
contradicts and supersedes for each surfaced neighbour with a citation" — the
SECOND behaviour of the authoring_discovery family. It introduces the
**adversarial pass**: over a draft and the set of neighbours surfaced by
``run_authoring_discovery``, it assigns EXACTLY ONE verdict per surfaced
neighbour — covered / contradicts / supersedes — each CITING the neighbour it is
about BY ID.

The scenario pins the shape of the pass, not one specific verdict (the three
downstream case scenarios force covered / contradicts / supersedes each on their
own). So the fixture is built to exercise all three verdict kinds at once:

* a **retry-policy** neighbour whose decision the draft restates unchanged
  (a parity claim that holds) -> covered;
* a **pagination** neighbour whose decision text is itself a governed change,
  against which the draft claims parity -> contradicts;
* a **read-through cache** neighbour the draft explicitly replaces -> supersedes.

The neighbours are produced by the real discovery pass (``build_l0l1_index`` +
``run_authoring_discovery``) so the adversarial pass is exercised against genuine
surfaced neighbours carrying id + L0 card + verbatim L1 extract (no L2).

RED leg: ``knowledge.adversarial`` does not yet exist, so it is imported inside
the ``When`` step body — the scenario fails there on the absent behaviour
(ImportError), not at collection/import time.
"""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from knowledge.discovery import (
    DraftDecision,
    build_l0l1_index,
    run_authoring_discovery,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "adversarial_corpus"

# Every decision in the corpus overlaps the draft's topic, so the discovery pass
# surfaces all three as neighbours — one per intended verdict kind.
COVERED_ID = "ADR-3001"  # retry policy the draft restates unchanged
CONTRADICTS_ID = "ADR-3002"  # pagination change the draft's parity claim denies
SUPERSEDES_ID = "ADR-3003"  # read-through cache the draft replaces
SURFACED_IDS = (COVERED_ID, CONTRADICTS_ID, SUPERSEDES_ID)


@pytest.fixture
def context() -> dict:
    return {}


@scenario(
    "adversarial_pass_verdicts.feature",
    "the discovery pass answers covered, contradicts and supersedes for each "
    "surfaced neighbour with a citation",
)
def test_adversarial_pass_verdicts() -> None:
    """Outer-loop binding; step bodies below carry the assertions."""


@given(
    "a draft decision being authored and a set of surfaced neighbours from the "
    "L0/L1 index"
)
def _draft_and_surfaced_neighbours(context: dict) -> None:
    # The raw source corpus. build_l0l1_index projects it down to L0/L1 material
    # (dropping the L2 bodies), and run_authoring_discovery surfaces the relevant
    # neighbours — exactly the input the adversarial pass reasons over.
    sources = {
        path.stem: path.read_text(encoding="utf-8")
        for path in sorted(FIXTURE_DIR.glob("*.md"))
    }

    # A single draft that takes a distinct stance toward each neighbour's subject:
    #   * retry: restates the accepted decision unchanged (parity holds) -> covered
    #   * pagination: claims the page size is unchanged, but the neighbour's
    #     decision text CHANGED it -> contradicts
    #   * cache: explicitly replaces the read-through cache -> supersedes
    draft = DraftDecision(
        id="DRAFT-projection-service-authoring",
        title="Projection service authoring draft",
        description="A draft revisiting the retry, pagination and cache decisions.",
        body=(
            "## Decision\n\n"
            "The retry policy keeps retrying a failed request three times with "
            "exponential backoff, unchanged from the accepted decision.\n"
            "Pagination page size stays unchanged at the default for every "
            "response.\n"
            "This decision replaces the read-through cache for the projection "
            "index with a write-through cache answered from memory.\n"
        ),
    )

    index = build_l0l1_index(sources)
    discovery = run_authoring_discovery(index, draft)

    # Precondition guard: all three decisions must be surfaced so the fixture can
    # exercise all three verdict kinds; a later fixture edit cannot quietly
    # weaken the scenario to a single verdict.
    assert set(discovery.ids()) == set(SURFACED_IDS), (
        f"discovery must surface all three neighbours {SURFACED_IDS}, got "
        f"{discovery.ids()}"
    )

    context["draft"] = draft
    context["neighbours"] = discovery.neighbours


@when(
    "the knowledge context runs the adversarial pass over the draft against "
    "those neighbours"
)
def _run_adversarial_pass(context: dict) -> None:
    # Imported HERE (not at module top): the RED commit fails at this step on the
    # absent knowledge.adversarial module, not at collection time.
    from knowledge.adversarial import VerdictKind, run_adversarial_pass

    context["VerdictKind"] = VerdictKind
    context["run_signature"] = inspect.signature(run_adversarial_pass)
    context["result"] = run_adversarial_pass(
        context["draft"], context["neighbours"]
    )


@then(
    "for each surfaced neighbour it returns a verdict on whether the draft is "
    "covered by, contradicts, or supersedes that neighbour"
)
def _one_verdict_per_neighbour(context: dict) -> None:
    result = context["result"]
    VerdictKind = context["VerdictKind"]
    neighbours = context["neighbours"]

    verdict_kinds = {VerdictKind.COVERED, VerdictKind.CONTRADICTS, VerdictKind.SUPERSEDES}

    # (a) The pass reasons over (draft, neighbours) — it takes no corpus/sources
    # parameter, so it cannot re-load the whole corpus into the adversarial step.
    params = list(context["run_signature"].parameters)
    assert params[:2] == ["draft", "neighbours"], (
        "the adversarial pass must consume (draft, neighbours); a corpus/sources "
        f"parameter would let it re-load the whole corpus, got {params}"
    )

    # (b) EXACTLY ONE verdict per surfaced neighbour — same cardinality, one apiece.
    assert len(result.verdicts) == len(neighbours), (
        f"expected one verdict per surfaced neighbour ({len(neighbours)}), got "
        f"{len(result.verdicts)}"
    )

    # (c) Every verdict is one of covered / contradicts / supersedes.
    for verdict in result.verdicts:
        assert verdict.verdict in verdict_kinds, (
            f"verdict for {verdict.neighbour_id} must be covered/contradicts/"
            f"supersedes, got {verdict.verdict!r}"
        )

    # (d) The three verdict kinds are each answered — the pass genuinely
    # discriminates covered from contradicts from supersedes over decision text
    # alone, with no pre-encoded invariant or baseline.
    kinds_by_id = {v.neighbour_id: v.verdict for v in result.verdicts}
    assert kinds_by_id[COVERED_ID] == VerdictKind.COVERED, kinds_by_id
    assert kinds_by_id[CONTRADICTS_ID] == VerdictKind.CONTRADICTS, kinds_by_id
    assert kinds_by_id[SUPERSEDES_ID] == VerdictKind.SUPERSEDES, kinds_by_id


@then("each verdict cites the neighbour it is about by id")
def _each_verdict_cites_by_id(context: dict) -> None:
    result = context["result"]
    neighbours = context["neighbours"]

    surfaced_ids = {neighbour.id for neighbour in neighbours}
    cited_ids = [verdict.neighbour_id for verdict in result.verdicts]

    # Each verdict cites a real surfaced neighbour by id...
    for verdict in result.verdicts:
        assert verdict.neighbour_id in surfaced_ids, (
            f"verdict cites {verdict.neighbour_id!r}, not a surfaced neighbour id "
            f"{sorted(surfaced_ids)}"
        )

    # ...the citations are distinct (one verdict per neighbour, no double-citing)...
    assert len(cited_ids) == len(set(cited_ids)), (
        f"each neighbour must be cited by exactly one verdict, got {cited_ids}"
    )

    # ...and the set of cited ids equals the set of surfaced neighbour ids.
    assert set(cited_ids) == surfaced_ids, (
        f"the set of cited ids {sorted(set(cited_ids))} must equal the set of "
        f"surfaced neighbour ids {sorted(surfaced_ids)}"
    )
    assert set(result.cited_ids()) == surfaced_ids

    # Each verdict carries explainable evidence citing the neighbour: the shared
    # subject tokens and the neighbour's verbatim L1 extract it reasoned over.
    for verdict in result.verdicts:
        assert verdict.subject, (
            f"verdict for {verdict.neighbour_id} must carry the shared subject "
            "tokens that explain which governed surface it is about"
        )
        assert verdict.l1_extract, (
            f"verdict for {verdict.neighbour_id} must carry the neighbour's "
            "verbatim L1 extract as cited evidence"
        )
