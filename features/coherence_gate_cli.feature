Feature: The installed coherence-gate command over a corpus root directory
  The coherence gate ships as a lead-installable contract command: an operator
  points it at a corpus root directory and it walks the real directory tree —
  the per-type subdirectories and the living current-state.md — parses each
  document's YAML frontmatter into a typed artifact, and feeds the resulting
  corpus into the already-pinned lifecycle and typed-edge checks. An absent
  typed-artifact subdirectory is treated as zero instances of that type rather
  than a loader error. A frontmatter link-field target that resolves to a real
  file carrying no frontmatter is reported unverifiable-legacy — advisory, not
  dangling and not asymmetric — while a target with no corresponding file
  anywhere stays dangling. The command defaults to authoring mode, honouring the
  already-pinned authoring-mode contract, and exits with the report's verdict.

  @scenario_hash:25628c9bd2e401d6 @bc:shopsystem-knowledge
  Scenario: the gate command walks a real directory tree and feeds typed documents into the already-pinned checks
    Given a corpus root directory containing a pdr file whose frontmatter declares a supersedes edge to a second pdr file
    And that second pdr file's frontmatter carries a superseded-by edge back to the first
    When the operator runs the knowledge context's installed coherence-gate command over the corpus root directory
    Then it reports no asymmetric-supersede finding for the pair
    And the aggregate verdict exits zero

  @scenario_hash:82d9df6a97c9a173 @bc:shopsystem-knowledge
  Scenario: the gate command defaults to authoring mode
    Given a corpus root directory that carries at least one coherence finding
    When the operator runs the knowledge context's installed coherence-gate command over the corpus root directory with no mode specified
    Then it runs in authoring mode
    And it exits zero despite the finding, per the already-pinned authoring-mode contract

  @scenario_hash:cd8e26dccaf8ddb3 @bc:shopsystem-knowledge
  Scenario: an absent typed-artifact directory does not crash the loader
    Given a corpus root directory that contains no prioritizations subdirectory at all
    When the operator runs the knowledge context's installed coherence-gate command over the corpus root directory
    Then the run completes and reports an aggregate verdict
    And it treats the absent subdirectory as zero prioritization-record instances, not as a loader error

  @scenario_hash:5184003b24ca939e @bc:shopsystem-knowledge
  Scenario: a supersedes edge to a target file with no YAML frontmatter is reported unverifiable-legacy, not dangling or asymmetric
    Given a corpus root directory containing a pdr file whose frontmatter declares supersedes: [pdr-032]
    And a file named pdr-032 present in the corpus root directory carrying no YAML frontmatter at all
    When the operator runs the knowledge context's installed coherence-gate command over the corpus root directory
    Then it reports the edge as an unverifiable-legacy finding naming the pdr and pdr-032 by id
    And it reports no dangling-edge finding for that edge, because pdr-032 resolves to a real file
    And it reports no asymmetric-supersede finding for that edge, because pdr-032 has no frontmatter that could carry a superseded-by field
    And the unverifiable-legacy finding does not by itself drive the aggregate verdict non-zero

  @scenario_hash:bfb4ce1264d5021c @bc:shopsystem-knowledge
  Scenario: a current-state incorporates claim naming a legacy decision is reported unverifiable-legacy, not as an unincorporated-decision violation
    Given a corpus root directory containing a current-state.md file whose frontmatter declares incorporates: [pdr-032, pdr-033, adr-059]
    And pdr-032, pdr-033, and adr-059 are each present in the corpus root directory as files carrying no YAML frontmatter
    When the operator runs the knowledge context's installed coherence-gate command over the corpus root directory
    Then it reports each of the three incorporates edges as an unverifiable-legacy finding naming current-state and the legacy target by id
    And it reports no unincorporated-decision finding for any of the three, because their accepted status cannot yet be machine-read
    And none of the three unverifiable-legacy findings by themselves drive the aggregate verdict non-zero

  @scenario_hash:d0f0ad4d25aa409a @bc:shopsystem-knowledge
  Scenario: a link-field target with no corresponding file anywhere in the corpus is still reported dangling, distinct from the legacy case
    Given a corpus root directory containing an artifact whose frontmatter declares a supersedes edge to an id with no corresponding file anywhere in the corpus root directory
    When the operator runs the knowledge context's installed coherence-gate command over the corpus root directory
    Then it reports a dangling-edge finding naming the source artifact and the unresolved id
    And it does not report an unverifiable-legacy finding for that edge, because no file exists to be legacy
