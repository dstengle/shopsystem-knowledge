Feature: Per-type required body sections resolved per kind
  Each artifact kind carries its own required-section set its document body must
  contain. The knowledge context checks a document's body against its own kind's
  required-section set: a kind missing one of the sections its set demands is
  reported non-conforming with the missing section named, and a kind carrying
  its full net-new required-section set passes on body structure. The set is
  resolved per kind from the single registry, so one kind's sections are never
  imposed on another.

  @bc:shopsystem-knowledge
  @scenario_hash:2fcf4828a7d65a84
  Scenario Outline: a document of its kind missing a required body section is reported non-conforming and names the section
    Given a <kind> document whose body omits the <section> section its type's required-section set demands
    When the knowledge context checks the document's body against its type's required-section set
    Then it reports the document as non-conforming for a missing required section
    And the diagnosis names <section> as the missing section

    Examples:
      | kind                  | section      |
      | adr                   | Context      |
      | adr                   | Decision     |
      | adr                   | Consequences |
      | brief                 | Summary      |
      | brief                 | Scope        |
      | prioritization-record | Ranking      |
      | prioritization-record | Rationale    |

  @bc:shopsystem-knowledge
  @scenario_hash:2514a9afbc1cf9c1
  Scenario Outline: a document carrying its kind's full net-new required-section set passes
    Given a <kind> document whose body carries <sections>
    When the knowledge context checks the document's body against its type's required-section set
    Then it reports the document as conforming on body structure
    And it names no missing required section

    Examples:
      | kind                  | sections                          |
      | adr                   | Context, Decision and Consequences |
      | brief                 | Summary and Scope                 |
      | prioritization-record | Ranking and Rationale             |
