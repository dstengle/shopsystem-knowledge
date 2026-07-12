Feature: Frontmatter conformance against the per-type schema
  The knowledge context validates an artifact's YAML frontmatter against the
  schema for its type. Every artifact shares eight required fields — type, id,
  title, status, created, updated, authors and description — and each of the
  eight recognized types then adds its own id pattern, status enum, and any
  type-additional required fields. A conforming artifact carries every required
  field, an id matching its type's pattern, and a status in its type's enum; a
  non-conforming artifact is reported with a diagnosis that names the specific
  missing field, offending value, or expected pattern. Disclosure level is a
  projection the tool emits, never a stored frontmatter field, so storing it is
  itself non-conforming.

  @scenario_hash:db21cc6c83e49a32 @bc:shopsystem-knowledge
  Scenario: a well-formed artifact passes frontmatter conformance
    Given an artifact whose frontmatter carries type, id, title, status, created, updated, authors and description
    And the id matches the id pattern its type requires
    And the status value is a member of the enum its type recognizes
    And it carries every field its type additionally requires
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as conforming
    And it reports no missing required fields

  @scenario_hash:dcb78f54444f0172 @bc:shopsystem-knowledge
  Scenario: an artifact missing the required description field is reported non-conforming and names it
    Given an artifact whose frontmatter omits the required description field
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming
    And the diagnosis names description as the missing required field

  @scenario_hash:3a2adff5f24f01d1 @bc:shopsystem-knowledge
  Scenario: an artifact missing the required authors field is reported non-conforming and names it
    Given an artifact whose frontmatter omits the required authors field
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming
    And the diagnosis names authors as the missing required field

  @scenario_hash:8d68a9e86023dab6 @bc:shopsystem-knowledge
  Scenario: an artifact missing the required updated field is reported non-conforming and names it
    Given an artifact whose frontmatter carries created but omits the required updated field
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming
    And the diagnosis names updated as the missing required field

  @scenario_hash:c07e8db63b3c1b42 @bc:shopsystem-knowledge
  Scenario: a status value outside the type's recognized enum is reported non-conforming and names the offending value
    Given a candidate artifact whose frontmatter carries a status value of "in-progress"
    And "in-progress" is not a member of the candidate status enum exploring, shaped, briefed, parked or rejected
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming for an unrecognized status
    And the diagnosis names the offending value "in-progress"

  @scenario_hash:b8ed5d4027a77e2f @bc:shopsystem-knowledge
  Scenario: an id that does not match the type's id pattern is reported non-conforming
    Given a candidate artifact whose id is "candidate-1" rather than the cand-NNN pattern its type requires
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming for an id that does not match its type pattern
    And the diagnosis names the offending id and the expected pattern

  @scenario_hash:6f57407593cf4701 @bc:shopsystem-knowledge
  Scenario: an unrecognized type value is reported non-conforming and names the offending value
    Given an artifact whose frontmatter carries a type value of "roadmap"
    And "roadmap" is not one of the eight recognized artifact types
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming for an unrecognized type
    And the diagnosis names the offending value "roadmap"

  @scenario_hash:2363911877f9f657 @bc:shopsystem-knowledge
  Scenario: an artifact missing a field its type additionally requires is reported non-conforming
    Given a pdr artifact whose frontmatter carries every shared required field but omits the decision-makers field its type additionally requires
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming
    And the diagnosis names decision-makers as the missing type-required field

  @scenario_hash:cc1cd04c1bf2cbe6 @bc:shopsystem-knowledge
  Scenario: a pdr omitting the required derives-from field is reported non-conforming and names it
    Given a pdr artifact whose frontmatter carries every shared required field but omits the derives-from field its type additionally requires
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming
    And the diagnosis names derives-from as the missing type-required field

  @scenario_hash:f40ef843faf4bb62 @bc:shopsystem-knowledge
  Scenario: an adr whose derives-from list is empty is reported non-conforming for anchoring to nothing
    Given an adr artifact whose frontmatter carries a derives-from field whose value is an empty list
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming for an adr that anchors to no upstream artifact
    And the diagnosis names derives-from and states that an adr requires at least one anchor

  @scenario_hash:290cf40f90b418b4 @bc:shopsystem-knowledge
  Scenario: optional fields may be absent and the artifact still conforms
    Given an artifact that carries every required field and a recognized status but omits the optional beads field
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as conforming
    And it does not report the absent beads field as missing

  @scenario_hash:90cd805cff6d9248 @bc:shopsystem-knowledge
  Scenario: disclosure level is a projection and is never a stored frontmatter field
    Given an artifact whose frontmatter carries a stored disclosure-level field pinning its own tier
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as non-conforming for storing a disclosure-level field
    And the diagnosis states that disclosure level is a projection emitted by the tool and is never a stored frontmatter field
