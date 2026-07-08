"""Step definitions for the authoring-time discovery outer-loop scenario.

Binds @scenario_hash:60f070ecddc891e5 — "the authoring event triggers discovery
and surfaces the relevant neighbours via the L0/L1 index" — the FIRST behaviour
of the authoring_discovery family and the primary coherence mechanism the
verdict / covered / contradict / supersede passes build on.

The scenario pins two observable properties of the discovery pass:

* **(i) relevant subset, named by id.** Given a corpus of existing decisions and
  a draft authored on a topic that overlaps only a *subset* of them, the pass
  surfaces exactly that subset — each neighbour named by id — and excludes the
  decision whose topic does not overlap the draft.

* **(ii) index-not-whole-corpus.** The pass selects those neighbours from the
  L0/L1 index (each existing decision's L0 card + L1 extract) rather than loading
  the whole corpus (the L2 bodies) into the pass. This is asserted concretely:
  the entry point consumes only ``(index, draft)``; the index it consumes carries
  L0/L1 material but provably none of the L2-only body text; and neither the
  index entries nor the surfaced neighbours expose an L2 attribute. Each surfaced
  neighbour still carries enough (id + L0 card + L1 extract) for a downstream
  adversarial pass to cite it by id without re-loading the whole corpus.

RED leg: the ``knowledge.discovery`` module does not yet exist, so it is imported
inside the ``When`` step body — the scenario fails at that step on the absent
behaviour (ImportError), not at collection/import time.
"""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from knowledge.projections import generate_projections

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "discovery_corpus"

# The subset of the corpus whose topic (a read-through cache over the projection
# index) overlaps the draft, and the decision whose topic (on-call pager
# rotation) does not overlap the draft at all.
RELEVANT_IDS = ("ADR-0021", "ADR-0022")
IRRELEVANT_ID = "ADR-0030"

# Distinctive sentences that appear ONLY in each relevant decision's L2 body (its
# "## Consequences" section) — never in its L0 card (frontmatter) or its L1
# extract (the "## Decision" section). If any of these leaks into the index the
# pass consumes, the index would be carrying whole-corpus L2 bodies rather than
# just L0/L1 material.
L2_ONLY_MARKERS = (
    "Hot lookups become cheap",
    "The cache never serves an entry",
)


@pytest.fixture
def context() -> dict:
    return {}


@scenario(
    "authoring_time_discovery.feature",
    "the authoring event triggers discovery and surfaces the relevant "
    "neighbours via the L0/L1 index",
)
def test_authoring_time_discovery() -> None:
    """Outer-loop binding; step bodies below carry the assertions."""


@given("a corpus of existing decisions with generated L0 cards and L1 extracts")
def _existing_corpus(context: dict) -> None:
    # The raw source corpus. Nothing here imports the discovery module: the
    # index (L0 cards + L1 extracts) is generated inside the When step so the RED
    # commit fails on the absent discovery behaviour, not on assembling inputs.
    sources = {
        path.stem: path.read_text(encoding="utf-8")
        for path in sorted(FIXTURE_DIR.glob("*.md"))
    }

    # Precompute the expected L0/L1 material per document straight from the
    # single-source generator, so the neighbour assertions can pin the surfaced
    # L1 extract to the verbatim decision-section text a downstream pass needs.
    expected = {}
    for doc_id, source in sources.items():
        bundle = generate_projections(source)
        expected[bundle.l0.id] = bundle

    # Guard the corpus's preconditions so a later fixture edit cannot quietly
    # weaken the scenario: the relevant subset and the irrelevant decision must
    # all be present and distinct.
    ids = {bundle.l0.id for bundle in expected.values()}
    assert set(RELEVANT_IDS) <= ids, f"relevant subset missing from corpus: {ids}"
    assert IRRELEVANT_ID in ids, f"irrelevant decision missing from corpus: {ids}"

    context["sources"] = sources
    context["expected"] = expected


@given(
    "a draft decision being authored on a topic that overlaps a subset of "
    "those decisions"
)
def _draft_decision(context: dict) -> None:
    # A draft on the projection-index caching topic: it shares topic tokens with
    # ADR-0021 / ADR-0022 (cache / projection / index) and none with the on-call
    # rotation decision. Stored as raw fields; the DraftDecision value object is
    # constructed inside the When step (from the discovery module under test).
    context["draft_fields"] = {
        "id": "DRAFT-cache-warming",
        "title": "Warm the projection index cache on startup",
        "description": (
            "Prime the read-through projection cache at startup so the first "
            "lookup of the projection index does not pay the regeneration cost."
        ),
        "body": (
            "## Decision\n\n"
            "Warm the projection index cache during startup by populating the "
            "read-through cache from the freshly generated index.\n"
        ),
    }


@when("the knowledge context runs the authoring-time discovery pass over the draft")
def _run_discovery(context: dict) -> None:
    # Imported HERE (not at module top): the RED commit fails at this step on the
    # absent knowledge.discovery module, not at collection time.
    from knowledge.discovery import (
        DraftDecision,
        build_l0l1_index,
        run_authoring_discovery,
    )

    # The index is built from the corpus's L0/L1 material only. build_l0l1_index
    # is the boundary that drops the L2 bodies: the pass downstream never receives
    # the raw source corpus.
    index = build_l0l1_index(context["sources"])
    draft = DraftDecision(**context["draft_fields"])

    context["index"] = index
    context["draft"] = draft
    context["run_signature"] = inspect.signature(run_authoring_discovery)
    context["result"] = run_authoring_discovery(index, draft)


@then(
    "it surfaces the subset of existing decisions relevant to the draft, "
    "named by id"
)
def _surfaces_relevant_subset(context: dict) -> None:
    result = context["result"]

    surfaced_ids = tuple(neighbour.id for neighbour in result.neighbours)

    # (i) exactly the overlapping subset is surfaced, each named by id...
    assert set(surfaced_ids) == set(RELEVANT_IDS), (
        f"discovery must surface exactly the relevant subset {RELEVANT_IDS}, "
        f"got {surfaced_ids}"
    )
    # ...and the non-overlapping decision is excluded.
    assert IRRELEVANT_ID not in surfaced_ids, (
        f"the non-overlapping decision {IRRELEVANT_ID} must NOT be surfaced, "
        f"got {surfaced_ids}"
    )
    # A convenience id accessor exposes the same subset for downstream callers.
    assert set(result.ids()) == set(RELEVANT_IDS)

    # Each surfaced neighbour is named by id and carries an explainable,
    # non-empty overlap signal — the shared topic tokens that made it relevant.
    for neighbour in result.neighbours:
        assert neighbour.id in RELEVANT_IDS
        assert neighbour.overlap, (
            f"neighbour {neighbour.id} must carry the shared topic tokens that "
            "explain why it is relevant"
        )


@then(
    "it selects those neighbours from the L0/L1 index rather than loading the "
    "whole corpus into the pass"
)
def _selects_from_l0l1_index(context: dict) -> None:
    index = context["index"]
    result = context["result"]

    # (ii-a) The entry point consumes ONLY the index + the draft — it takes no
    # corpus/sources/l2 parameter, so it structurally cannot load the whole
    # corpus into the pass.
    params = list(context["run_signature"].parameters)
    assert params == ["index", "draft"], (
        "the discovery pass must consume only (index, draft); a corpus/sources "
        f"parameter would let it load the whole corpus, got {params}"
    )

    # (ii-b) The index the pass consumes carries L0/L1 material but provably NONE
    # of the L2-only body text. Gather every string reachable from the index's
    # entries and assert no L2-only marker leaked in.
    index_text = "\n".join(
        "\n".join(
            [entry.l0.title, entry.l0.description, entry.l0.status, entry.l1_extract]
        )
        for entry in index.entries
    )
    for marker in L2_ONLY_MARKERS:
        assert marker not in index_text, (
            f"the L0/L1 index must not carry L2-only body text ({marker!r}); its "
            "presence would mean the whole corpus (L2 bodies) was loaded"
        )

    # (ii-c) Neither the index entries nor the surfaced neighbours expose an L2
    # attribute — the L2 bodies are absent from the material the pass selects on.
    for entry in index.entries:
        assert hasattr(entry, "l0") and hasattr(entry, "l1_extract")
        assert not hasattr(entry, "l2"), (
            "an L0/L1 index entry must not carry an L2 body"
        )

    # (ii-d) Each surfaced neighbour still carries enough for a downstream
    # adversarial pass to cite it BY ID without re-loading the whole corpus: its
    # id, its L0 card, and its verbatim L1 extract — and no L2 body.
    for neighbour in result.neighbours:
        assert not hasattr(neighbour, "l2"), (
            "a surfaced neighbour must not carry an L2 body"
        )
        expected_bundle = context["expected"][neighbour.id]
        assert neighbour.l0 == expected_bundle.l0, (
            f"neighbour {neighbour.id} must carry its real L0 card"
        )
        assert neighbour.l1_extract == expected_bundle.l1.text, (
            f"neighbour {neighbour.id} must carry its verbatim L1 extract for a "
            "downstream by-id pass"
        )
        assert neighbour.l1_extract, "the L1 extract material must be non-empty"
