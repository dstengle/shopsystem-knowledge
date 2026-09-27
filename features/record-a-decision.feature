Feature: Record a decision
So that a choice the shop has made is written down where the whole shop can find it, the user can record a decision.

  Background:
    Given a shop knowledge base holding the shop's types

  @slice-1
  Scenario: The user records a decision
    Pins the walking skeleton from the user's side: a decision in a file becomes a named record the shop can read back, under a name the shop mints.
    Given a decision in a file, with a title, a purpose, a rationale and the decision it supersedes
    When the user records that file as a decision, saying who they are and why
    Then the user is shown the name the decision was given, which the user did not choose
    And the shop holds the decision under that name and reads it back by it
    And the decision is at its first version

  @slice-28
  Scenario: A decision whose title is already used is given a name of its own
    Pins that names made from titles never collide: a repeated title gets its own name, and nothing already recorded is displaced.
    Given a decision in a file whose title is already used by a decision the shop holds
    When the user records that file as a decision, saying who they are and why
    Then the user is shown a name of its own for the new decision, the name already taken with a number added
    And the decision recorded earlier still reads back by the name it had

  @slice-28
  Scenario: The user pipes a decision in instead of naming a file
    Pins that a decision may arrive straight from another command, so an agent can compose one and record it without a file on disk.
    Given a decision produced by another command
    When the user records it by piping it in, saying who they are and why
    Then the shop holds the decision just as if it had come from a file

  @slice-28
  Scenario: The user records a decision as part of a piece of work
    Pins the second half of attribution: a change can be tied to the job it was done for, not only to the role that made it.
    Given a decision in a file
    And the user works as the shopkeeper on a named piece of work
    When the user records that file as a decision, saying who they are and why
    Then the change is attributed to the shopkeeper and to that piece of work

  @slice-26
  Scenario: A decision recorded by nobody is refused
    Pins that nothing enters the shop anonymously, so the history can always answer who.
    Given a decision in a file
    And the user has not said which role they are
    When the user records that file as a decision
    Then the decision is rejected because every change must say which role made it

  @slice-26
  Scenario: A decision recorded without a reason is refused
    Pins the companion rule to who: every change carries why, so the history stays readable later.
    Given a decision in a file
    When the user records that file as a decision without a message
    Then the decision is rejected because every change must carry a message

  @slice-26
  Scenario: A decision that does not fit the shop's decision type is refused
    Pins that the shop's types are enforced at the door, and that the refusal says enough to fix the file without reading the type itself.
    Given a file missing something the shop's decision type requires
    When the user records that file as a decision, saying who they are and why
    Then the decision is rejected because it does not fit the shop's decision type
    And the user is told which artifact and which place in it is at fault
    And the command reports failure to whatever ran it

  @slice-1.17
  Scenario: A title in a file that reads as a date is still a title
    Pins that the shop reads files the strict way, so a title that happens to look like a date stays the text that was written.
    Given a decision in a file whose title is written "2026-09-24"
    When the user records that file as a decision, saying who they are and why
    Then the shop reads the title back as the text that was written, not as a date
    And the name the decision was given is made from that text

  @slice-1.17
  Scenario: A title in a file that reads as a yes is still a title
    Pins the same strict reading for the other trap, a title that looks like a yes or a no.
    Given a decision in a file whose title is written "yes"
    When the user records that file as a decision, saying who they are and why
    Then the shop reads the title back as the text that was written, not as a yes or a no
    And the name the decision was given is made from that text

  @slice-1.24
  Scenario: A file naming the same entry twice is refused
    Pins that an ambiguous file is refused rather than resolved by guesswork, and that the user is told where in plain words.
    Given a decision in a file that names the same entry twice in the same place
    When the user records that file as a decision, saying who they are and why
    Then the decision is rejected because an entry is named once and only once, naming the place in the file
    And the user is shown that fault in plain words, never a traceback
    And the command reports failure to whatever ran it

  Scenario: Recording from a file given an empty name is refused
    Pins that a file named with nothing is refused as naming no file, rather than read from somewhere the user did not say.
    When the user records a decision from a file whose name is given empty, saying who they are and why
    Then the decision is rejected because the file it was given has an empty name, which names no place
    And the shop's knowledge base is unchanged
    And the command reports failure to whatever ran it
