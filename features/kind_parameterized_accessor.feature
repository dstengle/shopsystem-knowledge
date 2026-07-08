@bc:shopsystem-knowledge
Feature: Kind-parameterized projection accessor
  Projections are reached through a single accessor that is parameterized by
  document kind. A kind (for example the architecture-decision kind) is
  registered against its source corpus, and the accessor returns that kind's
  corpus projections only for a kind that has been registered. Requesting a
  kind that was never registered returns a definite kind-not-registered result
  rather than silently defaulting to some other kind's corpus, so an
  unregistered kind can never be mistaken for the architecture-decision corpus.

  @bc:shopsystem-knowledge
  @scenario_hash:f4b64423b77dd3e2
  Scenario: the accessor is parameterized by kind and refuses an unregistered kind
    Given the knowledge context with the architecture-decision kind registered and no other kind registered
    When a caller requests projections for kind "architecture-decision"
    Then the accessor returns the architecture-decision corpus projections
    When a caller requests projections for kind "development-principle"
    Then the accessor returns a definite kind-not-registered result rather than defaulting to the architecture-decision corpus
