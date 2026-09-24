Feature: Follow the links between what the shop knows
So that the user can see how the shop's knowledge hangs together, the user can follow the links between what it knows.

  Background:
    Given a shop knowledge base where a decision supersedes an older decision
    And two work items point at that decision
    And the older decision is tagged "pricing"

  @slice-32
  Scenario: The user sees what a decision points at
    Pins the outward question: what does this thing itself refer to.
    When the user follows the links out of the decision
    Then the user sees the older decision

  @slice-32
  Scenario: The user sees what points at a decision
    Pins the question the shop cannot answer by reading one file: who elsewhere depends on this.
    When the user follows the links into the decision
    Then the user sees both work items

  @slice-32
  Scenario: The user narrows the links to one kind of link and one kind of thing
    Pins that the question can be made narrow, by which link and by what sort of thing, so a big corpus still gives a small answer.
    When the user follows the links into the decision, only through the link a work item uses, and only from work items
    Then the user sees both work items and nothing else

  @slice-32
  Scenario: The user follows the links two steps out
    Pins reach beyond the immediate neighbours, with the route shown so a reader can tell how each thing was arrived at.
    When the user follows the links out of the decision two steps
    Then the user sees the older decision and the tag "pricing"
    And the user sees the route taken to each of them
