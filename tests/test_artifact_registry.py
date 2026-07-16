"""Unit tests for the artifact-type registry and artifact parser.

These are the foundation the Wave A schema/section/typedef behaviours (and the
later coherence-gate and digest waves) build on: a single well-documented
registry of the eight recognized artifact types, and a parser that turns one
source document (YAML frontmatter + Markdown body) into a structured
:class:`Artifact` exposing ``type``/``id``/``status``/``frontmatter`` and the
body's section headings.

RED leg: ``knowledge.artifact_types`` does not yet exist, so these tests fail on
the absent behaviour. The imports live at module top deliberately for the
registry invariants (they are the behaviour under test); the parser tests
exercise ``parse_artifact`` directly.
"""

from __future__ import annotations

import re

import pytest

from knowledge.artifact_types import (
    RECOGNIZED_ARTIFACT_TYPES,
    SHARED_REQUIRED_FIELDS,
    STORED_PROJECTION_FIELDS,
    Artifact,
    ArtifactType,
    artifact_type,
    parse_artifact,
)


def test_exactly_eight_recognized_artifact_types() -> None:
    """The system recognizes exactly eight artifact types, no more, no fewer."""
    assert len(RECOGNIZED_ARTIFACT_TYPES) == 8
    # Every recognized name resolves to an ArtifactType carrying that name.
    for name in RECOGNIZED_ARTIFACT_TYPES:
        atype = artifact_type(name)
        assert isinstance(atype, ArtifactType)
        assert atype.name == name


def test_roadmap_is_not_a_recognized_type() -> None:
    """``roadmap`` is deliberately not one of the eight recognized types."""
    assert "roadmap" not in RECOGNIZED_ARTIFACT_TYPES
    assert artifact_type("roadmap") is None


def test_shared_required_fields_are_the_eight_named_fields() -> None:
    """The shared required frontmatter fields are exactly the eight named ones."""
    assert SHARED_REQUIRED_FIELDS == (
        "type",
        "id",
        "title",
        "status",
        "created",
        "updated",
        "authors",
        "description",
    )


def test_disclosure_level_is_a_stored_projection_field() -> None:
    """disclosure-level is a projection, never a stored frontmatter field."""
    assert "disclosure-level" in STORED_PROJECTION_FIELDS


def test_candidate_type_rules() -> None:
    """The candidate type pins the cand-NNN id pattern and its status enum."""
    candidate = artifact_type("candidate")
    assert candidate is not None
    assert candidate.statuses == ("exploring", "shaped", "briefed", "committed", "parked", "rejected")
    # The id pattern accepts cand-NNN and rejects a spelled-out prefix.
    assert re.fullmatch(candidate.id_pattern, "cand-001")
    assert not re.fullmatch(candidate.id_pattern, "candidate-1")
    assert candidate.id_example == "cand-NNN"


def test_pdr_additionally_requires_decision_makers_and_derives_from() -> None:
    """The pdr type additionally requires decision-makers and derives-from."""
    pdr = artifact_type("pdr")
    assert pdr is not None
    assert "decision-makers" in pdr.extra_required_fields
    assert "derives-from" in pdr.extra_required_fields


def test_adr_requires_a_non_empty_derives_from_anchor() -> None:
    """The adr type requires derives-from and requires it to be non-empty."""
    adr = artifact_type("adr")
    assert adr is not None
    assert "derives-from" in adr.extra_required_fields
    assert "derives-from" in adr.non_empty_fields


def test_intent_record_does_not_require_the_pdr_options_section() -> None:
    """A type's required-section set is its own — intent-record != pdr."""
    pdr = artifact_type("pdr")
    intent = artifact_type("intent-record")
    assert pdr is not None and intent is not None
    assert "Options considered" in pdr.required_sections
    assert "Options considered" not in intent.required_sections


def test_parse_artifact_splits_frontmatter_and_body() -> None:
    """parse_artifact yields a structured Artifact from frontmatter + body."""
    source = (
        "---\n"
        "type: adr\n"
        "id: adr-007\n"
        "status: accepted\n"
        "authors:\n"
        "  - alice\n"
        "derives-from:\n"
        "  - pdr-003\n"
        "---\n"
        "## Context\n"
        "why\n"
        "## Decision\n"
        "what\n"
    )
    artifact = parse_artifact(source)
    assert isinstance(artifact, Artifact)
    assert artifact.type == "adr"
    assert artifact.id == "adr-007"
    assert artifact.status == "accepted"
    # List-valued frontmatter is parsed as a list, not a flattened string.
    assert artifact.frontmatter["authors"] == ["alice"]
    assert artifact.frontmatter["derives-from"] == ["pdr-003"]
    # Body section headings are exposed by their heading text.
    assert artifact.sections == ("Context", "Decision")


def test_parse_artifact_reads_an_empty_list_as_empty() -> None:
    """An inline empty derives-from list parses as an empty list, not a string."""
    source = "---\ntype: adr\nid: adr-009\nderives-from: []\n---\nbody\n"
    artifact = parse_artifact(source)
    assert artifact.frontmatter["derives-from"] == []
