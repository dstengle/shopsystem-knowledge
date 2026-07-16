Feature: Real-practice typedef corrections for intent-record, candidate and session-record
  Three typedefs drifted from the shapes real instances actually author. Because
  each artifact type is single-sourced by its typedef and the format generator
  derives its template and schema fragment deterministically from that typedef,
  correcting the typedef flows through to the generated template sections and
  order, the generated schema fragment's status enum and id pattern, and the
  body/frontmatter conformance checks. intent-record carries its eight
  real-practice sections and the single status recorded; candidate carries its
  nine narrative sections and admits the committed status; session-record uses
  the chronological sess-YYYY-MM-DD-x id and the Outcome / Open threads sections.

  @scenario_hash:896573b341f5b713 @bc:shopsystem-knowledge
  Scenario Outline: the intent-record typedef requires each of the 8 real-practice body sections
    Given the intent-record typedef, whose generated template today declares only "Intent" and "Signals of success", sections no real instance has ever used
    And 7 independently-authored intent-record instances (intent-001 through intent-007) that instead consistently carry "<section>" as a body section
    When the knowledge context runs the format generator over the intent-record typedef
    Then the generated intent-record template declares "<section>" as a required body section

    Examples:
      | section                  |
      | Verbatim anchors         |
      | The goal behind the ask  |
      | Who it serves            |
      | Constraints               |
      | Non-goals                |
      | Appetite signal          |
      | Failure conditions       |
      | Open threads             |

  @scenario_hash:55093832fe7b6018 @bc:shopsystem-knowledge
  Scenario Outline: the candidate typedef requires each of the real-practice narrative body sections beyond Verbatim anchors
    Given the candidate typedef, whose generated template today declares only "Context" and "Open questions", sections no real instance has ever used
    And 5 independently-authored candidate instances (cand-001 through cand-005) that instead consistently carry "<section>" as a body section
    When the knowledge context runs the format generator over the candidate typedef
    Then the generated candidate template declares "<section>" as a required body section

    Examples:
      | section                 |
      | Problem                 |
      | Appetite                |
      | Solution sketch         |
      | Rabbit holes            |
      | No-gos                  |
      | Evidence / experiments  |
      | Resolution               |
      | Changelog               |

  @scenario_hash:e44127dc5d9b6214 @bc:shopsystem-knowledge
  Scenario: the intent-record typedef positions Verbatim anchors first, immediately after the title
    Given the intent-record typedef's real-practice section order: Verbatim anchors, The goal behind the ask, Who it serves, Constraints, Non-goals, Appetite signal, Failure conditions, Open threads
    When the knowledge context runs the format generator over the intent-record typedef
    Then the generated intent-record template positions Verbatim anchors immediately after the title and before The goal behind the ask
    And the remaining sections appear in the order Who it serves, Constraints, Non-goals, Appetite signal, Failure conditions, Open threads

  @scenario_hash:4749e223aa6191fe @bc:shopsystem-knowledge
  Scenario: an intent-record document missing a required section is reported non-conforming and names it
    Given an intent-record document whose body carries every section in its type's required-section set except Failure conditions
    When the knowledge context checks the document's body against its type's required-section set
    Then it reports the document as non-conforming for a missing required section
    And the diagnosis names Failure conditions as the missing section

  @scenario_hash:53855e6890abe8f6 @bc:shopsystem-knowledge
  Scenario: an intent-record document carrying its type's full 8-section required set passes
    Given an intent-record document whose body carries Verbatim anchors, The goal behind the ask, Who it serves, Constraints, Non-goals, Appetite signal, Failure conditions and Open threads
    When the knowledge context checks the document's body against its type's required-section set
    Then it reports the document as conforming on body structure
    And it names no missing required section

  @scenario_hash:80695d5c7a12fa63 @bc:shopsystem-knowledge
  Scenario: "recorded" is a valid intent-record status value, matching every real instance
    Given an intent-record artifact whose frontmatter carries a status value of "recorded"
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as conforming
    And it does not report an unrecognized-status diagnosis

  @scenario_hash:74c0d72d8fe0a44a @bc:shopsystem-knowledge
  Scenario: the intent-record status enum is exactly the single real-practice value "recorded"
    Given the intent-record typedef, whose currently generated status enum is draft, active, fulfilled or abandoned — a set no real intent-record instance has ever used
    And 7 independently-authored intent-record instances (intent-001 through intent-007), each carrying status "recorded" and none carrying draft, active, fulfilled or abandoned
    When the knowledge context runs the format generator over the intent-record typedef
    Then the generated schema fragment's status enum for intent-record contains exactly one value, "recorded"
    And none of "draft", "active", "fulfilled" or "abandoned" is a member of the generated status enum

  @scenario_hash:b0f51c6fb7900093 @bc:shopsystem-knowledge
  Scenario: an intent-record artifact carrying a status value outside the real enum is reported non-conforming and names the offending value
    Given an intent-record artifact whose frontmatter carries a status value of "draft"
    And "draft" is not a member of the intent-record status enum recorded
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming for an unrecognized status
    And the diagnosis names the offending value "draft"

  @scenario_hash:9d1e859d505c3417 @bc:shopsystem-knowledge
  Scenario: the candidate typedef's narrative sections follow real practice's order, immediately after Verbatim anchors
    Given the candidate typedef's real-practice section order: Verbatim anchors, Problem, Appetite, Solution sketch, Rabbit holes, No-gos, Evidence / experiments, Resolution, Changelog
    When the knowledge context runs the format generator over the candidate typedef
    Then the generated candidate template positions Problem immediately after Verbatim anchors
    And the remaining sections appear in the order Appetite, Solution sketch, Rabbit holes, No-gos, Evidence / experiments, Resolution, Changelog

  @scenario_hash:a07781fd6a8be6fa @bc:shopsystem-knowledge
  Scenario: a candidate document missing the Resolution section is reported non-conforming and names it
    Given a candidate document whose body carries Verbatim anchors, Problem, Appetite, Solution sketch, Rabbit holes, No-gos and Evidence / experiments but omits Resolution
    When the knowledge context checks the document's body against its type's required-section set
    Then it reports the document as non-conforming for a missing required section
    And the diagnosis names Resolution as the missing section

  @scenario_hash:cd1c9fca88308b79 @bc:shopsystem-knowledge
  Scenario: a candidate document carrying its full 9-section required set passes
    Given a candidate document whose body carries Verbatim anchors, Problem, Appetite, Solution sketch, Rabbit holes, No-gos, Evidence / experiments, Resolution and Changelog
    When the knowledge context checks the document's body against its type's required-section set
    Then it reports the document as conforming on body structure
    And it names no missing required section

  @scenario_hash:ec33b8afc2f6bb2c @bc:shopsystem-knowledge
  Scenario: the candidate typedef's generated status enum includes committed, the value cand-005 uses
    Given the candidate typedef, whose currently generated status enum is exploring, shaped, briefed, parked or rejected — a set that omits committed, the value cand-005's ratification uses
    And 5 independently-authored candidate instances, four (cand-001 through cand-004) carrying status shaped and one (cand-005) carrying status committed once the product authority ratified it
    When the knowledge context runs the format generator over the candidate typedef
    Then the generated schema fragment's status enum for candidate is exploring, shaped, briefed, committed, parked and rejected
    And committed is a member of the generated status enum

  @scenario_hash:6a24c1f3209bc924 @bc:shopsystem-knowledge
  Scenario: a candidate artifact carrying status committed passes frontmatter conformance
    Given a candidate artifact whose frontmatter carries a status value of "committed"
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as conforming
    And it does not report an unrecognized-status diagnosis

  @scenario_hash:73c7c146e1fd5dd3 @bc:shopsystem-knowledge
  Scenario: a status value outside the type's recognized enum is reported non-conforming and names the offending value
    Given a candidate artifact whose frontmatter carries a status value of "in-progress"
    And "in-progress" is not a member of the candidate status enum exploring, shaped, briefed, committed, parked or rejected
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming for an unrecognized status
    And the diagnosis names the offending value "in-progress"

  @scenario_hash:ff935d77ed96b4ae @bc:shopsystem-knowledge
  Scenario: the session-record id pattern matches real practice's chronological, human-readable shape
    Given the session-record typedef, whose currently generated id pattern is session-\d{3,} (e.g. "session-001"), a shape no real instance has ever used
    And 5 independently-authored session-record instances (sess-2026-07-09-a through sess-2026-07-16-a), each using the chronological id pattern sess-YYYY-MM-DD-x
    When the knowledge context runs the format generator over the session-record typedef
    Then the generated session-record id pattern matches a date plus a same-day disambiguating letter suffix, of the shape sess-YYYY-MM-DD-x
    And a real id such as "sess-2026-07-16-a" matches the generated pattern
    And "session-001" no longer matches the generated pattern

  @scenario_hash:06597f5e411a4bd9 @bc:shopsystem-knowledge
  Scenario: a session-record id in the old session-NNN shape is reported non-conforming against the corrected pattern
    Given a session-record artifact whose id is "session-001" rather than the sess-YYYY-MM-DD-x pattern its type requires
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming for an id that does not match its type pattern
    And the diagnosis names the offending id and the expected pattern

  @scenario_hash:588f3f52e2bdf3d4 @bc:shopsystem-knowledge
  Scenario: the session-record typedef requires an Outcome section and an Open threads section, not Summary and Outcomes
    Given the session-record typedef, whose currently generated template declares "Summary" and "Outcomes" as its two body sections, headings no real instance has ever used
    And 5 independently-authored session-record instances that instead consistently carry "Outcome" and "Open threads" as their two body sections
    When the knowledge context runs the format generator over the session-record typedef
    Then the generated session-record template declares Outcome and Open threads as its required body sections
    And it does not declare Summary or Outcomes as required body sections

  @scenario_hash:e65c1fd4c1159391 @bc:shopsystem-knowledge
  Scenario: a session-record document missing the Open threads section is reported non-conforming and names it
    Given a session-record document whose body carries Outcome but omits the Open threads section its type's required-section set now demands
    When the knowledge context checks the document's body against its type's required-section set
    Then it reports the document as non-conforming for a missing required section
    And the diagnosis names Open threads as the missing section

  @scenario_hash:2ac5541d6c0ad3f6 @bc:shopsystem-knowledge
  Scenario: a session-record document carrying Outcome and Open threads passes conformance
    Given a session-record document whose body carries Outcome and Open threads, its type's full required-section set
    When the knowledge context checks the document's body against its type's required-section set
    Then it reports the document as conforming on body structure
    And it names no missing required section
