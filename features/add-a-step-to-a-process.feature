Feature: Add a step to a process
So that a process can be built up a step at a time, the user can add a step to a process.

  Background:
    Given a shop knowledge base holding a process with two steps
    And a shared step "check the stock" that other processes already use

  @slice-40
  Scenario: The user adds a step written in place
    Pins growing a process one step at a time: a step written out in place lands at the end, and the shop, not the user, names it.
    When the user adds a step describing what to do, saying who they are and why
    Then the new step is the last step of the process
    And the user is told the name the new step is known by

  @slice-40
  Scenario: The user adds a step that reuses a shared step
    Pins the reuse the shop is betting on: a process can borrow a shared step with its own settings without altering that step or the other processes that use it.
    When the user adds a step that uses "check the stock" with its own settings, saying who they are and why
    Then the process runs "check the stock" at that point with those settings
    And "check the stock" itself is unchanged
    And another process using it is unaffected
