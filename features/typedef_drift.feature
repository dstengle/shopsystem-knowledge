Feature: Typedef drift check over a generated template and schema fragment
  Each artifact type is defined by a typedef that emits a document template and
  a schema fragment. The generated set is committed alongside the typedef, and a
  drift check regenerates from the typedef and compares: an unchanged generated
  set passes and the check exits zero, a hand-edited generated file is caught as
  drift and the check exits non-zero naming the offending file, and regenerating
  over an unchanged typedef reproduces the generated set byte-for-byte, writing
  zero changed bytes. Generation is deterministic — it reads only the typedef.

  @scenario_hash:ad20e320470be043 @bc:shopsystem-knowledge
  Scenario: a generated set that matches its typedef passes the drift check
    Given a typedef together with a template and schema fragment that were emitted from that typedef and are unchanged
    When the knowledge context runs the drift check over the typedef and its generated set
    Then it reports no drift
    And the check exits zero

  @scenario_hash:a5c1fe90339df4ed @bc:shopsystem-knowledge
  Scenario: a hand-edited generated file is caught as drift and fails the check
    Given a typedef whose generated template or schema fragment has been hand-edited so it no longer matches what the typedef would emit
    When the knowledge context runs the drift check over the typedef and its generated set
    Then it reports drift naming the generated file that no longer matches the typedef
    And the check exits non-zero

  @scenario_hash:f8e379db80066582 @bc:shopsystem-knowledge
  Scenario: regenerating over an unchanged typedef reproduces the generated set byte-for-byte
    Given a typedef whose template and schema fragment have already been generated
    When the knowledge context regenerates the template and schema fragment from the unchanged typedef
    Then the regenerated files are byte-for-byte identical to the committed generated set
    And the regeneration writes zero changed bytes
