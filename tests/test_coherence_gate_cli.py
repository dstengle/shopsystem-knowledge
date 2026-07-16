"""Step definitions for the installed coherence-gate command over a corpus root.

Binds ``coherence_gate_cli.feature`` — the six scenarios that pin the gate as a
lead-installable contract command that walks a real corpus directory tree,
parses each document's YAML frontmatter into a typed artifact, and feeds the
resulting corpus into the already-pinned lifecycle and typed-edge checks.

Every scenario builds a real temporary corpus root directory on disk (via the
``tmp_path`` fixture) — the per-type subdirectories, the living
``current-state.md``, and, where the scenario calls for it, present-but-untyped
legacy files carrying no YAML frontmatter — and invokes the installed command
through ``knowledge.coherence_cli`` (its ``main`` for the exit code and its
``load_and_run`` for the returned :class:`CoherenceReport`).

RED convention: the new ``knowledge.coherence_cli`` / ``knowledge.corpus_loader``
modules are imported inside the step bodies, so each scenario fails at its
``When``/``Then`` step on the absent behaviour rather than at collection time.
"""

from __future__ import annotations

import io
from pathlib import Path

import pytest
from pytest_bdd import parsers, given, scenario, then, when

FEATURE = "coherence_gate_cli.feature"


# --- Corpus-building helpers -------------------------------------------------


def _write(path: Path, text: str) -> None:
    """Write ``text`` to ``path``, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _doc(frontmatter_lines: list[str], body: str = "\n") -> str:
    """Assemble a document from frontmatter lines and a body."""
    return "---\n" + "\n".join(frontmatter_lines) + "\n---\n" + body


@pytest.fixture
def context() -> dict:
    return {}


# --- Shared When (runs the installed command, default mode) ------------------


def _run_gate(context: dict) -> None:
    """Run the installed gate over ``context['root']`` in default mode."""
    from knowledge.coherence_cli import load_and_run, main

    root = context["root"]
    context["report"] = load_and_run(str(root))
    out, err = io.BytesIO(), io.BytesIO()
    context["exit_code"] = main([str(root)], stdout=out, stderr=err)
    context["stdout"] = out.getvalue().decode("utf-8")


@when(
    "the operator runs the knowledge context's installed coherence-gate command "
    "over the corpus root directory"
)
def _when_run(context: dict) -> None:
    _run_gate(context)


# --- Behavior 1: walks a real directory tree into the pinned checks ----------


@scenario(
    FEATURE,
    "the gate command walks a real directory tree and feeds typed documents "
    "into the already-pinned checks",
)
def test_walks_real_tree() -> None: ...


@given(
    "a corpus root directory containing a pdr file whose frontmatter declares a "
    "supersedes edge to a second pdr file"
)
def _given_two_pdrs(context: dict, tmp_path: Path) -> None:
    root = tmp_path / "corpus"
    _write(
        root / "pdrs" / "pdr-100.md",
        _doc(
            [
                "type: pdr",
                "id: pdr-100",
                "title: The newer decision",
                "status: proposed",
                "created: 2026-07-01",
                "updated: 2026-07-01",
                "authors: [alice]",
                "description: supersedes pdr-101",
                "decision-makers: [alice]",
                "derives-from: [pdr-101]",
                "supersedes: [pdr-101]",
            ]
        ),
    )
    context["root"] = root
    context["pair"] = ("pdr-100", "pdr-101")


@given(
    "that second pdr file's frontmatter carries a superseded-by edge back to "
    "the first"
)
def _given_back_edge(context: dict) -> None:
    root = context["root"]
    _write(
        root / "pdrs" / "pdr-101.md",
        _doc(
            [
                "type: pdr",
                "id: pdr-101",
                "title: The older decision",
                "status: superseded",
                "created: 2026-06-01",
                "updated: 2026-06-01",
                "authors: [alice]",
                "description: superseded by pdr-100",
                "decision-makers: [alice]",
                "derives-from: [pdr-100]",
                "superseded-by: [pdr-100]",
            ]
        ),
    )


@then("it reports no asymmetric-supersede finding for the pair")
def _then_no_asymmetric(context: dict) -> None:
    report = context["report"]
    source, target = context["pair"]
    for finding in report.findings_for_check("asymmetric-supersede"):
        assert source not in finding.subjects or target not in finding.subjects, (
            f"unexpected asymmetric-supersede finding for the pair: {finding}"
        )


@then("the aggregate verdict exits zero")
def _then_exits_zero(context: dict) -> None:
    assert context["report"].exit_code == 0
    assert context["exit_code"] == 0


# --- Behavior 2: the gate command defaults to authoring mode -----------------


@scenario(FEATURE, "the gate command defaults to authoring mode")
def test_defaults_to_authoring() -> None: ...


@given("a corpus root directory that carries at least one coherence finding")
def _given_corpus_with_finding(context: dict, tmp_path: Path) -> None:
    root = tmp_path / "corpus"
    # A briefed candidate that names no brief is a blocking finding
    # (briefed-without-brief); authoring mode must warn-not-block on it.
    _write(
        root / "candidates" / "cand-100.md",
        _doc(
            [
                "type: candidate",
                "id: cand-100",
                "title: A briefed idea",
                "status: briefed",
                "created: 2026-07-01",
                "updated: 2026-07-01",
                "authors: [alice]",
                "description: briefed but names no brief",
            ]
        ),
    )
    context["root"] = root


@when(
    "the operator runs the knowledge context's installed coherence-gate command "
    "over the corpus root directory with no mode specified"
)
def _when_run_no_mode(context: dict) -> None:
    _run_gate(context)


@then("it runs in authoring mode")
def _then_authoring_mode(context: dict) -> None:
    from knowledge.coherence import GateMode

    assert context["report"].mode is GateMode.AUTHORING


@then(
    "it exits zero despite the finding, per the already-pinned authoring-mode "
    "contract"
)
def _then_exits_zero_despite_finding(context: dict) -> None:
    report = context["report"]
    assert report.findings, "expected at least one finding to exist"
    assert report.exit_code == 0
    assert context["exit_code"] == 0


# --- Behavior 3: an absent typed-artifact directory loads as zero instances --


@scenario(FEATURE, "an absent typed-artifact directory does not crash the loader")
def test_absent_subdir() -> None: ...


@given("a corpus root directory that contains no prioritizations subdirectory at all")
def _given_no_prioritizations(context: dict, tmp_path: Path) -> None:
    root = tmp_path / "corpus"
    # A corpus with a pdrs/ subdirectory but deliberately no prioritizations/.
    _write(
        root / "pdrs" / "pdr-200.md",
        _doc(
            [
                "type: pdr",
                "id: pdr-200",
                "title: A standalone decision",
                "status: proposed",
                "created: 2026-07-01",
                "updated: 2026-07-01",
                "authors: [alice]",
                "description: no upstream anchor",
                "decision-makers: [alice]",
                "derives-from: []",
            ]
        ),
    )
    assert not (root / "prioritizations").exists()
    context["root"] = root


@then("the run completes and reports an aggregate verdict")
def _then_reports_verdict(context: dict) -> None:
    from knowledge.coherence import CoherenceReport

    assert isinstance(context["report"], CoherenceReport)
    assert isinstance(context["exit_code"], int)


@then(
    "it treats the absent subdirectory as zero prioritization-record instances, "
    "not as a loader error"
)
def _then_zero_prioritizations(context: dict) -> None:
    from knowledge.corpus_loader import load_corpus

    corpus = load_corpus(str(context["root"]))
    assert corpus.of_type("prioritization-record") == ()


# --- Behavior 4: supersedes to a no-frontmatter file is unverifiable-legacy --


def _distribution_report(context: dict):
    """Re-run the gate over the same root in distribution mode."""
    from knowledge.coherence import GateMode
    from knowledge.coherence_cli import load_and_run

    return load_and_run(str(context["root"]), mode=GateMode.DISTRIBUTION)


def _unverifiable_for(report, source: str, target: str) -> bool:
    return any(
        source in f.subjects and target in f.subjects
        for f in report.findings_for_check("unverifiable-legacy")
    )


@scenario(
    FEATURE,
    "a supersedes edge to a target file with no YAML frontmatter is reported "
    "unverifiable-legacy, not dangling or asymmetric",
)
def test_unverifiable_legacy_supersede() -> None: ...


@given(
    "a corpus root directory containing a pdr file whose frontmatter declares "
    "supersedes: [pdr-032]"
)
def _given_pdr_supersedes_legacy(context: dict, tmp_path: Path) -> None:
    root = tmp_path / "corpus"
    _write(
        root / "pdrs" / "pdr-500.md",
        _doc(
            [
                "type: pdr",
                "id: pdr-500",
                "title: The superseding decision",
                "status: proposed",
                "created: 2026-07-01",
                "updated: 2026-07-01",
                "authors: [alice]",
                "description: supersedes a legacy record",
                "decision-makers: [alice]",
                "derives-from: []",
                "supersedes: [pdr-032]",
            ]
        ),
    )
    context["root"] = root
    context["source"] = "pdr-500"
    context["legacy"] = "pdr-032"


@given(
    "a file named pdr-032 present in the corpus root directory carrying no YAML "
    "frontmatter at all"
)
def _given_legacy_file(context: dict) -> None:
    root = context["root"]
    _write(root / "pdr-032.md", "# PDR-032 (legacy)\n\nA decision recorded before the frontmatter convention.\n")


@then(
    "it reports the edge as an unverifiable-legacy finding naming the pdr and "
    "pdr-032 by id"
)
def _then_unverifiable_legacy(context: dict) -> None:
    report = context["report"]
    assert _unverifiable_for(report, context["source"], context["legacy"]), (
        "expected an unverifiable-legacy finding naming "
        f"{context['source']} and {context['legacy']}"
    )


@then(
    "it reports no dangling-edge finding for that edge, because pdr-032 resolves "
    "to a real file"
)
def _then_no_dangling_for_legacy(context: dict) -> None:
    report = context["report"]
    for finding in report.findings_for_check("dangling-edge"):
        assert context["legacy"] not in finding.subjects, (
            f"unexpected dangling-edge finding for legacy target: {finding}"
        )


@then(
    "it reports no asymmetric-supersede finding for that edge, because pdr-032 "
    "has no frontmatter that could carry a superseded-by field"
)
def _then_no_asymmetric_for_legacy(context: dict) -> None:
    report = context["report"]
    for finding in report.findings_for_check("asymmetric-supersede"):
        assert context["legacy"] not in finding.subjects, (
            f"unexpected asymmetric-supersede finding for legacy target: {finding}"
        )


@then(
    "the unverifiable-legacy finding does not by itself drive the aggregate "
    "verdict non-zero"
)
def _then_unverifiable_advisory(context: dict) -> None:
    # Under distribution mode (where blocking findings veto), the corpus still
    # exits zero: the unverifiable-legacy finding is advisory.
    assert _distribution_report(context).exit_code == 0


# --- Behavior 5: current-state incorporates naming legacy decisions ----------


@scenario(
    FEATURE,
    "a current-state incorporates claim naming a legacy decision is reported "
    "unverifiable-legacy, not as an unincorporated-decision violation",
)
def test_current_state_incorporates_legacy() -> None: ...


@given(
    "a corpus root directory containing a current-state.md file whose frontmatter "
    "declares incorporates: [pdr-032, pdr-033, adr-059]"
)
def _given_current_state_incorporates(context: dict, tmp_path: Path) -> None:
    root = tmp_path / "corpus"
    _write(
        root / "current-state.md",
        _doc(
            [
                "type: current-state",
                "id: current-state-001",
                "title: The living record",
                "status: current",
                "created: 2026-07-01",
                "updated: 2026-07-01",
                "authors: [alice]",
                "description: the settled decisions",
                "incorporates: [pdr-032, pdr-033, adr-059]",
            ]
        ),
    )
    context["root"] = root
    context["cs_id"] = "current-state-001"
    context["legacy_targets"] = ["pdr-032", "pdr-033", "adr-059"]


@given(
    "pdr-032, pdr-033, and adr-059 are each present in the corpus root directory "
    "as files carrying no YAML frontmatter"
)
def _given_three_legacy_files(context: dict) -> None:
    root = context["root"]
    for legacy in context["legacy_targets"]:
        _write(root / f"{legacy}.md", f"# {legacy} (legacy)\n\nA decision recorded before the frontmatter convention.\n")


@then(
    "it reports each of the three incorporates edges as an unverifiable-legacy "
    "finding naming current-state and the legacy target by id"
)
def _then_three_unverifiable(context: dict) -> None:
    report = context["report"]
    for target in context["legacy_targets"]:
        assert _unverifiable_for(report, context["cs_id"], target), (
            f"expected an unverifiable-legacy finding naming "
            f"{context['cs_id']} and {target}"
        )


@then(
    "it reports no unincorporated-decision finding for any of the three, because "
    "their accepted status cannot yet be machine-read"
)
def _then_no_unincorporated(context: dict) -> None:
    report = context["report"]
    targets = set(context["legacy_targets"])
    for finding in report.findings_for_check("unincorporated-decision"):
        assert not (targets & set(finding.subjects)), (
            f"unexpected unincorporated-decision finding for a legacy target: {finding}"
        )


@then(
    "none of the three unverifiable-legacy findings by themselves drive the "
    "aggregate verdict non-zero"
)
def _then_three_advisory(context: dict) -> None:
    assert _distribution_report(context).exit_code == 0
