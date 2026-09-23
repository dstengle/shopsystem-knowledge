Feature: Record a decision
So that a choice the shop has made is written down where the whole shop can find it, the user can record a decision.

  Background:
    Given a shop knowledge base holding the shop's types

  Scenario: The user records a decision
    Given a decision in a file, with a title, a purpose, a rationale and the decision it supersedes
    When the user records that file as a decision, saying who they are and why
    Then the shop holds the decision under a name the user can read it back by
    And the decision is at its first version

  Scenario: The user pipes a decision in instead of naming a file
    Given a decision produced by another command
    When the user records it by piping it in, saying who they are and why
    Then the shop holds the decision just as if it had come from a file

  Scenario: The user records a decision as part of a piece of work
    Given a decision in a file
    And the user works as the shopkeeper on a named piece of work
    When the user records that file as a decision, saying who they are and why
    Then the change is attributed to the shopkeeper and to that piece of work

  Scenario: A decision recorded by nobody is refused
    Given a decision in a file
    And the user has not said which role they are
    When the user records that file as a decision
    Then the decision is rejected because every change must say which role made it

  Scenario: A decision recorded without a reason is refused
    Given a decision in a file
    When the user records that file as a decision without a message
    Then the decision is rejected because every change must carry a message

  Scenario: A decision that does not fit the shop's decision type is refused
    Given a file missing something the shop's decision type requires
    When the user records that file as a decision, saying who they are and why
    Then the decision is rejected because it does not fit the shop's decision type
    And the user is told which artifact and which place in it is at fault
    And the command reports failure to whatever ran it
