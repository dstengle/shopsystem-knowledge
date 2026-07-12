Feature: Coherence gate modes, doctor-form findings, and the aggregate verdict
  The coherence gate runs in a mode. In authoring mode it warns and never blocks
  — it always exits zero and never prevents an author from committing — so a
  finding surfaced while drafting is guidance, not a gate. In distribution mode
  it vetoes a blocking-severity finding by exiting non-zero, but only warns on an
  advisory-severity finding and still exits zero. Every finding is reported in
  doctor form, mirroring bd doctor: it carries the name and check-id of the check
  that raised it, a severity status, and a remediation. The gate's findings fold
  into one aggregate verdict whose exit code follows the mode and the severities
  present.

  @scenario_hash:2f25bbade70105b5 @bc:shopsystem-knowledge
  Scenario: authoring mode warns and never blocks
    Given an artifact corpus that carries a coherence finding
    When the knowledge context runs the coherence gate with mode authoring
    Then it reports the finding as a warning
    And it exits zero
    And it does not prevent the author from committing the artifact

  @scenario_hash:ece5e70d4ff79e36 @bc:shopsystem-knowledge
  Scenario: distribution mode vetoes a blocking-severity finding
    Given an artifact corpus whose coherence finding is classified as blocking severity
    When the knowledge context runs the coherence gate with mode distribution
    Then it reports the blocking finding
    And it exits non-zero

  @scenario_hash:3ddf434d9ad17704 @bc:shopsystem-knowledge
  Scenario: distribution mode only warns on an advisory-severity finding
    Given an artifact corpus whose only coherence finding is classified as advisory severity
    When the knowledge context runs the coherence gate with mode distribution
    Then it reports the advisory finding as a warning
    And it exits zero

  @scenario_hash:581c3fee5a163491 @bc:shopsystem-knowledge
  Scenario: every finding is reported in doctor form
    Given an artifact corpus that carries a coherence finding
    When the knowledge context runs the coherence gate with mode authoring
    Then the reported finding carries its check name and check-id, a severity status, and a remediation
