Feature: L1 distribution to bounded contexts
  The knowledge context pours its L1 decision digest to BC channels, gated by the
  distribution-mode coherence check: a coherent corpus pours, a blocking finding
  refuses the pour, and only L0 and L1 projections ever cross the boundary — an
  L2 full document never does.

  @scenario_hash:218fa351bb1d48b5 @bc:shopsystem-knowledge
  Scenario: a coherent corpus pours its L1 digest to BCs
    Given an artifact corpus whose distribution-mode coherence check passes with no blocking finding
    When the knowledge context runs the L1 distribution
    Then it delivers the L1 decision digest to the BC channel

  @scenario_hash:353190f53fe739d2 @bc:shopsystem-knowledge
  Scenario: a blocking-severity finding refuses the pour
    Given an artifact corpus whose distribution-mode coherence check surfaces a blocking-severity finding
    When the knowledge context runs the L1 distribution
    Then it refuses to pour the L1 decision digest and delivers no digest to any BC
    And it reports the blocking finding that refused the pour

  @scenario_hash:88f923b94cdebd0d @bc:shopsystem-knowledge
  Scenario: L2 full documents never cross the distribution boundary
    Given an artifact corpus and a BC that consumes distributed knowledge
    When the knowledge context runs the L1 distribution
    Then only L0 and L1 projections cross to the BC channel
    And no L2 full document is delivered to any BC
