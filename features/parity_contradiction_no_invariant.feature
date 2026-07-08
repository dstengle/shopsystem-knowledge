Feature: A parity claim is contradicted by a neighbour's governed change with no pre-encoded invariant
  The tier-3-OPT-IN keystone of the adversarial pass. A decision is being
  authored that claims parity — an unchanged interface — over a surface whose
  existing decision text is itself a governed CHANGE. The corpus registers no
  invariants and no baselines: there is no invariant/baseline registry in play
  at all. The PRIMARY mechanism — the adversarial authoring pass reasoning over
  the neighbour's live L1 decision text — is enough to catch the contradiction
  and cite the neighbour by id, with the tier-3 formal-invariant check strictly
  OPT-IN, never required. This proves the contradiction is caught from the
  neighbour's decision text alone, not from any stored baseline.

  @scenario_hash:f77904953e96124e @bc:shopsystem-knowledge
  Scenario: a parity claim contradicted by a neighbour's governed change is caught with no pre-encoded invariant
    Given an existing decision whose decision text changes a governed interface
    And a draft decision being authored that claims parity or an unchanged interface over that same surface
    And the corpus carries no registered invariants and no registered baselines
    When the knowledge context runs the adversarial pass over the draft against that neighbour
    Then it flags the draft as contradicting the neighbour on the basis of the neighbour's decision text
    And it cites the contradicted neighbour by id
    And it produces this verdict without requiring any pre-encoded invariant or baseline to be registered
