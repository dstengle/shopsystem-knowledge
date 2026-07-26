"""Step definitions for answering the referenced-by back-edge from frontmatter.

Binds ``referenced_by_resolution.feature``. This is a *resolution/answering*
behaviour, distinct from the typed-edge coherence checks: it asks "what
references artifact B?" and pins that the answer is read from B's own
materialized ``referenced-by`` frontmatter field — NOT recomputed by scanning
the corpus for forward ``references`` edges naming B.

The corpus is built so the two answers provably diverge: artifact B carries a
materialized ``referenced-by`` edge naming A, but NO artifact in the corpus
carries a forward ``references`` edge to B. A pure corpus scan for forward
references therefore yields ``()``, while B's frontmatter declares ``("A",)``.
The resolver must return the frontmatter answer, not the scan answer.

RED leg: ``knowledge.typed_edges`` exposes no ``resolve_referenced_by`` query
yet (that is the blocked GREEN sub-issue). Rather than crash at collection on a
missing import, the ``When`` step resolves through :func:`_resolve`, which falls
back to the forward-references corpus scan the real resolver must NOT reduce to
when the symbol is absent — so RED lands on a meaningful assertion about the
*answer* (the scan answer ``()`` does not equal B's frontmatter ``("A",)``),
not on a collection error.
"""

from __future__ import annotations

import pytest
from pytest_bdd import given, scenario, then, when

from knowledge.artifact_types import Artifact
from knowledge.coherence import ArtifactCorpus

FEATURE = "referenced_by_resolution.feature"


def _artifact(**frontmatter) -> Artifact:
    return Artifact(frontmatter=dict(frontmatter), body=frontmatter.pop("body", ""))


def _forward_references_scan(corpus: ArtifactCorpus, target_id: str) -> tuple[str, ...]:
    """What answer a forward-references corpus scan yields for "what references target_id".

    Collects every artifact whose ``references`` frontmatter names ``target_id``.
    This is the whole-corpus scan the real resolver must NOT reduce to.
    """
    from knowledge.typed_edges import _link_targets

    return tuple(
        art.id
        for art in corpus.artifacts
        if isinstance(art.id, str) and target_id in _link_targets(art, "references")
    )


def _frontmatter_referenced_by(corpus: ArtifactCorpus, target_id: str) -> tuple[str, ...]:
    """The ids named in ``target_id``'s own ``referenced-by`` frontmatter field."""
    from knowledge.typed_edges import _link_targets

    art = corpus.get(target_id)
    assert art is not None, f"no artifact {target_id} in corpus"
    return tuple(_link_targets(art, "referenced-by"))


def _resolve(corpus: ArtifactCorpus, target_id: str) -> tuple[str, ...]:
    """Resolve "what references target_id" via the intended frontmatter-answering resolver.

    When ``resolve_referenced_by`` has not yet been built (RED), fall back to the
    forward-references corpus scan the real resolver must NOT reduce to, so the
    RED failure lands on a meaningful answer assertion rather than an ImportError.
    """
    from knowledge import typed_edges

    resolver = getattr(typed_edges, "resolve_referenced_by", None)
    if resolver is None:
        return _forward_references_scan(corpus, target_id)
    return tuple(resolver(corpus, target_id))


@pytest.fixture
def context() -> dict:
    return {}


@scenario(
    FEATURE,
    "the referenced-by back-edge is answered from frontmatter and not computed by corpus scan",
)
def test_referenced_by_answered_from_frontmatter() -> None: ...


@given(
    "an artifact corpus in which artifact B carries a materialized referenced-by edge "
    "naming artifact A in its frontmatter"
)
def _b_materialized_referenced_by(context: dict) -> None:
    context["A"] = "adr-100"
    context["B"] = "adr-050"
    # B declares the materialized referenced-by back-edge naming A, but A carries
    # NO forward references edge to B — so a pure corpus scan for forward
    # references naming B answers empty, while B's frontmatter answers ("adr-100",).
    context["artifacts"] = [
        _artifact(type="adr", id="adr-100", status="accepted"),
        _artifact(type="adr", id="adr-050", status="accepted", **{"referenced-by": ["adr-100"]}),
    ]


@when("the knowledge context resolves what references artifact B")
def _resolve_what_references_b(context: dict) -> None:
    corpus = ArtifactCorpus.from_artifacts(context["artifacts"])
    context["corpus"] = corpus
    context["answer"] = _resolve(corpus, context["B"])
    context["scan_answer"] = _forward_references_scan(corpus, context["B"])
    context["frontmatter_answer"] = _frontmatter_referenced_by(corpus, context["B"])


@then("it answers from artifact B's own referenced-by frontmatter field")
def _answers_from_frontmatter(context: dict) -> None:
    assert context["answer"] == context["frontmatter_answer"], (
        f"expected the answer to equal B's referenced-by frontmatter "
        f"{context['frontmatter_answer']}; got {context['answer']}"
    )
    assert context["A"] in context["answer"], (
        f"expected the materialized referenced-by naming {context['A']} in the answer; "
        f"got {context['answer']}"
    )


@then("it does not compute the answer by scanning the corpus for forward references edges")
def _not_computed_by_scan(context: dict) -> None:
    # The corpus is set up so a forward-references scan answers empty: nothing
    # forward-references B. If the resolver reduced to that scan, its answer would
    # equal the (empty) scan answer and lose the materialized back-edge.
    assert context["scan_answer"] == (), (
        f"fixture invariant: no artifact should forward-reference B; "
        f"scan answered {context['scan_answer']}"
    )
    assert context["answer"] != context["scan_answer"], (
        f"the resolver must not reduce to the forward-references corpus scan; "
        f"answer {context['answer']} matched the scan answer {context['scan_answer']}"
    )
