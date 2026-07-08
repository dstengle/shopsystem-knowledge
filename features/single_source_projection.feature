@bc:shopsystem-knowledge
Feature: Single-source projection generation
  The knowledge context generates every projection tier and both index
  entries deterministically from one source decision document whose
  frontmatter is the only machine truth.

  @scenario_hash:d121b489919c177e
  Scenario: L0/L1/L2 projections and the index are generated from the single source document
    Given a decision document whose only machine truth lives in its YAML frontmatter and whose body carries a recognized decision section
    When the knowledge context generates the architecture-decision projections from that single source
    Then it emits an L0 card carrying the id, title, status and description drawn from the frontmatter
    And it emits an L1 extract carrying the verbatim text of the recognized decision section
    And it emits an L2 projection that is the source document itself
    And it emits a machine index entry and a human index entry for that document, both derived from the same frontmatter
    And no projection introduces any fact that is not present in the single source
