Feature: Start a shop knowledge base
So that the shop has one place that holds everything it knows, the user can start a shop knowledge base.

  @assumes-seven-types-close-the-loop
  Scenario: The user starts a knowledge base and the shop's types are ready
    Given an empty directory for the shop's knowledge
    When the user starts a shop knowledge base in that directory
    Then the shop can hold decisions, features, work items, roles, processes, steps and tags
    And the user defines nothing of their own before recording the first one

  @assumes-renderers-match-the-harness
  Scenario: A role keeps its harness fields apart from its shop identity
    Given a shop knowledge base
    When the user records a role, saying who they are and why
    Then the fields the harness needs are kept as one named group
    And the fields that say who the role is in the shop are kept as another

  @assumes-tags-replace-flags-in-prose
  Scenario: Anything the shop knows can be tagged
    Given a shop knowledge base holding a tag "pricing" with a title and a description
    When the user tags a decision with "pricing", saying who they are and why
    Then the decision names that tag
    And the tag's description is held once, on the tag itself
