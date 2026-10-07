# formulated from spec/capabilities/see-what-is-formulated.md
Feature: See what is formulated
  Narrator: the user, checking which of a shop's Behaviour lines its scenarios formulate

  @slice-66
  Scenario: The user asks what is formulated in a shop, and is shown each line no scenario formulates
    Pins that every line left without a scenario is shown, each by its link with its capability's title and its own title, so the user can find it and know it at once.
    Given a shop knowledge base holding the shop "checkout" with these Behaviour lines, formulated by these scenarios
      | capability       | line                          | scenarios formulating it |
      | Apply a discount | A valid code lowers the price | 1                        |
      | Apply a discount | An expired code is refused    | 0                        |
      | Take a payment   | A paid order is confirmed     | 0                        |
    When the user asks what is formulated in the shop "checkout"
    Then the user is shown as formulated by no scenario each of these lines, by its link, and no other
      | capability       | line                       |
      | Apply a discount | An expired code is refused |
      | Take a payment   | A paid order is confirmed  |

  @slice-66
  Scenario: The user asks what is formulated in a shop, and is shown each line more than one scenario formulates
    Pins that every line formulated by more than one scenario is shown, each by its link with its capability's title and its own title, so the user can find the scenarios that overlap.
    Given a shop knowledge base holding the shop "checkout" with these Behaviour lines, formulated by these scenarios
      | capability       | line                          | scenarios formulating it |
      | Apply a discount | A valid code lowers the price | 2                        |
      | Apply a discount | An expired code is refused    | 1                        |
      | Take a payment   | A paid order is confirmed     | 3                        |
    When the user asks what is formulated in the shop "checkout"
    Then the user is shown as formulated by more than one scenario each of these lines, by its link, and no other
      | capability       | line                          |
      | Apply a discount | A valid code lowers the price |
      | Take a payment   | A paid order is confirmed     |

  @slice-66
  Scenario: Where some of the shop's lines have no scenario, the user asks what is formulated and is answered, not refused
    Pins that a line without a scenario is something the user is told, never a reason to refuse: seeing what is formulated is a report, not a check.
    Given a shop knowledge base holding the shop "checkout" with these Behaviour lines, formulated by these scenarios
      | capability       | line                          | scenarios formulating it |
      | Apply a discount | A valid code lowers the price | 1                        |
      | Apply a discount | An expired code is refused    | 0                        |
    When the user asks what is formulated in the shop "checkout"
    Then the user is answered
    And the command is not refused

  @slice-66
  Scenario: Every one of the shop's lines is formulated by exactly one scenario, and the user is shown none unformulated and none formulated twice
    Pins what a shop whose lines and scenarios match one to one looks like: nothing left out and nothing doubled.
    Given a shop knowledge base holding the shop "checkout" with these Behaviour lines, formulated by these scenarios
      | capability       | line                          | scenarios formulating it |
      | Apply a discount | A valid code lowers the price | 1                        |
      | Apply a discount | An expired code is refused    | 1                        |
      | Take a payment   | A paid order is confirmed     | 1                        |
    When the user asks what is formulated in the shop "checkout"
    Then the user is shown that no line is formulated by no scenario
    And the user is shown that no line is formulated by more than one scenario

  @slice-66
  Scenario: The user asks what is formulated in a shop the knowledge base does not hold
    Pins that asking about a shop that is not there is refused, and the refusal names the shop asked for, rather than answering as though it had no lines.
    Given a shop knowledge base holding no shop "returns"
    When the user asks what is formulated in the shop "returns"
    Then the answer is rejected because that shop is not there, naming "returns"
