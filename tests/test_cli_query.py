"""Step definitions for the query read verb on the shop-knowledge CLI.

Binds the pinned scenarios in ``cli_query.feature``. ``query`` is a net-new
third read verb over the ``shop-knowledge`` CLI (a sibling of ``navigate`` and
``render``): unlike those two — which project a *single* named document — query
is **corpus-wide**. Given a corpus root and a single frontmatter facet / value,
it selects every document whose facet equals that value and returns a *compact
list*: one record per matched document carrying that document's id, title, and
status.

The recognized facets are the frontmatter facets ``type``, ``status``,
``distribution`` (each a scalar frontmatter field) and ``tag`` (which matches by
*membership* — a document matches ``tag=<value>`` iff ``<value>`` is in the
document's ``tags`` list). A query whose facet matches no document is an empty
result (exit 0, empty list), not an error.

The CLI is exercised **in-process**, mirroring ``test_cli_navigate.py`` and
``test_cli_render.py``: each scenario drives ``knowledge.cli.main`` with an
explicit argv and captures the exit code plus the raw stdout/stderr bytes. The
compact list is emitted as a JSON array on stdout::

    [{"id": "adr-001", "title": "...", "status": "accepted"}, ...]

so a scenario can assert the record shape (id / title / status) and the
selection soundness (every returned record's document actually carries the
matched facet) structurally rather than by string-scraping.

Invocation shape (mirrors navigate/render's ``--corpus <root>`` head, minus the
positional document id since query is corpus-wide)::

    main(["query", "--corpus", <root>, "--facet", <facet>, "--value", <value>])

The fixture corpus varies documents across all four facets so each Examples row
selects a real, proper subset — non-matching documents are present so the
soundness assertion (every returned document has facet == value) genuinely
proves the verb *filters* rather than returning the whole corpus.
"""

from __future__ import annotations

import io
import json
from pathlib import Path

import pytest
import yaml
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "cli_query.feature"


@pytest.fixture
def context() -> dict:
    return {}


def _write_doc(
    root: Path,
    subdir: str,
    doc_id: str,
    *,
    doc_type: str,
    status: str,
    title: str,
    tags: list[str],
    distribution: str,
) -> None:
    """Write a typed document with frontmatter varying across the four facets.

    Non-empty frontmatter makes it a typed artifact to
    :func:`knowledge.corpus_loader.load_corpus`; ``doc_type`` / ``status`` /
    ``distribution`` are scalar frontmatter facets and ``tags`` is the list the
    ``tag`` facet matches membership against.
    """
    frontmatter: dict[str, object] = {
        "type": doc_type,
        "id": doc_id,
        "title": title,
        "status": status,
        "tags": tags,
        "distribution": distribution,
    }
    source = (
        "---\n"
        + yaml.safe_dump(frontmatter, sort_keys=False)
        + "---\n\n## Context\n\nBody.\n"
    )
    (root / subdir).mkdir(parents=True, exist_ok=True)
    (root / subdir / f"{doc_id}.md").write_text(source, encoding="utf-8")


# The fixture corpus: six documents varying across type / status / tag /
# distribution so each Examples row selects a real, proper subset while
# non-matching documents remain present to prove the verb filters.
#   (subdir, id, type, status, tags, distribution)
_FIXTURE_DOCS: tuple[tuple[str, str, str, str, list[str], str], ...] = (
    ("adrs", "adr-001", "adr", "accepted", ["restructuring", "foundational"], "product-wide"),
    ("adrs", "adr-002", "adr", "proposed", ["tactical"], "team-local"),
    ("pdrs", "pdr-001", "pdr", "accepted", ["restructuring"], "product-wide"),
    ("pdrs", "pdr-002", "pdr", "superseded", ["legacy"], "team-local"),
    ("candidates", "cand-001", "candidate", "exploring", ["restructuring"], "team-local"),
    ("briefs", "brief-001", "brief", "ready", ["tactical"], "product-wide"),
)


def _build_varied_corpus(root: Path) -> None:
    """Materialize the four-facet fixture corpus under ``root``."""
    for subdir, doc_id, doc_type, status, tags, distribution in _FIXTURE_DOCS:
        _write_doc(
            root,
            subdir,
            doc_id,
            doc_type=doc_type,
            status=status,
            title=f"Query subject {doc_id}",
            tags=tags,
            distribution=distribution,
        )


def _doc_has_facet(doc: object, facet: str, value: str) -> bool:
    """Whether ``doc`` carries frontmatter facet ``facet`` equal to ``value``.

    ``type`` / ``status`` / ``distribution`` are scalar frontmatter fields (equal
    when the stored scalar equals ``value``); ``tag`` matches by membership — the
    document matches iff ``value`` is in its ``tags`` list.
    """
    frontmatter = doc.frontmatter  # type: ignore[attr-defined]
    if facet == "tag":
        tags = frontmatter.get("tags") or []
        return value in tags
    return frontmatter.get(facet) == value


def _run_query(context: dict, facet: str, value: str) -> None:
    from knowledge.cli import main

    out, err = io.BytesIO(), io.BytesIO()
    rc = main(
        ["query", "--corpus", str(context["root"]), "--facet", facet, "--value", value],
        stdout=out,
        stderr=err,
    )
    context["exit"] = rc
    context["stdout"] = out.getvalue()
    context["stderr"] = err.getvalue()


def _records(context: dict) -> list:
    """Parse the query JSON array from stdout (asserting a clean run first)."""
    assert context["exit"] == 0, (
        f"expected query to exit 0; got {context['exit']} "
        f"(stderr: {context['stderr']!r})"
    )
    parsed = json.loads(context["stdout"].decode("utf-8"))
    assert isinstance(parsed, list), f"query output is not a JSON list: {parsed!r}"
    return parsed


# --- Scenario bindings -------------------------------------------------------


@scenario(FEATURE, "query selects documents by a single frontmatter facet and returns a compact list")
def test_query_by_facet() -> None: ...


@scenario(FEATURE, "query whose facet matches no document returns an empty result rather than an error")
def test_query_empty_result() -> None: ...


# --- Given -------------------------------------------------------------------


@given("a corpus containing documents that vary by type, status, tag, and distribution")
def _corpus_varied(context: dict, tmp_path: Path) -> None:
    root = tmp_path / "corpus"
    _build_varied_corpus(root)
    context["root"] = root

    from knowledge.corpus_loader import load_corpus

    corpus = load_corpus(root)
    context["corpus"] = corpus
    # Fixture invariant: the corpus genuinely varies across every facet — for
    # each facet there is at least one document that matches the Examples value
    # AND at least one that does not, so the soundness assertion proves filtering.
    checks: tuple[tuple[str, str], ...] = (
        ("type", "adr"),
        ("status", "accepted"),
        ("tag", "restructuring"),
        ("distribution", "product-wide"),
    )
    for facet, value in checks:
        matching = [d for d in corpus.artifacts if _doc_has_facet(d, facet, value)]
        non_matching = [d for d in corpus.artifacts if not _doc_has_facet(d, facet, value)]
        assert matching, (
            f"fixture invariant: at least one document must match {facet}={value}"
        )
        assert non_matching, (
            f"fixture invariant: at least one document must NOT match {facet}={value} "
            f"so filtering is provable"
        )


@given(parsers.re(r'a corpus that contains no document whose tag equals "(?P<value>[^"]+)"'))
def _corpus_without_tag(context: dict, tmp_path: Path, value: str) -> None:
    root = tmp_path / "corpus"
    _build_varied_corpus(root)
    context["root"] = root

    from knowledge.corpus_loader import load_corpus

    corpus = load_corpus(root)
    assert not any(_doc_has_facet(d, "tag", value) for d in corpus.artifacts), (
        f"fixture invariant: no document may carry tag {value!r}"
    )


# --- When --------------------------------------------------------------------


@when(parsers.re(r'I run the query verb selecting documents whose "(?P<facet>[^"]+)" equals "(?P<value>[^"]+)" requesting a compact list'))
def _run_verb_outline(context: dict, facet: str, value: str) -> None:
    _run_query(context, facet, value)


@when(parsers.re(r'I run the query verb selecting documents whose tag equals "(?P<value>[^"]+)"'))
def _run_verb_tag(context: dict, value: str) -> None:
    _run_query(context, "tag", value)


# --- Then --------------------------------------------------------------------


@then("the exit code is 0")
def _exit_zero(context: dict) -> None:
    assert context["exit"] == 0, (
        f"expected the query verb to exit 0; got {context['exit']} "
        f"(stderr: {context['stderr']!r})"
    )


@then("every returned record carries the matched document's id, title, and status")
def _records_carry_id_title_status(context: dict) -> None:
    records = _records(context)
    assert records, (
        "expected a non-empty compact list — the Examples value is present in the "
        "fixture corpus, so a correct query must return the matching documents"
    )
    for record in records:
        assert isinstance(record, dict), f"a query record is not a mapping: {record!r}"
        for key in ("id", "title", "status"):
            assert key in record and record[key] is not None, (
                f"query record omits {key!r}: {record!r}"
            )


@then(parsers.re(r'every returned document has "(?P<facet>[^"]+)" equal to "(?P<value>[^"]+)"'))
def _every_returned_has_facet(context: dict, facet: str, value: str) -> None:
    records = _records(context)
    corpus = context["corpus"]
    for record in records:
        doc = corpus.get(record["id"])
        assert doc is not None, (
            f"query returned id {record['id']!r} not present in the corpus: {record!r}"
        )
        assert _doc_has_facet(doc, facet, value), (
            f"query returned document {record['id']!r} whose {facet} is not {value!r}; "
            f"the verb must select only documents matching the facet: {record!r}"
        )


@then("the result is an empty list")
def _result_empty(context: dict) -> None:
    records = _records(context)
    assert records == [], f"expected an empty compact list, got: {records!r}"


@then("the CLI does not report the empty match as an error")
def _no_error_reported(context: dict) -> None:
    assert context["exit"] == 0, (
        f"the empty match must not be an error; exit was {context['exit']}"
    )
    stderr = context["stderr"].decode("utf-8")
    assert stderr.strip() == "", (
        f"the CLI reported the empty match as an error on stderr: {stderr!r}"
    )


# --- query by edge participation (0a2.15) ------------------------------------
#
# A second selection mode on ``query``: instead of ``--facet <f> --value <v>``
# (frontmatter facet equality), select every document that *participates* in a
# named materialized edge — i.e. carries a non-empty ``<edge>`` frontmatter link
# field. The three edges exercised are the materialized back/forward link fields
# ``superseded-by``, ``references``, and ``referenced-by``. The chosen option
# shape parallels ``--facet``: ``query --corpus <root> --edge <edge>`` (no value,
# since participation is a non-empty test, not an equality).
#
# The fixture corpus carries, for every exercised edge, at least one document
# that participates (a non-empty ``<edge>`` link field) AND at least one that
# does not, so the soundness assertions — every returned document carries a
# non-empty ``<edge>`` edge, and none lacking it — genuinely prove the verb
# *filters* on participation rather than returning the whole corpus.


def _write_edge_doc(
    root: Path,
    subdir: str,
    doc_id: str,
    *,
    status: str,
    edges: dict[str, list[str]],
) -> None:
    """Write a typed ``adr`` document carrying the given materialized ``edges``.

    ``edges`` maps a materialized link-field name (``superseded-by`` /
    ``references`` / ``referenced-by``) to its non-empty list of target ids; a
    document participates in an edge exactly when that field is present and
    non-empty. A document with an empty ``edges`` mapping participates in none.
    """
    frontmatter: dict[str, object] = {
        "type": "adr",
        "id": doc_id,
        "title": f"Edge subject {doc_id}",
        "status": status,
    }
    frontmatter.update(edges)
    source = (
        "---\n"
        + yaml.safe_dump(frontmatter, sort_keys=False)
        + "---\n\n## Context\n\nBody.\n"
    )
    (root / subdir).mkdir(parents=True, exist_ok=True)
    (root / subdir / f"{doc_id}.md").write_text(source, encoding="utf-8")


# The edge fixture: for each exercised edge there is a participant carrying a
# non-empty link field of that name and non-participants that carry none.
#   (subdir, id, status, {edge_field: [targets]})
_EDGE_FIXTURE_DOCS: tuple[tuple[str, str, str, dict[str, list[str]]], ...] = (
    ("adrs", "adr-super", "superseded", {"superseded-by": ["adr-plain"]}),
    ("adrs", "adr-ref", "accepted", {"references": ["adr-plain"]}),
    ("adrs", "adr-refby", "accepted", {"referenced-by": ["adr-plain"]}),
    ("adrs", "adr-plain", "accepted", {}),
)


def _build_edge_corpus(root: Path) -> None:
    """Materialize the edge-participation fixture corpus under ``root``."""
    for subdir, doc_id, status, edges in _EDGE_FIXTURE_DOCS:
        _write_edge_doc(root, subdir, doc_id, status=status, edges=edges)


def _doc_participates_in_edge(doc: object, edge: str) -> bool:
    """Whether ``doc`` carries a non-empty ``edge`` materialized link field.

    Participation is read the same way the edge-resolution pass reads it — via
    :func:`knowledge.typed_edges._link_targets`, non-empty — so a scalar id, a
    list of ids, and an absent/empty field are all interpreted uniformly.
    """
    from knowledge.typed_edges import _link_targets

    return bool(_link_targets(doc, edge))  # type: ignore[arg-type]


def _run_edge_query(context: dict, edge: str) -> None:
    """Drive ``query --corpus <root> --edge <edge>`` in-process."""
    from knowledge.cli import main

    out, err = io.BytesIO(), io.BytesIO()
    rc = main(
        ["query", "--corpus", str(context["root"]), "--edge", edge],
        stdout=out,
        stderr=err,
    )
    context["exit"] = rc
    context["stdout"] = out.getvalue()
    context["stderr"] = err.getvalue()


@scenario(FEATURE, "query selects documents by edge participation")
def test_query_by_edge_participation() -> None: ...


@given(parsers.re(
    r'a corpus in which some documents participate in the materialized '
    r'"(?P<edge>[^"]+)" relationship and some do not'
))
def _corpus_with_edge_participation(context: dict, tmp_path: Path, edge: str) -> None:
    root = tmp_path / "corpus"
    _build_edge_corpus(root)
    context["root"] = root

    from knowledge.corpus_loader import load_corpus

    corpus = load_corpus(root)
    context["corpus"] = corpus
    # Fixture invariant: the edge genuinely partitions the corpus — at least one
    # document participates in <edge> and at least one does not — so the
    # soundness assertions prove filtering rather than a whole-corpus return.
    participants = [d for d in corpus.artifacts if _doc_participates_in_edge(d, edge)]
    non_participants = [
        d for d in corpus.artifacts if not _doc_participates_in_edge(d, edge)
    ]
    assert participants, (
        f"fixture invariant: at least one document must participate in {edge!r}"
    )
    assert non_participants, (
        f"fixture invariant: at least one document must NOT participate in {edge!r} "
        f"so filtering is provable"
    )


@when(parsers.re(
    r'I run the query verb selecting documents that participate in the '
    r'"(?P<edge>[^"]+)" edge'
))
def _run_verb_edge(context: dict, edge: str) -> None:
    _run_edge_query(context, edge)


@then(parsers.re(
    r'every returned document carries a non-empty "(?P<edge>[^"]+)" frontmatter edge'
))
def _every_returned_participates(context: dict, edge: str) -> None:
    records = _records(context)
    assert records, (
        "expected a non-empty compact list — the fixture corpus has documents "
        "participating in this edge, so a correct query must return them"
    )
    corpus = context["corpus"]
    for record in records:
        doc = corpus.get(record["id"])
        assert doc is not None, (
            f"query returned id {record['id']!r} not present in the corpus: {record!r}"
        )
        assert _doc_participates_in_edge(doc, edge), (
            f"query returned document {record['id']!r} carrying no non-empty "
            f"{edge!r} edge; the verb must select only participants: {record!r}"
        )


@then(parsers.re(r'no returned document lacks the "(?P<edge>[^"]+)" edge'))
def _no_returned_lacks_edge(context: dict, edge: str) -> None:
    records = _records(context)
    corpus = context["corpus"]
    lacking = [
        record["id"]
        for record in records
        if not _doc_participates_in_edge(corpus.get(record["id"]), edge)
    ]
    assert not lacking, (
        f"query returned documents that lack the {edge!r} edge: {lacking!r}; "
        f"a participation query must exclude non-participants"
    )


# --- query rendered output under the current-system view filter (0a2.17) -----
#
# A third shape on ``query``: a ``--rendered`` flag on the facet selection.
# Without it, each matching document is emitted as the compact id/title/status
# record. WITH ``--rendered``, each matching document additionally carries a
# ``rendered`` field holding that document RENDERED under render's *current-
# system* view — its accepted content sections present, and the ``## Changelog``
# and ``## Supersede-chain`` transformation material SLICED OUT (the SAME drop
# render's current-system view performs via ``_current_system_body``). The
# chosen option shape parallels render's ``--view current-system``, expressed as
# a bare flag on the facet mode::
#
#     query --corpus <root> --facet <f> --value <v> --rendered
#
# The fixture corpus carries accepted documents matching the query facet, each
# carrying content sections + a ``## Changelog`` section (naming a superseded
# predecessor) + a ``## Supersede-chain`` section, plus at least one non-matching
# document so the facet filter is provable. Per-document markers are derived from
# the id so each match's content presence and changelog/supersede-chain absence
# are provable token-by-token in the rendered field.

# The query facet the rendered fixture selects on: every accepted document
# matches ``status == accepted`` while the non-accepted document does not, so the
# facet filter is provable AND the matches are exactly the accepted set.
_RENDERED_QUERY_FACET = "status"
_RENDERED_QUERY_VALUE = "accepted"

# The rendered fixture corpus: two accepted documents that match the facet and
# one non-accepted document that does not.
#   (subdir, id, status)
_RENDERED_FIXTURE_DOCS: tuple[tuple[str, str, str], ...] = (
    ("adrs", "adr-100", "accepted"),
    ("adrs", "adr-101", "accepted"),
    ("adrs", "adr-102", "proposed"),
)


def _rendered_content_markers(doc_id: str) -> tuple[str, ...]:
    """The three content-section markers for ``doc_id`` (must survive the view)."""
    return (
        f"CTX-{doc_id}-CONTENT",
        f"DEC-{doc_id}-CONTENT",
        f"CON-{doc_id}-CONTENT",
    )


def _rendered_changelog_marker(doc_id: str) -> str:
    """The changelog-section marker for ``doc_id`` (must be dropped by the view)."""
    return f"CHG-{doc_id}-CHANGELOG"


def _rendered_supersede_marker(doc_id: str) -> str:
    """The supersede-chain material marker for ``doc_id`` (dropped by the view)."""
    return f"SUP-{doc_id}-SUPERSEDE"


def _rendered_doc_body(doc_id: str) -> str:
    """Body for a rendered-query fixture document.

    Three content sections (each a distinct per-id marker), a ``## Changelog``
    section carrying a changelog marker AND naming a superseded predecessor, and
    a distinct ``## Supersede-chain`` section carrying supersede-chain material.
    The current-system view keeps the content sections and drops the changelog +
    supersede-chain material.
    """
    ctx, dec, con = _rendered_content_markers(doc_id)
    return (
        f"## Context\n\n{ctx}\n\n"
        f"## Decision\n\n{dec}\n\n"
        f"## Consequences\n\n{con}\n\n"
        f"## Changelog\n\n{_rendered_changelog_marker(doc_id)}\n\n"
        f"Supersedes PRED-{doc_id}.\n\n"
        f"## Supersede-chain\n\n{_rendered_supersede_marker(doc_id)}\n"
    )


def _write_rendered_doc(root: Path, subdir: str, doc_id: str, *, status: str) -> None:
    """Write a typed ``adr`` document carrying content + changelog + supersede-chain."""
    frontmatter: dict[str, object] = {
        "type": "adr",
        "id": doc_id,
        "title": f"Rendered query subject {doc_id}",
        "status": status,
    }
    source = (
        "---\n"
        + yaml.safe_dump(frontmatter, sort_keys=False)
        + "---\n\n"
        + _rendered_doc_body(doc_id)
    )
    (root / subdir).mkdir(parents=True, exist_ok=True)
    (root / subdir / f"{doc_id}.md").write_text(source, encoding="utf-8")


def _build_rendered_corpus(root: Path) -> None:
    """Materialize the rendered-query fixture corpus under ``root``."""
    for subdir, doc_id, status in _RENDERED_FIXTURE_DOCS:
        _write_rendered_doc(root, subdir, doc_id, status=status)


def _run_rendered_query(context: dict, facet: str, value: str) -> None:
    """Drive ``query --corpus <root> --facet <f> --value <v> --rendered`` in-process."""
    from knowledge.cli import main

    out, err = io.BytesIO(), io.BytesIO()
    rc = main(
        [
            "query",
            "--corpus",
            str(context["root"]),
            "--facet",
            facet,
            "--value",
            value,
            "--rendered",
        ],
        stdout=out,
        stderr=err,
    )
    context["exit"] = rc
    context["stdout"] = out.getvalue()
    context["stderr"] = err.getvalue()


@scenario(FEATURE, "query with rendered output emits matching documents under the same current-system view filter as render")
def test_query_rendered_output() -> None: ...


@given("a corpus containing accepted documents that carry changelog sections and match a query facet")
def _corpus_rendered_matches(context: dict, tmp_path: Path) -> None:
    root = tmp_path / "corpus"
    _build_rendered_corpus(root)
    context["root"] = root

    from knowledge.corpus_loader import load_corpus

    corpus = load_corpus(root)
    context["corpus"] = corpus

    expected: set[str] = set()
    for _subdir, doc_id, status in _RENDERED_FIXTURE_DOCS:
        subject = corpus.get(doc_id)
        assert subject is not None, (
            f"fixture invariant: {doc_id} must load as a typed artifact"
        )
        if status == _RENDERED_QUERY_VALUE:
            assert "Changelog" in subject.sections, (
                f"fixture invariant: matching {doc_id} must carry a changelog "
                f"section: {subject.sections!r}"
            )
            assert "Supersede-chain" in subject.sections, (
                f"fixture invariant: matching {doc_id} must carry supersede-chain "
                f"material: {subject.sections!r}"
            )
            expected.add(doc_id)
    context["expected_match_ids"] = expected

    assert expected, "fixture invariant: at least one accepted document must match"
    non_matching = [
        d for d in corpus.artifacts if not _doc_has_facet(d, _RENDERED_QUERY_FACET, _RENDERED_QUERY_VALUE)
    ]
    assert non_matching, (
        "fixture invariant: at least one non-matching document must be present so "
        "the facet filter is provable"
    )


@when("I run the query verb selecting those documents requesting rendered output in the current-system view")
def _run_verb_rendered(context: dict) -> None:
    _run_rendered_query(context, _RENDERED_QUERY_FACET, _RENDERED_QUERY_VALUE)


@then("each matching document is rendered with its accepted content sections")
def _each_match_rendered_content(context: dict) -> None:
    records = _records(context)
    got_ids = {record["id"] for record in records}
    assert got_ids == context["expected_match_ids"], (
        f"rendered query returned ids {got_ids!r}; expected exactly the matching "
        f"documents {context['expected_match_ids']!r} — the facet filter must "
        f"select only matches"
    )
    for record in records:
        assert "rendered" in record and isinstance(record["rendered"], str), (
            f"rendered query record omits a string 'rendered' field: {record!r}"
        )
        rendered = record["rendered"]
        for marker in _rendered_content_markers(record["id"]):
            assert marker in rendered, (
                f"the rendered output for {record['id']!r} omits accepted content "
                f"marker {marker!r}: {rendered!r}"
            )


@then("no rendered match contains its changelog section or supersede-chain transformation material")
def _no_match_leaks_transformation(context: dict) -> None:
    records = _records(context)
    for record in records:
        assert "rendered" in record and isinstance(record["rendered"], str), (
            f"rendered query record omits a string 'rendered' field: {record!r}"
        )
        rendered = record["rendered"]
        changelog = _rendered_changelog_marker(record["id"])
        supersede = _rendered_supersede_marker(record["id"])
        assert changelog not in rendered, (
            f"the rendered output for {record['id']!r} leaked its changelog section "
            f"(marker {changelog!r}); the current-system view must drop it: {rendered!r}"
        )
        assert supersede not in rendered, (
            f"the rendered output for {record['id']!r} leaked supersede-chain "
            f"transformation material (marker {supersede!r}); the current-system view "
            f"must drop it: {rendered!r}"
        )
