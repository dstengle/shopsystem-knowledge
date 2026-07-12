"""Step definitions for the L1 decision digest scenarios (3 scenarios).

Binds every scenario of ``l1_decision_digest.feature`` and asserts each
Then/And leg against the digest ``knowledge.digest.generate_l1_digest`` (and the
filesystem materializer ``write_digest``) build over an artifact corpus:

* @scenario_hash:1e54b6db4a552943 — the digest contains an entry for exactly the
  accepted decisions and none for a proposed, rejected, or superseded decision;
* @scenario_hash:203bebfdad68329c — each entry is self-contained, carrying its
  own id, status, supersede edges, and the verbatim L1 decision extract; and
* @scenario_hash:f74c632acd68f308 — the digest is derived from the single source,
  so regeneration over an unchanged source writes zero changed bytes and no
  entry carries a fact absent from that source.

RED leg: ``knowledge.digest`` does not exist yet, so every symbol is imported
inside a step body — each scenario fails at the step that first needs the
behaviour, not at collection/import time. The GREEN leg adds the module and
makes every leg pass.

The corpus is a directory of conforming decision fixtures: an accepted adr that
supersedes a prior (now superseded) adr, plus a proposed adr and a rejected pdr
that the digest must exclude.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from knowledge.projections import generate_projections

FEATURE = "l1_decision_digest.feature"
CORPUS_DIR = Path(__file__).parent / "fixtures" / "digest_corpus"

# The corpus's known facts, so the scenarios assert against a fixed shape rather
# than re-deriving it from the fixtures.
ACCEPTED_ID = "adr-0031"
SUPERSEDED_PRIOR_ID = "adr-0028"
EXCLUDED_IDS = ("adr-0028", "adr-0032", "pdr-0007")  # superseded, proposed, rejected


def _load_corpus() -> dict[str, str]:
    """Load the fixture corpus as an id -> source-text mapping, guarding shape."""
    sources = {
        path.stem: path.read_text(encoding="utf-8")
        for path in sorted(CORPUS_DIR.glob("*.md"))
    }
    assert len(sources) >= 4, "corpus must carry the accepted, superseded, proposed and rejected docs"
    return sources


def _by_id(sources: dict[str, str]) -> dict[str, str]:
    """Re-key the corpus by each document's frontmatter id (not its filename)."""
    from knowledge.artifact_types import parse_artifact

    keyed: dict[str, str] = {}
    for text in sources.values():
        art = parse_artifact(text)
        assert isinstance(art.id, str) and art.id
        keyed[art.id] = text
    return keyed


@pytest.fixture
def context() -> dict:
    return {}


# --- Scenario bindings -------------------------------------------------------


@scenario(FEATURE, "the digest contains exactly the accepted decisions and excludes the rest")
def test_exactly_accepted() -> None: ...


@scenario(FEATURE, "each digest entry is self-contained")
def test_self_contained() -> None: ...


@scenario(
    FEATURE,
    "the digest is derived from the single source and regeneration is idempotent",
)
def test_single_source_idempotent() -> None: ...


# --- Given steps -------------------------------------------------------------


@given(
    "an artifact corpus containing accepted decisions and decisions whose status "
    "is proposed, rejected or superseded"
)
def _mixed_status_corpus(context: dict) -> None:
    sources = _load_corpus()
    keyed = _by_id(sources)
    # Guard the precondition: an accepted decision and each excluded status present.
    assert ACCEPTED_ID in keyed, "corpus must carry an accepted decision"
    for excluded in EXCLUDED_IDS:
        assert excluded in keyed, f"corpus must carry the excluded decision {excluded}"
    context["sources"] = sources


@given("an artifact corpus containing an accepted decision that supersedes a prior decision")
def _accepted_supersedes_prior(context: dict) -> None:
    sources = _load_corpus()
    keyed = _by_id(sources)
    assert ACCEPTED_ID in keyed and SUPERSEDED_PRIOR_ID in keyed
    assert SUPERSEDED_PRIOR_ID in keyed[ACCEPTED_ID], (
        "accepted decision's source must name the prior decision it supersedes"
    )
    context["sources"] = sources
    context["accepted_source"] = keyed[ACCEPTED_ID]


@given("an artifact corpus whose L1 decision digest has already been generated")
def _already_generated(context: dict, tmp_path: Path) -> None:
    from knowledge.digest import write_digest

    sources = _load_corpus()
    out_dir = tmp_path / "digest-out"
    initial = write_digest(sources, out_dir)
    assert initial.changed_count > 0, "initial digest generation must write the manifest"
    context["sources"] = sources
    context["out_dir"] = out_dir


# --- When steps --------------------------------------------------------------


@when("the knowledge context generates the L1 decision digest over the corpus")
def _generate_digest(context: dict) -> None:
    from knowledge.digest import generate_l1_digest

    context["digest"] = generate_l1_digest(context["sources"])


@when("the knowledge context regenerates the L1 decision digest over the unchanged source")
def _regenerate_digest(context: dict) -> None:
    from knowledge.digest import write_digest

    context["regen"] = write_digest(context["sources"], context["out_dir"])


# --- Then steps: exactly the accepted decisions ------------------------------


@then("the digest contains an entry for every accepted decision")
def _entry_for_every_accepted(context: dict) -> None:
    digest = context["digest"]
    keyed = _by_id(context["sources"])
    accepted_ids = tuple(
        aid for aid, text in keyed.items() if _status_of(text) == "accepted"
    )
    assert accepted_ids, "the corpus must carry at least one accepted decision"
    for aid in accepted_ids:
        assert digest.entry_for(aid) is not None, f"digest must carry an entry for {aid}"


@then("the digest contains no entry for any proposed, rejected or superseded decision")
def _no_entry_for_non_accepted(context: dict) -> None:
    digest = context["digest"]
    keyed = _by_id(context["sources"])
    for aid, text in keyed.items():
        if _status_of(text) != "accepted":
            assert digest.entry_for(aid) is None, (
                f"digest must not carry an entry for non-accepted decision {aid}"
            )
    for excluded in EXCLUDED_IDS:
        assert digest.entry_for(excluded) is None


# --- Then steps: self-contained entry ----------------------------------------


@then(
    "the entry for that accepted decision carries its own id, its status, its "
    "supersede edges and the verbatim L1 decision extract"
)
def _entry_self_contained(context: dict) -> None:
    digest = context["digest"]
    entry = digest.entry_for(ACCEPTED_ID)
    assert entry is not None, "the accepted decision must have a digest entry"
    assert entry.id == ACCEPTED_ID
    assert entry.status == "accepted"
    # Its supersede edges name the prior decision it supersedes.
    assert SUPERSEDED_PRIOR_ID in entry.supersedes, (
        f"entry must carry its supersede edge to {SUPERSEDED_PRIOR_ID}"
    )
    # The verbatim L1 decision extract matches the single-source projection.
    expected_l1 = generate_projections(context["accepted_source"]).l1.text
    assert entry.l1_extract == expected_l1
    assert expected_l1, "the L1 extract must be non-empty for a conforming decision"


@then(
    "a reader of that single entry can determine the decision, its status and "
    "what it supersedes without consulting any other entry or the source document"
)
def _entry_reader_self_sufficient(context: dict) -> None:
    digest = context["digest"]
    entry = digest.entry_for(ACCEPTED_ID)
    assert entry is not None
    # The entry alone carries the decision (its verbatim extract), its status,
    # and what it supersedes — no other entry or the source is needed.
    assert entry.l1_extract.strip(), "the decision text must be in the entry itself"
    assert entry.status == "accepted", "the status must be in the entry itself"
    assert entry.supersedes == (SUPERSEDED_PRIOR_ID,), (
        "what the decision supersedes must be in the entry itself"
    )


# --- Then steps: single source + idempotence ---------------------------------


@then("the regeneration writes zero changed bytes")
def _zero_changed_bytes(context: dict) -> None:
    regen = context["regen"]
    assert regen.changed_count == 0, (
        "regeneration over an unchanged source must rewrite nothing; "
        f"changed paths: {regen.changed_paths!r}"
    )
    assert regen.changed_paths == (), "no path may be reported as changed"


@then("no digest entry carries any fact absent from the single source")
def _no_fact_absent_from_source(context: dict) -> None:
    from knowledge.digest import generate_l1_digest

    digest = generate_l1_digest(context["sources"])
    keyed = _by_id(context["sources"])
    assert digest.entries, "the digest must carry at least one entry"
    for entry in digest.entries:
        source = keyed[entry.id]
        assert entry.id in source, f"entry id {entry.id!r} absent from its source"
        assert entry.status in source, f"entry status {entry.status!r} absent from its source"
        assert entry.l1_extract in source, "entry L1 extract must be verbatim from its source"
        for target in entry.supersedes:
            assert target in source, f"supersede target {target!r} absent from its source"


# --- Small helper ------------------------------------------------------------


def _status_of(text: str) -> object:
    from knowledge.artifact_types import parse_artifact

    return parse_artifact(text).status
