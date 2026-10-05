# formulated from spec/capabilities/revise-an-artifact.md
Feature: Revise an artifact
  Narrator: the user, revising what the shop has recorded

  Background:
    Given a shop knowledge base holding a decision with a purpose and a rationale, at its first version

  @slice-24
  Scenario: The user revises a recorded decision
    Pins that recorded knowledge is not frozen: new wording replaces the old and the version moves on so readers can tell something changed.
    When the user replaces the decision from a file, saying who they are and why
    Then the shop holds the new wording
    And the decision is at a later version than before

  @slice-24
  Scenario: The user revises one part of a recorded decision
    Pins that a small correction stays small: one section can be rewritten without resubmitting or disturbing the rest.
    When the user replaces the rationale of the decision from a file, saying who they are and why
    Then only the rationale changes
    And the rest of the decision reads as before

  @slice-50.18.1
  Scenario Outline: A revision whose prose the shop cannot keep is refused
    Pins that a revision is held to the same rule as a new record: text the shop cannot keep as written is refused in plain words, and what was recorded stays as it was.
    Given a file whose prose has a line ending in a space before its last line
    When the user replaces <what> from that file, saying who they are and why
    Then the change is rejected because the shop cannot keep prose in which a line before the last ends in a space, naming the place in the file
    And the user is shown that fault in plain words, never a traceback
    And the decision reads as before, still at its first version
    And the command reports failure to whatever ran it

    Examples:
      | what                          |
      | the decision                  |
      | the rationale of the decision |
