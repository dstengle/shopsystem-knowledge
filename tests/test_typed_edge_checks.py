"""Step definitions for the typed-edge coherence checks (11 scenarios).

Binds every scenario in ``typed_edge_checks.feature`` and asserts each Then/And
leg against the :class:`~knowledge.coherence.CoherenceReport` returned by
``run_coherence_gate(corpus, config, checks=TYPED_EDGE_CHECKS)`` — the SAME fold
and verdict machinery the artifact-lifecycle wave uses, extended with a new
check tuple rather than a re-spelled aggregate.

RED leg: ``knowledge.typed_edges`` does not yet exist, so ``TYPED_EDGE_CHECKS``
and the edge-inspection helpers are imported inside the step bodies — every
scenario fails at its first typed-edge step on the absent behaviour, not at
collection time.

Corpora are built two ways, matching the codebase's split:

* the two whole-corpus scenarios (clean corpus, multiple defects) load real
  on-disk ``.md`` fixtures under ``tests/fixtures/typed_edge_corpus`` through
  :func:`~knowledge.artifact_types.parse_artifact`, exercising the list /
  empty-list link-field round-trip;
* the focused single-invariant scenarios state their one edge shape in-process
  from :class:`~knowledge.artifact_types.Artifact` objects, mirroring the
  artifact-lifecycle sibling.

Edges are resolved from frontmatter link fields only — never from body prose —
so the prose-mention scenario asserts on the resolved edge set directly.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenario, then, when

from knowledge.artifact_types import Artifact, parse_artifact

FEATURE = "typed_edge_checks.feature"
FIXTURE_DIR = Path(__file__).parent / "fixtures" / "typed_edge_corpus"
REFERENCE = date(2026, 7, 1)


def _artifact(**frontmatter) -> Artifact:
    return Artifact(frontmatter=dict(frontmatter), body=frontmatter.pop("body", ""))


def _load_corpus_dir(name: str) -> list[Artifact]:
    return [parse_artifact(p.read_text()) for p in sorted((FIXTURE_DIR / name).glob("*.md"))]


@pytest.fixture
def context() -> dict:
    return {}


# --- Scenario bindings -------------------------------------------------------


@scenario(FEATURE, "an asymmetric supersede without a back-edge is flagged")
def test_asymmetric_supersede() -> None: ...


@scenario(FEATURE, "a list-valued supersedes with one missing per-pair back-edge is flagged")
def test_list_supersede_one_missing() -> None: ...


@scenario(FEATURE, "a list-valued supersedes with every per-pair back-edge present passes")
def test_list_supersede_all_present() -> None: ...


@scenario(FEATURE, "a superseded artifact whose status is not superseded is flagged")
def test_active_yet_superseded() -> None: ...


@scenario(FEATURE, "a link field pointing to a target absent from the corpus is flagged")
def test_dangling_edge() -> None: ...


@scenario(FEATURE, "a supersede cycle is flagged")
def test_supersede_cycle() -> None: ...


@scenario(FEATURE, "an id mentioned only in body prose creates no graph edge")
def test_prose_mention_no_edge() -> None: ...


@scenario(FEATURE, "a load-bearing prose mention promoted to derives-from becomes a resolved graph edge")
def test_promoted_prose_resolved_edge() -> None: ...


@scenario(FEATURE, "a clean corpus passes with a success aggregate verdict")
def test_clean_corpus_passes() -> None: ...


@scenario(FEATURE, "multiple defects fold into one aggregate verdict")
def test_multiple_defects_fold() -> None: ...


@scenario(FEATURE, "the governed-delta invariant tripwire is opt-in and skips artifacts that register none")
def test_governed_delta_opt_in() -> None: ...


# --- Given steps -------------------------------------------------------------


@given("an artifact corpus in which artifact A declares that it supersedes artifact B")
def _a_supersedes_b(context: dict) -> None:
    context["A"] = "adr-100"
    context["B"] = "adr-050"
    context["artifacts"] = [
        _artifact(type="adr", id="adr-100", status="accepted", supersedes=["adr-050"]),
        _artifact(type="adr", id="adr-050", status="accepted"),
    ]


@given("artifact B carries no superseded-by edge back to A")
def _b_no_backedge(context: dict) -> None:
    for art in context["artifacts"]:
        assert "superseded-by" not in art.frontmatter


@given("an artifact corpus in which artifact A declares that it supersedes a list of artifacts B and C")
def _a_supersedes_list_bc(context: dict) -> None:
    context["A"] = "adr-100"
    context["B"] = "adr-050"
    context["C"] = "adr-060"
    context["artifacts"] = [
        _artifact(type="adr", id="adr-100", status="accepted", supersedes=["adr-050", "adr-060"]),
        _artifact(type="adr", id="adr-050", status="superseded"),
        _artifact(type="adr", id="adr-060", status="superseded"),
    ]


def _set_field(context: dict, artifact_id: str, field: str, value) -> None:
    for art in context["artifacts"]:
        if art.id == artifact_id:
            art.frontmatter[field] = value
            return
    raise AssertionError(f"no artifact {artifact_id} in corpus")


@given("artifact B carries a superseded-by edge back to A")
def _b_backedge(context: dict) -> None:
    _set_field(context, context["B"], "superseded-by", [context["A"]])


@given("artifact C carries no superseded-by edge back to A")
def _c_no_backedge(context: dict) -> None:
    for art in context["artifacts"]:
        if art.id == context["C"]:
            assert "superseded-by" not in art.frontmatter


@given("artifacts B and C each carry a superseded-by edge back to A")
def _bc_backedges(context: dict) -> None:
    _set_field(context, context["B"], "superseded-by", [context["A"]])
    _set_field(context, context["C"], "superseded-by", [context["A"]])


@given("artifacts B and C each carry a superseded status")
def _bc_superseded_status(context: dict) -> None:
    _set_field(context, context["B"], "status", "superseded")
    _set_field(context, context["C"], "status", "superseded")


@given("an artifact corpus in which artifact B is superseded by artifact A yet artifact B's status is not superseded")
def _b_superseded_wrong_status(context: dict) -> None:
    context["A"] = "adr-100"
    context["B"] = "adr-050"
    context["artifacts"] = [
        _artifact(type="adr", id="adr-100", status="accepted", supersedes=["adr-050"]),
        _artifact(type="adr", id="adr-050", status="accepted", **{"superseded-by": ["adr-100"]}),
    ]


@given(
    parsers.parse(
        "an artifact corpus in which an artifact declares a {link_field} edge to a "
        "target id that is not present in the corpus"
    )
)
def _dangling_link_field(context: dict, link_field: str) -> None:
    context["source"] = "adr-100"
    context["target"] = "missing-999"
    context["link_field"] = link_field
    context["artifacts"] = [
        _artifact(type="adr", id="adr-100", status="accepted", **{link_field: "missing-999"}),
    ]


@given("an artifact corpus in which artifact A supersedes artifact B and artifact B supersedes artifact A")
def _supersede_cycle(context: dict) -> None:
    context["A"] = "adr-100"
    context["B"] = "adr-050"
    context["artifacts"] = [
        _artifact(type="adr", id="adr-100", status="accepted", supersedes=["adr-050"]),
        _artifact(type="adr", id="adr-050", status="accepted", supersedes=["adr-100"]),
    ]


@given(
    "an artifact corpus in which an artifact's body prose references another present "
    "artifact's id but its frontmatter carries no link field naming that id"
)
def _prose_mention(context: dict) -> None:
    context["mentioned"] = "adr-050"
    context["artifacts"] = [
        Artifact(
            frontmatter={"type": "adr", "id": "adr-100", "status": "accepted"},
            body="## Decision\n\nThis reverses the reasoning in adr-050, but only in prose.\n",
        ),
        _artifact(type="adr", id="adr-050", status="accepted"),
    ]


@given(
    "an artifact whose previously prose-only reference to an upstream artifact has been "
    "promoted into its derives-from frontmatter field"
)
def _promoted_prose(context: dict) -> None:
    context["source"] = "adr-100"
    context["upstream"] = "pdr-010"
    context["artifacts"] = [
        _artifact(type="adr", id="adr-100", status="accepted", **{"derives-from": ["pdr-010"]}),
    ]


@given("that upstream artifact is present in the corpus")
def _upstream_present(context: dict) -> None:
    context["artifacts"].append(_artifact(type="pdr", id="pdr-010", status="accepted"))


@given(
    "an artifact corpus whose supersede edges are all symmetric, whose superseded "
    "artifacts are all set to superseded status, whose link-field targets all resolve, "
    "and which contains no supersede cycle"
)
def _clean_corpus(context: dict) -> None:
    context["artifacts"] = _load_corpus_dir("clean")


@given("an artifact corpus carrying both an asymmetric-supersede defect and a dangling-edge defect")
def _multi_defect_corpus(context: dict) -> None:
    context["artifacts"] = _load_corpus_dir("multi_defect")


@given("an artifact that registers no governed-delta invariant")
def _no_governed_delta(context: dict) -> None:
    context["unregistered"] = "adr-100"
    context["artifacts"] = [_artifact(type="adr", id="adr-100", status="accepted")]


@given("a separate artifact that opts in by registering a governed-delta invariant over a governed surface")
def _opts_in_governed_delta(context: dict) -> None:
    context["registered"] = "adr-200"
    context["artifacts"].append(
        _artifact(
            type="adr",
            id="adr-200",
            status="accepted",
            **{"governed-delta": {"invariant": "delta-bounded", "surface": "adr-100"}},
        )
    )


# --- When steps --------------------------------------------------------------


def _run_gate(context: dict) -> None:
    from knowledge.coherence import CoherenceConfig, run_coherence_gate
    from knowledge.typed_edges import TYPED_EDGE_CHECKS

    from knowledge.coherence import ArtifactCorpus

    corpus = ArtifactCorpus.from_artifacts(context["artifacts"])
    config = CoherenceConfig(reference_date=REFERENCE)
    context["corpus"] = corpus
    context["report"] = run_coherence_gate(corpus, config=config, checks=TYPED_EDGE_CHECKS)


@when("the knowledge context runs the typed-edge coherence checks over the corpus")
def _run_typed_edge(context: dict) -> None:
    _run_gate(context)


@when("the knowledge context runs its coherence checks over the corpus")
def _run_coherence(context: dict) -> None:
    from knowledge.coherence import ArtifactCorpus
    from knowledge.typed_edges import evaluated_governed_delta_subjects

    corpus = ArtifactCorpus.from_artifacts(context["artifacts"])
    context["corpus"] = corpus
    context["evaluated"] = evaluated_governed_delta_subjects(corpus)


# --- Then steps --------------------------------------------------------------


def _findings(context: dict, check_id: str):
    return context["report"].findings_for_check(check_id)


@then("it reports an asymmetric-supersede finding naming A and B by id")
def _reports_asym_ab(context: dict) -> None:
    found = _findings(context, "asymmetric-supersede")
    assert found, "expected an asymmetric-supersede finding"
    finding = found[0]
    assert context["A"] in finding.subjects and context["B"] in finding.subjects
    assert context["A"] in finding.message and context["B"] in finding.message


@then("the finding carries its check-id and a remediation to write the superseded-by back-edge on B")
def _asym_remediation(context: dict) -> None:
    finding = _findings(context, "asymmetric-supersede")[0]
    assert finding.check_id == "asymmetric-supersede"
    assert "superseded-by" in finding.remediation.lower()


@then("it reports an asymmetric-supersede finding naming A and C by id for the missing back-edge")
def _reports_asym_ac(context: dict) -> None:
    found = _findings(context, "asymmetric-supersede")
    assert found, "expected an asymmetric-supersede finding"
    assert any(context["A"] in f.subjects and context["C"] in f.subjects for f in found)


@then("it reports no asymmetric-supersede finding for the resolved A and B pair")
def _no_asym_ab(context: dict) -> None:
    for f in _findings(context, "asymmetric-supersede"):
        assert not (context["A"] in f.subjects and context["B"] in f.subjects)


@then("it reports no asymmetric-supersede finding for A")
def _no_asym_for_a(context: dict) -> None:
    for f in _findings(context, "asymmetric-supersede"):
        assert context["A"] not in f.subjects


@then("it reports an active-yet-superseded finding naming B by id")
def _reports_active_superseded(context: dict) -> None:
    found = _findings(context, "active-yet-superseded")
    assert found, "expected an active-yet-superseded finding"
    finding = found[0]
    assert context["B"] in finding.subjects
    assert context["B"] in finding.message


@then("the finding carries its check-id and a remediation to set B's status to superseded")
def _active_superseded_remediation(context: dict) -> None:
    finding = _findings(context, "active-yet-superseded")[0]
    assert finding.check_id == "active-yet-superseded"
    assert "superseded" in finding.remediation.lower()


@then(
    parsers.parse(
        "it reports a dangling-edge finding naming the source artifact and the "
        "unresolved target id on its {link_field} edge"
    )
)
def _reports_dangling(context: dict, link_field: str) -> None:
    found = _findings(context, "dangling-edge")
    assert found, "expected a dangling-edge finding"
    finding = found[0]
    assert context["source"] in finding.subjects
    assert context["target"] in finding.subjects
    assert context["source"] in finding.message
    assert context["target"] in finding.message
    assert link_field in finding.message


@then("the finding carries its check-id and a remediation")
def _dangling_remediation(context: dict) -> None:
    found = _findings(context, "dangling-edge") or _findings(context, "supersede-cycle")
    assert found, "expected a finding carrying a check-id"
    finding = found[0]
    assert finding.check_id
    assert finding.remediation


@then("it reports a supersede-cycle finding naming the artifacts in the cycle by id")
def _reports_cycle(context: dict) -> None:
    found = _findings(context, "supersede-cycle")
    assert found, "expected a supersede-cycle finding"
    finding = found[0]
    assert context["A"] in finding.subjects and context["B"] in finding.subjects
    assert context["A"] in finding.message and context["B"] in finding.message


@then("it forms no edge from the prose mention because the gate resolves frontmatter link fields only")
def _no_prose_edge(context: dict) -> None:
    from knowledge.typed_edges import resolve_edges

    edges = resolve_edges(context["corpus"])
    assert all(edge.target != context["mentioned"] for edge in edges), (
        "prose mention must not form a resolved graph edge"
    )


@then("it reports no dangling-edge finding arising from the prose mention")
def _no_dangling_from_prose(context: dict) -> None:
    assert not _findings(context, "dangling-edge")


@then("it resolves a derives-from edge from the promoting artifact to the upstream artifact")
def _resolves_derives_from(context: dict) -> None:
    from knowledge.typed_edges import resolve_edges

    edges = resolve_edges(context["corpus"])
    match = [
        e
        for e in edges
        if e.source == context["source"]
        and e.link_field == "derives-from"
        and e.target == context["upstream"]
    ]
    assert match, "expected a derives-from edge from the promoting artifact to the upstream"
    assert match[0].resolved, "the promoted derives-from edge must resolve"


@then("it reports no dangling-edge finding for that edge")
def _no_dangling_for_promoted(context: dict) -> None:
    for f in _findings(context, "dangling-edge"):
        assert context["upstream"] not in f.subjects


@then("it reports no findings")
def _no_findings(context: dict) -> None:
    assert context["report"].findings == (), (
        f"expected no findings; got {[f.check_id for f in context['report'].findings]}"
    )


@then("it reports both findings, each named by its own check-id")
def _reports_both(context: dict) -> None:
    assert context["report"].has_finding("asymmetric-supersede")
    assert context["report"].has_finding("dangling-edge")


@then("it folds them into a single aggregate verdict that exits non-zero")
def _folds_non_zero(context: dict) -> None:
    assert context["report"].exit_code != 0


@then("it evaluates no governed-delta tripwire against the artifact that registered none")
def _no_tripwire_unregistered(context: dict) -> None:
    assert context["unregistered"] not in context["evaluated"]


@then("it evaluates the governed-delta tripwire only against the artifact that opted in")
def _tripwire_only_registered(context: dict) -> None:
    assert context["evaluated"] == (context["registered"],)


@then("the aggregate verdict exits non-zero")
def _exits_non_zero(context: dict) -> None:
    assert context["report"].exit_code != 0


@then("the aggregate verdict exits zero")
def _exits_zero(context: dict) -> None:
    assert context["report"].exit_code == 0, (
        f"expected zero; findings: {[f.check_id for f in context['report'].findings]}"
    )
