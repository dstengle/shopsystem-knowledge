Feature: Start a shop knowledge base
So that the shop has one place that holds everything it knows, the user can start a shop knowledge base.

  @slice-4
  Scenario: The user starts a knowledge base and the shop's types are ready
    Given an empty directory for the shop's knowledge
    When the user starts a shop knowledge base in that directory, saying who they are
    Then the shop can hold decisions, features, work items, roles, processes, steps and tags
    And the user defines nothing of their own before recording the first one

  @slice-52
  Scenario: Starting a knowledge base asks for no reason
    Given an empty directory for the shop's knowledge
    When the user starts a shop knowledge base in that directory, saying who they are and giving no reason
    Then the shop's knowledge base is started
    And everything it was given is recorded in the shop's history under a reason the command writes itself

  @slice-52
  Scenario: Starting a knowledge base without saying who is refused
    Given an empty directory for the shop's knowledge
    And the user has not said which role they are
    When the user starts a shop knowledge base in that directory
    Then starting the knowledge base is rejected because starting one must say which role did it
    And that directory holds no knowledge base
    And the command reports failure to whatever ran it

  @slice-52
  Scenario: The shop's knowledge sits in a place of its own inside the directory it was started in
    Given a directory holding work of the shop's that is not its knowledge
    When the user starts a shop knowledge base in that directory, saying who they are
    Then the shop's knowledge is kept in a place of its own inside that directory
    And the work that was already in that directory is left as it was

  @slice-52
  Scenario: Starting a knowledge base where the directory already holds one is refused
    Given a directory that already holds the shop's knowledge
    When the user starts a shop knowledge base in that directory, saying who they are
    Then starting the knowledge base is rejected because that directory already holds a knowledge base
    And everything the shop already knows is still there, unchanged

  @slice-52
  Scenario: Starting a knowledge base inside one the shop already has is refused
    Given a directory that sits inside the shop's knowledge
    When the user starts a shop knowledge base in that directory, saying who they are
    Then starting the knowledge base is rejected because that directory is inside a knowledge base
    And everything the shop already knows is still there, unchanged

  @slice-46
  Scenario: A role keeps its harness fields apart from its shop identity
    Given a shop knowledge base
    When the user records a role, saying who they are and why
    Then the fields the harness needs are kept as one named group
    And the fields that say who the role is in the shop are kept as another

  @slice-46
  Scenario: Anything the shop knows can be tagged
    Given a shop knowledge base holding a tag "pricing" with a title and a description
    When the user tags a decision with "pricing", saying who they are and why
    Then the decision names that tag
    And the tag's description is held once, on the tag itself
