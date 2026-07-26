Feature: Per-type status enum conformance
  The knowledge context validates an artifact's status against the status enum
  of its own type, resolved from the single type registry. Each of the
  recognized types declares its own status enum — an adr and a pdr recognize
  proposed, accepted, superseded and rejected; a brief recognizes draft, ready,
  delivered and withdrawn; a session-record recognizes open and closed; a
  prioritization-record recognizes draft, active and superseded. A status inside
  its kind's enum conforms; a status outside it is non-conforming and the
  diagnosis names the offending value. Because the enum is resolved from the
  artifact's own type, one type's enum is never imposed on another.

  @bc:shopsystem-knowledge
  @scenario_hash:b718f46bba84455d
  Scenario Outline: a status value inside its kind's enum conforms
    Given a <kind> artifact whose frontmatter carries a status value of "<status>"
    And "<status>" is a member of the <kind> status enum
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as conforming
    And it does not report an unrecognized-status diagnosis

    Examples:
      | kind                  | status     |
      | adr                   | proposed   |
      | adr                   | accepted   |
      | adr                   | superseded |
      | adr                   | rejected   |
      | pdr                   | proposed   |
      | pdr                   | accepted   |
      | pdr                   | superseded |
      | pdr                   | rejected   |
      | brief                 | draft      |
      | brief                 | ready      |
      | brief                 | delivered  |
      | brief                 | withdrawn  |
      | session-record        | open       |
      | session-record        | closed     |
      | prioritization-record | draft      |
      | prioritization-record | active     |
      | prioritization-record | superseded |

  @bc:shopsystem-knowledge
  @scenario_hash:4ad1f47ccbd15b91
  Scenario Outline: a status value outside its kind's enum is reported non-conforming and names the offending value
    Given a <kind> artifact whose frontmatter carries a status value of "<status>"
    And "<status>" is not a member of the <kind> status enum
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming for an unrecognized status
    And the diagnosis names the offending value "<status>"

    Examples:
      | kind                  | status    |
      | adr                   | committed |
      | pdr                   | briefed   |
      | brief                 | accepted  |
      | session-record        | recorded  |
      | prioritization-record | accepted  |
