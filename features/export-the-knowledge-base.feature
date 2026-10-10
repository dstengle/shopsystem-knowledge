# formulated from spec/capabilities/export-the-knowledge-base.md
Feature: Export the knowledge base
  Narrator: the user, keeping a readable copy of the shop's knowledge

  Background:
    Given a shop knowledge base holding two shops, each with its own capabilities and decisions

  Scenario: The user exports the knowledge base into an empty directory
    Pins that the readable copy of the shop's knowledge is kb's own export of everything the knowledge base holds, written where the user asked.
    Given an empty directory
    When the user exports the knowledge base into that directory
    Then the directory holds kb's export of the whole knowledge base

  Scenario: The user exports one context into an empty directory
    Pins that a single shop's knowledge can be kept on its own, as kb exports that one context.
    Given an empty directory
    When the user exports the context of one of the two shops into that directory
    Then the directory holds kb's export of that shop's context

  Scenario: The user exports the whole knowledge base and is shown its position
    Pins that a whole export says where in the knowledge base's history it was taken, so the copy can be placed against later changes.
    Given an empty directory
    When the user exports the knowledge base into that directory
    Then the user is shown the knowledge base's position in its history at the moment the export was taken

  Scenario: The user exports one context and is shown the knowledge base's position, not the context's last change
    Pins that a single context's export is placed in the history of the whole knowledge base, even when other knowledge changed after that context last did.
    Given an empty directory
    And the other shop's knowledge was changed after the first shop's last change
    When the user exports the context of the first shop into that directory
    Then the user is shown the knowledge base's position in its history at the moment the export was taken
    And the user is not shown the position of the first shop's last change

  Scenario: Exporting into a directory that is not empty is refused
    Pins that an export never mixes with or overwrites what a directory already holds: the user is told which directory, and it is left as it was.
    Given a directory that already holds a file
    When the user exports the knowledge base into that directory
    Then the export is rejected because the directory is not empty, naming the directory
    And the directory holds only the file it held before
    And the command reports failure to whatever ran it
