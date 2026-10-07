# formulated from spec/capabilities/use-the-shops-types.md
Feature: Use the shop's types
  Narrator: the user, working with the shop's kinds of thing

  @slice-58
  Scenario: The user asks which types the shop holds
    Pins that the shop's kinds of thing can be seen through a command of their own, all of them at once.
    Given a shop knowledge base
    When the user asks which types the shop holds
    Then the user is shown each of the shop's ten types

  @slice-58
  Scenario: The user reads one of the shop's types by its name
    Pins that a type is readable as the shop actually holds it, so the user can see what a role must say before recording one.
    Given a shop knowledge base
    When the user reads the role type by its name
    Then the user is shown the role type as the shop holds it

  @slice-58
  Scenario Outline: Every artifact of the shop's ten types can carry an owner, a status and tags
    Pins that owner, status and tags are common to every kind of thing the shop holds, not a feature of some kinds only.
    Given a shop knowledge base holding a tag "pricing"
    When the user records a <kind> with an owner, a status and the tag "pricing", saying who they are and why
    Then the <kind> carries that owner, that status and that tag

    Examples:
      | kind       |
      | product    |
      | shop       |
      | capability |
      | decision   |
      | feature    |
      | work item  |
      | role       |
      | process    |
      | step       |
      | tag        |

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

  Scenario Outline: The user reads a product, a shop, a capability, a decision or a feature at a glance
    Pins that a glance at one of the spec's kinds of thing shows only short lines and links, each just as the user recorded it.
    Given a shop knowledge base holding a product "shopsystem", a shop "knowledge" of "shopsystem", a capability "checkout" of "knowledge" and a decision "prices-include-tax" of "knowledge"
    And the user has recorded a <kind> "<name>" <recorded with>
    When the user reads the <kind> "<name>" at a glance
    Then each field it shows is one short line or a link, as it was recorded

    Examples:
      | kind       | name                | recorded with                                                                                         |
      | product    | storefront          | with the gist "Sells what the shop makes"                                                             |
      | shop       | catalogue           | of the product "shopsystem", with the gist "Holds what is for sale"                                   |
      | capability | apply-a-code        | of the shop "knowledge", with the gist "A customer takes money off with a code"                       |
      | decision   | prices-exclude-tax  | with the statement "Prices are shown before tax", the date 2026-10-07, superseding "prices-include-tax" |
      | feature    | checkout            | formulating the capability "checkout"                                                                 |

  Scenario: The user reads an artifact holding parts at a glance
    Pins that a glance names an artifact's parts by their titles, so the user sees what it holds without reading each part.
    Given a shop knowledge base holding a capability "checkout" with Behaviour lines titled "Show the price" and "Apply a code"
    When the user reads the capability "checkout" at a glance
    Then each of its Behaviour lines is shown by its title

  Scenario: The user records an artifact holding parts
    Pins that the user gives a part a title and the shop gives it its name, so no part's name is chosen by hand.
    Given a shop knowledge base
    When the user records a capability with a Behaviour line titled "Show the price", saying who they are and why
    Then the Behaviour line's name is minted from its title "Show the price"

  Scenario Outline: The user records a gist or a statement longer than 200 characters
    Pins that the one-line summaries a glance shows cannot grow past their limit.
    Given a shop knowledge base
    When the user records a <kind> whose <field> is 201 characters long, saying who they are and why
    Then the change is refused because it does not fit its type

    Examples:
      | kind     | field     |
      | product  | gist      |
      | decision | statement |

  Scenario Outline: The user records a gist or a statement that holds a line break
    Pins that the one-line summaries a glance shows stay on one line.
    Given a shop knowledge base
    When the user records a <kind> whose <field> holds a line break, saying who they are and why
    Then the change is refused because it does not fit its type

    Examples:
      | kind     | field     |
      | product  | gist      |
      | decision | statement |

  Scenario: The user records a part whose title is longer than 80 characters
    Pins that the title a part is shown and named by cannot grow past its limit.
    Given a shop knowledge base
    When the user records a capability with a Behaviour line whose title is 81 characters long, saying who they are and why
    Then the change is refused because it does not fit its type

  Scenario: The user records a part whose title holds a line break
    Pins that the title a part is shown and named by stays on one line.
    Given a shop knowledge base
    When the user records a capability with a Behaviour line whose title holds a line break, saying who they are and why
    Then the change is refused because it does not fit its type

  Scenario: The user records a scenario whose uses points at anything but a capability
    Pins that a scenario can say it uses only capabilities, not other kinds of thing the shop holds.
    Given a shop knowledge base holding a capability "checkout" with a Behaviour line titled "Show the price"
    And a decision "prices-include-tax"
    When the user records a feature with a scenario that formulates the Behaviour line "Show the price" and uses the decision "prices-include-tax", saying who they are and why
    Then the change is refused because it does not fit its type

  Scenario: The user records a feature
    Pins that a scenario is tied to the very Behaviour line it formulates, so the line can be found from the scenario.
    Given a shop knowledge base holding a capability "checkout" with a Behaviour line titled "Show the price"
    When the user records a feature with a scenario that formulates the Behaviour line "Show the price", saying who they are and why
    Then the scenario names the Behaviour line "Show the price" as a link into the Behaviour lines of "checkout"

  Scenario: The user records a scenario with labels
    Pins that a scenario's labels are words of their own, not the shop's tags, even when a tag shares the word.
    Given a shop knowledge base holding a tag "pricing"
    And a capability "checkout" with a Behaviour line titled "Show the price"
    When the user records a feature with a scenario labelled "@pricing" that formulates the Behaviour line "Show the price", saying who they are and why
    Then the label is kept as the plain word "@pricing", not as a link to the tag "pricing"
