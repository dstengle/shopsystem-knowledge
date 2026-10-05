# formulated from spec/capabilities/record-what-a-piece-of-work-read.md
Feature: Record what a piece of work read
  Narrator: an agent doing a piece of work

  Background:
    Given a shop knowledge base holding a decision and a process

  @slice-38
  Scenario: An agent records what it read
    Pins how a piece of work is anchored in time: one entry in the history naming what it read and at which version, so later changes cannot rewrite what it was working from.
    When the agent records, for its piece of work, the decision and the process it read
    Then the shop's history holds one entry naming each of them with the version read
