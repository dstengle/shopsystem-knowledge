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

  @slice-54
  Scenario: Where no knowledge base is found, the shop's knowledge sits in a place of its own inside the working directory
    Pins that a new knowledge base is started only where none can be found, and then keeps to its own corner beside the shop's other work without mingling with it.
    Given the user is working in a directory holding work of the shop's that is not its knowledge
    And no knowledge base is found from that directory, neither above it nor named by KB_ROOT
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

  @slice-54
  Scenario Outline: With no directory named, an empty knowledge base kb finds from the working directory is furnished with the shop's types
    Pins that the user who works where kb's operator already started an empty knowledge base gets that one furnished, whichever way kb finds it.
    Given <situation>
    When the user starts a shop knowledge base without naming a directory, saying who they are
    Then that knowledge base holds the shop's types and nothing else of the shop's

    Examples:
      | found          | situation                                                                                                  |
      | upward         | the user is working in a folder inside a knowledge base kb's operator started empty, and nothing names one |
      | through KB_ROOT | the user is working outside any knowledge base, with KB_ROOT naming a knowledge base kb's operator started empty |

  @slice-55.2
  Scenario: With no directory named, an empty store kb reaches through a server is furnished with the shop's types
    Pins that a knowledge base reached through a server is furnished just as one found in place is.
    Given the user is working where kb finds a connection to a server hosting a store kb's operator started empty
    When the user starts a shop knowledge base without naming a directory, saying who they are
    Then that knowledge base holds the shop's types and nothing else of the shop's

  @slice-54
  Scenario: Naming a directory that holds an empty knowledge base furnishes it with the shop's types
    Pins that naming a place where kb's operator already started an empty knowledge base furnishes that one, not a second one.
    Given the user is working in one directory, and another directory holds a knowledge base kb's operator started empty
    When the user starts a shop knowledge base in the other directory by naming it, saying who they are
    Then that knowledge base holds the shop's types and nothing else of the shop's

  @slice-55
  Scenario Outline: With no directory named, starting where finding the knowledge base is refused is refused for finding's reason
    Pins that init finds the knowledge base the way every other command does, so a finding that fails stops init too instead of starting one somewhere.
    Given <situation>
    When the user starts a shop knowledge base without naming a directory, saying who they are
    Then starting the knowledge base is rejected because <reason>
    And no knowledge base is started

    Examples:
      | situation                                                                                                            | reason                                                                  |
      | the user is working outside any knowledge base, with KB_ROOT naming a directory that holds no knowledge base          | KB_ROOT names a directory that holds no knowledge base                  |
      | the user is working inside a knowledge base kb's operator started empty, with KB_ROOT naming a different one          | KB_ROOT names a knowledge base other than the one they are working in   |

  @slice-47
  Scenario: Starting a knowledge base without saying who is refused
    Pins that the who rule holds from the very first change, and that a refused start leaves nothing half-made behind.
    Given the user is working in an empty directory for the shop's knowledge
    And the user has not said which role they are
    When the user starts a shop knowledge base there without naming a directory
    Then starting the knowledge base is rejected because starting one must say which role did it
    And that directory holds no knowledge base
    And the command reports failure to whatever ran it

  @slice-54
  Scenario: Starting a knowledge base where the directory already holds one is refused
    Pins the protection against starting over by accident: an existing knowledge base is never overwritten.
    Given the user is working in a directory that already holds the shop's knowledge, and nothing names a different knowledge base
    When the user starts a shop knowledge base there without naming a directory, saying who they are
    Then starting the knowledge base is rejected because that directory already holds a knowledge base
    And everything the shop already knows is still there, unchanged

  @slice-54
  Scenario: With nothing naming another knowledge base, starting from inside one the shop already has is refused
    Pins that knowledge bases never nest, so looking upward from anywhere can only ever find one.
    Given the user is working in a directory that sits inside the shop's knowledge, and nothing names a different knowledge base
    When the user starts a shop knowledge base there without naming a directory, saying who they are
    Then starting the knowledge base is rejected because that directory is inside a knowledge base
    And everything the shop already knows is still there, unchanged

  @slice-55.1
  Scenario Outline: Starting where the knowledge base to furnish already holds the shop's types is refused
    Pins that furnishing never runs twice: a knowledge base that already has the shop's types is left exactly as it was, whether it was found or named.
    Given <situation>
    When the user starts a shop knowledge base <how>, saying who they are
    Then starting the knowledge base is rejected because it already holds the shop's knowledge
    And nothing changes

    Examples:
      | found             | situation                                                                                                      | how                                    |
      | through KB_ROOT   | the user is working outside any knowledge base, with KB_ROOT naming a knowledge base holding the shop's types | without naming a directory             |
      | through a server  | the user is working where kb finds a connection to a server hosting a store holding the shop's types          | without naming a directory             |
      | in a named directory | the user is working in one directory, and another directory holds a knowledge base holding the shop's types | in the other directory by naming it    |

  @slice-55
  Scenario Outline: Starting where the knowledge base to furnish holds something other than the shop's types is refused
    Pins that only an empty knowledge base is furnished: one already holding something else is refused, and the user is told what is in it.
    Given the user is working outside any knowledge base, with KB_ROOT naming a knowledge base holding <what it holds> and not the shop's types
    When the user starts a shop knowledge base without naming a directory, saying who they are
    Then starting the knowledge base is rejected because it is not empty
    And the refusal names what it holds
    And nothing changes

    Examples:
      | what it holds              |
      | types other than the shop's |
      | content                    |

  @slice-54
  Scenario: Starting a knowledge base from a removed directory, with nothing naming a knowledge base, ends in a plain refusal
    Pins that even the first command, with nowhere to put what it would make and nothing named to furnish, stops in words the user can read and never in a traceback.
    Given the user is working in a directory that has since been removed, and nothing names a knowledge base
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
