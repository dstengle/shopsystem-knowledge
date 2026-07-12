Feature: L1 decision digest
  The knowledge context generates an L1 decision digest over an artifact corpus:
  exactly the accepted decisions, each entry self-contained (its own id, status,
  supersede edges and verbatim L1 decision extract), derived from the single
  source so regeneration over the unchanged source is idempotent.

  @scenario_hash:1e54b6db4a552943 @bc:shopsystem-knowledge
  Scenario: the digest contains exactly the accepted decisions and excludes the rest
    Given an artifact corpus containing accepted decisions and decisions whose status is proposed, rejected or superseded
    When the knowledge context generates the L1 decision digest over the corpus
    Then the digest contains an entry for every accepted decision
    And the digest contains no entry for any proposed, rejected or superseded decision

  @scenario_hash:203bebfdad68329c @bc:shopsystem-knowledge
  Scenario: each digest entry is self-contained
    Given an artifact corpus containing an accepted decision that supersedes a prior decision
    When the knowledge context generates the L1 decision digest over the corpus
    Then the entry for that accepted decision carries its own id, its status, its supersede edges and the verbatim L1 decision extract
    And a reader of that single entry can determine the decision, its status and what it supersedes without consulting any other entry or the source document

  @scenario_hash:f74c632acd68f308 @bc:shopsystem-knowledge
  Scenario: the digest is derived from the single source and regeneration is idempotent
    Given an artifact corpus whose L1 decision digest has already been generated
    When the knowledge context regenerates the L1 decision digest over the unchanged source
    Then the regeneration writes zero changed bytes
    And no digest entry carries any fact absent from the single source
