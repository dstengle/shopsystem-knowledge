"""Step definitions for the single-source typedef-set feature.

Binds the assigned scenarios in ``typedef_single_source.feature`` and exercises
the whole per-type typedef SET (not one typedef in isolation): the eight
recognized types, the set-level format generator, its generated/read-only marks,
the drift check that covers the generated set, the shared-field-set requirement
on every schema fragment, and the current-state living-document shape.

RED leg: the set-level entry points (``typedef_type_names``,
``generate_format_set``) do not yet exist, and the registry is not yet reshaped
to the eight typedef types — so each scenario fails on the absent behaviour, not
at collection time. The entry points are imported inside the step bodies for the
same reason.
"""

from __future__ import annotations

import pytest
from pytest_bdd import given, parsers, scenario, then, when

# The eight artifact types that must each be single-sourced by a typedef.
EXPECTED_TYPEDEF_TYPES = frozenset(
    {
        "intent-record",
        "candidate",
        "session-record",
        "prioritization-record",
        "brief",
        "pdr",
        "adr",
        "current-state",
    }
)


@pytest.fixture
def context() -> dict:
    return {}


# --- Scenario bindings -------------------------------------------------------


@scenario("typedef_single_source.feature", "the typedef set covers exactly the eight artifact types")
def test_typedef_set_covers_exactly_eight() -> None: ...


# --- Given -------------------------------------------------------------------


@given("the knowledge context's set of per-type artifact typedefs")
def _typedef_set(context: dict) -> None:
    from knowledge.artifact_types import ARTIFACT_TYPES

    context["typedefs"] = ARTIFACT_TYPES


# --- When --------------------------------------------------------------------


@when("the knowledge context enumerates the artifact types that have a typedef")
def _enumerate_typedef_types(context: dict) -> None:
    from knowledge.typedefs import typedef_type_names

    context["names"] = typedef_type_names(context["typedefs"])


# --- Then --------------------------------------------------------------------


@then(
    "the enumerated set is exactly intent-record, candidate, session-record, "
    "prioritization-record, brief, pdr, adr and current-state"
)
def _enumerated_set_is_exactly_eight(context: dict) -> None:
    assert set(context["names"]) == EXPECTED_TYPEDEF_TYPES
    # Exactly eight — no duplicates hiding a missing or extra type.
    assert len(tuple(context["names"])) == 8


@then("no recognized artifact type lacks a typedef")
def _no_recognized_type_lacks_a_typedef(context: dict) -> None:
    from knowledge.artifact_types import RECOGNIZED_ARTIFACT_TYPES

    names = set(context["names"])
    for recognized in RECOGNIZED_ARTIFACT_TYPES:
        assert recognized in names, f"recognized type {recognized!r} has no typedef"


@then("no typedef declares a type outside the eight recognized artifact types")
def _no_typedef_outside_the_eight(context: dict) -> None:
    from knowledge.artifact_types import RECOGNIZED_ARTIFACT_TYPES

    recognized = set(RECOGNIZED_ARTIFACT_TYPES)
    for name in context["names"]:
        assert name in recognized, f"typedef {name!r} declares an unrecognized type"
        assert name in EXPECTED_TYPEDEF_TYPES, f"typedef {name!r} is outside the eight"
