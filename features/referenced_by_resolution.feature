Feature: Answering the referenced-by back-edge from frontmatter
  Beyond resolving the corpus into an edge set and folding the typed-edge
  coherence checks over it, the knowledge context answers the query "what
  references artifact B?". That answer is read from artifact B's own
  materialized referenced-by frontmatter field — the back-edge the reciprocity
  check requires — and is not recomputed by scanning the corpus for forward
  references edges that name B. Reading the materialized back-edge keeps the
  answer a single deterministic frontmatter lookup rather than a whole-corpus
  scan, and lets a corpus answer the query even where the forward references
  edge was never materialized on the referencing artifact.

  @scenario_hash:ebcd6ee47aed6f6d @bc:shopsystem-knowledge
  Scenario: the referenced-by back-edge is answered from frontmatter and not computed by corpus scan
    Given an artifact corpus in which artifact B carries a materialized referenced-by edge naming artifact A in its frontmatter
    When the knowledge context resolves what references artifact B
    Then it answers from artifact B's own referenced-by frontmatter field
    And it does not compute the answer by scanning the corpus for forward references edges
