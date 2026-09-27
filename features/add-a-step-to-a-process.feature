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

  Scenario: A step whose prose the shop cannot keep is refused
    Pins that adding to a process is held to the same rule as recording and revising: text the shop cannot keep as written is refused in plain words, and the process is left as it was.
    Given a step written in a file whose prose has a line ending in a space before its last line
    When the user adds that step, saying who they are and why
    Then the step is rejected because the shop cannot keep prose in which a line before the last ends in a space, naming the place in the file
    And the user is shown that fault in plain words, never a traceback
    And the process still has its two steps
    And the command reports failure to whatever ran it
