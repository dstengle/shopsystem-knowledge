Feature: Per-type derives-from optionality
  The knowledge context resolves each type's required fields from the single
  registry in knowledge.artifact_types. Only the types that additionally
  require a derives-from anchor — brief, pdr and adr — carry it in their
  extra_required_fields; the discovery-first kinds intent-record, candidate
  and prioritization-record do not schema-require derives-from at all. So an
  artifact of one of those kinds conforms when it omits derives-from, and the
  conformance check never reports derives-from as a missing required field for
  a kind whose type does not require it. This pins the negative — that
  derives-from optionality is resolved per type, not imposed globally.

  @bc:shopsystem-knowledge
  @scenario_hash:074dabd350908eda
  Scenario Outline: a kind that does not schema-require derives-from conforms when the field is absent
    Given a <kind> artifact that carries every field its type additionally requires but carries no derives-from field
    When the knowledge context validates the artifact's frontmatter against the schema
    Then it reports the artifact as conforming
    And it does not report derives-from as a missing required field

    Examples:
      | kind                  |
      | intent-record         |
      | candidate             |
      | prioritization-record |
