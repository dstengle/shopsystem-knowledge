"""Step definitions for the artifact-lifecycle coherence checks (13 scenarios).

Binds every scenario in ``artifact_lifecycle_checks.feature`` and asserts each
Then/And leg against the :class:`CoherenceReport` returned by
``knowledge.coherence.run_coherence_gate``.

RED leg: ``knowledge.coherence`` does not yet exist, so ``run_coherence_gate``
(and the ``ArtifactCorpus`` / ``CoherenceConfig`` it needs) is imported inside
the shared ``When`` step body — every scenario fails at that step on the absent
behaviour, not at collection time. The GREEN leg adds ``knowledge.coherence``
and makes all thirteen pass.

Corpora are built in-process from :class:`~knowledge.artifact_types.Artifact`
objects (rather than on-disk fixture files) so each Given states exactly the one
lifecycle shape the scenario is about. The config carries a fixed reference date
and a 30-day staleness threshold so the age comparison is deterministic and
ambient-free.
"""

from __future__ import annotations

from datetime import date

import pytest
from pytest_bdd import given, scenario, then, when

from knowledge.artifact_types import Artifact

FEATURE = "artifact_lifecycle_checks.feature"

# A fixed as-of date and threshold so staleness is deterministic: an "old"
# artifact is dated well before REFERENCE - 30d, a "recent" one just inside it.
REFERENCE = date(2026, 7, 1)
OLD = "2026-01-01"  # ~180 days before REFERENCE -> stale
RECENT = "2026-06-25"  # 6 days before REFERENCE -> fresh


def _artifact(**frontmatter) -> Artifact:
    frontmatter.setdefault("updated", RECENT)
    return Artifact(frontmatter=dict(frontmatter), body="")


@pytest.fixture
def context() -> dict:
    return {}


# --- Scenario bindings -------------------------------------------------------


@scenario(FEATURE, "a briefed candidate that names no brief is flagged")
def test_briefed_without_brief() -> None: ...


@scenario(FEATURE, "a briefed candidate whose brief does not point back is flagged")
def test_briefed_brief_asymmetry() -> None: ...


@scenario(FEATURE, "a briefed candidate bidirectionally tied to its brief passes")
def test_briefed_bidirectional() -> None: ...


@scenario(FEATURE, "a brief numbered above 015 that names no candidate is flagged")
def test_brief_without_candidate() -> None: ...


@scenario(FEATURE, "a legacy brief numbered 001 through 015 without a candidate is exempt")
def test_legacy_brief_exempt() -> None: ...


@scenario(FEATURE, "a closed session-record with both produced and revised empty is flagged")
def test_empty_closed_session() -> None: ...


@scenario(FEATURE, "a closed session-record linking at least one produced artifact passes")
def test_closed_session_with_produced() -> None: ...


@scenario(FEATURE, "an accepted decision claimed by no current-state incorporates list is flagged")
def test_unincorporated_decision() -> None: ...


@scenario(FEATURE, "an accepted decision claimed by a current-state incorporates list passes")
def test_incorporated_decision() -> None: ...


@scenario(
    FEATURE,
    "an in-flight artifact older than the age threshold draws a warning-severity finding",
)
def test_stale_in_flight() -> None: ...


@scenario(FEATURE, "a pdr with an empty derives-from anchor draws a root-decision warning")
def test_root_decision_anchor() -> None: ...


@scenario(
    FEATURE,
    "a pdr that anchors to at least one upstream artifact draws no root-decision warning",
)
def test_anchored_pdr_no_warning() -> None: ...


@scenario(FEATURE, "an in-flight artifact younger than the age threshold draws no warning")
def test_fresh_in_flight_no_warning() -> None: ...


# --- Given steps -------------------------------------------------------------


@given("an artifact corpus containing a candidate whose status is briefed and whose brief field is unset")
def _briefed_no_brief(context: dict) -> None:
    context["candidate_id"] = "cand-001"
    context["artifacts"] = [_artifact(type="candidate", id="cand-001", status="briefed")]


@given(
    "an artifact corpus containing a candidate whose status is briefed and whose "
    "brief field names a brief"
)
def _briefed_with_brief(context: dict) -> None:
    context["candidate_id"] = "cand-001"
    context["brief_id"] = "brief-020"
    context["artifacts"] = [
        _artifact(type="candidate", id="cand-001", status="briefed", brief="brief-020"),
        _artifact(type="brief", id="brief-020", status="ready"),
    ]


@given("that brief's candidate field does not point back to the candidate")
def _brief_no_backref(context: dict) -> None:
    # Leave the brief's candidate field pointing at a different candidate.
    for art in context["artifacts"]:
        if art.frontmatter.get("type") == "brief":
            art.frontmatter["candidate"] = "cand-999"


@given("that brief's candidate field names the candidate back")
def _brief_backref(context: dict) -> None:
    for art in context["artifacts"]:
        if art.frontmatter.get("type") == "brief":
            art.frontmatter["candidate"] = context["candidate_id"]


@given(
    "an artifact corpus containing a brief whose id is brief-042 and whose "
    "candidate field is unset"
)
def _brief_042_no_candidate(context: dict) -> None:
    context["brief_id"] = "brief-042"
    context["artifacts"] = [_artifact(type="brief", id="brief-042", status="ready")]


@given(
    "an artifact corpus containing a brief whose id is brief-009 and whose "
    "candidate field is unset"
)
def _brief_009_no_candidate(context: dict) -> None:
    context["brief_id"] = "brief-009"
    context["artifacts"] = [_artifact(type="brief", id="brief-009", status="ready")]


@given(
    "an artifact corpus containing a session-record whose status is closed and "
    "whose produced and revised fields are both empty"
)
def _empty_closed_session(context: dict) -> None:
    context["session_id"] = "session-001"
    context["artifacts"] = [
        _artifact(
            type="session-record",
            id="session-001",
            status="closed",
            produced=[],
            revised=[],
        )
    ]


@given(
    "an artifact corpus containing a session-record whose status is closed and "
    "whose produced field links one artifact"
)
def _closed_session_with_produced(context: dict) -> None:
    context["session_id"] = "session-001"
    context["artifacts"] = [
        _artifact(
            type="session-record",
            id="session-001",
            status="closed",
            produced=["adr-001"],
            revised=[],
        )
    ]


@given(
    "an artifact corpus containing an accepted pdr whose id appears in no "
    "current-state incorporates list"
)
def _unincorporated_pdr(context: dict) -> None:
    context["decision_id"] = "pdr-001"
    context["artifacts"] = [
        _artifact(type="pdr", id="pdr-001", status="accepted"),
        _artifact(type="charter", id="charter-001", status="ratified", incorporates=[]),
    ]


@given(
    "an artifact corpus containing an accepted adr whose id appears in a "
    "current-state incorporates list"
)
def _incorporated_adr(context: dict) -> None:
    context["decision_id"] = "adr-001"
    context["artifacts"] = [
        _artifact(type="adr", id="adr-001", status="accepted"),
        _artifact(
            type="charter", id="charter-001", status="ratified", incorporates=["adr-001"]
        ),
    ]


@given(
    "an artifact corpus containing an artifact whose status is draft and whose "
    "updated date is older than the configured age threshold"
)
def _stale_draft(context: dict) -> None:
    context["subject_id"] = "intent-001"
    context["artifacts"] = [
        _artifact(type="intent-record", id="intent-001", status="draft", updated=OLD)
    ]


@given("an artifact corpus containing a pdr whose derives-from field is an empty list")
def _pdr_empty_anchor(context: dict) -> None:
    context["decision_id"] = "pdr-001"
    art = _artifact(type="pdr", id="pdr-001", status="proposed")
    art.frontmatter["derives-from"] = []
    context["artifacts"] = [art]


@given(
    "an artifact corpus containing a pdr whose derives-from field names at least "
    "one upstream artifact present in the corpus"
)
def _pdr_anchored(context: dict) -> None:
    context["decision_id"] = "pdr-001"
    pdr = _artifact(type="pdr", id="pdr-001", status="proposed")
    pdr.frontmatter["derives-from"] = ["adr-001"]
    context["artifacts"] = [
        pdr,
        _artifact(type="adr", id="adr-001", status="proposed"),
    ]


@given(
    "an artifact corpus containing an artifact whose status is exploring and "
    "whose updated date is within the configured age threshold"
)
def _fresh_exploring(context: dict) -> None:
    context["subject_id"] = "cand-001"
    context["artifacts"] = [
        _artifact(type="candidate", id="cand-001", status="exploring", updated=RECENT)
    ]


# --- When step (shared) ------------------------------------------------------


@when("the knowledge context runs the artifact-lifecycle coherence checks over the corpus")
def _run_checks(context: dict) -> None:
    from knowledge.coherence import ArtifactCorpus, CoherenceConfig, run_coherence_gate

    corpus = ArtifactCorpus(artifacts=tuple(context["artifacts"]))
    config = CoherenceConfig(reference_date=REFERENCE)
    context["report"] = run_coherence_gate(corpus, config=config)


# --- Then steps --------------------------------------------------------------


def _findings(context: dict, check_id: str):
    return context["report"].findings_for_check(check_id)


@then("it reports a briefed-without-brief finding naming the candidate by id")
def _reports_briefed_without_brief(context: dict) -> None:
    found = _findings(context, "briefed-without-brief")
    assert found, "expected a briefed-without-brief finding"
    assert any(context["candidate_id"] in f.message for f in found)
    assert any(context["candidate_id"] in f.subjects for f in found)


@then("the finding carries its check-id and a remediation to set the candidate's brief field")
def _briefed_without_brief_remediation(context: dict) -> None:
    finding = _findings(context, "briefed-without-brief")[0]
    assert finding.check_id == "briefed-without-brief"
    assert "brief" in finding.remediation.lower()


@then("it reports a briefed-brief-asymmetry finding naming the candidate and the brief by id")
def _reports_asymmetry(context: dict) -> None:
    found = _findings(context, "briefed-brief-asymmetry")
    assert found, "expected a briefed-brief-asymmetry finding"
    finding = found[0]
    assert context["candidate_id"] in finding.subjects
    assert context["brief_id"] in finding.subjects
    assert context["candidate_id"] in finding.message
    assert context["brief_id"] in finding.message


@then(
    "the finding carries its check-id and a remediation to set the brief's "
    "candidate field back to the candidate"
)
def _asymmetry_remediation(context: dict) -> None:
    finding = _findings(context, "briefed-brief-asymmetry")[0]
    assert finding.check_id == "briefed-brief-asymmetry"
    assert "candidate" in finding.remediation.lower()


@then("it reports no briefed-candidate finding for that pair")
def _no_briefed_finding(context: dict) -> None:
    assert not _findings(context, "briefed-without-brief")
    assert not _findings(context, "briefed-brief-asymmetry")


@then("it reports a brief-without-candidate finding naming the brief by id")
def _reports_brief_without_candidate(context: dict) -> None:
    found = _findings(context, "brief-without-candidate")
    assert found, "expected a brief-without-candidate finding"
    assert any(context["brief_id"] in f.message for f in found)
    assert any(context["brief_id"] in f.subjects for f in found)


@then("the finding carries its check-id and a remediation to set the brief's candidate field")
def _brief_without_candidate_remediation(context: dict) -> None:
    finding = _findings(context, "brief-without-candidate")[0]
    assert finding.check_id == "brief-without-candidate"
    assert "candidate" in finding.remediation.lower()


@then("it reports no brief-without-candidate finding for that brief")
def _no_brief_without_candidate(context: dict) -> None:
    assert not _findings(context, "brief-without-candidate")


@then("it reports an empty-closed-session finding naming the session-record by id")
def _reports_empty_closed(context: dict) -> None:
    found = _findings(context, "empty-closed-session")
    assert found, "expected an empty-closed-session finding"
    assert any(context["session_id"] in f.message for f in found)
    assert any(context["session_id"] in f.subjects for f in found)


@then(
    "the finding carries its check-id and a remediation to link at least one "
    "produced or revised artifact"
)
def _empty_closed_remediation(context: dict) -> None:
    finding = _findings(context, "empty-closed-session")[0]
    assert finding.check_id == "empty-closed-session"
    remediation = finding.remediation.lower()
    assert "produced" in remediation or "revised" in remediation


@then("it reports no empty-closed-session finding for that session-record")
def _no_empty_closed(context: dict) -> None:
    assert not _findings(context, "empty-closed-session")


@then("it reports an unincorporated-decision finding naming the pdr by id")
def _reports_unincorporated(context: dict) -> None:
    found = _findings(context, "unincorporated-decision")
    assert found, "expected an unincorporated-decision finding"
    assert any(context["decision_id"] in f.message for f in found)
    assert any(context["decision_id"] in f.subjects for f in found)


@then(
    "the finding carries its check-id and a remediation to claim the pdr in a "
    "current-state incorporates list"
)
def _unincorporated_remediation(context: dict) -> None:
    finding = _findings(context, "unincorporated-decision")[0]
    assert finding.check_id == "unincorporated-decision"
    assert "incorporat" in finding.remediation.lower()


@then("it reports no unincorporated-decision finding for that adr")
def _no_unincorporated(context: dict) -> None:
    assert not _findings(context, "unincorporated-decision")


@then("it reports a stale-in-flight finding naming the artifact by id at warning severity")
def _reports_stale(context: dict) -> None:
    from knowledge.coherence import Severity

    found = _findings(context, "stale-in-flight")
    assert found, "expected a stale-in-flight finding"
    finding = found[0]
    assert context["subject_id"] in finding.message
    assert context["subject_id"] in finding.subjects
    assert finding.severity is Severity.ADVISORY


@then("the finding carries its check-id and a remediation to advance or close the artifact")
def _stale_remediation(context: dict) -> None:
    finding = _findings(context, "stale-in-flight")[0]
    assert finding.check_id == "stale-in-flight"
    remediation = finding.remediation.lower()
    assert "advance" in remediation or "close" in remediation


@then("it reports no stale-in-flight finding for that artifact")
def _no_stale(context: dict) -> None:
    assert not _findings(context, "stale-in-flight")


@then("it reports a root-decision-anchor finding naming the pdr by id at warning severity")
def _reports_root_decision(context: dict) -> None:
    from knowledge.coherence import Severity

    found = _findings(context, "root-decision-anchor")
    assert found, "expected a root-decision-anchor finding"
    finding = found[0]
    assert context["decision_id"] in finding.message
    assert context["decision_id"] in finding.subjects
    assert finding.severity is Severity.ADVISORY


@then(
    "the finding carries its check-id and a remediation to anchor the pdr to an "
    "upstream artifact unless it is a root decision"
)
def _root_decision_remediation(context: dict) -> None:
    finding = _findings(context, "root-decision-anchor")[0]
    assert finding.check_id == "root-decision-anchor"
    assert "anchor" in finding.remediation.lower()


@then("it reports no root-decision-anchor finding for that pdr")
def _no_root_decision(context: dict) -> None:
    assert not _findings(context, "root-decision-anchor")


@then("the aggregate verdict exits non-zero")
def _exits_non_zero(context: dict) -> None:
    assert context["report"].exit_code != 0


@then("the aggregate verdict exits zero")
def _exits_zero(context: dict) -> None:
    assert context["report"].exit_code == 0, (
        f"expected zero; findings: {[f.check_id for f in context['report'].findings]}"
    )


@then("the warning does not by itself drive the aggregate verdict non-zero")
def _warning_does_not_block(context: dict) -> None:
    assert context["report"].exit_code == 0, (
        f"advisory finding should not block; findings: "
        f"{[(f.check_id, f.severity) for f in context['report'].findings]}"
    )
