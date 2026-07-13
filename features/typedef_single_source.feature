Feature: Each artifact type is single-sourced by its own typedef
  The knowledge context recognizes exactly eight artifact types, and each is
  single-sourced by its own per-type typedef. The format generator runs over the
  whole typedef set: from each typedef it emits a document template and a schema
  fragment, marks that generated set generated and read-only, and the drift check
  covers it. The typedef set covers exactly the eight types — no recognized type
  lacks a typedef and no typedef declares a type outside the eight. Every schema
  fragment requires the shared field set including description, and the
  current-state typedef generates a single living stewarded document carrying an
  incorporates list rather than an append-only numbered-series instance.

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

  @scenario_hash:d038584b238f2fee @bc:shopsystem-knowledge
  Scenario: the current-state typedef generates a living stewarded document rather than an append-only instance
    Given the current-state typedef, which declares a single living document stewarded in place with an incorporates list rather than an append-only numbered-series record
    When the knowledge context runs the format generator over the current-state typedef
    Then it emits a current-state template shaped as a single stewarded living document carrying an incorporates list
    And it emits a schema fragment for current-state from the same typedef
    And the generated current-state template and schema fragment are marked generated and read-only under the same drift check as every other type

  @scenario_hash:3bcea617f9a026d9 @bc:shopsystem-knowledge
  Scenario: every type's generated schema fragment requires the shared field set including description
    Given the knowledge context's set of per-type artifact typedefs
    When the knowledge context runs the format generator over the typedef set
    Then every generated schema fragment requires the shared field set type, id, title, description, status, created, updated and authors
    And no generated schema fragment omits description from its required set
