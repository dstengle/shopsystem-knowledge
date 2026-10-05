# formulated from spec/capabilities/list-what-the-shop-holds.md
Feature: List what the shop holds
  Narrator: the user, who knows the kind of thing but no name

  Background:
    Given a shop knowledge base holding three decisions, one of them superseded

  @slice-30
  Scenario: The user lists every decision
    Pins the way in when the user knows the kind of thing but no name: the whole set, each entry identified well enough to pick from.
    When the user lists the decisions
    Then the user sees all three, each with its name and title

  @slice-30
  Scenario: The user lists the decisions that match a field
    Pins narrowing the list by what a field says, so the user can ask for a subset without reading each one.
    When the user lists the decisions that are superseded
    Then the user sees only the superseded one

  @slice-30
  Scenario: The user lists only the names, to feed another command
    Pins the bare shape meant for machines: names alone, so the list can be piped into the next command.
    When the user lists the decisions asking for names only
    Then the user sees three names and nothing else
