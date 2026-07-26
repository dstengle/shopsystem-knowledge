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
