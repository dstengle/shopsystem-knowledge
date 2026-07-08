@bc:shopsystem-knowledge
Feature: Byte-stable corpus generation
  The knowledge context generates the full projection set and index for a fixed
  decision corpus deterministically, reading only the source corpus. Generation
  embeds no ambient state — no wall-clock timestamp, no build hostname, and no
  absolute filesystem path — so two regenerations of the same corpus on
  different hosts at different times are byte-for-byte identical.

  @scenario_hash:d71b9384bb5d13d9
  Scenario: generation is byte-stable and free of ambient state
    Given a fixed decision corpus as the single source
    When the knowledge context generates the projections and index twice on two different hosts at two different times
    Then the two generated outputs are byte-for-byte identical
    And no output byte carries a timestamp, hostname, or absolute filesystem path
