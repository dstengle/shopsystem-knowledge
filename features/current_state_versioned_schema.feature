Feature: Current-state versioned conformance against its per-type schema
  The knowledge context validates a current-state artifact against the rules of
  its type. Under ADR-069 D7 current-state became a versioned append-only
  instance: each snapshot is a numbered instance whose id matches the
  current-state-NNN pattern, whose status is a member of the versioned enum
  current or superseded, and whose frontmatter additionally requires an
  incorporates list naming the accepted decisions the snapshot reflects. Its
  body carries the Current decisions and Stewardship required sections. A
  conforming current-state artifact carries every required field, an id matching
  its type's pattern, and a status in its type's enum; a non-conforming one is
  reported with a diagnosis that names the specific missing field, offending
  value, or expected pattern. These scenarios pin the versioned current-state
  schema the type system now enforces.

  @bc:shopsystem-knowledge
  @scenario_hash:327a0a2cac055761
  Scenario: a versioned current-state instance with a current-state-NNN id and status current conforms
    Given a current-state artifact whose id is "current-state-001" and whose status is "current"
    And it carries an incorporates list naming the accepted decisions the snapshot reflects
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as conforming
    And it does not report an unrecognized-status diagnosis

  @bc:shopsystem-knowledge
  @scenario_hash:68fef1413837a594
  Scenario Outline: each value of the current-state versioned status enum conforms
    Given a current-state artifact whose frontmatter carries a status value of "<status>"
    And "<status>" is a member of the current-state status enum current or superseded
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as conforming
    And it does not report an unrecognized-status diagnosis

    Examples:
      | status     |
      | current    |
      | superseded |

  @bc:shopsystem-knowledge
  @scenario_hash:f12e9eabf88c0222
  Scenario: the singleton status live is reported non-conforming against the versioned current or superseded enum
    Given a current-state artifact whose frontmatter carries a status value of "live"
    And "live" is not a member of the current-state status enum current or superseded
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming for an unrecognized status
    And the diagnosis names the offending value "live"

  @bc:shopsystem-knowledge
  @scenario_hash:67ee9629a499470f
  Scenario: a bare current-state id is reported non-conforming against the versioned current-state-NNN pattern
    Given a current-state artifact whose id is "current-state" rather than the current-state-NNN pattern its type now requires
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming for an id that does not match its type pattern
    And the diagnosis names the offending id and the expected current-state-NNN pattern

  @bc:shopsystem-knowledge
  @scenario_hash:a9512a74882726ac
  Scenario: a current-state document carrying Current decisions and Stewardship passes body conformance
    Given a current-state document whose body carries Current decisions and Stewardship, its type's required-section set
    When the knowledge context checks the document's body against its type's required-section set
    Then it reports the document as conforming on body structure
    And it names no missing required section

  @bc:shopsystem-knowledge
  @scenario_hash:03f1fc709ff69054
  Scenario: a current-state document missing the Stewardship section is reported non-conforming and names it
    Given a current-state document whose body carries Current decisions but omits the Stewardship section its type's required-section set demands
    When the knowledge context checks the document's body against its type's required-section set
    Then it reports the document as non-conforming for a missing required section
    And the diagnosis names Stewardship as the missing section

  @bc:shopsystem-knowledge
  @scenario_hash:e3de5a93c475bce5
  Scenario: a current-state artifact omitting the required incorporates field is reported non-conforming and names it
    Given a current-state artifact whose frontmatter carries every shared required field but omits the incorporates field its type additionally requires
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming
    And the diagnosis names incorporates as the missing type-required field
