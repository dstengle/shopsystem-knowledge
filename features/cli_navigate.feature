Feature: The navigate read verb — edge-neighbourhood from frontmatter
  Beyond generating templates and schemas and validating a single document, the
  shop-knowledge CLI answers "what does this document connect to?". The navigate
  verb reads a document's edge-neighbourhood from that document's own
  materialized frontmatter link fields — the forward edges it declares and the
  back-edges materialized on it — listing each incident edge as a link-field,
  target id, and resolved flag, and surfacing each resolved neighbour's id,
  type, status, and title. Because the answer is a single frontmatter lookup on
  the named document, the verb never scans the rest of the corpus for inbound
  edges pointing at it. A navigate on an id absent from the corpus is a named
  error rather than an empty answer.

  @scenario_hash:6197383392195e90 @bc:shopsystem-knowledge
  Scenario: navigate returns the edge-neighbourhood of a document from its materialized frontmatter edges
    Given a corpus whose document "adr-068" carries materialized edges to several neighbours across the three edge pairs
    When I run the navigate verb on document id "adr-068"
    Then the output lists each edge incident on "adr-068" as a link-field, target id, and resolved flag
    And each listed neighbour carries its id, type, status, and title
    And the neighbourhood is answered from "adr-068"'s own frontmatter without scanning the corpus for inbound edges

  @scenario_hash:74bdefca5008a645 @bc:shopsystem-knowledge
  Scenario: navigate on an unknown document id fails and names the offending id
    Given a corpus that contains no document with id "adr-999"
    When I run the navigate verb on document id "adr-999"
    Then the exit code is non-zero
    And stderr names "adr-999" as a document id not present in the corpus

  @scenario_hash:8cb7314c14694005 @bc:shopsystem-knowledge
  Scenario Outline: navigate's direction filter selects which half of the edge pairs the neighbourhood returns
    Given a corpus whose document "adr-068" carries both forward edges and materialized back-edges
    When I run the navigate verb on document id "adr-068" with a direction filter of "<direction>"
    Then the neighbourhood includes the "<included>" edges
    And the neighbourhood excludes the "<excluded>" edges

    Examples:
      | direction | included         | excluded         |
      | forward   | forward          | back             |
      | back      | back             | forward          |
      | both      | forward and back |                  |

  @scenario_hash:cb9dab0549acdf38 @bc:shopsystem-knowledge
  Scenario: navigate surfaces an unresolved or legacy-target edge faithfully rather than hiding it
    Given a corpus whose document "adr-068" carries an edge to a target whose resolution is false or whose target is a legacy artifact
    When I run the navigate verb on document id "adr-068"
    Then the neighbourhood includes that edge with its resolved flag reported as false
    And the CLI does not silently drop the unresolved edge from the neighbourhood

  @scenario_hash:3150738158b1dc32 @bc:shopsystem-knowledge
  Scenario Outline: navigate emits its neighbourhood in the selected output format
    Given a corpus whose document "adr-068" carries materialized edges to several neighbours
    When I run the navigate verb on document id "adr-068" requesting "<format>" output
    Then the exit code is 0
    And the neighbourhood is emitted as a well-formed "<format>" document carrying the incident edges and neighbour facets

    Examples:
      | format |
      | md     |
      | json   |
      | yaml   |
