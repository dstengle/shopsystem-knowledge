Feature: The read verbs leave the corpus unchanged — a read-only invariant
  The three read verbs over the shop-knowledge CLI — navigate, render, and
  query — answer questions about a corpus without ever writing back to it. Each
  loads the corpus, projects the answer, and emits it; none materializes an
  artifact file, rewrites a document, or alters an edge. This invariant pins
  that read-only contract across all three verbs: after a verb runs its full
  read path over a corpus, every artifact file on disk is byte-for-byte what it
  was before the run, and the corpus's materialized frontmatter edges — the
  link-field graph the verbs read — are exactly as they were, with none added,
  removed, or altered. A verb that mutated the corpus while answering a read
  would be a defect this invariant catches.

  @scenario_hash:02e612708e0de104 @bc:shopsystem-knowledge
  Scenario Outline: every read verb leaves the corpus artifacts and edges unchanged
    Given a corpus whose artifact files and materialized frontmatter edges are recorded before the run
    When I run the "<verb>" verb over that corpus
    Then the exit code is 0
    And every artifact file on disk is byte-for-byte unchanged after the run
    And no materialized frontmatter edge has been added, removed, or altered

    Examples:
      | verb     |
      | navigate |
      | render   |
      | query    |
