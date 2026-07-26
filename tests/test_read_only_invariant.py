"""Step definitions for the read-only invariant over the three read verbs.

Binds the pinned Scenario Outline in ``read_only_invariant.feature``. The three
read verbs over the ``shop-knowledge`` CLI — ``navigate``, ``render``, and
``query`` — are all pure reads: each :func:`~knowledge.corpus_loader.load_corpus`
over a corpus root, projects an answer, and emits it, never writing an artifact
file or altering the materialized frontmatter link-field graph. This invariant
pins that read-only contract across all three verbs at once.

The scenario is a Scenario Outline over the three verbs. Each example:

* builds a single fixture corpus on disk and records, **before the run**, every
  artifact file's exact bytes and the corpus's materialized frontmatter edge set
  (:func:`~knowledge.typed_edges.resolve_edges` over
  :func:`~knowledge.corpus_loader.load_corpus`);
* runs the named verb with a **valid, work-doing** invocation — navigate on a
  present id, render on an accepted id under the current-system view, query on a
  matching facet — so the verb runs its full read path rather than bailing on an
  argument error;
* asserts exit 0, that every artifact file on disk is byte-for-byte unchanged,
  and that the materialized frontmatter edge set is exactly as recorded (none
  added, removed, or altered).

The CLI is exercised **in-process**, mirroring ``test_cli_navigate.py`` /
``test_cli_render.py`` / ``test_cli_query.py``: each verb drives
``knowledge.cli.main`` with an explicit argv and captures the exit code plus the
raw stdout/stderr bytes.
"""

from __future__ import annotations

import io
from pathlib import Path

import pytest
import yaml
from pytest_bdd import given, parsers, scenario, then, when

from knowledge.cli import main
from knowledge.corpus_loader import load_corpus
from knowledge.typed_edges import Edge, resolve_edges

FEATURE = "read_only_invariant.feature"

# The subject the navigate/render invocations name, and a neighbour it links to
# so the corpus carries real materialized frontmatter edges to leave unchanged.
SUBJECT_ID = "adr-068"
NEIGHBOUR_ID = "adr-070"


@pytest.fixture
def context() -> dict:
    return {}


def _write_adr(
    root: Path, doc_id: str, *, status: str, title: str, body: str, **edges: object
) -> None:
    """Write an ``adr`` document with YAML frontmatter into ``<root>/adrs/``.

    Non-empty frontmatter makes it a typed artifact to
    :func:`knowledge.corpus_loader.load_corpus`; ``edges`` supply the link fields
    (``references``, ``referenced-by``, ...) that form the materialized edge
    graph the read verbs read and this invariant pins unchanged.
    """
    frontmatter: dict[str, object] = {
        "type": "adr",
        "id": doc_id,
        "title": title,
        "status": status,
    }
    frontmatter.update(edges)
    source = (
        "---\n"
        + yaml.safe_dump(frontmatter, sort_keys=False)
        + "---\n\n"
        + body
    )
    (root / "adrs").mkdir(parents=True, exist_ok=True)
    (root / "adrs" / f"{doc_id}.md").write_text(source, encoding="utf-8")


def _build_corpus_root(root: Path) -> None:
    """Materialize the read-only-invariant fixture corpus under ``root``.

    Two accepted ``adr`` documents joined by a reciprocal references edge, each
    with body content, so every verb has real work to do: navigate reads
    ``adr-068``'s incident edges, render projects ``adr-068``'s accepted content
    under the current-system view, and query selects both documents on
    ``type == adr``.
    """
    _write_adr(
        root,
        SUBJECT_ID,
        status="accepted",
        title="Read-only invariant subject",
        body="## Context\n\nSubject context.\n\n## Decision\n\nSubject decision.\n",
        **{"references": [NEIGHBOUR_ID]},
    )
    _write_adr(
        root,
        NEIGHBOUR_ID,
        status="accepted",
        title="Referenced neighbour",
        body="## Context\n\nNeighbour context.\n",
        **{"referenced-by": [SUBJECT_ID]},
    )


def _snapshot_files(root: Path) -> dict[str, bytes]:
    """Every file under ``root`` mapped from its relative path to its exact bytes."""
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _snapshot_edges(root: Path) -> frozenset[Edge]:
    """The corpus's materialized frontmatter edge set, loaded fresh from ``root``."""
    return frozenset(resolve_edges(load_corpus(root)))


# The valid, work-doing invocation each verb runs over the fixture corpus.
def _argv_for(verb: str, root: str) -> list[str]:
    if verb == "navigate":
        return ["navigate", SUBJECT_ID, "--corpus", root]
    if verb == "render":
        return ["render", SUBJECT_ID, "--corpus", root, "--view", "current-system"]
    if verb == "query":
        return ["query", "--corpus", root, "--facet", "type", "--value", "adr"]
    raise AssertionError(f"unexpected verb {verb!r}")  # pragma: no cover


# --- Scenario binding --------------------------------------------------------


@scenario(FEATURE, "every read verb leaves the corpus artifacts and edges unchanged")
def test_read_verbs_leave_corpus_unchanged() -> None: ...


# --- Given -------------------------------------------------------------------


@given("a corpus whose artifact files and materialized frontmatter edges are recorded before the run")
def _corpus_recorded(context: dict, tmp_path: Path) -> None:
    root = tmp_path / "corpus"
    _build_corpus_root(root)
    context["root"] = root
    context["files_before"] = _snapshot_files(root)
    context["edges_before"] = _snapshot_edges(root)

    # Fixture invariant: the recorded edge set is non-empty, so "no edge added,
    # removed, or altered" is a meaningful assertion rather than vacuous.
    assert context["edges_before"], "fixture invariant: the corpus must carry materialized edges"


# --- When --------------------------------------------------------------------


@when(parsers.re(r'I run the "(?P<verb>[^"]+)" verb over that corpus'))
def _run_verb(context: dict, verb: str) -> None:
    out, err = io.BytesIO(), io.BytesIO()
    rc = main(_argv_for(verb, str(context["root"])), stdout=out, stderr=err)
    context["exit"] = rc
    context["stdout"] = out.getvalue()
    context["stderr"] = err.getvalue()


# --- Then --------------------------------------------------------------------


@then("the exit code is 0")
def _exit_zero(context: dict) -> None:
    assert context["exit"] == 0, (
        f"expected the read verb to exit 0; got {context['exit']} "
        f"(stderr: {context['stderr']!r})"
    )


@then("every artifact file on disk is byte-for-byte unchanged after the run")
def _files_unchanged(context: dict) -> None:
    after = _snapshot_files(context["root"])
    before = context["files_before"]
    assert set(after) == set(before), (
        "the set of files on disk changed across the run: "
        f"added {sorted(set(after) - set(before))}, "
        f"removed {sorted(set(before) - set(after))}"
    )
    for rel, data in before.items():
        assert after[rel] == data, (
            f"artifact file {rel!r} was not byte-for-byte unchanged across the run"
        )


@then("no materialized frontmatter edge has been added, removed, or altered")
def _edges_unchanged(context: dict) -> None:
    after = _snapshot_edges(context["root"])
    before = context["edges_before"]
    assert after == before, (
        "the corpus's materialized frontmatter edges changed across the run: "
        f"added {sorted(after - before)}, removed {sorted(before - after)}"
    )
