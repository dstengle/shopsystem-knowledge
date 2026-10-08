# formulated from spec/capabilities/see-what-a-shop-depends-on.md
Feature: See what a shop depends on
  Narrator: the user, checking whether a shop's capabilities lean on capabilities being removed

  @slice-71
  Scenario: The user asks what a shop depends on, and is shown each of its active or deprecated capabilities that depends on a deprecated or retired capability, in any shop
    Pins that every active or deprecated capability of the shop leaning on a capability on its way out, in the shop itself or another, is shown with what it leans on, that capability's shop and status, and the scenarios using it, and that nothing else is shown.
    Given a shop knowledge base holding the shop "checkout" with these capabilities, depending on these capabilities
      | capability       | status     | depends on      | shop of what it depends on | status of what it depends on |
      | Apply a discount | active     | Look up a code  | catalogue                  | deprecated                   |
      | Take a payment   | deprecated | Charge a card   | payments                   | retired                      |
      | Confirm an order | active     | Take a payment  | checkout                   | deprecated                   |
      | Show the basket  | active     | Price a product | catalogue                  | active                       |
      | Ship an order    | retired    | Book a courier  | delivery                   | deprecated                   |
    And these scenarios of the shop's capabilities, using these capabilities
      | capability       | scenario                       | uses            |
      | Apply a discount | A valid code lowers the price  | Look up a code  |
      | Apply a discount | An empty code is ignored       | nothing         |
      | Take a payment   | A card payment is taken        | Charge a card   |
      | Confirm an order | A paid order is confirmed      | Take a payment  |
      | Confirm an order | An unpaid order is held        | Take a payment  |
      | Show the basket  | The basket shows its prices    | Price a product |
      | Ship an order    | A confirmed order is booked    | Book a courier  |
    When the user asks what the shop "checkout" depends on
    Then the user is shown each of these capabilities, with the capability it depends on, that capability's shop and its status, and no other
      | capability       | depends on     | shop of what it depends on | status of what it depends on |
      | Apply a discount | Look up a code | catalogue                  | deprecated                   |
      | Take a payment   | Charge a card  | payments                   | retired                      |
      | Confirm an order | Take a payment | checkout                   | deprecated                   |
    And the user is shown, with each of those capabilities, these of its scenarios using what it depends on, and no other
      | capability       | scenario                      |
      | Apply a discount | A valid code lowers the price |
      | Take a payment   | A card payment is taken       |
      | Confirm an order | A paid order is confirmed     |
      | Confirm an order | An unpaid order is held       |

  @slice-71
  Scenario: Where some of the shop's capabilities depend on a retired capability, the user asks what the shop depends on and is answered, not refused
    Pins that leaning on a retired capability is something the user is told, never a reason to refuse: seeing what a shop depends on is a report, not a check.
    Given a shop knowledge base holding the shop "checkout" with these capabilities, depending on these capabilities
      | capability     | status | depends on    | shop of what it depends on | status of what it depends on |
      | Take a payment | active | Charge a card | payments                   | retired                      |
    When the user asks what the shop "checkout" depends on
    Then the user is answered
    And the command is not refused

  @slice-71
  Scenario: None of the shop's published capabilities depends on a deprecated or retired capability, and the user is shown none
    Pins what a shop leaning on nothing on its way out looks like: an answer with no capability in it.
    Given a shop knowledge base holding the shop "checkout" with these capabilities, depending on these capabilities
      | capability       | status     | depends on      | shop of what it depends on | status of what it depends on |
      | Apply a discount | active     | Look up a code  | catalogue                  | active                       |
      | Take a payment   | deprecated | Charge a card   | payments                   | active                       |
    When the user asks what the shop "checkout" depends on
    Then the user is shown no capability depending on a deprecated or retired capability

  @slice-71
  Scenario: The user asks what a shop depends on, and the knowledge base does not hold that shop
    Pins that asking about a shop that is not there is refused, and the refusal names the shop asked for, rather than answering as though it depended on nothing.
    Given a shop knowledge base holding no shop "returns"
    When the user asks what the shop "returns" depends on
    Then the answer is rejected because that shop is not there, naming "returns"
