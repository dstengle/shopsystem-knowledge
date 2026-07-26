# RETIRED SCENARIO (provenance — outside every canonical scenario region, ADR-064 D2):
#   original hash d038584b238f2fee (block-only scenario hash of the deleted body)
#   title: "the current-state typedef generates a living stewarded document rather
#           than an append-only instance"
#   Retired per ADR-069 D7 — current-state is now a versioned append-only instance,
#   NOT a living stewarded document. The old living-document contract is superseded.
#   work_id: lead-4vvdo
#   (The scenario body is deleted from the live block region above the Feature; this
#    comment carries no @scenario-hash tag token, so no block-only recompute reaches it.)
Feature: Each artifact type is single-sourced by its own typedef
  The knowledge context recognizes exactly eight artifact types, and each is
  single-sourced by its own per-type typedef. The format generator runs over the
  whole typedef set: from each typedef it emits a document template and a schema
  fragment, marks that generated set generated and read-only, and the drift check
  covers it. The typedef set covers exactly the eight types — no recognized type
  lacks a typedef and no typedef declares a type outside the eight. Every schema
  fragment requires the shared field set including description. (The current-state
  typedef's living-document contract was retired per ADR-069 D7 — current-state is
  now a versioned append-only instance; see the retirement provenance comment above.)

  @scenario_hash:1afdfb1b5cfcbe71 @bc:shopsystem-knowledge
  Scenario Outline: each artifact type is single-sourced by its own typedef that drives the generator
    Given the knowledge context's set of per-type artifact typedefs
    When the knowledge context runs the format generator over that typedef set
    Then the set contains a typedef for the "<type>" artifact type
    And the generator emits a template and a schema fragment for "<type>" from its typedef
    And the generated template and schema fragment for "<type>" are marked generated and read-only
    And the drift check covers the generated template and schema fragment for "<type>"

    Examples:
      | type                  |
      | intent-record         |
      | candidate             |
      | session-record        |
      | prioritization-record |
      | brief                 |
      | pdr                   |
      | adr                   |
      | current-state         |

  @scenario_hash:1a1b80bd796ead01 @bc:shopsystem-knowledge
  Scenario: the typedef set covers exactly the eight artifact types
    Given the knowledge context's set of per-type artifact typedefs
    When the knowledge context enumerates the artifact types that have a typedef
    Then the enumerated set is exactly intent-record, candidate, session-record, prioritization-record, brief, pdr, adr and current-state
    And no recognized artifact type lacks a typedef
    And no typedef declares a type outside the eight recognized artifact types

  @scenario_hash:3bcea617f9a026d9 @bc:shopsystem-knowledge
  Scenario: every type's generated schema fragment requires the shared field set including description
    Given the knowledge context's set of per-type artifact typedefs
    When the knowledge context runs the format generator over the typedef set
    Then every generated schema fragment requires the shared field set type, id, title, description, status, created, updated and authors
    And no generated schema fragment omits description from its required set
