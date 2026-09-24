Feature: Retire what the shop no longer uses
So that the shop's knowledge does not fill with things it has stopped using, the user can retire what it no longer uses.

  Background:
    Given a shop knowledge base holding a tag "seasonal" that nothing points at
    And a tag "pricing" that a decision is tagged with

  @slice-42
  Scenario: The user retires something nothing points at
    Pins that the shop can be tidied: something nothing depends on can be taken out for good.
    When the user retires "seasonal", saying who they are and why
    Then the shop no longer holds it

  @slice-42
  Scenario: The user retires something that is still pointed at
    Pins that tidying never breaks a link: the shop refuses and hands back the list of things still depending on it.
    When the user retires "pricing", saying who they are and why
    Then the removal is rejected because something in the shop still points at it
    And the user is told everything that points at it
