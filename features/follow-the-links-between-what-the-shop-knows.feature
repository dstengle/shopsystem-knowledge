Feature: Follow the links between what the shop knows
So that the user can see how the shop's knowledge hangs together, the user can follow the links between what it knows.

  Background:
    Given a shop knowledge base where a decision supersedes an older decision
    And two work items point at that decision
    And the older decision is tagged "pricing"

  @slice-47
  Scenario: The user sees what a decision points at
    When the user follows the links out of the decision
    Then the user sees the older decision

  @slice-48
  Scenario: The user sees what points at a decision
    When the user follows the links into the decision
    Then the user sees both work items

  @slice-49
  Scenario: The user narrows the links to one kind of link and one kind of thing
    When the user follows the links into the decision, only through the link a work item uses, and only from work items
    Then the user sees both work items and nothing else

  @slice-50
  Scenario: The user follows the links two steps out
    When the user follows the links out of the decision two steps
    Then the user sees the older decision and the tag "pricing"
    And the user sees the route taken to each of them
