Feature: The shop-knowledge CLI distributes templates, schema fragments, and validation
  The knowledge context ships a "shop-knowledge" command-line distribution with
  three subcommands over the single per-type typedef registry. "template <type>"
  and "schema <type>" print the canonical generated template and JSON Schema
  fragment for a recognized artifact type byte-for-byte, and both reject an
  unrecognized type by naming the offending value and the eight recognized types.
  "validate <path>" parses a document's frontmatter type and runs the same
  frontmatter and required-section checks the context uses internally, reporting
  a conforming document as conforming and a non-conforming one with every
  violation named — missing field by field name, missing section by heading —
  rather than stopping at the first or silently skipping an undeterminable type.

  @scenario_hash:f4f5ed358bd8cb05 @bc:shopsystem-knowledge
  Scenario Outline: "shop-knowledge template" prints the canonical authoring template for a recognized artifact type
    Given the installed "shop-knowledge" distribution
    When I run "shop-knowledge template <type>"
    Then the exit code is 0
    And stdout is the "<type>" typedef's generated template byte-for-byte
    And stderr is empty

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

  @scenario_hash:5b4249797a787e87 @bc:shopsystem-knowledge
  Scenario Outline: "shop-knowledge schema" prints the canonical JSON Schema fragment for a recognized artifact type
    Given the installed "shop-knowledge" distribution
    When I run "shop-knowledge schema <type>"
    Then the exit code is 0
    And stdout is the "<type>" typedef's generated schema fragment byte-for-byte
    And stderr is empty

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

  @scenario_hash:89a5c44117688941 @bc:shopsystem-knowledge
  Scenario Outline: "shop-knowledge template" and "shop-knowledge schema" both reject an unrecognized artifact type and name the offending value
    Given the installed "shop-knowledge" distribution
    When I run "shop-knowledge <subcommand> roadmap"
    Then the exit code is non-zero
    And stderr names "roadmap" as an unrecognized artifact type
    And stderr lists the eight recognized artifact types

    Examples:
      | subcommand |
      | template   |
      | schema     |

  @scenario_hash:a640a9d897c0b144 @bc:shopsystem-knowledge
  Scenario: "shop-knowledge validate" reports a conforming document as conforming
    Given a document on disk at "/tmp/example-artifact.md" whose frontmatter declares a recognized "type" and satisfies every frontmatter-required field, id pattern, and status enum for that type
    And the document's body carries every section its type's required-section set demands
    When I run "shop-knowledge validate /tmp/example-artifact.md"
    Then the exit code is 0
    And stdout reports the document as conforming
    And stdout names no violation

  @scenario_hash:a72ff18b65420b35 @bc:shopsystem-knowledge
  Scenario: "shop-knowledge validate" on a document missing a required frontmatter field reports the same named diagnosis the internal frontmatter check produces
    Given a document on disk at "/tmp/example-artifact.md" whose frontmatter omits a field its recognized type requires
    When I run "shop-knowledge validate /tmp/example-artifact.md"
    Then the exit code is non-zero
    And stdout reports the document as non-conforming
    And stdout names the missing required field by its field name

  @scenario_hash:9bfae1a9bd3103c9 @bc:shopsystem-knowledge
  Scenario: "shop-knowledge validate" on a document missing a required body section reports the same named diagnosis the internal body-section check produces
    Given a document on disk at "/tmp/example-artifact.md" whose recognized type's frontmatter is otherwise conforming but whose body omits a section that type's required-section set demands
    When I run "shop-knowledge validate /tmp/example-artifact.md"
    Then the exit code is non-zero
    And stdout reports the document as non-conforming
    And stdout names the missing required section by its section heading

  @scenario_hash:60ba623cc4f6f4b0 @bc:shopsystem-knowledge
  Scenario: "shop-knowledge validate" reports every violation on a document that carries more than one, not only the first
    Given a document on disk at "/tmp/example-artifact.md" whose frontmatter omits a required field AND whose body separately omits a required section, both for its recognized type
    When I run "shop-knowledge validate /tmp/example-artifact.md"
    Then the exit code is non-zero
    And stdout names the missing required field by its field name
    And stdout also names the missing required section by its section heading
    And stdout does not stop at the first violation found

  @scenario_hash:3c0e3cd8259c8698 @bc:shopsystem-knowledge
  Scenario: "shop-knowledge validate" on a document whose frontmatter omits or misdeclares the type field reports that specific diagnosis rather than skipping validation
    Given a document on disk at "/tmp/example-artifact.md" whose frontmatter omits the "type" field, or declares a "type" value outside the eight recognized artifact types
    When I run "shop-knowledge validate /tmp/example-artifact.md"
    Then the exit code is non-zero
    And stdout reports the document as non-conforming for a missing or unrecognized type
    And stdout does not silently skip validation for lack of a determinable type
