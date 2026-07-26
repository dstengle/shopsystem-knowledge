Feature: The render read verb — current-system view
  Beyond navigating a document's edges, the shop-knowledge CLI answers "what
  does the accepted system say right now?". The render verb's current-system
  view projects a single document from a corpus root: for a document in the
  accepted set it emits that document's accepted content sections, and for a
  document outside the accepted set it reports that the document has no
  current-system rendering — because it is not in the accepted set — rather
  than emitting stale content. The view is selected with the ``--view
  current-system`` option, mirroring the navigate verb's positional-head plus
  ``--corpus <root>`` invocation shape.

  @scenario_hash:4cd6d3d6dc4fcd33 @bc:shopsystem-knowledge
  Scenario: render current-system view emits only the accepted content sections of a document
    Given a corpus whose document "adr-068" has status "accepted" and carries content sections plus a changelog section
    When I run the render verb on document id "adr-068" in the current-system view
    Then the exit code is 0
    And the rendered output contains the document's accepted content sections

  @scenario_hash:7583e99ef2647bd4 @bc:shopsystem-knowledge
  Scenario: render current-system view has no rendering for a document whose status is not accepted
    Given a corpus whose document "adr-034" has status "superseded"
    When I run the render verb on document id "adr-034" in the current-system view
    Then the CLI reports that "adr-034" has no current-system rendering because it is not in the accepted set
    And no accepted content is emitted for "adr-034"

  @scenario_hash:3f752398f17674a4 @bc:shopsystem-knowledge
  Scenario: render current-system view DROPS the changelog and supersede-chain transformation material and does not leak it
    Given a corpus whose document "adr-068" has status "accepted", carries a changelog section naming a superseded predecessor, and carries supersede-chain transformation material
    When I run the render verb on document id "adr-068" in the current-system view
    Then the rendered output does not contain the changelog section
    And the rendered output does not contain the named superseded predecessor reference
    And the rendered output does not contain the supersede-chain transformation material

  @scenario_hash:335eb88e9c9fb357 @bc:shopsystem-knowledge
  Scenario: render transformation view emits the full document including changelog and supersede-chain material
    Given a corpus whose document "adr-068" has status "accepted", carries a changelog section, and carries supersede-chain transformation material
    When I run the render verb on document id "adr-068" in the transformation view
    Then the exit code is 0
    And the rendered output contains the document's content sections
    And the rendered output contains the changelog section
    And the rendered output contains the supersede-chain transformation material
