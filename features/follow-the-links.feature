# formulated from spec/capabilities/follow-the-links.md
Feature: Follow the links
  Narrator: the user, seeing how the shop's knowledge hangs together

  Background:
    Given a shop knowledge base where a decision supersedes an older decision
    And two work items point at that decision
    And the older decision is tagged "pricing"

  @slice-68
  Scenario: The user sees what a decision points at
    Pins the outward question: what does this thing itself refer to.
    When the user follows the links out of the decision
    Then the user sees the older decision and the decision's shop

  Scenario: The user follows the links out of a decision holding a link to something the knowledge base does not hold
    Pins that a link to nothing is still shown when following links out, marked so the reader can tell it lands on nothing the knowledge base holds.
    Given the decision also holds a link to an artifact the knowledge base does not hold
    When the user follows the links out of the decision
    Then the user sees that link, marked as landing on nothing the knowledge base holds
    And the user sees the older decision and the decision's shop

  @slice-32
  Scenario: The user sees what points at a decision
    Pins the question the shop cannot answer by reading one file: who elsewhere depends on this.
    When the user follows the links into the decision
    Then the user sees both work items

  @slice-32
  Scenario: The user narrows the links to one kind of link and one kind of thing
    Pins that the question can be made narrow, by which link and by what sort of thing, so a big corpus still gives a small answer.
    When the user follows the links into the decision, only through the link a work item uses, and only from work items
    Then the user sees both work items and nothing else

  @slice-68
  Scenario: The user follows the links two steps out
    Pins reach beyond the immediate neighbours, with the route shown so a reader can tell how each thing was arrived at.
    When the user follows the links out of the decision two steps
    Then the user sees the older decision, the tag "pricing", the decision's shop and that shop's product
    And the user sees the route taken to each of them

  @slice-71
  Scenario: The user follows the links into a capability
    Pins that who builds on a capability is found by asking, across every shop, rather than kept as a list on the capability itself.
    Given the shops "checkout" and "payments" of the product "shopsystem"
    And the capability "apply-a-code" of the shop "checkout"
    And the capability "show-the-total" of the shop "checkout", depending on "apply-a-code"
    And the capability "redeem-a-gift-card" of the shop "payments", depending on "apply-a-code"
    And a feature formulating "redeem-a-gift-card", with a scenario whose uses name "apply-a-code"
    When the user follows the links into the capability "apply-a-code"
    Then the user sees the capabilities "show-the-total" and "redeem-a-gift-card"
    And the user sees the feature formulating "redeem-a-gift-card"
