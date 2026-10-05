# formulated from spec/capabilities/review-who-changed-what.md
Feature: Review who changed what
  Narrator: the user, seeing how the shop's knowledge came to be as it is

  Background:
    Given today is 2026-09-23
    And a shop knowledge base where the shopkeeper recorded a decision on 2026-09-21 and an agent revised it today as part of a named piece of work

  @slice-16
  Scenario: The user reviews the changes to one thing
    Pins the payoff of demanding who and why on every change: the story of one artifact reads back whole.
    When the user reviews the changes to that decision
    Then the user sees both changes, each with who made it, when, what it did and why

  @slice-36
  Scenario: The user reviews what one role did
    Pins reading the history the other way round, by who was working, rather than by what was worked on.
    When the user reviews the changes made by the shopkeeper
    Then the user sees only the recording of the decision

  @slice-36
  Scenario: The user reviews what one piece of work did
    Pins that a single job's whole footprint on the shop's knowledge can be pulled out on its own.
    When the user reviews the changes made for that piece of work
    Then the user sees only the revision made by the agent

  @slice-36
  Scenario: The user reviews the changes since a date
    Pins the question of what has moved lately, which is how anyone catches up after time away.
    When the user reviews the changes since 2026-09-22
    Then the user sees only the revision made today
