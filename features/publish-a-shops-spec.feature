# formulated from spec/capabilities/publish-a-shops-spec.md
Feature: Publish a shop's spec
  Narrator: the user, publishing a shop's spec into the shop's repository

  Background:
    Given a knowledge base holding a product and a shop of that product, with the shop's capabilities in its reading order, its decisions, and a feature formulating each capability

  @slice-61
  Scenario: The user publishes a shop's spec and the directory holds its index
    Pins that the shop itself becomes the spec's index, and that publishing a whole spec only reads from the knowledge base.
    When the user publishes the shop's spec into a directory
    Then that directory holds `spec/index.md` from the shop
    And the shop's knowledge base is unchanged

  @slice-63
  Scenario: The user publishes a shop's spec and the directory holds a file for each capability
    Pins that every capability of the shop reaches the repository as a file of its own under the spec's capabilities.
    When the user publishes the shop's spec into a directory
    Then that directory holds `spec/capabilities/<name>.md` for each capability of the shop

  @slice-64
  Scenario: The user publishes a shop's spec and the directory holds its ledger
    Pins that the ledger gathers both what the shop decided and what its capabilities rest on, in one file.
    When the user publishes the shop's spec into a directory
    Then that directory holds `spec/decisions.md`
    And the ledger lists each of the shop's decisions and each decision its capabilities rest on

  @slice-65
  Scenario: The user publishes a shop's spec and the directory holds a feature file for each formulated capability
    Pins that the feature files formulating the shop's capabilities come from the knowledge base along with the spec they formulate.
    When the user publishes the shop's spec into a directory
    Then that directory holds `features/<name>.feature` for each feature formulating one of the shop's capabilities

  @slice-64
  Scenario: The user publishes a shop's spec and the directory holds a record for each decision
    Pins that every decision of the shop is published as a decision record, so no decision stands only as a ledger entry.
    When the user publishes the shop's spec into a directory
    Then that directory holds `adrs/<number>-<name>.md` for each of the shop's decisions

  @slice-63
  Scenario Outline: The user publishes a shop's spec and a capability's file is named from its title
    Pins that a capability's file and its feature's file both take one name made from the title, so either can be found from the other.
    Given one of the shop's capabilities titled "<title>", and a feature formulating it
    When the user publishes the shop's spec into a directory
    Then that directory holds `spec/capabilities/<name>.md` for that capability
    And that directory holds `features/<name>.feature` for the feature formulating it

    Examples:
      | title                       | name                       |
      | Publish a shop's spec       | publish-a-shops-spec       |
      | Read the log’s tail         | read-the-logs-tail         |
      | Rock 'n' roll               | rock-n-roll                |
      | Read the Log                | read-the-log               |
      | Café menus, 2 per table     | caf-menus-2-per-table      |
      | -- Trim both ends! --       | trim-both-ends             |
      | Step 1 / step 2 — then wait | step-1-step-2-then-wait    |

  @slice-64
  Scenario Outline: The user publishes a shop's spec and a decision's record is named from its number and title
    Pins that a decision's record sorts by its number and carries a name made from its title the same way a capability's is.
    Given one of the shop's decisions numbered <number>, titled "<title>"
    When the user publishes the shop's spec into a directory
    Then that directory holds `adrs/<file>.md` for that decision

    Examples:
      | number | title                               | file                                     |
      | 7      | Keep the log                        | 0007-keep-the-log                        |
      | 51     | The shop's types model the BDD spec | 0051-the-shops-types-model-the-bdd-spec  |
      | 1234   | Every decision is an ADR            | 1234-every-decision-is-an-adr            |
      | 12345  | Kb’s pin is bumped, never edited    | 12345-kbs-pin-is-bumped-never-edited     |

  @slice-67
  Scenario Outline: The user publishes a shop's spec and every file it writes carries the published-from line
    Pins that every published file tells its reader where it came from and at which revision, so no one mends it by hand, without displacing a capability's frontmatter.
    When the user publishes the shop's spec into a directory
    Then <file> carries a line saying it was published from the knowledge base and is not to be edited by hand
    And that line names <published from> and <published from>'s revision
    And that line is <where>

    Examples:
      | file                               | published from                     | where                                                                      |
      | `spec/index.md`                    | the shop                           | the first line of the file                                                 |
      | `spec/decisions.md`                | the shop                           | the first line of the file                                                 |
      | each capability's file             | the capability it is published from | directly after the frontmatter, which stays first in the file             |
      | each feature file                  | the feature it is published from   | the first line of the file                                                 |
      | each decision's record             | the decision it is published from  | the first line of the file                                                 |

  @slice-64
  Scenario: The user publishes a shop's spec and every ledger entry is a decision the knowledge base holds
    Pins that the ledger is made only of decisions the knowledge base holds, never an entry written for the ledger alone.
    Given the shop's capabilities rest on decisions of the shop
    When the user publishes the shop's spec into a directory
    Then every entry in the ledger is a decision the knowledge base holds

  @slice-64
  Scenario: The user publishes a shop's spec whose capabilities rest on a decision of another shop
    Pins that a decision borrowed from another shop is listed, but after the shop's own, and points the reader to the shop that holds its record.
    Given another shop of the same product holds a decision
    And one of the shop's capabilities rests on that decision
    When the user publishes the shop's spec into a directory
    Then the ledger lists that decision after the shop's own decisions
    And the ledger gives that decision's source as the other shop's record of it

  @slice-67
  Scenario: Publishing is refused when a capability names the shop but is not in the shop's reading order
    Pins that a capability the shop's reading order leaves out is never silently dropped from the spec or silently added to it.
    Given a capability that names the shop but is not in the shop's reading order
    When the user publishes the shop's spec into a directory
    Then publishing is rejected because that capability is not in the shop's reading order, naming that capability
    And nothing is written to the directory

  @slice-67
  Scenario: Publishing is refused when a capability in the shop's reading order names another shop
    Pins that a shop's spec never publishes a capability another shop owns as if it were its own.
    Given another shop of the same product
    And a capability that names the other shop is in the shop's reading order
    When the user publishes the shop's spec into a directory
    Then publishing is rejected because that capability belongs to another shop, naming that capability
    And nothing is written to the directory

  @slice-67
  Scenario: Publishing is refused when two of the shop's capabilities would be published under one file name
    Pins that one capability's file never overwrites another's.
    Given two of the shop's capabilities titled "Read the log" and "Read the Log"
    When the user publishes the shop's spec into a directory
    Then publishing is rejected because those capabilities would share a file, naming both
    And nothing is written to the directory

  @slice-67
  Scenario: Publishing is refused when two of the shop's decisions would be published under one file name
    Pins that one decision's record never overwrites another's.
    Given two of the shop's decisions numbered 7, titled "Keep the log" and "Keep the Log"
    When the user publishes the shop's spec into a directory
    Then publishing is rejected because those decisions would share a file, naming both
    And nothing is written to the directory

  @slice-67
  Scenario: Publishing is refused when two of the shop's decisions carry one number
    Pins that a decision's number names one decision only, so a number cited anywhere leads to one record.
    Given two of the shop's decisions numbered 7, titled "Keep the log" and "Drop the cache"
    When the user publishes the shop's spec into a directory
    Then publishing is rejected because a number names one decision, naming both decisions
    And nothing is written to the directory

  @slice-67
  Scenario: Publishing is refused when a capability of the shop rests on a decision no shop names
    Pins that the ledger never lists a decision that has no shop's record behind it.
    Given one of the shop's capabilities rests on a decision that no shop names among its decisions
    When the user publishes the shop's spec into a directory
    Then publishing is rejected because that decision belongs to no shop, naming it
    And nothing is written to the directory

  @slice-67
  Scenario: Publishing is refused when two features formulate one of the shop's capabilities
    Pins that a capability has one feature file, never two competing for it.
    Given two features that each formulate the same one of the shop's capabilities
    When the user publishes the shop's spec into a directory
    Then publishing is rejected because those features would share a file, naming both
    And nothing is written to the directory

  @slice-67
  Scenario: Publishing is refused when a scenario's uses points at a capability of its own shop
    Pins that a scenario reaches only across to another shop's capability, never back into its own shop.
    Given a scenario in a feature formulating one of the shop's capabilities, whose uses points at another of the shop's capabilities
    When the user publishes the shop's spec into a directory
    Then publishing is rejected because a scenario uses only another shop's capability, naming that scenario
    And nothing is written to the directory
