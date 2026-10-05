# formulated from spec/capabilities/use-the-shops-types.md
Feature: Use the shop's types
  Narrator: the user, working with the shop's kinds of thing

  @slice-58
  Scenario: The user asks which types the shop holds
    Pins that the shop's kinds of thing can be seen through a command of their own, all of them at once.
    Given a shop knowledge base
    When the user asks which types the shop holds
    Then the user is shown each of the shop's seven types

  @slice-58
  Scenario: The user reads one of the shop's types by its name
    Pins that a type is readable as the shop actually holds it, so the user can see what a role must say before recording one.
    Given a shop knowledge base
    When the user reads the role type by its name
    Then the user is shown the role type as the shop holds it

  @slice-58
  Scenario Outline: Every artifact of the shop's seven types can carry an owner, a status and tags
    Pins that owner, status and tags are common to every kind of thing the shop holds, not a feature of some kinds only.
    Given a shop knowledge base holding a tag "pricing"
    When the user records a <kind> with an owner, a status and the tag "pricing", saying who they are and why
    Then the <kind> carries that owner, that status and that tag

    Examples:
      | kind      |
      | decision  |
      | feature   |
      | work item |
      | role      |
      | process   |
      | step      |
      | tag       |

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

  @slice-58
  Scenario Outline: A process's step either defines a step in place or uses a shared step with settings of its own
    Pins the two ways a process can say what happens at a step: written out where it is, or borrowed from a shared step and set up for this process.
    Given a shop knowledge base holding a shared step "check the stock"
    When the user records a process with a step that <given as>, saying who they are and why
    Then the process keeps that step <kept as>

    Examples:
      | given as                                         | kept as                                            |
      | describes what to do in place                    | as described, in place                             |
      | uses "check the stock" with settings of its own  | as a use of "check the stock" with those settings  |
