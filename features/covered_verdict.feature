Feature: A draft already decided elsewhere is flagged covered
  The covered case of the adversarial pass. When a decision is being authored
  that decides a question the corpus has ALREADY decided the same way, the
  authoring-time discovery flow surfaces the covering decision as a neighbour and
  the adversarial pass flags the draft as covered by it — citing the covering
  decision BY ID. The verdict is derived from the covering decision's stable L1
  decision text and the draft's own restated decision, deterministically, with no
  pre-encoded invariants or baselines. This is the specific covered verdict that
  the shape-level adversarial pass answers for a stable neighbour the draft
  restates.

  @scenario_hash:3092efb62e739d3a @bc:shopsystem-knowledge
  Scenario: a draft already decided elsewhere is flagged covered with a citation to the covering decision
    Given an existing accepted decision that already decides a question
    And a draft decision being authored that decides the same question the same way
    When the knowledge context runs the authoring-time discovery pass over the draft
    Then it flags the draft as covered by the existing decision
    And it cites the covering decision by id
