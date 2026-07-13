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


@scenario(
    "typedef_single_source.feature",
    "each artifact type is single-sourced by its own typedef that drives the generator",
)
def test_each_type_single_sourced() -> None: ...


@scenario(
    "typedef_single_source.feature",
    "every type's generated schema fragment requires the shared field set including description",
)
def test_every_fragment_requires_shared_fields() -> None: ...


@scenario(
    "typedef_single_source.feature",
    "the current-state typedef generates a living stewarded document rather than an append-only instance",
)
def test_current_state_living_document() -> None: ...


# The shared frontmatter field set every schema fragment must require.
SHARED_FIELD_SET = frozenset(
    {"type", "id", "title", "description", "status", "created", "updated", "authors"}
)


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


# --- Set-level format generation (scenarios 1afdfb1b, 3bcea617) --------------


@when("the knowledge context runs the format generator over that typedef set")
def _run_format_generator_over_set(context: dict) -> None:
    from knowledge.typedefs import generate_format_set

    context["format_set"] = generate_format_set(context["typedefs"])


@when("the knowledge context runs the format generator over the typedef set")
def _run_format_generator_over_the_set(context: dict) -> None:
    from knowledge.typedefs import generate_format_set

    context["format_set"] = generate_format_set(context["typedefs"])


@then(parsers.parse('the set contains a typedef for the "{type_name}" artifact type'))
def _set_contains_typedef(context: dict, type_name: str) -> None:
    assert type_name in context["typedefs"], f"no typedef for {type_name!r}"
    assert type_name in context["format_set"], f"format set missing {type_name!r}"


@then(
    parsers.parse(
        'the generator emits a template and a schema fragment for "{type_name}" from its typedef'
    )
)
def _emits_template_and_fragment(context: dict, type_name: str) -> None:
    fmt = context["format_set"][type_name]
    assert fmt.template.rel_path == f"templates/{type_name}.md"
    assert fmt.schema_fragment.rel_path == f"schema/{type_name}.json"
    assert fmt.template.data, "template bytes are empty"
    assert fmt.schema_fragment.data, "schema fragment bytes are empty"


@then(
    parsers.parse(
        'the generated template and schema fragment for "{type_name}" are marked generated and read-only'
    )
)
def _marked_generated_read_only(context: dict, type_name: str) -> None:
    fmt = context["format_set"][type_name]
    for artifact in (fmt.template, fmt.schema_fragment):
        assert artifact.generated is True, f"{artifact.rel_path} not marked generated"
        assert artifact.read_only is True, f"{artifact.rel_path} not marked read-only"


@then(
    parsers.parse('the drift check covers the generated template and schema fragment for "{type_name}"')
)
def _drift_covers(context: dict, type_name: str) -> None:
    from knowledge.artifact_types import artifact_type
    from knowledge.typedefs import generate_typedef_set

    fmt = context["format_set"][type_name]
    # The drift check regenerates exactly this manifest and compares it byte for
    # byte; covering a file means the file is in that manifest with these bytes.
    drift_manifest = generate_typedef_set(artifact_type(type_name))
    for artifact in (fmt.template, fmt.schema_fragment):
        assert artifact.rel_path in drift_manifest, f"{artifact.rel_path} not drift-covered"
        assert drift_manifest[artifact.rel_path] == artifact.data


@then(
    "every generated schema fragment requires the shared field set type, id, title, "
    "description, status, created, updated and authors"
)
def _every_fragment_requires_shared_fields(context: dict) -> None:
    import json

    for type_name, fmt in context["format_set"].items():
        assert SHARED_FIELD_SET <= set(fmt.required_fields), (
            f"{type_name} required fields miss part of the shared set"
        )
        payload = json.loads(fmt.schema_fragment.data.decode("utf-8"))
        assert set(payload["shared_required_fields"]) == SHARED_FIELD_SET, (
            f"{type_name} schema fragment does not require exactly the shared field set"
        )


@then("no generated schema fragment omits description from its required set")
def _no_fragment_omits_description(context: dict) -> None:
    import json

    for type_name, fmt in context["format_set"].items():
        assert "description" in fmt.required_fields, f"{type_name} omits description"
        payload = json.loads(fmt.schema_fragment.data.decode("utf-8"))
        assert "description" in payload["shared_required_fields"], (
            f"{type_name} schema fragment omits description"
        )


# --- current-state living document (scenario d038584b) -----------------------


@given(
    "the current-state typedef, which declares a single living document stewarded "
    "in place with an incorporates list rather than an append-only numbered-series "
    "record"
)
def _current_state_typedef(context: dict) -> None:
    from knowledge.artifact_types import artifact_type

    atype = artifact_type("current-state")
    assert atype is not None
    # The typedef itself declares the living shape and its incorporates list.
    assert atype.document_shape == "living", "current-state is not declared a living document"
    assert "incorporates" in atype.extra_required_fields, "current-state declares no incorporates list"
    context["current_state"] = atype


@when("the knowledge context runs the format generator over the current-state typedef")
def _run_generator_over_current_state(context: dict) -> None:
    from knowledge.typedefs import generate_typedef_format

    context["fmt"] = generate_typedef_format(context["current_state"])


@then(
    "it emits a current-state template shaped as a single stewarded living document "
    "carrying an incorporates list"
)
def _living_template(context: dict) -> None:
    from knowledge.typedefs import LIVING_DOCUMENT_MARKER

    text = context["fmt"].template.data.decode("utf-8")
    # Carries an incorporates list (a YAML list, not a bare scalar key).
    assert "incorporates: []" in text, "template does not carry an incorporates list"
    # Shaped as a single stewarded living document, not an append-only instance.
    assert LIVING_DOCUMENT_MARKER in text, "template is not marked a living stewarded document"


@then("it emits a schema fragment for current-state from the same typedef")
def _current_state_fragment(context: dict) -> None:
    import json

    fmt = context["fmt"]
    assert fmt.schema_fragment.rel_path == "schema/current-state.json"
    payload = json.loads(fmt.schema_fragment.data.decode("utf-8"))
    assert payload["type"] == "current-state"
    # The living shape is single-sourced into the fragment too.
    assert payload["document_shape"] == "living"


@then(
    "the generated current-state template and schema fragment are marked generated "
    "and read-only under the same drift check as every other type"
)
def _current_state_marked_and_drift_covered(context: dict) -> None:
    from knowledge.typedefs import generate_typedef_set

    fmt = context["fmt"]
    for artifact in (fmt.template, fmt.schema_fragment):
        assert artifact.generated is True
        assert artifact.read_only is True
    # Same drift check as every other type: the bytes the drift check regenerates
    # and compares are exactly these.
    drift_manifest = generate_typedef_set(context["current_state"])
    for artifact in (fmt.template, fmt.schema_fragment):
        assert drift_manifest[artifact.rel_path] == artifact.data
