Feature: Retire what the shop no longer uses
So that the shop's knowledge does not fill with things it has stopped using, the user can retire what it no longer uses.

  Background:
    Given a shop knowledge base holding a tag "seasonal" that nothing points at
    And a tag "pricing" that a decision is tagged with

  @assumes-one-command-line-is-enough
  Scenario: The user retires something nothing points at
    When the user retires "seasonal", saying who they are and why
    Then the shop no longer holds it

  @assumes-passed-through-errors-are-actionable
  Scenario: The user retires something that is still pointed at
    When the user retires "pricing", saying who they are and why
    Then the removal is rejected because something in the shop still points at it
    And the user is told everything that points at it
