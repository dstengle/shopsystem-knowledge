# formulated from spec/capabilities/check-the-knowledge-base.md
Feature: Check the knowledge base
  Narrator: the user, or a script, checking the shop's knowledge is sound

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

  @slice-50.13
  Scenario: The user is told what is behind its type even when the check finds faults
    Pins that a failing check does not hide what is out of date: the user sees the faults and what needs catching up in the same answer, and the shop is still called unsound only for the faults.
    Given a shop knowledge base where a decision is missing something its type requires and another decision was last checked against an older version of the decision type
    When the user checks the shop's knowledge
    Then the fault is listed, naming the artifact and the place in it at fault
    And the other decision is listed as behind its type
    And it is not listed as a fault
    And the command reports failure to whatever ran it

  @slice-1.28
  Scenario: The user checks a knowledge base holding a file the shop cannot read
    Pins that a file mangled by hand is just another fault in the list, named and explained in plain words, rather than an error that stops the check.
    Given a shop knowledge base where someone edited a decision's file by hand and left it in a shape the shop cannot read
    When the user checks the shop's knowledge
    Then that file is listed as a fault, naming the file
    And everything else the shop knows is checked and listed alongside it
    And the user is shown that fault in plain words, never a traceback
    And the command reports failure to whatever ran it

  @slice-50.18.3
  Scenario Outline: Checking where the shop's knowledge cannot be found is refused
    Pins that a check with no single knowledge base to check is refused rather than answered, so a failure to find the shop's knowledge never reads as a shop with nothing wrong.
    Given the user is working <where>
    When the user checks the shop's knowledge
    Then the command is rejected because <reason>
    And the user is shown no answer from a check, neither that nothing is wrong nor anything as behind its type
    And the command reports failure to whatever ran it

    Examples:
      | where                                                                                    | reason                                                                                                      |
      | outside any knowledge base and nothing names one                                         | no knowledge base was found, neither above where they are working nor named outright                        |
      | outside any knowledge base, with KB_ROOT naming a directory that holds no knowledge base | KB_ROOT names a directory that holds no knowledge base                                                      |
      | inside the shop's knowledge base, with KB_ROOT naming a different one                    | KB_ROOT names a knowledge base other than the one they are working in, and neither of the two is guessed at |

  @slice-76
  Scenario Outline: The user checks a knowledge base where a scenario uses a capability its capability does not depend on
    Pins that a scenario may use only what its own capability depends on, and that the check holds every shop in the knowledge base to it, not only the shop being worked on.
    Given a knowledge base holding the shop and another shop
    And a capability of <shop> that does not depend on the capability "find the knowledge base"
    And a scenario of that capability whose uses names "find the knowledge base"
    When the user checks the shop's knowledge
    Then that scenario is listed as a fault
    And the command reports failure to whatever ran it

    Examples:
      | shop            |
      | the shop        |
      | the other shop  |

  Scenario: The user checks a knowledge base where an artifact links to an artifact the knowledge base does not hold
    Pins that a link to something missing is laid at the door of the artifact that holds the link, where the user can fix it, and that it makes the shop unsound.
    Given a shop knowledge base where a capability depends on a capability the knowledge base does not hold
    When the user checks the shop's knowledge
    Then that link is listed as a fault of the capability that depends on it
    And the command reports failure to whatever ran it
