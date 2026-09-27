Feature: Make several changes at once
So that a set of changes that only makes sense together lands together, the user can make several changes at once.

  Background:
    Given a shop knowledge base holding the shop's types and a work item

  @slice-15
  Scenario: The user makes several changes at once
    Pins that related changes land as one: both are in the shop, and the history records one change rather than two half-stories.
    Given a batch that records a decision and points the work item at it
    When the user applies the batch, saying who they are and why
    Then both changes are in the shop
    And the shop's history shows them as one change

  @slice-48
  Scenario: One bad change in a batch leaves the shop untouched
    Pins all-or-nothing: a single bad change rolls the whole batch back, and the user is told every fault at once so the batch can be fixed in one pass.
    Given a batch whose second change does not fit its type
    When the user applies the batch, saying who they are and why
    Then the batch is rejected because a change in it does not fit its type
    And none of the changes are in the shop
    And the user is told every fault in the batch, not only the first

  Scenario: A batch whose prose the shop cannot keep leaves the shop untouched
    Pins that a batch is held to the same rule as a single change: text the shop cannot keep as written is refused in plain words, naming where it is, and nothing in the batch lands.
    Given a batch that records a decision and points the work item at it, the decision's prose having a line ending in a space before its last line
    When the user applies the batch, saying who they are and why
    Then the batch is rejected because the shop cannot keep prose in which a line before the last ends in a space, naming the place in the batch
    And the user is shown that fault in plain words, never a traceback
    And none of the changes are in the shop
    And the command reports failure to whatever ran it
