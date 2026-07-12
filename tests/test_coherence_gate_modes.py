"""Step definitions for the coherence gate modes + doctor form (4 scenarios).

Binds every scenario in ``coherence_gate_modes.feature`` and asserts each
Then/And leg against the :class:`CoherenceReport` returned by
``knowledge.coherence.run_coherence_gate`` under an explicit
:class:`~knowledge.coherence.GateMode`.

RED leg: ``GateMode`` (and the mode-aware reporting the scenarios assert) does
not yet exist, so it is imported inside the shared ``When`` step body — every
scenario fails at that step on the absent behaviour, not at collection time. The
GREEN leg adds the mode enum, the mode-aware exit code, and the doctor-form
report surface, making all four pass.

Corpora are built in-process from real lifecycle shapes so each finding is a
genuine gate finding of the intended severity: a briefed candidate that names no
brief yields a single blocking finding; a pdr with an empty derives-from anchor
yields a single advisory finding.
"""

from __future__ import annotations

from datetime import date

import pytest
from pytest_bdd import parsers, given, scenario, then, when

from knowledge.artifact_types import Artifact
from knowledge.coherence import ArtifactCorpus

FEATURE = "coherence_gate_modes.feature"
REFERENCE = date(2026, 7, 1)


def _blocking_corpus() -> ArtifactCorpus:
    """A corpus that yields exactly one blocking finding (briefed-without-brief)."""
    return ArtifactCorpus(
        artifacts=(
            Artifact(
                frontmatter={
                    "type": "candidate",
                    "id": "cand-001",
                    "status": "briefed",
                    "updated": "2026-06-25",
                },
                body="",
            ),
        )
    )


def _advisory_corpus() -> ArtifactCorpus:
    """A corpus whose only finding is advisory (root-decision-anchor)."""
    return ArtifactCorpus(
        artifacts=(
            Artifact(
                frontmatter={
                    "type": "pdr",
                    "id": "pdr-001",
                    "status": "proposed",
                    "updated": "2026-06-25",
                    "derives-from": [],
                },
                body="",
            ),
        )
    )


@pytest.fixture
def context() -> dict:
    return {}


# --- Scenario bindings -------------------------------------------------------


@scenario(FEATURE, "authoring mode warns and never blocks")
def test_authoring_warns() -> None: ...


@scenario(FEATURE, "distribution mode vetoes a blocking-severity finding")
def test_distribution_vetoes_blocking() -> None: ...


@scenario(FEATURE, "distribution mode only warns on an advisory-severity finding")
def test_distribution_warns_advisory() -> None: ...


@scenario(FEATURE, "every finding is reported in doctor form")
def test_doctor_form() -> None: ...


# --- Given steps -------------------------------------------------------------


@given("an artifact corpus that carries a coherence finding")
def _carries_finding(context: dict) -> None:
    context["corpus"] = _blocking_corpus()


@given("an artifact corpus whose coherence finding is classified as blocking severity")
def _blocking_finding(context: dict) -> None:
    context["corpus"] = _blocking_corpus()


@given("an artifact corpus whose only coherence finding is classified as advisory severity")
def _advisory_finding(context: dict) -> None:
    context["corpus"] = _advisory_corpus()


# --- When step (shared) ------------------------------------------------------


@when(parsers.parse("the knowledge context runs the coherence gate with mode {mode}"))
def _run_gate(context: dict, mode: str) -> None:
    from knowledge.coherence import CoherenceConfig, GateMode, run_coherence_gate

    gate_mode = GateMode(mode)
    config = CoherenceConfig(reference_date=REFERENCE)
    context["report"] = run_coherence_gate(context["corpus"], config, mode=gate_mode)


# --- Then steps --------------------------------------------------------------


@then("it reports the finding as a warning")
def _reports_as_warning(context: dict) -> None:
    from knowledge.coherence import ReportStatus

    report = context["report"]
    assert report.findings, "expected at least one finding"
    assert all(
        report.reported_status(f) is ReportStatus.WARNING for f in report.findings
    )


@then("it reports the advisory finding as a warning")
def _reports_advisory_as_warning(context: dict) -> None:
    from knowledge.coherence import ReportStatus, Severity

    report = context["report"]
    assert report.findings, "expected at least one finding"
    finding = report.findings[0]
    assert finding.severity is Severity.ADVISORY
    assert report.reported_status(finding) is ReportStatus.WARNING


@then("it reports the blocking finding")
def _reports_blocking(context: dict) -> None:
    from knowledge.coherence import ReportStatus, Severity

    report = context["report"]
    assert report.blocking_findings, "expected a blocking finding"
    finding = report.blocking_findings[0]
    assert finding.severity is Severity.BLOCKING
    assert report.reported_status(finding) is ReportStatus.BLOCKING


@then("it exits zero")
def _exits_zero(context: dict) -> None:
    assert context["report"].exit_code == 0


@then("it exits non-zero")
def _exits_non_zero(context: dict) -> None:
    assert context["report"].exit_code != 0


@then("it does not prevent the author from committing the artifact")
def _does_not_prevent_commit(context: dict) -> None:
    assert context["report"].prevents_commit is False


@then(
    "the reported finding carries its check name and check-id, a severity status, "
    "and a remediation"
)
def _doctor_form(context: dict) -> None:
    from knowledge.coherence import Severity

    report = context["report"]
    assert report.findings, "expected at least one finding"
    finding = report.findings[0]
    assert isinstance(finding.check_name, str) and finding.check_name
    assert isinstance(finding.check_id, str) and finding.check_id
    assert isinstance(finding.severity, Severity)
    assert isinstance(finding.remediation, str) and finding.remediation
