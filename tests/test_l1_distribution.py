"""Step definitions for the L1 distribution scenarios (3 scenarios).

Binds every scenario of ``l1_distribution.feature`` and asserts each Then/And
leg against ``knowledge.distribution.distribute_l1`` — the distribution step that
pours the L1 decision digest to BC channels, gated by the distribution-mode
coherence check (``LIFECYCLE_CHECKS + TYPED_EDGE_CHECKS`` under
``GateMode.DISTRIBUTION``):

* @scenario_hash:218fa351bb1d48b5 — a coherent corpus (no blocking finding)
  delivers its L1 decision digest to the BC channel;
* @scenario_hash:353190f53fe739d2 — a blocking-severity finding refuses the pour,
  no digest reaches any BC, and the blocking finding is reported; and
* @scenario_hash:88f923b94cdebd0d — only L0 and L1 projections cross the boundary;
  no L2 full document is ever delivered to a BC.

RED leg: ``knowledge.distribution`` does not exist yet, so every symbol is
imported inside a step body — each scenario fails at the step that first needs
the behaviour, not at collection/import time. The GREEN leg adds the module and
makes every leg pass.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

FEATURE = "l1_distribution.feature"
FIXTURES = Path(__file__).parent / "fixtures"
COHERENT_DIR = FIXTURES / "distribution_corpus"
BLOCKING_EXTRA_DIR = FIXTURES / "distribution_blocking_extra"

REFERENCE = date(2026, 7, 1)
ACCEPTED_DECISION_ID = "adr-0040"


def _load(directory: Path) -> dict[str, str]:
    return {
        path.stem: path.read_text(encoding="utf-8")
        for path in sorted(directory.glob("*.md"))
    }


@pytest.fixture
def context() -> dict:
    return {}


# --- Scenario bindings -------------------------------------------------------


@scenario(FEATURE, "a coherent corpus pours its L1 digest to BCs")
def test_coherent_pours() -> None: ...


@scenario(FEATURE, "a blocking-severity finding refuses the pour")
def test_blocking_refuses() -> None: ...


@scenario(FEATURE, "L2 full documents never cross the distribution boundary")
def test_l2_never_crosses() -> None: ...


# --- Given steps -------------------------------------------------------------


@given(
    "an artifact corpus whose distribution-mode coherence check passes with no "
    "blocking finding"
)
def _coherent_corpus(context: dict) -> None:
    context["sources"] = _load(COHERENT_DIR)


@given(
    "an artifact corpus whose distribution-mode coherence check surfaces a "
    "blocking-severity finding"
)
def _blocking_corpus(context: dict) -> None:
    sources = _load(COHERENT_DIR)
    sources.update(_load(BLOCKING_EXTRA_DIR))
    context["sources"] = sources


@given("an artifact corpus and a BC that consumes distributed knowledge")
def _corpus_and_consuming_bc(context: dict) -> None:
    context["sources"] = _load(COHERENT_DIR)


# --- When step ---------------------------------------------------------------


@when("the knowledge context runs the L1 distribution")
def _run_distribution(context: dict) -> None:
    from knowledge.coherence import CoherenceConfig
    from knowledge.distribution import BCChannel, distribute_l1

    channel = BCChannel(name="consumer-bc")
    config = CoherenceConfig(reference_date=REFERENCE)
    context["channel"] = channel
    context["result"] = distribute_l1(context["sources"], config, channels=(channel,))


# --- Then steps: coherent pours ----------------------------------------------


@then("it delivers the L1 decision digest to the BC channel")
def _delivers_digest(context: dict) -> None:
    from knowledge.digest import generate_l1_digest

    result = context["result"]
    channel = context["channel"]
    assert result.poured is True, "a coherent corpus must pour its digest"
    # The L1 entries that crossed match the corpus's L1 decision digest.
    expected = generate_l1_digest(context["sources"])
    crossed_ids = tuple(sorted(p.doc_id for p in channel.l1_deliveries))
    assert crossed_ids == expected.ids, (
        f"channel must receive the L1 digest entries {expected.ids}, got {crossed_ids}"
    )
    assert channel.l1_deliveries, "at least one L1 entry must be delivered"


# --- Then steps: blocking refuses --------------------------------------------


@then("it refuses to pour the L1 decision digest and delivers no digest to any BC")
def _refuses_and_delivers_nothing(context: dict) -> None:
    result = context["result"]
    channel = context["channel"]
    assert result.poured is False, "a blocking finding must refuse the pour"
    assert result.refused is True
    assert channel.deliveries == (), "no projection may cross when the pour is refused"


@then("it reports the blocking finding that refused the pour")
def _reports_blocking(context: dict) -> None:
    result = context["result"]
    assert result.blocking_findings, "the refusal must report the blocking finding"
    assert any(
        f.check_id == "briefed-without-brief" for f in result.blocking_findings
    ), "the reported blocking finding must be the one the corpus carries"


# --- Then steps: L2 never crosses --------------------------------------------


@then("only L0 and L1 projections cross to the BC channel")
def _only_l0_l1_cross(context: dict) -> None:
    channel = context["channel"]
    assert channel.deliveries, "the coherent corpus must deliver something"
    assert channel.tiers_crossed == frozenset({"L0", "L1"}), (
        f"only L0 and L1 tiers may cross; got {set(channel.tiers_crossed)}"
    )


@then("no L2 full document is delivered to any BC")
def _no_l2_crosses(context: dict) -> None:
    channel = context["channel"]
    result = context["result"]
    # No delivery is tagged L2...
    assert all(p.tier != "L2" for p in channel.deliveries), "no L2 tier may cross"
    assert result.l2_crossed is False
    # ...and no delivered payload is the full L2 source document.
    full_source = context["sources"]["adr_0040_accepted"]
    for projection in channel.deliveries:
        assert str(projection.payload) != full_source, (
            "the full L2 source document must never be delivered"
        )
        # The L2-only Consequences section never rides along in a crossed payload.
        assert "## Consequences" not in str(projection.payload), (
            "an L2-only section must not cross the boundary"
        )
