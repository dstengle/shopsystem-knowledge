"""Step definitions for the byte-stable corpus-generation outer-loop scenario.

Binds @scenario_hash:d71b9384bb5d13d9 — "generation is byte-stable and free of
ambient state" — and asserts both Then/And legs:

* generating the projections and index for a fixed corpus twice, under two
  distinct ambient contexts (different hostname, HOME, cwd and time source),
  yields byte-for-byte identical output; and
* no output byte carries a timestamp, a hostname, or an absolute filesystem
  path.

RED leg: the corpus-generation entry point ``generate_corpus`` does not yet
exist, so it is imported inside the ``When`` step body — the scenario fails at
that step (behaviour absent), not at collection/import time. The GREEN leg adds
a deterministic ``generate_corpus`` and makes both legs pass.
"""

from __future__ import annotations

import re
import time
from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "corpus"

# Two distinct ambient contexts. Generation must be independent of every one of
# these values: hostname, HOME, cwd, and the wall-clock time source. The
# concrete strings are what the "no output byte carries ..." leg searches for.
_AMBIENT_A = {
    "hostname": "host-alpha-11111111",
    "home": "/home/alpha-9999",
    "now": 1000000000.0,
}
_AMBIENT_B = {
    "hostname": "host-bravo-22222222",
    "home": "/root/bravo-8888",
    "now": 2000000000.0,
}

# A conservative ISO-8601-ish timestamp pattern (e.g. 2026-07-08T12:34:56).
_TIMESTAMP_RE = re.compile(rb"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}")


@pytest.fixture
def context() -> dict:
    return {}


@scenario(
    "byte_stable_generation.feature",
    "generation is byte-stable and free of ambient state",
)
def test_byte_stable_generation() -> None:
    """Outer-loop binding; step bodies below carry the assertions."""


@given("a fixed decision corpus as the single source")
def _fixed_corpus(context: dict) -> None:
    sources = {
        path.stem: path.read_text(encoding="utf-8")
        for path in sorted(FIXTURE_DIR.glob("*.md"))
    }
    # Guard the corpus's own preconditions so a later fixture edit cannot
    # silently weaken the scenario: at least two conforming documents, each with
    # frontmatter and a recognized decision heading.
    assert len(sources) >= 2, "corpus must carry at least two documents"
    for name, src in sources.items():
        assert src.startswith("---\n"), f"{name} must open with YAML frontmatter"
        assert (
            "## Decision" in src or "## Decision Outcome" in src
        ), f"{name} body must carry a recognized decision heading"
    context["corpus"] = sources


@when(
    "the knowledge context generates the projections and index twice on two "
    "different hosts at two different times"
)
def _generate_twice(context: dict, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    # Imported here (not at module top) so the RED commit fails at this step on
    # the absent behaviour, not on a collection-time ImportError.
    from knowledge.projections import generate_corpus

    corpus = context["corpus"]

    def run(ambient: dict, cwd: Path):
        cwd.mkdir(parents=True, exist_ok=True)
        with monkeypatch.context() as m:
            m.setenv("HOSTNAME", ambient["hostname"])
            m.setenv("HOST", ambient["hostname"])
            m.setenv("HOME", ambient["home"])
            m.setattr(time, "time", lambda: ambient["now"])
            m.chdir(cwd)
            return generate_corpus(corpus)

    context["manifest_a"] = run(_AMBIENT_A, tmp_path / "host-a")
    context["manifest_b"] = run(_AMBIENT_B, tmp_path / "host-b")


@then("the two generated outputs are byte-for-byte identical")
def _byte_identical(context: dict) -> None:
    manifest_a = context["manifest_a"]
    manifest_b = context["manifest_b"]

    # Every emitted value is raw bytes (a byte manifest, not decoded text).
    for value in list(manifest_a.values()) + list(manifest_b.values()):
        assert isinstance(value, (bytes, bytearray)), "outputs must be raw bytes"

    # Byte-for-byte identity across the two ambient contexts, including path
    # order — comparing the ordered items catches any ordering non-determinism
    # that plain dict equality would hide.
    assert list(manifest_a.items()) == list(manifest_b.items())


@then("no output byte carries a timestamp, hostname, or absolute filesystem path")
def _free_of_ambient_state(context: dict) -> None:
    manifest = context["manifest_a"]

    # Output paths (the manifest keys) must themselves be relative.
    for path in manifest:
        assert not path.startswith("/"), f"output path {path!r} is absolute"

    blob = b"".join(manifest.values())

    for ambient in (_AMBIENT_A, _AMBIENT_B):
        assert ambient["hostname"].encode("utf-8") not in blob, "output leaked a hostname"
        assert ambient["home"].encode("utf-8") not in blob, "output leaked an absolute HOME path"
        assert str(ambient["now"]).encode("utf-8") not in blob, "output leaked a time value"

    # No absolute filesystem path segment anywhere in the emitted bytes.
    for needle in (b"/home/", b"/root/", b"/tmp/", b"/workspace/"):
        assert needle not in blob, f"output leaked an absolute path segment {needle!r}"

    # No embedded ISO-8601 timestamp.
    assert _TIMESTAMP_RE.search(blob) is None, "output leaked an ISO timestamp"
