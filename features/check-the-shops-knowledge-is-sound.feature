Feature: Check the shop's knowledge is sound
So that the shop can trust what it has recorded, the user can check its knowledge is sound.

  @slice-44
  Scenario: The user checks a sound knowledge base
    Pins the clean answer: when nothing is wrong the check says so plainly, so a quiet run is a signal and not a silence.
    Given a shop knowledge base where everything fits its type
    When the user checks the shop's knowledge
    Then the user is told nothing is wrong

  @slice-44
  Scenario: The user checks a knowledge base with faults
    Pins that one check finds every fault at once and names where each one is, and that a script running it can tell the shop is unsound.
    Given a shop knowledge base where a decision is missing something its type requires and a work item points at something the shop does not hold
    When the user checks the shop's knowledge
    Then both faults are listed, each naming the artifact and the place in it at fault
    And the command reports failure to whatever ran it

  @slice-44
  Scenario: The user is told what is behind its type
    Pins the line between out of date and broken: something last checked against an older version of its type is reported so it can be caught up, but the shop is not called unsound for it.
    Given a shop knowledge base where a decision was last checked against an older version of the decision type
    When the user checks the shop's knowledge
    Then that decision is listed as behind its type
    And it is not listed as a fault

  @slice-1.28
  Scenario: The user checks a knowledge base holding a file the shop cannot read
    Pins that a file mangled by hand is just another fault in the list, named and explained in plain words, rather than an error that stops the check.
    Given a shop knowledge base where someone edited a decision's file by hand and left it in a shape the shop cannot read
    When the user checks the shop's knowledge
    Then that file is listed as a fault, naming the file
    And everything else the shop knows is checked and listed alongside it
    And the user is shown that fault in plain words, never a traceback
    And the command reports failure to whatever ran it
