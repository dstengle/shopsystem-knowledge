Feature: Idempotent regeneration and check mode
  Projection tiers and the index are build output regenerated from the source
  corpus, never hand-edited. Regenerating over an unchanged source rewrites
  nothing — the already-materialized bytes already match what the source would
  generate — and a check mode compares the freshly generated manifest against
  the on-disk outputs, reporting no drift and a success exit status when the
  outputs are already current.

  @scenario_hash:9feadfd3e1a0efad @bc:shopsystem-knowledge
  Scenario: regeneration over an unchanged source is idempotent and the check mode reports no drift
    Given a decision corpus whose projections and index have already been generated
    When the knowledge context regenerates the projections and index over the unchanged source
    Then the regeneration writes zero changed bytes
    And running the generation in check mode over the unchanged source reports no drift and exits with a success status
