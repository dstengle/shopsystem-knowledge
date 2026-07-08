"""Step definitions for the kind-parameterized accessor outer-loop scenario.

Binds @scenario_hash:f4b64423b77dd3e2 — "the accessor is parameterized by kind
and refuses an unregistered kind" — and asserts both When/Then pairs:

* a caller requesting the *registered* architecture-decision kind receives that
  kind's corpus projections (the same byte manifest ``generate_corpus`` builds
  for the architecture-decision source corpus); and
* a caller requesting an *unregistered* kind ("development-principle") receives
  a definite kind-not-registered result — one whose ``registered`` flag is
  ``False`` and that is explicitly NOT the architecture-decision corpus
  projections — rather than silently defaulting to the architecture-decision
  corpus.

RED leg: the kind-parameterized ``KnowledgeContext`` registry/accessor does not
yet exist, so it is imported inside the ``Given`` step body — the scenario fails
at that step (behaviour absent), not at collection/import time. The GREEN leg
adds the registry + accessor and makes both When/Then pairs pass.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenario, then, when

from knowledge.projections import generate_corpus

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "corpus"

# The kind under which the architecture-decision corpus is registered, and a
# kind that is deliberately never registered.
ARCHITECTURE_DECISION_KIND = "architecture-decision"
UNREGISTERED_KIND = "development-principle"


@pytest.fixture
def context() -> dict:
    return {"results": {}}


@scenario(
    "kind_parameterized_accessor.feature",
    "the accessor is parameterized by kind and refuses an unregistered kind",
)
def test_kind_parameterized_accessor() -> None:
    """Outer-loop binding; step bodies below carry the assertions."""


@given(
    "the knowledge context with the architecture-decision kind registered and "
    "no other kind registered"
)
def _registry_with_only_ad_kind(context: dict) -> None:
    # Imported here (not at module top) so the RED commit fails at this step on
    # the absent behaviour, not on a collection-time ImportError.
    from knowledge.projections import KnowledgeContext

    ad_sources = {
        path.stem: path.read_text(encoding="utf-8")
        for path in sorted(FIXTURE_DIR.glob("*.md"))
    }
    # Guard the corpus's own precondition so a later fixture edit cannot quietly
    # weaken the scenario.
    assert len(ad_sources) >= 1, "architecture-decision corpus must carry a document"

    ctx = KnowledgeContext()
    ctx.register(ARCHITECTURE_DECISION_KIND, ad_sources)

    # "no other kind registered" is a real precondition: exactly one kind is
    # registered, and it is the architecture-decision kind.
    assert ctx.registered_kinds() == (ARCHITECTURE_DECISION_KIND,), (
        "precondition: exactly the architecture-decision kind is registered, "
        f"got {ctx.registered_kinds()!r}"
    )

    context["ctx"] = ctx
    context["ad_sources"] = ad_sources


@when(parsers.parse('a caller requests projections for kind "{kind}"'))
def _request_projections(context: dict, kind: str) -> None:
    context["results"][kind] = context["ctx"].projections_for(kind)


@then("the accessor returns the architecture-decision corpus projections")
def _returns_ad_corpus(context: dict) -> None:
    result = context["results"][ARCHITECTURE_DECISION_KIND]

    assert result.registered is True, (
        "the architecture-decision kind is registered, so its result must be "
        "a registered result"
    )
    assert result.kind == ARCHITECTURE_DECISION_KIND

    # The registered result carries exactly the architecture-decision corpus
    # projections — the byte manifest generate_corpus builds for that corpus.
    expected = generate_corpus(context["ad_sources"])
    assert result.projections == expected, (
        "the registered-kind result must carry the architecture-decision corpus "
        "projections"
    )


@then(
    "the accessor returns a definite kind-not-registered result rather than "
    "defaulting to the architecture-decision corpus"
)
def _returns_definite_not_registered(context: dict) -> None:
    result = context["results"][UNREGISTERED_KIND]

    # A definite kind-not-registered result: the flag says so unambiguously and
    # it names the requested (unregistered) kind.
    assert result.registered is False, (
        "an unregistered kind must yield a definite not-registered result, not a "
        "registered one"
    )
    assert result.kind == UNREGISTERED_KIND
    assert result.projections is None, (
        "a not-registered result must carry no projections at all"
    )

    # The distinction is explicit: the unregistered-kind result must NOT be the
    # architecture-decision corpus projections — it did not silently default.
    ad_projections = generate_corpus(context["ad_sources"])
    assert result.projections != ad_projections, (
        "the unregistered kind must not default to the architecture-decision "
        "corpus projections"
    )
