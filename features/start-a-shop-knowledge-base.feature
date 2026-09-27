Feature: Start a shop knowledge base
So that the shop has one place that holds everything it knows, the user can start a shop knowledge base.

  @slice-4
  Scenario: The user starts a knowledge base and the shop's types are ready
    Pins that a new knowledge base arrives furnished with the shop's seven kinds of thing, so nobody has to define a type before recording anything.
    Given the user is working in an empty directory for the shop's knowledge
    When the user starts a shop knowledge base there without naming a directory, saying who they are
    Then the shop can hold decisions, features, work items, roles, processes, steps and tags
    And the user defines nothing of their own before recording the first one

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
  Scenario: The shop's knowledge sits in a place of its own inside the directory it was started in
    Pins that the shop's knowledge keeps to its own corner, so it can live alongside the shop's other work without mingling with it.
    Given the user is working in a directory holding work of the shop's that is not its knowledge
    When the user starts a shop knowledge base there without naming a directory, saying who they are
    Then the shop's knowledge is kept in a place of its own inside that directory
    And the work that was already in that directory is left as it was

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

  Scenario: The user starts a knowledge base somewhere else on purpose by naming the place
    Pins that naming a place is the only way to start the shop's knowledge away from where the user works, so it lands elsewhere only when they mean it to.
    Given the user is working in one directory, and another directory is empty
    When the user starts a shop knowledge base in the other directory by naming it, saying who they are
    Then the shop's knowledge is kept in a place of its own inside the named directory
    And the directory they are working in holds no knowledge base

  @slice-49
  Scenario: A role keeps its harness fields apart from its shop identity
    Pins the split in the role type that lets a role be published to the harness later: what the harness needs is one group, who the role is in the shop is another.
    Given a shop knowledge base
    When the user records a role, saying who they are and why
    Then the fields the harness needs are kept as one named group
    And the fields that say who the role is in the shop are kept as another

  @slice-49
  Scenario: Anything the shop knows can be tagged
    Pins the bet that a tag is a thing in its own right rather than a word in prose: the meaning is written down once, on the tag, and everything else just names it.
    Given a shop knowledge base holding a tag "pricing" with a title and a description
    When the user tags a decision with "pricing", saying who they are and why
    Then the decision names that tag
    And the tag's description is held once, on the tag itself
