Feature: The query read verb — select by frontmatter facet
  Beyond navigating a document's edges and rendering a single document, the
  shop-knowledge CLI answers "which documents match this facet?". The query
  verb is corpus-wide: given a corpus root and a single frontmatter facet /
  value, it selects every document whose facet equals that value and returns a
  compact list — each returned record carrying the matched document's id,
  title, and status. The recognized facets are the frontmatter facets ``type``,
  ``status``, ``tag`` (membership in the document's ``tags`` list), and
  ``distribution``. A query whose facet matches no document is an empty result,
  not an error, mirroring the navigate and render verbs' ``--corpus <root>``
  invocation shape.

  @scenario_hash:7706494f82e8ee1c @bc:shopsystem-knowledge
  Scenario Outline: query selects documents by a single frontmatter facet and returns a compact list
    Given a corpus containing documents that vary by type, status, tag, and distribution
    When I run the query verb selecting documents whose "<facet>" equals "<value>" requesting a compact list
    Then the exit code is 0
    And every returned record carries the matched document's id, title, and status
    And every returned document has "<facet>" equal to "<value>"

    Examples:
      | facet        | value         |
      | type         | adr           |
      | status       | accepted      |
      | tag          | restructuring |
      | distribution | product-wide  |

  @scenario_hash:a374f3f98e20bb25 @bc:shopsystem-knowledge
  Scenario: query whose facet matches no document returns an empty result rather than an error
    Given a corpus that contains no document whose tag equals "nonexistent-tag"
    When I run the query verb selecting documents whose tag equals "nonexistent-tag"
    Then the exit code is 0
    And the result is an empty list
    And the CLI does not report the empty match as an error
