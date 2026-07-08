Feature: Authoring-time discovery of relevant neighbours
  When a decision is being authored, the knowledge context runs an
  authoring-time discovery pass that surfaces the existing decisions relevant
  to the draft. The pass reads the L0/L1 index — each existing decision's L0
  card and L1 extract — rather than loading the whole corpus (the L2 bodies)
  into the pass, and it names each surfaced neighbour by id. This discovery
  pass is the coherence mechanism the verdict, covered, contradict and
  supersede passes build on: each surfaced neighbour carries enough material
  (its id, L0 card and L1 extract) for a downstream adversarial pass to cite it
  by id without re-loading the whole corpus.

  @scenario_hash:60f070ecddc891e5 @bc:shopsystem-knowledge
  Scenario: the authoring event triggers discovery and surfaces the relevant neighbours via the L0/L1 index
    Given a corpus of existing decisions with generated L0 cards and L1 extracts
    And a draft decision being authored on a topic that overlaps a subset of those decisions
    When the knowledge context runs the authoring-time discovery pass over the draft
    Then it surfaces the subset of existing decisions relevant to the draft, named by id
    And it selects those neighbours from the L0/L1 index rather than loading the whole corpus into the pass
