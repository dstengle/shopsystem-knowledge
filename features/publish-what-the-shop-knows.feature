Feature: Publish what the shop knows
So that the harness and people outside the command line can use what the shop knows, the user can publish it into files.

  Background:
    Given a shop knowledge base holding a process whose steps include a branch and a reused shared step, and a role

  @slice-16
  Scenario: The user publishes a process as a skill
    When the user publishes the process as a skill into a directory
    Then that directory holds a skill whose heading block is the process's identity and whose body is its steps, with the reused step written out in full
    And the shop's knowledge base is unchanged

  @slice-47
  Scenario: The user publishes a role as an agent
    When the user publishes the role as an agent into a directory
    Then that directory holds an agent whose heading block is the role's harness fields and whose body is the role's prose

  @slice-18
  Scenario: The user publishes a process as a diagram
    When the user publishes the process as a diagram into a directory
    Then that directory holds a diagram of the process's steps and their branches

  @slice-19
  Scenario: The user publishes anything as markdown
    When the user publishes the role as markdown into a directory
    Then that directory holds a page with the identity as a heading, the fields as a list, the sections at their levels and the parts as tables

  @slice-17
  Scenario: A skill the harness would reject is not published
    Given a process whose steps run past the limits the harness publishes
    When the user publishes the process as a skill into a directory
    Then the skill is rejected because it goes beyond the limits the harness publishes
    And nothing is written to the directory
