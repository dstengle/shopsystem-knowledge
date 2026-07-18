"""Unit tests for the filesystem corpus loader's per-type subdirectory map.

These pin the directory convention the loader walks. Every typed artifact lives
under a *plural* per-type subdirectory (candidates/ sessions/ prioritizations/
briefs/ pdrs/ adrs/); intent-record must be no exception — it is walked from
``intents/`` (plural), not ``intent/`` (singular). Product authority ratified
the directory convention as uniformly plural (David, 2026-07-17).

RED leg: the loader's ``SUBDIR_TYPES`` map currently keys intent-record on the
singular ``intent``, so ``test_loader_walks_intents_plural_for_intent_record``
fails (the plural directory is not walked) and
``test_loader_does_not_walk_intent_singular`` fails (the singular directory is
still walked).
"""

from __future__ import annotations

from pathlib import Path

from knowledge.corpus_loader import load_corpus


def _intent_record(root: Path, subdir: str) -> None:
    """Write a conforming intent-record document under ``root/<subdir>``."""
    doc = root / subdir / "intent-900.md"
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text(
        "---\n"
        "type: intent-record\n"
        "id: intent-900\n"
        "title: A recorded intent\n"
        "status: recorded\n"
        "created: 2026-07-01\n"
        "updated: 2026-07-01\n"
        "authors: [alice]\n"
        "description: an intent placed for the loader to walk\n"
        "---\n\n# Body\n",
        encoding="utf-8",
    )


def test_loader_walks_intents_plural_for_intent_record(tmp_path: Path) -> None:
    """An intent-record under ``intents/`` (plural) is loaded as a typed artifact."""
    root = tmp_path / "corpus"
    _intent_record(root, "intents")

    corpus = load_corpus(str(root))

    loaded = corpus.of_type("intent-record")
    assert len(loaded) == 1
    assert loaded[0].id == "intent-900"


def test_loader_does_not_walk_intent_singular(tmp_path: Path) -> None:
    """An intent-record under ``intent/`` (singular) is NOT walked by the loader."""
    root = tmp_path / "corpus"
    _intent_record(root, "intent")

    corpus = load_corpus(str(root))

    assert corpus.of_type("intent-record") == ()
