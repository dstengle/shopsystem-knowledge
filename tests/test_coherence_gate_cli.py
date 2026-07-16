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
