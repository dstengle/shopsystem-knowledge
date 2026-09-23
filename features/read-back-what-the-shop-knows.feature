Feature: Read back what the shop knows
So that anyone in the shop can look up what has been recorded, the user can read back what the shop knows.

  Background:
    Given a shop knowledge base holding a decision with a purpose and a rationale, tagged "pricing", superseding an older decision, and pointed at by two work items

  @slice-1
  Scenario: The user reads a decision at a glance
    When the user reads the decision
    Then the user sees its name, its title and the few fields the shop shows for a decision
    And the user sees a stub of each thing it points at
    And the user sees how many things point back at it, and of what kind

  @slice-21
  Scenario: The user reads one section of a decision
    When the user reads the rationale of the decision
    Then the user sees that section and nothing else

  @slice-21
  Scenario: The user reads the whole decision
    When the user reads the whole decision
    Then the user sees every field, every section and every part it holds
    And what it points at is shown by name only

  @slice-21
  Scenario: The user reads a decision with the things it points at filled in
    When the user reads the whole decision asking for what it points at to be filled in, without saying how far
    Then the superseded decision is shown in place of the pointer, as the shop holds it now
    And what that older decision points at is shown by name only

  @slice-21
  Scenario: The user asks for the links to be followed two steps
    Given the older decision is tagged "seasonal"
    When the user reads the whole decision asking for what it points at to be filled in two steps
    Then the superseded decision is shown in place of the pointer
    And the tag "seasonal" is shown in place of the pointer inside it

  @slice-21
  Scenario: The user takes the same answer as JSON
    When the user reads the decision asking for JSON
    Then the user gets the same answer as the default, written as JSON
