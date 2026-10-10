# formulated from spec/capabilities/name-an-artifact.md
Feature: Name an artifact
  Narrator: the user, naming an artifact to any shop-knol command

  Background:
    Given a shop knowledge base holding a capability named "find-the-knowledge-base" in the context "missingmass.io/shopsystem/shop-knowledge"
    And a capability of the same name in the context "missingmass.io/shopsystem/shop-kb"

  Scenario Outline: Whenever shop-knol shows the user the name of an artifact, it is shown short, in a JSON answer as in a YAML one
    Pins that every artifact name the user is shown is in short form whichever way the answer is written, so the user can type back whatever they read.
    Given the capability in "missingmass.io/shopsystem/shop-knowledge" rests on a decision of that context
    When the user reads the capability, naming it by its short IRI and asking for <the answer>
    Then every name of an artifact the user is shown is its short IRI, never its full one

    Examples:
      | the answer          |
      | the default, YAML   |
      | JSON                |

  Scenario Outline: Whenever shop-knol shows the user the name of a shop or a product, it is shown short, in a JSON answer as in a YAML one
    Pins that a shop and a product are named back to the user like any artifact, in short form whichever way the answer is written.
    Given the capability in "missingmass.io/shopsystem/shop-knowledge" links to its shop, "missingmass.io/shopsystem/shop-knowledge", of the product "missingmass.io/shopsystem"
    When the user follows the capability's links to its shop and that shop's product, asking for <the answer>
    Then the name of the <one named> the user is shown is its short IRI, never its full one

    Examples:
      | one named | the answer        |
      | shop      | the default, YAML |
      | shop      | JSON              |
      | product   | the default, YAML |
      | product   | JSON              |

  Scenario Outline: Whenever shop-knol shows the user a type beside an artifact, it is shown by its name and the version that artifact names, in a JSON answer as in a YAML one
    Pins that an artifact shows the version of its type it was last written against, even where a later version would also fit it, so what is behind its type stays in sight.
    Given the capability in "missingmass.io/shopsystem/shop-knowledge" was last written against the first version of the capability type
    And the capability type has a later version, which the capability also fits
    When the user reads the capability, naming it by its short IRI and asking for <the answer>
    Then the capability's type is shown by its name and its first version

    Examples:
      | the answer        |
      | the default, YAML |
      | JSON              |

  Scenario Outline: Whenever shop-knol shows the user a type on its own, it is shown by its name and its current version, in a JSON answer as in a YAML one
    Pins that a type shown apart from any artifact is shown as it stands now, by name and version, whichever way the answer is written.
    Given the capability type has a version later than its first
    When the user lists the shop's types, asking for <the answer>
    Then the capability type is shown by its name and its current version

    Examples:
      | the answer        |
      | the default, YAML |
      | JSON              |

  Scenario Outline: The user names an artifact by its short IRI, whatever context it is in
    Pins that a short IRI names one artifact on its own, so the context the user has set neither narrows nor redirects it.
    Given SHOP_CONTEXT names <the context set>
    When the user reads the capability in "missingmass.io/shopsystem/shop-knowledge", naming it by its short IRI
    Then the user sees the capability in "missingmass.io/shopsystem/shop-knowledge", and not the one of the same name in "missingmass.io/shopsystem/shop-kb"

    Examples:
      | the context set                                                          |
      | the capability's own context, "missingmass.io/shopsystem/shop-knowledge" |
      | another context, "missingmass.io/shopsystem/shop-kb"                     |

  Scenario Outline: The user names an artifact by its full IRI, whatever context it is in
    Pins that a full IRI names one artifact on its own, so the context the user has set neither narrows nor redirects it.
    Given SHOP_CONTEXT names <the context set>
    When the user reads the capability in "missingmass.io/shopsystem/shop-knowledge", naming it by its full IRI
    Then the user sees the capability in "missingmass.io/shopsystem/shop-knowledge", and not the one of the same name in "missingmass.io/shopsystem/shop-kb"

    Examples:
      | the context set                                                          |
      | the capability's own context, "missingmass.io/shopsystem/shop-knowledge" |
      | another context, "missingmass.io/shopsystem/shop-kb"                     |

  Scenario: Where SHOP_CONTEXT names a context, the user names an artifact by its name alone
    Pins that a bare name is read in the context the user has set, and only there, even when another context holds an artifact of the same name.
    Given SHOP_CONTEXT names "missingmass.io/shopsystem/shop-knowledge"
    When the user reads "find-the-knowledge-base", naming it by its name alone
    Then the user sees the capability in "missingmass.io/shopsystem/shop-knowledge", and not the one of the same name in "missingmass.io/shopsystem/shop-kb"

  Scenario: Where SHOP_CONTEXT names a context, the user names an artifact by its type and its name
    Pins that giving the type with the name picks out the one artifact of that type in the context set, past others of the same name.
    Given SHOP_CONTEXT names "missingmass.io/shopsystem/shop-knowledge"
    And a decision named "find-the-knowledge-base" in the context "missingmass.io/shopsystem/shop-knowledge"
    When the user reads "find-the-knowledge-base", naming it by its type, capability, and its name
    Then the user sees the capability in "missingmass.io/shopsystem/shop-knowledge"
    And not the decision of the same name, nor the capability of the same name in "missingmass.io/shopsystem/shop-kb"

  Scenario: Where SHOP_CONTEXT names a context, a name alone carried by artifacts of more than one type in it is refused
    Pins that a bare name the context cannot settle is refused rather than guessed at, and that the refusal shows the user what they could have meant.
    Given SHOP_CONTEXT names "missingmass.io/shopsystem/shop-knowledge"
    And a decision named "find-the-knowledge-base" in the context "missingmass.io/shopsystem/shop-knowledge"
    When the user reads "find-the-knowledge-base", naming it by its name alone
    Then the command is rejected because the name is ambiguous, naming the capability and the decision in "missingmass.io/shopsystem/shop-knowledge" that carry it
    And the command reports failure to whatever ran it

  Scenario: A name that is neither a short nor a full IRI, while SHOP_CONTEXT is not set, is refused
    Pins that a name needing a context is refused when none is set, and that the refusal tells the user which setting supplies one.
    Given SHOP_CONTEXT is not set
    When the user reads "find-the-knowledge-base", naming it by its name alone
    Then the command is rejected because no context is named, naming SHOP_CONTEXT
    And the command reports failure to whatever ran it

  Scenario: A name that is neither a short nor a full IRI, while SHOP_CONTEXT is set empty, is refused
    Pins that an empty setting is told apart from a missing one: it is refused as naming no context, not read as any context.
    Given SHOP_CONTEXT is set empty
    When the user reads "find-the-knowledge-base", naming it by its name alone
    Then the command is rejected because SHOP_CONTEXT names no context
    And the command reports failure to whatever ran it
