# formulated from spec/capabilities/read-an-artifact.md
Feature: Read an artifact
  Narrator: the user, reading back one artifact by its name

  Background:
    Given a shop knowledge base holding a decision with a purpose and a rationale, tagged "pricing", superseding an older decision, and pointed at by two work items

  @slice-1
  Scenario: The user reads a decision at a glance
    Pins the default answer, sized for a first look: what this is, the little it points at, and how much of the shop leans on it.
    When the user reads the decision
    Then the user sees its name, its title and the few fields the shop shows for a decision
    And the user sees a stub of each thing it points at
    And the user sees how many things point back at it, and of what kind

  @slice-22
  Scenario: The user reads one section of a decision
    Pins that a reader can ask for one piece of the prose alone, so a long artifact need not be read whole to answer a narrow question.
    When the user reads the rationale of the decision
    Then the user sees that section and nothing else

  @slice-22
  Scenario: The user reads the whole decision
    Pins the full contents of the one artifact, with pointers left as pointers, so reading deep is always a separate and deliberate ask.
    When the user reads the whole decision
    Then the user sees every field, every section and every part it holds
    And what it points at is shown by name only

  @slice-22
  Scenario: The user reads a decision with the things it points at filled in
    Pins the ordinary depth of filling links in: one step, showing what is pointed at as the shop holds it today, and stopping there.
    When the user reads the whole decision asking for what it points at to be filled in, without saying how far
    Then the superseded decision is shown in place of the pointer, as the shop holds it now
    And what that older decision points at is shown by name only

  @slice-22
  Scenario: The user asks for the links to be followed two steps
    Pins that the reader chooses how deep to go, and that the filling in carries on through the things it has already brought in.
    Given the older decision is tagged "seasonal"
    When the user reads the whole decision asking for what it points at to be filled in two steps
    Then the superseded decision is shown in place of the pointer
    And the tag "seasonal" is shown in place of the pointer inside it

  @slice-22
  Scenario: The user takes the same answer as JSON
    Pins that the shape is a choice for the consumer and not a different answer: the same content, written for a program.
    When the user reads the decision asking for JSON
    Then the user gets the same answer as the default, written as JSON

  @slice-1.27
  Scenario: Reading something whose file the shop cannot read is refused
    Pins how a file damaged by hand surfaces to a reader: a plain refusal naming the file, never a traceback to decipher.
    Given someone edited the decision's file by hand and left it in a shape the shop cannot read
    When the user reads the decision
    Then the command is rejected because that file cannot be read, naming the file
    And the user is shown that fault in plain words, never a traceback
    And the command reports failure to whatever ran it

  @slice-50.17
  Scenario: Reading something given an empty name is refused
    Pins that asking for nothing by name is refused as naming no artifact, rather than answered as if some artifact were meant.
    When the user reads an artifact whose name is given empty
    Then the command is rejected because the artifact it was given has an empty name, which names no place
    And the user is shown the refusal in plain words, never a traceback
    And the command reports failure to whatever ran it
