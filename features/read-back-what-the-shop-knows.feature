Feature: Read back what the shop knows
So that anyone in the shop can look up what has been recorded, the user can read back what the shop knows.

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

  @slice-22
  Scenario: The user reads from a folder inside the shop's knowledge
    Pins that the shop's knowledge is found by looking upward, the way git finds a repository, so nobody has to say where it is while working in it.
    Given the user is working in a folder deep inside the directory that holds the shop's knowledge
    When the user reads the decision
    Then the user sees the decision, from the knowledge base found above where they are working

  @slice-22
  Scenario: The user reads while working elsewhere, having named the knowledge base
    Pins the other way in: naming the knowledge base outright, for work done from somewhere else entirely.
    Given the user is working outside any knowledge base, with KB_ROOT naming the shop's
    When the user reads the decision
    Then the user sees the decision, from the knowledge base KB_ROOT names

  @slice-22
  Scenario: Reading where no knowledge base can be found is refused
    Pins that with neither way in available the command stops and says so, instead of guessing or quietly answering from nothing.
    Given the user is working outside any knowledge base and nothing names one
    When the user reads the decision
    Then the command is rejected because no knowledge base was found, neither above where they are working nor named outright
    And the command reports failure to whatever ran it

  @slice-22
  Scenario: Reading with KB_ROOT naming somewhere that holds no knowledge base is refused
    Pins that a name pointing nowhere is called out as such, so a mistyped setting reads as a mistake and not as an empty shop.
    Given the user is working outside any knowledge base, with KB_ROOT naming a directory that holds no knowledge base
    When the user reads the decision
    Then the command is rejected because KB_ROOT names a directory that holds no knowledge base
    And the command reports failure to whatever ran it

  @slice-22
  Scenario: Reading from inside one knowledge base while KB_ROOT names another is refused
    Pins that when the two ways in disagree the shop refuses rather than silently pick one, since either choice could answer from the wrong corpus.
    Given the user is working inside the shop's knowledge base, with KB_ROOT naming a different one
    When the user reads the decision
    Then the command is rejected because KB_ROOT names a knowledge base other than the one they are working in, and neither of the two is guessed at
    And the command reports failure to whatever ran it

  Scenario: Reading from a directory that has been removed ends in a plain refusal
    Pins that losing the place the user was working in is refused like any other failure to find the shop's knowledge: in plain words, never a traceback.
    Given the user is working in a directory that has since been removed, and nothing names a knowledge base
    When the user reads the decision
    Then the user is shown the refusal in plain words, never a traceback
    And the command reports failure to whatever ran it

  @slice-1.27
  Scenario: Reading something whose file the shop cannot read is refused
    Pins how a file damaged by hand surfaces to a reader: a plain refusal naming the file, never a traceback to decipher.
    Given someone edited the decision's file by hand and left it in a shape the shop cannot read
    When the user reads the decision
    Then the command is rejected because that file cannot be read, naming the file
    And the user is shown that fault in plain words, never a traceback
    And the command reports failure to whatever ran it
