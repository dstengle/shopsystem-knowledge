"""Step definitions for the covered-verdict outer-loop scenario.

Binds @scenario_hash:3092efb62e739d3a — "a draft already decided elsewhere is
flagged covered with a citation to the covering decision" — the covered case of
the adversarial pass. A decision is being authored that decides a question the
corpus has ALREADY decided the same way; the authoring-time flow surfaces the
covering decision as a neighbour and the adversarial pass flags the draft as
covered by it, citing the covering decision BY ID.

The fixture is a single ACCEPTED decision (ADR-3101, a retry policy) whose L1
decision text is stable — it carries no governed-change marker — and a draft
that restates that same decision the same way (a parity claim that holds). By
the existing classification ladder (parity claim over a stable neighbour) this
lands COVERED with no change to the classifier.

The covering decision is surfaced by the real discovery pass and the covered
verdict is produced by the real adversarial pass, composed through the
authoring-time review entry point.

RED leg: ``authoring_time_review`` does not yet exist, so it is imported inside
the ``When`` step body — the scenario fails there on the absent behaviour
(ImportError), not at collection/import time.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from knowledge.discovery import DraftDecision

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "covered_corpus"

COVERING_ID = "ADR-3101"  # the accepted decision that already decides the question


@pytest.fixture
def context() -> dict:
    return {}


@scenario(
    "covered_verdict.feature",
    "a draft already decided elsewhere is flagged covered with a citation to "
    "the covering decision",
)
def test_covered_verdict() -> None:
    """Outer-loop binding; step bodies below carry the assertions."""


@given("an existing accepted decision that already decides a question")
def _existing_accepted_decision(context: dict) -> None:
    # The raw source corpus: a single ACCEPTED decision that decides the retry
    # question. It becomes the covering decision the draft is measured against.
    context["sources"] = {
        path.stem: path.read_text(encoding="utf-8")
        for path in sorted(FIXTURE_DIR.glob("*.md"))
    }


@given(
    "a draft decision being authored that decides the same question the same way"
)
def _draft_decides_same_way(context: dict) -> None:
    # The draft restates the accepted retry decision unchanged — a parity claim
    # over a stable neighbour, which the ladder resolves to COVERED.
    context["draft"] = DraftDecision(
        id="DRAFT-retry-policy-restated",
        title="Retry policy for the projection service",
        description="A draft that keeps the retry policy the same as the accepted decision.",
        body=(
            "## Decision\n\n"
            "The retry policy keeps retrying a failed request three times with "
            "exponential backoff before surfacing an error to the caller, "
            "unchanged from the accepted decision.\n"
        ),
    )


@when(
    "the knowledge context runs the authoring-time discovery pass over the draft"
)
def _run_authoring_time_review(context: dict) -> None:
    # Imported HERE (not at module top): the RED commit fails at this step on the
    # absent authoring_time_review entry point, not at collection time.
    from knowledge.adversarial import VerdictKind, authoring_time_review

    context["VerdictKind"] = VerdictKind
    context["result"] = authoring_time_review(context["sources"], context["draft"])


@then("it flags the draft as covered by the existing decision")
def _flagged_covered(context: dict) -> None:
    result = context["result"]
    VerdictKind = context["VerdictKind"]

    # The covering decision was surfaced and it carries a verdict.
    assert COVERING_ID in result.cited_ids(), (
        f"the covering decision {COVERING_ID} must be surfaced and cited, got "
        f"{result.cited_ids()}"
    )

    verdict = result.for_id(COVERING_ID)
    assert verdict.verdict == VerdictKind.COVERED, (
        f"the draft restates {COVERING_ID}'s stable decision, so it must be "
        f"flagged COVERED, got {verdict.verdict!r} ({verdict.rationale})"
    )


@then("it cites the covering decision by id")
def _cites_covering_by_id(context: dict) -> None:
    result = context["result"]
    verdict = result.for_id(COVERING_ID)

    # The verdict cites the covering decision BY ID...
    assert verdict.neighbour_id == COVERING_ID, (
        f"the covered verdict must cite {COVERING_ID} by id, got "
        f"{verdict.neighbour_id!r}"
    )

    # ...and carries the explainable evidence it reasoned over: the shared subject
    # tokens and the covering decision's verbatim L1 extract.
    assert verdict.subject, (
        "the covered verdict must carry the shared subject tokens that explain "
        "which governed surface it is about"
    )
    assert verdict.l1_extract, (
        "the covered verdict must carry the covering decision's verbatim L1 "
        "extract as cited evidence"
    )
