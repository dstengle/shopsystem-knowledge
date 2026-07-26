"""Step definitions for the distribution-scope coherence check (1 scenario).

Binds ``distribution_scope_checks.feature`` and asserts each Then/And leg against
the :class:`~knowledge.coherence.CoherenceReport` returned by
``run_coherence_gate(corpus, config, checks=DISTRIBUTION_CHECKS)`` — the SAME
fold and verdict machinery the artifact-lifecycle and typed-edge waves use,
extended with the distribution-scope check rather than a re-spelled aggregate.

Modelling "resident on the lead host": the corpus the knowledge context ranges
over IS the lead host's knowledge corpus (the context runs on the lead host),
so an artifact carried in this corpus that declares ``distribution: bc-local``
is misfiled by construction — bc-local artifacts belong in a BC repo. The Given
step therefore states exactly the one shape the scenario is about: a single
lead-host corpus artifact whose frontmatter carries ``distribution: bc-local``,
chosen as an ``intent-record`` (status ``recorded``) so it trips no lifecycle or
typed-edge check and the only finding under test is ``misfiled-bc-local``.

RED leg: ``DISTRIBUTION_CHECKS`` (the distribution gate's check registry) exists
but does not yet carry the distribution-scope check, so the gate produces no
``misfiled-bc-local`` finding — the first Then leg fails on the missing finding,
not at collection/import time. The GREEN leg adds ``check_misfiled_bc_local`` to
the distribution gate and makes every leg pass.
"""

from __future__ import annotations

from datetime import date

import pytest
from pytest_bdd import given, scenario, then, when

from knowledge.artifact_types import Artifact

FEATURE = "distribution_scope_checks.feature"
REFERENCE = date(2026, 7, 1)


@pytest.fixture
def context() -> dict:
    return {}


# --- Scenario binding --------------------------------------------------------


@scenario(FEATURE, "a lead-host artifact carrying distribution bc-local is flagged as misfiled")
def test_misfiled_bc_local() -> None: ...


# --- Given step --------------------------------------------------------------


@given(
    "an artifact corpus resident on the lead host in which an artifact carries a "
    "distribution value of bc-local"
)
def _lead_host_bc_local(context: dict) -> None:
    # The corpus the knowledge context ranges over is the lead host's corpus.
    context["artifact_id"] = "intent-001"
    context["artifacts"] = [
        Artifact(
            frontmatter={
                "type": "intent-record",
                "id": "intent-001",
                "status": "recorded",
                "updated": "2026-06-25",
                "distribution": "bc-local",
            },
            body="",
        )
    ]


# --- When step ---------------------------------------------------------------


@when("the knowledge context runs the distribution-scope coherence check over the corpus")
def _run_distribution_scope(context: dict) -> None:
    from knowledge.coherence import ArtifactCorpus, CoherenceConfig, run_coherence_gate
    from knowledge.distribution import DISTRIBUTION_CHECKS

    corpus = ArtifactCorpus.from_artifacts(context["artifacts"])
    config = CoherenceConfig(reference_date=REFERENCE)
    context["report"] = run_coherence_gate(corpus, config, checks=DISTRIBUTION_CHECKS)


# --- Then steps --------------------------------------------------------------


def _findings(context: dict):
    return context["report"].findings_for_check("misfiled-bc-local")


@then("it reports a misfiled-bc-local finding naming the artifact by id")
def _reports_misfiled(context: dict) -> None:
    found = _findings(context)
    assert found, (
        "expected a misfiled-bc-local finding; got "
        f"{[f.check_id for f in context['report'].findings]}"
    )
    finding = found[0]
    assert context["artifact_id"] in finding.subjects
    assert context["artifact_id"] in finding.message


@then(
    "the finding carries its check-id and a remediation to relocate the artifact to "
    "its BC repo or correct its distribution scope"
)
def _carries_check_id_and_remediation(context: dict) -> None:
    finding = _findings(context)[0]
    assert finding.check_id == "misfiled-bc-local"
    remediation = finding.remediation.lower()
    assert "bc repo" in remediation or "bc-local" in remediation or "relocate" in remediation
    assert "distribution" in remediation or "scope" in remediation


@then("the aggregate verdict exits non-zero")
def _exits_non_zero(context: dict) -> None:
    assert context["report"].exit_code != 0
