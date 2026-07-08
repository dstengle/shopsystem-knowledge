"""Step definitions for the idempotent-regeneration / check-mode outer-loop scenario.

Binds @scenario_hash:9feadfd3e1a0efad — "regeneration over an unchanged source
is idempotent and the check mode reports no drift" — and asserts both Then/And
legs:

* regenerating the projections and index over an unchanged source writes zero
  changed bytes (the already-materialized outputs already match the manifest
  the source would generate, so nothing is rewritten); and
* running the generation in check mode over the unchanged source reports no
  drift and exits with a success status.

The scenario builds on the pure ``generate_corpus`` byte manifest: this
sub-issue adds a filesystem materialization entry point (``write_corpus``) and
a check mode (``check_corpus``) on top of that manifest, rather than re-deriving
the layout.

RED leg: neither ``write_corpus`` nor ``check_corpus`` exists yet, so both are
imported inside the step bodies — the scenario fails at the step that first
needs the behaviour (the Given, which materializes the corpus once), not at
collection/import time. The GREEN leg adds both entry points and makes every
leg pass.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "corpus"


@pytest.fixture
def context() -> dict:
    return {}


@scenario(
    "idempotent_regeneration.feature",
    "regeneration over an unchanged source is idempotent and the check mode reports no drift",
)
def test_idempotent_regeneration() -> None:
    """Outer-loop binding; step bodies below carry the assertions."""


@given("a decision corpus whose projections and index have already been generated")
def _already_generated(context: dict, tmp_path: Path) -> None:
    # Imported here (not at module top) so the RED commit fails at this step on
    # the absent behaviour, not on a collection-time ImportError.
    from knowledge.projections import write_corpus

    sources = {
        path.stem: path.read_text(encoding="utf-8")
        for path in sorted(FIXTURE_DIR.glob("*.md"))
    }
    # Guard the corpus's own preconditions so a later fixture edit cannot
    # silently weaken the scenario: at least two conforming documents, each with
    # frontmatter and a recognized decision heading.
    assert len(sources) >= 2, "corpus must carry at least two documents"
    for name, src in sources.items():
        assert src.startswith("---\n"), f"{name} must open with YAML frontmatter"
        assert (
            "## Decision" in src or "## Decision Outcome" in src
        ), f"{name} body must carry a recognized decision heading"

    out_dir = tmp_path / "corpus-out"

    # First materialization: from an empty output dir, every manifest path is
    # written, so the initial regeneration reports a non-empty changed set.
    initial = write_corpus(sources, out_dir)
    assert initial.changed_count > 0, "initial generation must write the manifest"

    context["corpus"] = sources
    context["out_dir"] = out_dir


@when("the knowledge context regenerates the projections and index over the unchanged source")
def _regenerate_unchanged(context: dict) -> None:
    from knowledge.projections import write_corpus

    context["regen"] = write_corpus(context["corpus"], context["out_dir"])


@then("the regeneration writes zero changed bytes")
def _zero_changed_bytes(context: dict) -> None:
    regen = context["regen"]
    assert regen.changed_count == 0, (
        "regeneration over an unchanged source must rewrite nothing; "
        f"changed paths: {regen.changed_paths!r}"
    )
    assert regen.changed_paths == (), "no path may be reported as changed"


@then(
    "running the generation in check mode over the unchanged source reports no "
    "drift and exits with a success status"
)
def _check_mode_no_drift(context: dict) -> None:
    from knowledge.projections import check_corpus

    result = check_corpus(context["corpus"], context["out_dir"])
    assert result.has_drift is False, f"check mode reported drift: {result.drift!r}"
    assert result.drift == (), "no drifted path may be reported"
    assert result.exit_code == 0, "check mode over an unchanged source must exit success (0)"
