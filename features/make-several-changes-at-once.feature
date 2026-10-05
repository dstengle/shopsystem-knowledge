# formulated from spec/capabilities/make-several-changes-at-once.md
Feature: Make several changes at once
  Narrator: the user, landing changes that only make sense together

  Background:
    Given a shop knowledge base holding the shop's types and a work item

  @slice-56
  Scenario: The user makes several changes at once
    Pins that related changes land as one: both are in the shop, and the history records one change rather than two half-stories.
    Given a batch that records a decision and a work item pointing at it
    When the user applies the batch, saying who they are and why
    Then both changes are in the shop
    And the shop's history shows them as one change

  @slice-57
  Scenario: The user applies a batch whose changes are all writes
    Pins that replacing several existing artifacts lands as one: each takes its new wording, and the history records a single change.
    Given the shop also holds a decision
    And a batch that rewrites the decision and the work item
    When the user applies the batch, saying who they are and why
    Then the shop holds the new wording of both
    And the shop's history shows them as one change

  @slice-56
  Scenario Outline: A link written with a key a create in the batch carries names that create's artifact
    Pins that new artifacts in one batch can point at each other through a key the user chose, wherever in the batch the link is written.
    Given a batch that records a decision carrying a key of the user's choosing, and a work item whose link is written with that key, the work item coming <order> the decision in the batch
    When the user applies the batch, saying who they are and why
    Then the work item's link names the decision the batch created

    Examples:
      | order  |
      | before |
      | after  |

  @slice-56
  Scenario: A link written with a key no create in the batch carries leaves the shop untouched
    Pins that a link whose key no create in the batch carries is refused, naming the key, rather than landing as a link to nothing.
    Given a batch that records a decision and a work item whose link is written with a key no create in the batch carries
    When the user applies the batch, saying who they are and why
    Then the batch is rejected because the link lands on nothing, naming the key
    And none of the changes are in the shop

  @slice-56
  Scenario: Two creates carrying the same key leave the shop untouched
    Pins that a key must name exactly one create in the batch; a key two creates share is refused, naming it.
    Given a batch that records a decision and a work item, both carrying the same key
    When the user applies the batch, saying who they are and why
    Then the batch is rejected because a key names one create in the batch, naming the key
    And none of the changes are in the shop

  @slice-57
  Scenario: A write carrying a key leaves the shop untouched
    Pins that keys belong to creates alone: a write that carries one is refused, naming the key.
    Given a batch that rewrites the work item, the write carrying a key
    When the user applies the batch, saying who they are and why
    Then the batch is rejected because only a create carries a key, naming the key
    And none of the changes are in the shop

  @slice-57
  Scenario: A batch mixing creates and writes leaves the shop untouched
    Pins that a batch holds one kind of change; one that records something new and rewrites something existing is refused as a whole.
    Given a batch that records a decision and rewrites the work item
    When the user applies the batch, saying who they are and why
    Then the batch is rejected because a batch holds one kind of change, naming the batch
    And none of the changes are in the shop

  @slice-56
  Scenario: One bad change in a batch leaves the shop untouched
    Pins all-or-nothing: a single bad change rolls the whole batch back, and the user is told every fault at once so the batch can be fixed in one pass.
    Given a batch whose second change does not fit its type
    When the user applies the batch, saying who they are and why
    Then the batch is rejected because a change in it does not fit its type
    And none of the changes are in the shop
    And the user is told every fault in the batch, not only the first

  @slice-56
  Scenario: A batch whose prose the shop cannot keep leaves the shop untouched
    Pins that a batch is held to the same rule as a single change: text the shop cannot keep as written is refused in plain words, naming where it is, and nothing in the batch lands.
    Given a batch that records a decision and a work item pointing at it, the decision's prose having a line ending in a space before its last line
    When the user applies the batch, saying who they are and why
    Then the batch is rejected because the shop cannot keep prose in which a line before the last ends in a space, naming the place in the batch
    And the user is shown that fault in plain words, never a traceback
    And none of the changes are in the shop
    And the command reports failure to whatever ran it
