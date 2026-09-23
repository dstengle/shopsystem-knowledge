Feature: Work on the shop's knowledge without a shell
So that a role that only tends the shop's knowledge cannot reach anything else, the corpus-only role can work through the command line alone.

  @assumes-corpus-only-roles-get-no-shell
  Scenario: A corpus-only role records a decision
    Given a corpus-only role whose only permission is to run shop-knol
    When the corpus-only role records a decision, saying who they are and why
    Then the decision is in the shop

  @assumes-corpus-only-roles-get-no-shell
  Scenario: A corpus-only role cannot reach the files behind the knowledge base
    Given a corpus-only role whose only permission is to run shop-knol
    When the corpus-only role tries to run anything other than shop-knol
    Then the command is rejected because a corpus-only role may run nothing but shop-knol
