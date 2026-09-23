Feature: Review who changed what
So that the shop can see how its knowledge came to be the way it is, the user can review who changed what.

  Background:
    Given today is 2026-09-23
    And a shop knowledge base where the shopkeeper recorded a decision on 2026-09-21 and an agent revised it today as part of a named piece of work

  @slice-15
  Scenario: The user reviews the changes to one thing
    When the user reviews the changes to that decision
    Then the user sees both changes, each with who made it, when, what it did and why

  @slice-35
  Scenario: The user reviews what one role did
    When the user reviews the changes made by the shopkeeper
    Then the user sees only the recording of the decision

  @slice-35
  Scenario: The user reviews what one piece of work did
    When the user reviews the changes made for that piece of work
    Then the user sees only the revision made by the agent

  @slice-35
  Scenario: The user reviews the changes since a date
    When the user reviews the changes since 2026-09-22
    Then the user sees only the revision made today
