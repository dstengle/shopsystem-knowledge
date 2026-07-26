"""Step definitions for the navigate read verb on the shop-knowledge CLI.

Binds the pinned scenarios in ``cli_navigate.feature``. ``navigate`` is a
net-new read verb over the ``shop-knowledge`` CLI: given a corpus root and a
document id, it answers that document's *edge-neighbourhood* — every edge
incident on the document, read from the document's **own** materialized
frontmatter link fields (its forward edges and the back-edges materialized on
it), each listed as a link-field, target id, and resolved flag, with each
resolved neighbour's id / type / status / title surfaced.

The CLI is exercised **in-process**, mirroring ``test_shop_knowledge_cli.py``:
each scenario drives ``knowledge.cli.main`` with an explicit argv and captures
the exit code plus the raw stdout/stderr bytes. The neighbourhood is emitted as
a JSON object on stdout::

    {"id": "adr-068",
     "edges": [{"link_field": "supersedes", "target": "adr-060",
                "resolved": true,
                "neighbour": {"id": "adr-060", "type": "adr",
                              "status": "superseded", "title": "..."}},
               ...]}

so a scenario can assert the record shape (link-field / target / resolved plus
the neighbour facets) structurally rather than by string-scraping.

The fixture is built so the "answered from the document's own frontmatter
without scanning the corpus for inbound edges" leg is *provable*: adr-068
carries a materialized ``referenced-by`` back-edge naming adr-080 (which itself
declares NO forward edge back to adr-068), while a separate adr-090 declares a
forward ``references`` edge naming adr-068 but is NOT named in adr-068's own
frontmatter. A frontmatter-only answer therefore MUST include adr-080 and MUST
NOT include adr-090; a whole-corpus inbound scan would do the opposite.
"""

from __future__ import annotations

import io
import json
from pathlib import Path

import pytest
import yaml
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "cli_navigate.feature"

# The document the neighbourhood scenario navigates from, and the two probes
# that pin the frontmatter-only (no inbound-scan) property.
SUBJECT_ID = "adr-068"
# Reachable ONLY via adr-068's own materialized referenced-by back-edge; it
# declares no forward edge back to adr-068.
BACKEDGE_ONLY_NEIGHBOUR = "adr-080"
# Declares a forward references edge naming adr-068 but is NOT named in
# adr-068's frontmatter; a frontmatter-only answer must omit it.
INBOUND_SCAN_DISTRACTOR = "adr-090"

# The edge-neighbourhood adr-068's own frontmatter declares, across the three
# edge pairs (supersedes/superseded-by, derives-from/derived-by,
# references/referenced-by): (link_field, target, expected neighbour facets).
NEIGHBOURS: dict[str, dict[str, str]] = {
    "adr-060": {"type": "adr", "status": "superseded", "title": "Superseded predecessor"},
    "adr-050": {"type": "adr", "status": "accepted", "title": "Derivation base"},
    "adr-070": {"type": "adr", "status": "accepted", "title": "Referenced note"},
    BACKEDGE_ONLY_NEIGHBOUR: {"type": "adr", "status": "accepted", "title": "Back-edge consumer"},
}
EXPECTED_EDGES: set[tuple[str, str]] = {
    ("supersedes", "adr-060"),
    ("derives-from", "adr-050"),
    ("references", "adr-070"),
    ("referenced-by", BACKEDGE_ONLY_NEIGHBOUR),
}


@pytest.fixture
def context() -> dict:
    return {}


def _write_doc(root: Path, doc_id: str, *, status: str, title: str, **edges: object) -> None:
    """Write an ``adr`` document with YAML frontmatter into ``<root>/adrs/``.

    Non-empty frontmatter makes it a typed artifact to
    :func:`knowledge.corpus_loader.load_corpus`; ``edges`` supply the link
    fields (``supersedes``, ``referenced-by``, ...) that form the graph.
    """
    frontmatter: dict[str, object] = {
        "type": "adr",
        "id": doc_id,
        "title": title,
        "status": status,
    }
    frontmatter.update(edges)
    source = "---\n" + yaml.safe_dump(frontmatter, sort_keys=False) + "---\n\n## Context\n\nBody.\n"
    (root / "adrs").mkdir(parents=True, exist_ok=True)
    (root / "adrs" / f"{doc_id}.md").write_text(source, encoding="utf-8")


def _build_corpus_root(root: Path) -> None:
    """Materialize the navigate fixture corpus under ``root``.

    adr-068 carries materialized edges across the three edge pairs, including a
    referenced-by back-edge to adr-080; adr-080 declares no forward edge back to
    adr-068, and adr-090 declares a forward references edge to adr-068 while
    being absent from adr-068's own frontmatter.
    """
    _write_doc(
        root,
        SUBJECT_ID,
        status="accepted",
        title="Neighbourhood subject",
        **{
            "supersedes": ["adr-060"],
            "derives-from": ["adr-050"],
            "references": ["adr-070"],
            "referenced-by": [BACKEDGE_ONLY_NEIGHBOUR],
        },
    )
    _write_doc(root, "adr-060", status="superseded", title="Superseded predecessor",
               **{"superseded-by": [SUBJECT_ID]})
    _write_doc(root, "adr-050", status="accepted", title="Derivation base")
    _write_doc(root, "adr-070", status="accepted", title="Referenced note")
    # Reachable only via adr-068's referenced-by back-edge; no forward edge back.
    _write_doc(root, BACKEDGE_ONLY_NEIGHBOUR, status="accepted", title="Back-edge consumer")
    # Forward-references adr-068 but is not named in adr-068's frontmatter.
    _write_doc(root, INBOUND_SCAN_DISTRACTOR, status="accepted", title="Forward referencer",
               **{"references": [SUBJECT_ID]})


def _run_navigate(context: dict, doc_id: str) -> None:
    from knowledge.cli import main

    out, err = io.BytesIO(), io.BytesIO()
    rc = main(["navigate", doc_id, "--corpus", str(context["root"])], stdout=out, stderr=err)
    context["exit"] = rc
    context["stdout"] = out.getvalue()
    context["stderr"] = err.getvalue()


def _payload(context: dict) -> dict:
    """Parse the navigate JSON payload from stdout (asserting a clean run first)."""
    assert context["exit"] == 0, (
        f"expected navigate to exit 0; got {context['exit']} "
        f"(stderr: {context['stderr']!r})"
    )
    return json.loads(context["stdout"].decode("utf-8"))


# --- Scenario bindings -------------------------------------------------------


@scenario(FEATURE, "navigate returns the edge-neighbourhood of a document from its materialized frontmatter edges")
def test_navigate_neighbourhood() -> None: ...


@scenario(FEATURE, "navigate on an unknown document id fails and names the offending id")
def test_navigate_unknown_id() -> None: ...


# --- Given -------------------------------------------------------------------


@given(parsers.re(r'a corpus whose document "(?P<doc_id>[^"]+)" carries materialized edges to several neighbours across the three edge pairs'))
def _corpus_with_subject(context: dict, tmp_path: Path, doc_id: str) -> None:
    root = tmp_path / "corpus"
    _build_corpus_root(root)
    context["root"] = root

    # Fixture invariants that make the no-inbound-scan leg provable.
    from knowledge.corpus_loader import load_corpus
    from knowledge.typed_edges import _link_targets

    corpus = load_corpus(root)
    context["corpus"] = corpus
    backedge = corpus.get(BACKEDGE_ONLY_NEIGHBOUR)
    assert backedge is not None
    assert SUBJECT_ID not in _link_targets(backedge, "references"), (
        "fixture invariant: the back-edge-only neighbour must declare NO forward "
        "references edge to the subject, so it is reachable only via the subject's "
        "own referenced-by frontmatter"
    )
    distractor = corpus.get(INBOUND_SCAN_DISTRACTOR)
    assert distractor is not None
    assert SUBJECT_ID in _link_targets(distractor, "references"), (
        "fixture invariant: the distractor must forward-reference the subject, so a "
        "whole-corpus inbound scan (which navigate must NOT do) would surface it"
    )


@given(parsers.re(r'a corpus that contains no document with id "(?P<doc_id>[^"]+)"'))
def _corpus_without_id(context: dict, tmp_path: Path, doc_id: str) -> None:
    root = tmp_path / "corpus"
    _build_corpus_root(root)
    context["root"] = root

    from knowledge.corpus_loader import load_corpus

    corpus = load_corpus(root)
    assert corpus.get(doc_id) is None, f"fixture invariant: {doc_id} must be absent"


# --- When --------------------------------------------------------------------


@when(parsers.re(r'I run the navigate verb on document id "(?P<doc_id>[^"]+)"'))
def _run_verb(context: dict, doc_id: str) -> None:
    _run_navigate(context, doc_id)


# --- Then --------------------------------------------------------------------


@then(parsers.re(r'the output lists each edge incident on "(?P<doc_id>[^"]+)" as a link-field, target id, and resolved flag'))
def _lists_incident_edges(context: dict, doc_id: str) -> None:
    payload = _payload(context)
    assert payload.get("id") == doc_id, f"payload id is not {doc_id}: {payload!r}"
    edges = payload.get("edges")
    assert isinstance(edges, list) and edges, f"expected a non-empty edges list, got {edges!r}"

    seen: set[tuple[str, str]] = set()
    for edge in edges:
        assert set(("link_field", "target", "resolved")).issubset(edge), (
            f"edge record missing link-field/target/resolved: {edge!r}"
        )
        assert isinstance(edge["resolved"], bool), f"resolved flag is not a bool: {edge!r}"
        seen.add((edge["link_field"], edge["target"]))

    assert seen == EXPECTED_EDGES, (
        f"the listed incident edges do not match {doc_id}'s own frontmatter edges; "
        f"expected {sorted(EXPECTED_EDGES)}, got {sorted(seen)}"
    )


@then("each listed neighbour carries its id, type, status, and title")
def _neighbour_facets(context: dict) -> None:
    payload = _payload(context)
    by_target = {edge["target"]: edge for edge in payload["edges"]}
    for target, facts in NEIGHBOURS.items():
        edge = by_target.get(target)
        assert edge is not None, f"no listed edge to neighbour {target}"
        assert edge["resolved"] is True, f"neighbour {target} should resolve: {edge!r}"
        neighbour = edge.get("neighbour")
        assert isinstance(neighbour, dict), f"edge to {target} carries no neighbour facets: {edge!r}"
        assert neighbour.get("id") == target, f"neighbour id mismatch: {neighbour!r}"
        assert neighbour.get("type") == facts["type"], f"neighbour type mismatch for {target}: {neighbour!r}"
        assert neighbour.get("status") == facts["status"], f"neighbour status mismatch for {target}: {neighbour!r}"
        assert neighbour.get("title") == facts["title"], f"neighbour title mismatch for {target}: {neighbour!r}"


@then(parsers.re(r'the neighbourhood is answered from "(?P<doc_id>[^"]+)"\'s own frontmatter without scanning the corpus for inbound edges'))
def _answered_from_frontmatter(context: dict, doc_id: str) -> None:
    payload = _payload(context)
    targets = {edge["target"] for edge in payload["edges"]}

    # The materialized back-edge target — reachable only via the subject's own
    # frontmatter — MUST be present.
    assert BACKEDGE_ONLY_NEIGHBOUR in targets, (
        f"the materialized referenced-by back-edge to {BACKEDGE_ONLY_NEIGHBOUR} is "
        f"missing; the neighbourhood must be read from {doc_id}'s own frontmatter"
    )
    # The forward-referencer absent from the subject's frontmatter MUST be
    # absent — a whole-corpus inbound scan would wrongly include it.
    assert INBOUND_SCAN_DISTRACTOR not in targets, (
        f"{INBOUND_SCAN_DISTRACTOR} forward-references {doc_id} but is not named in "
        f"{doc_id}'s frontmatter; its presence proves the answer scanned the corpus "
        f"for inbound edges instead of reading {doc_id}'s own frontmatter"
    )
    # And the neighbourhood is exactly the subject's own frontmatter edge set.
    assert targets == {target for _field, target in EXPECTED_EDGES}, (
        f"the neighbourhood targets do not equal {doc_id}'s own frontmatter edge "
        f"targets: {sorted(targets)}"
    )


@then("the exit code is non-zero")
def _exit_nonzero(context: dict) -> None:
    assert context["exit"] != 0, f"expected a non-zero exit code, got {context['exit']}"


@then(parsers.re(r'stderr names "(?P<doc_id>[^"]+)" as a document id not present in the corpus'))
def _stderr_names_unknown_id(context: dict, doc_id: str) -> None:
    stderr = context["stderr"].decode("utf-8")
    assert doc_id in stderr, (
        f"stderr does not name the offending document id {doc_id!r}: {stderr!r}"
    )
    assert "corpus" in stderr.lower(), (
        f"stderr does not frame {doc_id!r} as absent from the corpus: {stderr!r}"
    )
