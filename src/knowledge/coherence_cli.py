"""The ``shop-knowledge-gate`` command: run the coherence gate over a corpus root.

This is the lead-installable contract command. An operator points it at a corpus
*root directory*; it loads the tree with
:func:`knowledge.corpus_loader.load_corpus`, runs the already-pinned lifecycle
and typed-edge checks through :func:`knowledge.coherence.run_coherence_gate`,
prints each finding in doctor form, and exits with the report's verdict.

The command defaults to **authoring** mode — the already-pinned authoring-mode
contract, where the gate warns and never blocks — so a run made while drafting
surfaces guidance without vetoing. ``--mode distribution`` opts into the
blocking verdict.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from typing import BinaryIO, Sequence

from knowledge.coherence import (
    CoherenceConfig,
    CoherenceReport,
    GateMode,
    LIFECYCLE_CHECKS,
    run_coherence_gate,
)
from knowledge.corpus_loader import load_corpus
from knowledge.typed_edges import TYPED_EDGE_CHECKS

# The gate runs every already-pinned check over the loaded corpus: the
# artifact-lifecycle registry and the typed-edge registry, folded through the
# one aggregate verdict.
GATE_CHECKS = LIFECYCLE_CHECKS + TYPED_EDGE_CHECKS


def load_and_run(root: str, mode: GateMode = GateMode.AUTHORING) -> CoherenceReport:
    """Load the corpus at ``root`` and run the gate over it under ``mode``.

    The mode defaults to :attr:`GateMode.AUTHORING`, matching the installed
    command's default: the gate warns and never blocks unless the operator opts
    into distribution mode.
    """
    corpus = load_corpus(root)
    config = CoherenceConfig(reference_date=date.today())
    return run_coherence_gate(corpus, config, mode=mode, checks=GATE_CHECKS)


def _render_finding(report: CoherenceReport, finding) -> str:
    """Render one finding in doctor form under the report's mode."""
    status = report.reported_status(finding).value.upper()
    return (
        f"[{status}] {finding.check_id} ({finding.check_name}): {finding.message}\n"
        f"    remediation: {finding.remediation}"
    )


def main(
    argv: Sequence[str] | None = None,
    stdout: BinaryIO | None = None,
    stderr: BinaryIO | None = None,
) -> int:
    """Run the gate command over ``argv``; return the report's exit code."""
    out = stdout if stdout is not None else sys.stdout.buffer
    err = stderr if stderr is not None else sys.stderr.buffer

    parser = argparse.ArgumentParser(
        prog="shop-knowledge-gate",
        description="Run the coherence gate over a corpus root directory.",
    )
    parser.add_argument("root", help="the corpus root directory to walk")
    parser.add_argument(
        "--mode",
        choices=[m.value for m in GateMode],
        default=GateMode.AUTHORING.value,
        help="gate mode (default: authoring — warn and never block)",
    )
    try:
        args = parser.parse_args(list(argv) if argv is not None else None)
    except SystemExit as exc:  # argparse already wrote usage to its own stderr
        return int(exc.code) if exc.code is not None else 2

    report = load_and_run(args.root, mode=GateMode(args.mode))

    lines = [_render_finding(report, f) for f in report.findings]
    if not lines:
        lines = ["no coherence findings"]
    lines.append(f"aggregate verdict: exit {report.exit_code} (mode {report.mode.value})")
    out.write(("\n".join(lines) + "\n").encode("utf-8"))
    return report.exit_code


def run() -> int:
    """Console-script entry point: drive :func:`main` over ``sys.argv``."""
    return main()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(run())
