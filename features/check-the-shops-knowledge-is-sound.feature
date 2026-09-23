Feature: Check the shop's knowledge is sound
So that the shop can trust what it has recorded, the user can check its knowledge is sound.

  @slice-75
  Scenario: The user checks a sound knowledge base
    Given a shop knowledge base where everything fits its type
    When the user checks the shop's knowledge
    Then the user is told nothing is wrong

  @slice-76
  Scenario: The user checks a knowledge base with faults
    Given a shop knowledge base where a decision is missing something its type requires and a work item points at something the shop does not hold
    When the user checks the shop's knowledge
    Then both faults are listed, each naming the artifact and the place in it at fault
    And the command reports failure to whatever ran it

  @slice-77
  Scenario: The user is told what is behind its type
    Given a shop knowledge base where a decision was last checked against an older version of the decision type
    When the user checks the shop's knowledge
    Then that decision is listed as behind its type
    And it is not listed as a fault
