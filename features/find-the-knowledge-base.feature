# formulated from spec/capabilities/find-the-knowledge-base.md
Feature: Find the knowledge base
  Narrator: the user, running any shop-knol command other than init

  Background:
    Given a shop knowledge base holding a decision with a purpose and a rationale, tagged "pricing", superseding an older decision, and pointed at by two work items

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

  @slice-50.22
  Scenario: The user reads from a directory that has been removed, having named the knowledge base
    Pins that a lost working directory takes away only the looking upward: naming the knowledge base outright still works, since a directory that is gone is inside no knowledge base to disagree with it.
    Given the user is working in a directory that has since been removed, with KB_ROOT naming the shop's
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

  @slice-50.22
  Scenario: Reading from a directory that has been removed ends in a plain refusal
    Pins that losing the place the user was working in is refused like any other failure to find the shop's knowledge: in plain words, never a traceback.
    Given the user is working in a directory that has since been removed, and nothing names a knowledge base
    When the user reads the decision
    Then the command is rejected because the directory they are working in is gone
    And the user is shown the refusal in plain words, never a traceback
    And the command reports failure to whatever ran it

  @slice-53
  Scenario: Reading where the knowledge base found is a connection to a server hosting the store
    Pins that a knowledge base reached through a connection to its server serves exactly as the store found in place does, so where the store lives changes nothing the user sees.
    Given the shop's knowledge base is hosted by a server
    And the user is working in a folder deep inside a directory holding a connection to that server
    When the user reads the decision
    Then the user sees the decision, just as they would from the store itself
