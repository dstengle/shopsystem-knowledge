Feature: A draft that replaces a prior decision is flagged supersedes and names the supersede edge
  The supersedes case of the adversarial pass, carried one step further to name
  the typed edge the draft owes. When a decision is being authored that REPLACES
  a prior accepted decision on a question, the authoring-time discovery flow
  surfaces the prior decision as a neighbour and the adversarial pass flags the
  draft as SUPERSEDES — citing the prior decision BY ID. On top of that verdict
  the pass names the typed supersede EDGE the draft owes: a "supersedes" edge
  from the draft to the prior decision, identified by the prior decision's id.
  The edge is a thin, deterministic derivation from the supersedes verdict and
  the cited neighbour id — no new classification, no pre-encoded invariants or
  baselines. This is the specific supersede-edge naming the shape-level
  adversarial pass answers for a prior decision the draft replaces.

  @scenario_hash:4f85b0b3af16073e @bc:shopsystem-knowledge
  Scenario: a draft that replaces a prior decision is flagged supersedes and names the supersede edge to write
    Given an existing accepted decision on a question
    And a draft decision being authored that replaces that prior decision
    When the knowledge context runs the authoring-time discovery pass over the draft
    Then it flags the draft as superseding the prior decision
    And it names the typed supersede edge the draft owes to the prior decision by id
