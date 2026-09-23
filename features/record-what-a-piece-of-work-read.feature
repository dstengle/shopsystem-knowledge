Feature: Record what a piece of work read
So that a piece of work can say which version of the shop's knowledge it was built on while the shop keeps learning, the agent can record what it read.

  Background:
    Given a shop knowledge base holding a decision and a process

  @assumes-one-command-line-is-enough
  Scenario: An agent records what it read
    When the agent records, for its piece of work, the decision and the process it read
    Then the shop's history holds one entry naming each of them with the version read
