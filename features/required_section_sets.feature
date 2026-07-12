Feature: Required-section sets resolved per type
  Beyond frontmatter, each artifact type carries a required-section set its
  document body must contain. The knowledge context checks a document's body
  against its own type's required-section set — a pdr must carry the sections
  the pdr set demands (including Options considered), an intent-record must
  carry the intent-record set, and neither type's set is imposed on the other.
  A document missing a required section is reported non-conforming with the
  missing section named; a document carrying its full set passes.

  @scenario_hash:13d1e7a3a4098b20 @bc:shopsystem-knowledge
  Scenario: a document missing a required body section is reported non-conforming and names the section
    Given a pdr document whose body omits the Options considered section its type's required-section set demands
    When the knowledge context checks the document's body against its type's required-section set
    Then it reports the document as non-conforming for a missing required section
    And the diagnosis names Options considered as the missing section

  @scenario_hash:35ab526df01673b5 @bc:shopsystem-knowledge
  Scenario: a document carrying its type's full required-section set passes
    Given a pdr document whose body carries every section in its type's required-section set
    When the knowledge context checks the document's body against its type's required-section set
    Then it reports the document as conforming on body structure
    And it names no missing required section

  @scenario_hash:f7aed937f67018da @bc:shopsystem-knowledge
  Scenario: the required-section set is resolved per type
    Given an intent-record document whose body omits a section that the pdr required-section set demands but that the intent-record required-section set does not
    When the knowledge context checks the document's body against its type's required-section set
    Then it reports the intent-record as conforming on body structure
    And it does not impose the pdr section set on the intent-record
