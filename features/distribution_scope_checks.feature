Feature: Distribution-scope coherence checks over a corpus
  Beyond the artifact-lifecycle and typed-edge checks, the knowledge context
  runs a distribution-scope coherence check over its artifact corpus. The
  corpus the knowledge context ranges over is resident on the lead host; an
  artifact in it that carries a distribution value of bc-local is misfiled —
  bc-local artifacts belong in a BC repo, not on the lead host. The check
  produces a misfiled-bc-local finding that names the offending artifact by id,
  carries its own check-id and a remediation to relocate the artifact to its BC
  repo or correct its distribution scope, and folds into the same aggregate
  verdict that exits non-zero on any blocking defect.

  @scenario_hash:e15914fade4a5406 @bc:shopsystem-knowledge
  Scenario: a lead-host artifact carrying distribution bc-local is flagged as misfiled
    Given an artifact corpus resident on the lead host in which an artifact carries a distribution value of bc-local
    When the knowledge context runs the distribution-scope coherence check over the corpus
    Then it reports a misfiled-bc-local finding naming the artifact by id
    And the finding carries its check-id and a remediation to relocate the artifact to its BC repo or correct its distribution scope
    And the aggregate verdict exits non-zero
