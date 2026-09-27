Feature: Publish what the shop knows
So that the harness and people outside the command line can use what the shop knows, the user can publish it into files.

  Background:
    Given a shop knowledge base holding a process whose steps include a branch and a reused shared step, and a role

  @slice-17
  Scenario: The user publishes a process as a skill
    Pins the bet that a process the shop holds can become a skill the harness loads as is, with shared steps written out, and that publishing only reads from the shop.
    When the user publishes the process as a skill into a directory
    Then that directory holds a skill whose heading block is the process's identity and whose body is its steps, with the reused step written out in full
    And the shop's knowledge base is unchanged

  @slice-50
  Scenario: The user publishes a role as an agent
    Pins why a role keeps its harness fields separate: they become the agent's heading block, and the role's prose becomes its body.
    When the user publishes the role as an agent into a directory
    Then that directory holds an agent whose heading block is the role's harness fields and whose body is the role's prose

  @slice-19
  Scenario: The user publishes a process as a diagram
    Pins the belief that steps and branches carry enough structure to draw the process, with no hand layout anywhere.
    When the user publishes the process as a diagram into a directory
    Then that directory holds a diagram of the process's steps and their branches

  @slice-20
  Scenario: The user publishes anything as markdown
    Pins the fallback that keeps every type readable to a person without each type needing a publisher of its own.
    When the user publishes the role as markdown into a directory
    Then that directory holds a page with the identity as a heading, the fields as a list, the sections at their levels and the parts as tables

  @slice-50.6
  Scenario Outline: Markdown lays out each kind of value as markdown
    Pins that a page published as markdown reads as markdown all the way down, so a person never meets a value written the way a program would print it.
    Given the <thing> holds <holding>
    When the user publishes the <thing> as markdown into a directory
    Then that directory holds a page showing <shown> as <layout>
    And nothing on the page is a programming language's representation of a value

    Examples:
      | thing   | holding                                 | shown     | layout                                             |
      | process | steps that each say more than one thing | its steps | a table with one column for each thing a step says |
      | role    | more than one tag                       | its tags  | a bullet list                                      |

  @slice-50.11
  Scenario Outline: Markdown never shows a yes, a no or an empty value the way a program prints it
    Pins that the simplest values are held to the same rule as lists and mappings, wherever they sit on the page, so a person reading it never meets a program's spelling of true, false or nothing.
    Given the <thing> holds <holding>
    When the user publishes the <thing> as markdown into a directory
    Then that directory holds a page of the <thing>
    And nothing on the page is a programming language's representation of a value

    Examples:
      | thing   | holding                                                              |
      | role    | a field that is a yes and a field that is a no                       |
      | role    | a field with no value                                                |
      | process | steps that each say more than one thing, one of them a yes and a no  |
      | process | steps that each say more than one thing, one of them with no value   |

  @slice-18
  Scenario: A skill the harness would reject is not published
    Pins that publishing checks its own output against the harness's limits and refuses outright, rather than leaving a file that fails later.
    Given a process whose steps run past the limits the harness publishes
    When the user publishes the process as a skill into a directory
    Then the skill is rejected because it goes beyond the limits the harness publishes
    And nothing is written to the directory

  @slice-50.7
  Scenario: An agent the harness would reject is not published
    Pins that an agent is held to the harness's limits just as a skill is, so a role never becomes an agent file the harness will not load.
    Given a role whose harness fields run past the limits the harness publishes
    When the user publishes the role as an agent into a directory
    Then the agent is rejected because it goes beyond the limits the harness publishes
    And nothing is written to the directory
