Feature: Additive discipline over the per-type typedefs
  The base schema governs the shared frontmatter fields every artifact carries —
  type, id, title, description, status, created, updated, authors — plus the
  base-governed optionals (distribution, tags, external-references). A per-type
  typedef must state ONLY its per-type deltas: its own required body sections, its
  status enum, and its edge participation (extra required fields). It must not
  re-declare a field the base schema already governs. The knowledge context runs
  an additive-discipline check over the per-type typedef set: a typedef that
  re-declares a base-governed field draws a base-field-redeclaration defect naming
  the typedef and the re-declared field, carrying its check-id and a remediation
  to remove the re-declared base field and inherit it from the base schema, and
  the aggregate verdict exits non-zero. A typedef stating only its per-type deltas
  re-declares no base field and passes.

  @scenario_hash:e4d8b3c856424c18 @bc:shopsystem-knowledge
  Scenario: a per-type typedef re-declaring a base shared field is reported as a defect
    Given a per-type typedef that, beyond its per-type deltas, re-declares the base shared field distribution the base schema already governs
    When the knowledge context runs the additive-discipline check over the per-type typedefs
    Then it reports a base-field-redeclaration defect naming the typedef and the re-declared field distribution
    And the finding carries its check-id and a remediation to remove the re-declared base field and inherit it from the base schema
    And the aggregate verdict exits non-zero

  @scenario_hash:d5e1af8a4c00ffda @bc:shopsystem-knowledge
  Scenario: a per-type typedef stating only its per-type deltas and re-declaring no base field passes
    Given a per-type typedef that declares only its required body sections, its status enum and its edge participation, re-declaring no base shared field
    When the knowledge context runs the additive-discipline check over the per-type typedefs
    Then it reports no base-field-redeclaration defect for that typedef
    And the aggregate verdict exits zero
