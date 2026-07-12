Feature: Typed-edge coherence checks over a corpus
  Beyond the artifact-lifecycle checks, the knowledge context runs a set of
  typed-edge coherence checks over an artifact corpus. Edges are resolved from
  frontmatter link fields only — supersedes, superseded-by, derives-from,
  session, brief, candidate, produced, incorporates — never from body prose. A
  supersede must be symmetric (the target must carry a superseded-by back-edge),
  a superseded artifact must set its status to superseded, every link-field
  target must resolve to an artifact present in the corpus, and the supersede
  graph must be acyclic. Each finding carries its own check-id, blocking
  severity, and a remediation, and the findings fold into the same aggregate
  verdict that exits non-zero on any defect. The governed-delta invariant
  tripwire is opt-in: it is evaluated only against artifacts that register a
  governed-delta invariant, and skips artifacts that register none.

  @scenario_hash:bf193a08baeca6a5 @bc:shopsystem-knowledge
  Scenario: an asymmetric supersede without a back-edge is flagged
    Given an artifact corpus in which artifact A declares that it supersedes artifact B
    And artifact B carries no superseded-by edge back to A
    When the knowledge context runs the typed-edge coherence checks over the corpus
    Then it reports an asymmetric-supersede finding naming A and B by id
    And the finding carries its check-id and a remediation to write the superseded-by back-edge on B
    And the aggregate verdict exits non-zero

  @scenario_hash:78018b7a77377e6b @bc:shopsystem-knowledge
  Scenario: a list-valued supersedes with one missing per-pair back-edge is flagged
    Given an artifact corpus in which artifact A declares that it supersedes a list of artifacts B and C
    And artifact B carries a superseded-by edge back to A
    And artifact C carries no superseded-by edge back to A
    When the knowledge context runs the typed-edge coherence checks over the corpus
    Then it reports an asymmetric-supersede finding naming A and C by id for the missing back-edge
    And it reports no asymmetric-supersede finding for the resolved A and B pair
    And the aggregate verdict exits non-zero

  @scenario_hash:108a7e052c710d45 @bc:shopsystem-knowledge
  Scenario: a list-valued supersedes with every per-pair back-edge present passes
    Given an artifact corpus in which artifact A declares that it supersedes a list of artifacts B and C
    And artifacts B and C each carry a superseded-by edge back to A
    And artifacts B and C each carry a superseded status
    When the knowledge context runs the typed-edge coherence checks over the corpus
    Then it reports no asymmetric-supersede finding for A
    And the aggregate verdict exits zero

  @scenario_hash:e983ffe0fd0f8456 @bc:shopsystem-knowledge
  Scenario: a superseded artifact whose status is not superseded is flagged
    Given an artifact corpus in which artifact B is superseded by artifact A yet artifact B's status is not superseded
    When the knowledge context runs the typed-edge coherence checks over the corpus
    Then it reports an active-yet-superseded finding naming B by id
    And the finding carries its check-id and a remediation to set B's status to superseded
    And the aggregate verdict exits non-zero

  @scenario_hash:a2f381efec69a4dd @bc:shopsystem-knowledge
  Scenario Outline: a link field pointing to a target absent from the corpus is flagged
    Given an artifact corpus in which an artifact declares a <link-field> edge to a target id that is not present in the corpus
    When the knowledge context runs the typed-edge coherence checks over the corpus
    Then it reports a dangling-edge finding naming the source artifact and the unresolved target id on its <link-field> edge
    And the finding carries its check-id and a remediation
    And the aggregate verdict exits non-zero

    Examples:
      | link-field    |
      | supersedes    |
      | derives-from  |
      | session       |
      | brief         |
      | candidate     |
      | produced      |
      | incorporates  |

  @scenario_hash:2d1e857cebe9bb38 @bc:shopsystem-knowledge
  Scenario: a supersede cycle is flagged
    Given an artifact corpus in which artifact A supersedes artifact B and artifact B supersedes artifact A
    When the knowledge context runs the typed-edge coherence checks over the corpus
    Then it reports a supersede-cycle finding naming the artifacts in the cycle by id
    And the finding carries its check-id and a remediation
    And the aggregate verdict exits non-zero

  @scenario_hash:06e15d23af5e7474 @bc:shopsystem-knowledge
  Scenario: an id mentioned only in body prose creates no graph edge
    Given an artifact corpus in which an artifact's body prose references another present artifact's id but its frontmatter carries no link field naming that id
    When the knowledge context runs the typed-edge coherence checks over the corpus
    Then it forms no edge from the prose mention because the gate resolves frontmatter link fields only
    And it reports no dangling-edge finding arising from the prose mention
    And the aggregate verdict exits zero

  @scenario_hash:e8cdd261ed7a2325 @bc:shopsystem-knowledge
  Scenario: a load-bearing prose mention promoted to derives-from becomes a resolved graph edge
    Given an artifact whose previously prose-only reference to an upstream artifact has been promoted into its derives-from frontmatter field
    And that upstream artifact is present in the corpus
    When the knowledge context runs the typed-edge coherence checks over the corpus
    Then it resolves a derives-from edge from the promoting artifact to the upstream artifact
    And it reports no dangling-edge finding for that edge

  @scenario_hash:a42f119a97f362f8 @bc:shopsystem-knowledge
  Scenario: a clean corpus passes with a success aggregate verdict
    Given an artifact corpus whose supersede edges are all symmetric, whose superseded artifacts are all set to superseded status, whose link-field targets all resolve, and which contains no supersede cycle
    When the knowledge context runs the typed-edge coherence checks over the corpus
    Then it reports no findings
    And the aggregate verdict exits zero

  @scenario_hash:0921f02f6d4ac7fc @bc:shopsystem-knowledge
  Scenario: multiple defects fold into one aggregate verdict
    Given an artifact corpus carrying both an asymmetric-supersede defect and a dangling-edge defect
    When the knowledge context runs the typed-edge coherence checks over the corpus
    Then it reports both findings, each named by its own check-id
    And it folds them into a single aggregate verdict that exits non-zero

  @scenario_hash:f6c211e571ec7a64 @bc:shopsystem-knowledge
  Scenario: the governed-delta invariant tripwire is opt-in and skips artifacts that register none
    Given an artifact that registers no governed-delta invariant
    And a separate artifact that opts in by registering a governed-delta invariant over a governed surface
    When the knowledge context runs its coherence checks over the corpus
    Then it evaluates no governed-delta tripwire against the artifact that registered none
    And it evaluates the governed-delta tripwire only against the artifact that opted in
