Feature: List what the shop has recorded
So that the user can see everything of one kind without knowing its name, the user can list what the shop has recorded.

  Background:
    Given a shop knowledge base holding three decisions, one of them superseded

  @assumes-shop-knol-is-the-only-interface
  Scenario: The user lists every decision
    When the user lists the decisions
    Then the user sees all three, each with its name and title

  @assumes-shop-knol-is-the-only-interface
  Scenario: The user lists the decisions that match a field
    When the user lists the decisions that are superseded
    Then the user sees only the superseded one

  @assumes-output-is-the-same-shape-in-yaml-and-json
  Scenario: The user lists only the names, to feed another command
    When the user lists the decisions asking for names only
    Then the user sees three names and nothing else
