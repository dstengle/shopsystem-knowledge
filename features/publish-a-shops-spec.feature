# formulated from spec/capabilities/publish-a-shops-spec.md
Feature: Publish a shop's spec
  Narrator: the user, publishing a shop's spec into the shop's repository

  Background:
    Given a knowledge base holding a product and a shop of that product, active capabilities linking to the shop each carrying an order of its own, decisions linking to the shop each carrying a number of its own, and a feature formulating each capability

  @slice-69
  Scenario: The user publishes a shop's spec and the directory holds its index
    Pins that the shop itself becomes the spec's index, and that publishing a whole spec only reads from the knowledge base.
    When the user publishes the shop's spec into a directory
    Then that directory holds `spec/index.md` from the shop
    And the shop's knowledge base is unchanged

  @slice-69
  Scenario: The user publishes a shop's spec and the directory holds a file for each active or deprecated capability linking to the shop
    Pins that a capability reaches the repository as a file of its own when it links to the shop and is still in use, whether active or deprecated.
    Given one of the capabilities linking to the shop is deprecated
    When the user publishes the shop's spec into a directory
    Then that directory holds `spec/capabilities/<name>.md` for each capability linking to the shop whose status is active or deprecated

  @slice-69
  Scenario: The user publishes a shop's spec and the directory holds the ledger of the shop's own decisions in number order
    Pins that the ledger is made of the decisions linking to the shop and no others, read from the lowest number to the highest whatever order they were made in.
    Given the decisions linking to the shop are three, numbered 12, 3 and 7, created in that order
    And another shop of the same product, with a decision linking to it
    When the user publishes the shop's spec into a directory
    Then that directory holds `spec/decisions.md`
    And the ledger lists the decisions numbered 3, 7 and 12, in that order
    And the ledger does not list the other shop's decision

  @slice-69
  Scenario: The user publishes a shop's spec and the directory holds a feature file for each formulated capability
    Pins that the feature files formulating the shop's capabilities come from the knowledge base along with the spec they formulate.
    When the user publishes the shop's spec into a directory
    Then that directory holds `features/<name>.feature` for each feature formulating one of the shop's capabilities

  @slice-69
  Scenario: The user publishes a shop's spec and the directory holds a record for each decision
    Pins that every decision of the shop is published as a decision record, so no decision stands only as a ledger entry.
    When the user publishes the shop's spec into a directory
    Then that directory holds `adrs/<number>-<name>.md` for each of the shop's decisions

  @slice-69
  Scenario: The user publishes a shop's spec and the index lists its capabilities in their order, dotted numbers compared part by part as numbers
    Pins that the reading order follows the number in each part, so 1.10 comes after 1.2 and 10 after 2, never the order the characters sort in or the order the capabilities were made in.
    Given the capabilities linking to the shop are these, created in this order:
      | title          | order |
      | Keep the cache | 10    |
      | Read the log   | 1.10  |
      | Write the log  | 2     |
      | Open the log   | 1.2   |
    When the user publishes the shop's spec into a directory
    Then the index lists the shop's capabilities in this order:
      | title          |
      | Open the log   |
      | Read the log   |
      | Write the log  |
      | Keep the cache |

  @slice-72
  Scenario: The user publishes a shop's spec holding a deprecated capability
    Pins that a deprecated capability is still published, and that its reader is told it is deprecated both on its page and in the index.
    Given one of the capabilities linking to the shop is deprecated
    When the user publishes the shop's spec into a directory
    Then that directory holds that capability's page
    And that page says the capability is deprecated
    And that capability's line in the index says it is deprecated

  @slice-72
  Scenario: The user publishes a shop's spec holding a retired capability
    Pins that a retired capability leaves the published spec entirely: no page, no feature file, no line in the index.
    Given a capability linking to the shop whose status is retired, and a feature formulating it
    When the user publishes the shop's spec into a directory
    Then that directory holds no page for that capability
    And that directory holds no feature file for it
    And the index does not list it

  @slice-69
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

  @slice-69
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

  @slice-69
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

  @slice-69
  Scenario: The user publishes a shop's spec and every ledger entry is a decision the knowledge base holds
    Pins that the ledger is made only of decisions the knowledge base holds, never an entry written for the ledger alone.
    Given the shop's capabilities rest on decisions of the shop
    When the user publishes the shop's spec into a directory
    Then every entry in the ledger is a decision the knowledge base holds

  @slice-72
  Scenario Outline: The user publishes a shop's spec into a directory holding files published earlier, and those this publish does not write are deleted
    Pins that a published file this publish does not write leaves the repository, both one whose artifact is no longer published and one its artifact left behind on taking a new name, and that deleting reaches nothing outside the three published directories.
    Given <artifact> was published earlier as <old file>, and its title has since changed so that it is now published as <new file>
    And the directory also holds <stale file>, published earlier from <stale artifact>
    And the directory holds `notes/old.md`, whose published-from line names <stale artifact>
    When the user publishes the shop's spec into that directory
    Then <old file> is deleted
    And <stale file> is deleted
    And that directory holds <new file>
    And `notes/old.md` is still in that directory, as it was

    Examples:
      | artifact                                              | old file                          | new file                          | stale file                       | stale artifact                                                                   |
      | one of the shop's capabilities                        | `spec/capabilities/read-the-log.md` | `spec/capabilities/tail-the-log.md` | `spec/capabilities/old-cache.md` | a capability linking to the shop whose status is retired                          |
      | the feature formulating one of the shop's capabilities | `features/read-the-log.feature`   | `features/tail-the-log.feature`   | `features/old-cache.feature`     | the feature formulating a capability linking to the shop whose status is retired |
      | one of the shop's decisions, numbered 7               | `adrs/0007-keep-the-log.md`       | `adrs/0007-keep-every-log.md`     | `adrs/0099-old-rule.md`          | a decision linking to another shop of the same product                            |

  @slice-70
  Scenario Outline: The user publishes a shop's spec into a directory holding a file with no published-from line, at a name it does not write
    Pins that a file written by hand beside the published ones, at a name nothing is published under, is neither deleted nor changed by publishing.
    Given a directory holding <file>, which has no published-from line
    And no artifact is published under that name
    When the user publishes the shop's spec into that directory
    Then <file> is left as it was

    Examples:
      | file                         |
      | `spec/capabilities/notes.md` |
      | `features/notes.feature`     |
      | `adrs/notes.md`              |

  @slice-69
  Scenario: Publishing is refused when two of the shop's capabilities would be published under one file name
    Pins that one capability's file never overwrites another's, and that a refused publish leaves the directory exactly as it found it.
    Given two of the shop's capabilities, each with an order of its own, titled "Read the log" and "Read the Log"
    And a directory holding `adrs/0099-old-rule.md`, whose published-from line names a decision linking to another shop of the same product
    When the user publishes the shop's spec into that directory
    Then publishing is rejected because those capabilities would share a file, naming both
    And nothing is written to the directory
    And `adrs/0099-old-rule.md` is still in that directory

  @slice-69
  Scenario: Publishing is refused when two of the shop's decisions would be published under one file name
    Pins that one decision's record never overwrites another's, and that a refused publish leaves the directory exactly as it found it.
    Given two of the shop's decisions numbered 7, titled "Keep the log" and "Keep the Log"
    And a directory holding `adrs/0099-old-rule.md`, whose published-from line names a decision linking to another shop of the same product
    When the user publishes the shop's spec into that directory
    Then publishing is rejected because those decisions would share a file, naming both
    And nothing is written to the directory
    And `adrs/0099-old-rule.md` is still in that directory

  @slice-69
  Scenario: Publishing is refused when two of the shop's decisions carry one number
    Pins that a decision's number names one decision only, so a number cited anywhere leads to one record, and that a refused publish leaves the directory exactly as it found it.
    Given two of the shop's decisions numbered 7, titled "Keep the log" and "Drop the cache"
    And a directory holding `adrs/0099-old-rule.md`, whose published-from line names a decision linking to another shop of the same product
    When the user publishes the shop's spec into that directory
    Then publishing is rejected because a number names one decision, naming both decisions
    And nothing is written to the directory
    And `adrs/0099-old-rule.md` is still in that directory

  @slice-73
  Scenario: Publishing is refused when two of the shop's capabilities carry one order
    Pins that an order places one capability only, so the index never has to choose between two, and that a refused publish leaves the directory exactly as it found it.
    Given two of the shop's capabilities, both active, both at order 3, titled "Read the log" and "Keep the cache"
    And a directory holding `adrs/0099-old-rule.md`, whose published-from line names a decision linking to another shop of the same product
    When the user publishes the shop's spec into that directory
    Then publishing is rejected because an order places one capability, naming both capabilities
    And nothing is written to the directory
    And `adrs/0099-old-rule.md` is still in that directory

  @slice-73
  Scenario: Publishing is refused when a capability of the shop rests on a decision of another shop
    Pins that a capability's decisions are always in its own shop's ledger, never borrowed from another shop's, and that a refused publish leaves the directory exactly as it found it.
    Given another shop of the same product, with a decision linking to it
    And one of the shop's capabilities rests on that decision
    And a directory holding `adrs/0099-old-rule.md`, whose published-from line names a decision linking to the other shop
    When the user publishes the shop's spec into that directory
    Then publishing is rejected because a capability rests only on its own shop's decisions, naming that capability and that decision
    And nothing is written to the directory
    And `adrs/0099-old-rule.md` is still in that directory

  @slice-73
  Scenario: Publishing is refused when a scenario's uses names a capability its capability does not depend on
    Pins that a scenario reaches only what its capability is declared to depend on, and that a refused publish leaves the directory exactly as it found it.
    Given another shop of the same product, with an active capability linking to it
    And a scenario in a feature formulating one of the shop's capabilities, whose uses names that other shop's capability
    And the scenario's capability does not depend on that other shop's capability
    And a directory holding `adrs/0099-old-rule.md`, whose published-from line names a decision linking to the other shop
    When the user publishes the shop's spec into that directory
    Then publishing is rejected because a scenario uses only what its capability depends on, naming that scenario and the capability it uses
    And nothing is written to the directory
    And `adrs/0099-old-rule.md` is still in that directory

  @slice-72
  Scenario Outline: Publishing is refused when an active or deprecated capability of the shop depends on a retired capability
    Pins that a capability still published never leans on one taken out of use, wherever the retired one lives, and that a refused publish leaves the directory exactly as it found it.
    Given another shop of the same product
    And a capability linking to <owner> whose status is retired
    And a capability linking to the shop whose status is <status> depends on that retired capability
    And a directory holding `adrs/0099-old-rule.md`, whose published-from line names a decision linking to the other shop
    When the user publishes the shop's spec into that directory
    Then publishing is rejected because it depends on a retired capability, naming both capabilities
    And nothing is written to the directory
    And `adrs/0099-old-rule.md` is still in that directory

    Examples:
      | status     | owner          |
      | active     | the shop       |
      | deprecated | the shop       |
      | active     | the other shop |
      | deprecated | the other shop |

  @slice-74
  Scenario Outline: Publishing is refused when a constraint of the shop is tested in a retired capability, in any shop
    Pins that a constraint the shop carries is never shown as tested in a capability taken out of use, wherever that capability lives, and that a refused publish leaves the directory exactly as it found it.
    Given another shop of the same product
    And a capability linking to <owner> whose status is retired
    And a constraint of the shop tested in that retired capability
    And a directory holding `adrs/0099-old-rule.md`, whose published-from line names a decision linking to the other shop
    When the user publishes the shop's spec into that directory
    Then publishing is rejected because that capability is retired, naming that constraint and that capability
    And nothing is written to the directory
    And `adrs/0099-old-rule.md` is still in that directory

    Examples:
      | owner          |
      | the shop       |
      | the other shop |

  @slice-69
  Scenario: Publishing is refused when two features formulate one of the shop's capabilities
    Pins that a capability has one feature file, never two competing for it, and that a refused publish leaves the directory exactly as it found it.
    Given two features that each formulate the same one of the shop's capabilities
    And a directory holding `adrs/0099-old-rule.md`, whose published-from line names a decision linking to another shop of the same product
    When the user publishes the shop's spec into that directory
    Then publishing is rejected because those features would share a file, naming both
    And nothing is written to the directory
    And `adrs/0099-old-rule.md` is still in that directory

  @slice-69
  Scenario: Publishing is refused when a table in a feature has rows of different widths
    Pins that a published feature file never holds a table whose rows do not line up, that the user is told which scenario holds it, and that a refused publish leaves the directory exactly as it found it.
    Given a scenario in a feature formulating one of the shop's capabilities, whose step's table has a row with fewer cells than its header
    And a directory holding `adrs/0099-old-rule.md`, whose published-from line names a decision linking to another shop of the same product
    When the user publishes the shop's spec into that directory
    Then publishing is rejected because a table's rows must each have one cell per column, naming that scenario
    And nothing is written to the directory
    And `adrs/0099-old-rule.md` is still in that directory

  @slice-75
  Scenario Outline: Publishing is refused when, among the files publishing may delete, one cannot be read
    Pins that publishing never deletes around a file it could not read, that the user is told which file it is, and that a refused publish leaves the directory exactly as it found it.
    Given a directory holding <unreadable file>, which cannot be read
    And no artifact is published under that name
    And the directory also holds `adrs/0099-old-rule.md`, whose published-from line names a decision linking to another shop of the same product
    When the user publishes the shop's spec into that directory
    Then publishing is rejected because that file cannot be read, naming <unreadable file>
    And nothing is written to the directory
    And `adrs/0099-old-rule.md` is still in that directory
    And <unreadable file> is still in that directory

    Examples:
      | unreadable file                  |
      | `spec/capabilities/old-cache.md` |
      | `features/old-cache.feature`     |
      | `adrs/0098-old-cache.md`         |
