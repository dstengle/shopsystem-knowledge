"""Step definitions for the render read verb — current-system view.

Binds the pinned scenarios in ``cli_render.feature``. ``render`` is a net-new
second read verb over the ``shop-knowledge`` CLI (a sibling of ``navigate``):
given a corpus root, a document id, and a ``--view`` selector, its
*current-system* view projects a single document as the accepted system sees it
right now.

The current-system view has exactly two shapes:

* For a document **in the accepted set** (frontmatter ``status: accepted``) the
  view emits that document's accepted **content sections** — the body sections
  that carry the decision's content — so a reader sees what the accepted system
  currently says.
* For a document **outside the accepted set** (any non-accepted status, e.g.
  ``superseded``) the current-system view has **no rendering**: the CLI reports
  that the document has no current-system rendering *because it is not in the
  accepted set*, and emits none of that document's content.

The CLI is exercised **in-process**, mirroring ``test_cli_navigate.py``: each
scenario drives ``knowledge.cli.main`` with an explicit argv and captures the
exit code plus the raw stdout/stderr bytes. The invocation shape mirrors
navigate's positional-head + trailer-pairs parser::

    main(["render", "adr-068", "--corpus", <root>, "--view", "current-system"])

Fixtures are built with distinctive per-section content markers so "the accepted
content sections are emitted" and "no accepted content is emitted" are each
provable against the captured output rather than by string-shape guessing.
"""

from __future__ import annotations

import io
from pathlib import Path

import pytest
import yaml
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "cli_render.feature"

# The accepted subject and its distinctive per-content-section body markers. Each
# content section carries a unique token so "the rendered output contains the
# document's accepted content sections" is provable token-by-token.
ACCEPTED_ID = "adr-068"
ACCEPTED_CONTENT_MARKERS: tuple[str, ...] = (
    "CTX-068-ACCEPTED-CONTENT",
    "DEC-068-ACCEPTED-CONTENT",
    "CON-068-ACCEPTED-CONTENT",
)
# The changelog section marker — a NON-content section. (Whether the current-
# system view drops the changelog is pinned by a separate later scenario; here
# we only assert the accepted content IS present, so this marker is unused by
# the assertions but present in the fixture body.)
ACCEPTED_CHANGELOG_MARKER = "CHG-068-CHANGELOG-ENTRY"

# The non-accepted subject and a distinctive content marker whose absence from
# the output proves "no accepted content is emitted".
NON_ACCEPTED_ID = "adr-034"
NON_ACCEPTED_CONTENT_MARKER = "DEC-034-SUPERSEDED-CONTENT"


@pytest.fixture
def context() -> dict:
    return {}


def _write_adr(root: Path, doc_id: str, *, status: str, body: str) -> None:
    """Write an ``adr`` document with full frontmatter and ``body`` under ``root``.

    Non-empty frontmatter makes it a typed artifact to
    :func:`knowledge.corpus_loader.load_corpus`; ``status`` places the document
    in (or out of) the accepted set, and ``body`` supplies the Markdown content
    (and changelog) sections the current-system view projects.
    """
    frontmatter: dict[str, object] = {
        "type": "adr",
        "id": doc_id,
        "title": f"Render subject {doc_id}",
        "status": status,
        "created": "2026-07-01",
        "updated": "2026-07-01",
        "authors": ["someone"],
        "description": f"Render subject {doc_id}.",
        "derives-from": ["pdr-001"],
    }
    source = "---\n" + yaml.safe_dump(frontmatter, sort_keys=False) + "---\n\n" + body
    (root / "adrs").mkdir(parents=True, exist_ok=True)
    (root / "adrs" / f"{doc_id}.md").write_text(source, encoding="utf-8")


def _accepted_body() -> str:
    """The body of the accepted subject: three content sections + a changelog."""
    return (
        f"## Context\n\n{ACCEPTED_CONTENT_MARKERS[0]}\n\n"
        f"## Decision\n\n{ACCEPTED_CONTENT_MARKERS[1]}\n\n"
        f"## Consequences\n\n{ACCEPTED_CONTENT_MARKERS[2]}\n\n"
        f"## Changelog\n\n{ACCEPTED_CHANGELOG_MARKER}\n"
    )


def _non_accepted_body() -> str:
    """The body of the non-accepted subject: a single distinctive content section."""
    return (
        f"## Context\n\nSome superseded context.\n\n"
        f"## Decision\n\n{NON_ACCEPTED_CONTENT_MARKER}\n\n"
        f"## Consequences\n\nSuperseded consequences.\n"
    )


def _run_render_current_system(context: dict, doc_id: str) -> None:
    from knowledge.cli import main

    out, err = io.BytesIO(), io.BytesIO()
    rc = main(
        ["render", doc_id, "--corpus", str(context["root"]), "--view", "current-system"],
        stdout=out,
        stderr=err,
    )
    context["exit"] = rc
    context["stdout"] = out.getvalue()
    context["stderr"] = err.getvalue()


def _combined_text(context: dict) -> str:
    """The full CLI output (stdout followed by stderr) as decoded text."""
    return context["stdout"].decode("utf-8") + context["stderr"].decode("utf-8")


# --- Scenario bindings -------------------------------------------------------


@scenario(FEATURE, "render current-system view emits only the accepted content sections of a document")
def test_render_accepted_content_sections() -> None: ...


@scenario(FEATURE, "render current-system view has no rendering for a document whose status is not accepted")
def test_render_non_accepted_no_rendering() -> None: ...


# --- Given -------------------------------------------------------------------


@given(parsers.re(r'a corpus whose document "(?P<doc_id>[^"]+)" has status "accepted" and carries content sections plus a changelog section'))
def _corpus_accepted_with_changelog(context: dict, tmp_path: Path, doc_id: str) -> None:
    root = tmp_path / "corpus"
    _write_adr(root, doc_id, status="accepted", body=_accepted_body())
    context["root"] = root

    from knowledge.corpus_loader import load_corpus

    corpus = load_corpus(root)
    subject = corpus.get(doc_id)
    assert subject is not None, f"fixture invariant: {doc_id} must load as a typed artifact"
    assert subject.status == "accepted", (
        f"fixture invariant: {doc_id} must be in the accepted set: {subject.status!r}"
    )
    assert "Changelog" in subject.sections, (
        f"fixture invariant: {doc_id} must carry a changelog section: {subject.sections!r}"
    )


@given(parsers.re(r'a corpus whose document "(?P<doc_id>[^"]+)" has status "superseded"'))
def _corpus_non_accepted(context: dict, tmp_path: Path, doc_id: str) -> None:
    root = tmp_path / "corpus"
    _write_adr(root, doc_id, status="superseded", body=_non_accepted_body())
    context["root"] = root

    from knowledge.corpus_loader import load_corpus

    corpus = load_corpus(root)
    subject = corpus.get(doc_id)
    assert subject is not None, f"fixture invariant: {doc_id} must load as a typed artifact"
    assert subject.status == "superseded", (
        f"fixture invariant: {doc_id} must NOT be in the accepted set: {subject.status!r}"
    )


# --- When --------------------------------------------------------------------


@when(parsers.re(r'I run the render verb on document id "(?P<doc_id>[^"]+)" in the current-system view'))
def _run_verb(context: dict, doc_id: str) -> None:
    _run_render_current_system(context, doc_id)


# --- Then --------------------------------------------------------------------


@then("the exit code is 0")
def _exit_zero(context: dict) -> None:
    assert context["exit"] == 0, (
        f"expected the render verb to exit 0; got {context['exit']} "
        f"(stderr: {context['stderr']!r})"
    )


@then("the rendered output contains the document's accepted content sections")
def _output_has_accepted_content(context: dict) -> None:
    stdout = context["stdout"].decode("utf-8")
    for marker in ACCEPTED_CONTENT_MARKERS:
        assert marker in stdout, (
            f"the current-system rendering omits accepted content section marker "
            f"{marker!r}; rendered stdout: {stdout!r}"
        )


@then(parsers.re(r'the CLI reports that "(?P<doc_id>[^"]+)" has no current-system rendering because it is not in the accepted set'))
def _reports_no_rendering(context: dict, doc_id: str) -> None:
    combined = _combined_text(context)
    lowered = combined.lower()
    assert doc_id in combined, (
        f"the CLI does not name {doc_id!r} in its report: {combined!r}"
    )
    assert "no current-system rendering" in lowered, (
        f"the CLI does not report that {doc_id!r} has no current-system rendering: {combined!r}"
    )
    assert "not in the accepted set" in lowered, (
        f"the CLI does not report that {doc_id!r} is not in the accepted set: {combined!r}"
    )


@then(parsers.re(r'no accepted content is emitted for "(?P<doc_id>[^"]+)"'))
def _no_content_emitted(context: dict, doc_id: str) -> None:
    combined = _combined_text(context)
    assert NON_ACCEPTED_CONTENT_MARKER not in combined, (
        f"the current-system view emitted content for the non-accepted document "
        f"{doc_id!r} (marker {NON_ACCEPTED_CONTENT_MARKER!r} present): {combined!r}"
    )
