# formulated from spec/capabilities/start-a-knowledge-base.md
Feature: Start a knowledge base
  Narrator: the user, setting up the shop's knowledge base

  @slice-4
  Scenario: The user starts a knowledge base and the shop's types are ready
    Pins that a new knowledge base arrives furnished with the shop's seven kinds of thing, so nobody has to define a type before recording anything.
    Given the user is working in an empty directory for the shop's knowledge
    When the user starts a shop knowledge base there without naming a directory, saying who they are
    Then the shop can hold decisions, features, work items, roles, processes, steps and tags
    And the user defines nothing of their own before recording the first one

  @slice-47
  Scenario: The shop's knowledge sits in a place of its own inside the directory it was started in
    Pins that the shop's knowledge keeps to its own corner, so it can live alongside the shop's other work without mingling with it.
    Given the user is working in a directory holding work of the shop's that is not its knowledge
    When the user starts a shop knowledge base there without naming a directory, saying who they are
    Then the shop's knowledge is kept in a place of its own inside that directory
    And the work that was already in that directory is left as it was

  @slice-50.8
  Scenario: The user starts a knowledge base somewhere else on purpose by naming the place
    Pins that naming a place is the only way to start the shop's knowledge away from where the user works, so it lands elsewhere only when they mean it to.
    Given the user is working in one directory, and another directory is empty
    When the user starts a shop knowledge base in the other directory by naming it, saying who they are
    Then the shop's knowledge is kept in a place of its own inside the named directory
    And the directory they are working in holds no knowledge base

  @slice-47
  Scenario: Starting a knowledge base asks for no reason
    Pins the one exception to always saying why: starting the shop explains itself, and the setting up still shows in the history.
    Given the user is working in an empty directory for the shop's knowledge
    When the user starts a shop knowledge base there without naming a directory, saying who they are and giving no reason
    Then the shop's knowledge base is started
    And everything it was given is recorded in the shop's history under a reason the command writes itself

  @slice-47
  Scenario: Starting a knowledge base without saying who is refused
    Pins that the who rule holds from the very first change, and that a refused start leaves nothing half-made behind.
    Given the user is working in an empty directory for the shop's knowledge
    And the user has not said which role they are
    When the user starts a shop knowledge base there without naming a directory
    Then starting the knowledge base is rejected because starting one must say which role did it
    And that directory holds no knowledge base
    And the command reports failure to whatever ran it

  @slice-47
  Scenario: Starting a knowledge base where the directory already holds one is refused
    Pins the protection against starting over by accident: an existing knowledge base is never overwritten.
    Given the user is working in a directory that already holds the shop's knowledge
    When the user starts a shop knowledge base there without naming a directory, saying who they are
    Then starting the knowledge base is rejected because that directory already holds a knowledge base
    And everything the shop already knows is still there, unchanged

  @slice-47
  Scenario: Starting a knowledge base inside one the shop already has is refused
    Pins that knowledge bases never nest, so looking upward from anywhere can only ever find one.
    Given the user is working in a directory that sits inside the shop's knowledge
    When the user starts a shop knowledge base there without naming a directory, saying who they are
    Then starting the knowledge base is rejected because that directory is inside a knowledge base
    And everything the shop already knows is still there, unchanged

  @slice-50.18
  Scenario: Starting a knowledge base from a directory that has been removed ends in a plain refusal
    Pins that even the first command, with nowhere to put what it would make, stops in words the user can read and never in a traceback.
    Given the user is working in a directory that has since been removed
    When the user starts a shop knowledge base there without naming a directory, saying who they are
    Then starting the knowledge base is rejected because the directory they are working in is gone
    And the user is shown the refusal in plain words, never a traceback
    And the command reports failure to whatever ran it

  @slice-50.17
  Scenario: Starting a knowledge base in a directory given an empty name is refused
    Pins that an empty name is never taken to mean "here": the user who meant to name a place and named none is told so, and nothing is started where they happen to be working.
    Given the user is working in an empty directory for the shop's knowledge
    When the user starts a shop knowledge base in a directory whose name is given empty, saying who they are
    Then starting the knowledge base is rejected because the directory it was given has an empty name, which names no place
    And the directory they are working in holds no knowledge base
    And the command reports failure to whatever ran it
