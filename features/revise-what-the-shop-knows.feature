Feature: Revise what the shop knows
So that what the shop knows stays true as the shop learns, the user can revise what it has recorded.

  Background:
    Given a shop knowledge base holding a decision with a purpose and a rationale, at its first version

  @assumes-shop-knol-is-the-only-interface
  Scenario: The user revises a recorded decision
    When the user replaces the decision from a file, saying who they are and why
    Then the shop holds the new wording
    And the decision is at a later version than before

  @assumes-shop-knol-is-the-only-interface
  Scenario: The user revises one part of a recorded decision
    When the user replaces the rationale of the decision from a file, saying who they are and why
    Then only the rationale changes
    And the rest of the decision reads as before
