Feature: Search what the shop knows
So that the user can find knowledge without knowing where it lives, the user can search what the shop knows.

  Background:
    Given a shop knowledge base where two decisions and a process mention restocking in their prose

  Scenario: The user searches the prose
    When the user searches for restocking
    Then each result names the section it matched and shows a snippet of it
    And the one that mentions restocking most often in a section comes first

  Scenario: The user searches within one kind of thing
    When the user searches for restocking among decisions only
    Then the user sees the two decisions and not the process

  Scenario: The user searches the fields as well as the prose
    When the user searches for restocking in the fields as well as the prose
    Then the user also sees a decision whose title mentions restocking
