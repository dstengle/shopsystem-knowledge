Feature: Make several changes at once
So that a set of changes that only makes sense together lands together, the user can make several changes at once.

  Background:
    Given a shop knowledge base holding the shop's types and a work item

  @assumes-shop-knol-is-the-only-interface
  Scenario: The user makes several changes at once
    Given a batch that records a decision and points the work item at it
    When the user applies the batch, saying who they are and why
    Then both changes are in the shop
    And the shop's history shows them as one change

  @assumes-a-refused-change-leaves-nothing-behind
  Scenario: One bad change in a batch leaves the shop untouched
    Given a batch whose second change does not fit its type
    When the user applies the batch, saying who they are and why
    Then the batch is rejected because a change in it does not fit its type
    And none of the changes are in the shop
    And the user is told every fault in the batch, not only the first
