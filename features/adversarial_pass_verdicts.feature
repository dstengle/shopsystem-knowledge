@bc:shopsystem-knowledge
Feature: Adversarial pass assigns a verdict per surfaced neighbour
  The authoring-time discovery pass surfaces the existing decisions relevant to
  a draft; the adversarial pass is the coherence step that runs next. Over the
  draft and the set of surfaced neighbours (each carrying its id, L0 card and
  verbatim L1 extract — no L2), it assigns EXACTLY ONE verdict per surfaced
  neighbour: whether the draft is covered by, contradicts, or supersedes that
  neighbour. Every verdict cites the neighbour it is about BY ID, so the set of
  cited ids equals the set of surfaced neighbour ids. This is the primary
  coherence mechanism (adversarial authoring) — verdicts are derived from the
  neighbour's L0/L1 material and the draft's decision text, deterministically,
  with no pre-encoded invariants or baselines and without re-loading the whole
  corpus. The covered / contradict / supersede case behaviours build directly on
  this pass.

  @bc:shopsystem-knowledge
  @scenario_hash:bea7c4aa89633418
  Scenario: the discovery pass answers covered, contradicts and supersedes for each surfaced neighbour with a citation
    Given a draft decision being authored and a set of surfaced neighbours from the L0/L1 index
    When the knowledge context runs the adversarial pass over the draft against those neighbours
    Then for each surfaced neighbour it returns a verdict on whether the draft is covered by, contradicts, or supersedes that neighbour
    And each verdict cites the neighbour it is about by id
