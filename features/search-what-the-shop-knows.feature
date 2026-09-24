Feature: Search what the shop knows
So that the user can find knowledge without knowing where it lives, the user can search what the shop knows.

  Background:
    Given a shop knowledge base where two decisions and a process mention restocking in their prose

  @slice-33
  Scenario: The user searches the prose
    Pins the way in when neither name nor kind is known: results say where the words were found, show enough to judge, and put the strongest first.
    When the user searches for restocking
    Then each result names the section it matched and shows a snippet of it
    And the one that mentions restocking most often in a section comes first

  @slice-33
  Scenario: The user searches within one kind of thing
    Pins narrowing a search to one kind of thing, so a common word does not drown the answer.
    When the user searches for restocking among decisions only
    Then the user sees the two decisions and not the process

  @slice-33
  Scenario: The user searches the fields as well as the prose
    Pins that a search can reach past the prose into the fields, catching things whose title says it but whose body does not.
    When the user searches for restocking in the fields as well as the prose
    Then the user also sees a decision whose title mentions restocking
