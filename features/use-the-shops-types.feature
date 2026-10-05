# formulated from spec/capabilities/use-the-shops-types.md
Feature: Use the shop's types
  Narrator: the user, working with the shop's kinds of thing

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
