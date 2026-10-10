# formulated from spec/capabilities/record-an-artifact.md
Feature: Record an artifact
  Narrator: the user, recording something new in the shop's knowledge

  Background:
    Given a shop knowledge base holding the shop's types

  @slice-1
  Scenario: The user records a file as a decision under a name of their choosing
    Pins that the name a decision is recorded under is the one the user chose, and that the shop reads it back by that name from its first version.
    Given a decision in a file, with a title, a purpose, a rationale and the decision it supersedes
    When the user records that file as a decision under a name of their choosing, saying which role they are and why
    Then the user is shown the name they chose
    And the shop reads the decision back by that name
    And the decision is at its first version

  Scenario: The user records an artifact naming some of its parts
    Pins that a part the user names keeps that name, so it can be found by it later.
    Given an artifact in a file with several parts
    When the user records that file under a name of their choosing, naming some of its parts, saying which role they are and why
    Then each part the user named is known by the name the user gave it

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

  Scenario: An artifact recorded without a name is refused
    Pins that the shop never names an artifact on the user's behalf: a record with no name enters nothing.
    Given a decision in a file
    When the user records that file as a decision without naming it, saying which role they are and why
    Then the decision is rejected because every artifact is named by the user
    And the shop's knowledge base is unchanged

  Scenario: An artifact recorded under a name the shop already holds is refused
    Pins that a name already taken is never reused or altered: the record is refused, the taken name is given back, and what was held stays as it was.
    Given a decision the shop holds under a name
    And another decision in a file
    When the user records that file as a decision under that same name, saying which role they are and why
    Then the decision is rejected because that name is taken
    And the user is told the name that is taken
    And the shop's knowledge base is unchanged

  @slice-26
  Scenario: A decision that does not fit the shop's decision type is refused
    Pins that the shop's types are enforced at the door, and that the refusal says enough to fix the file without reading the type itself.
    Given a file missing something the shop's decision type requires
    When the user records that file as a decision, saying who they are and why
    Then the decision is rejected because it does not fit the shop's decision type
    And the user is told which artifact and which place in it is at fault
    And the command reports failure to whatever ran it

  @slice-1.17
  Scenario: The user records a file whose title is written as a date
    Pins that the shop reads files the strict way, so a title that happens to look like a date stays the text that was written.
    Given a decision in a file whose title is written "2026-09-24"
    When the user records that file as a decision under a name of their choosing, saying which role they are and why
    Then the shop reads the title back as the text that was written, not as a date

  @slice-1.17
  Scenario: The user records a file whose title is written as a yes
    Pins the same strict reading for the other trap, a title that looks like a yes or a no.
    Given a decision in a file whose title is written "yes"
    When the user records that file as a decision under a name of their choosing, saying which role they are and why
    Then the shop reads the title back as the text that was written, not as a yes or a no

  @slice-1.24
  Scenario: A file naming the same entry twice is refused
    Pins that an ambiguous file is refused rather than resolved by guesswork, and that the user is told where in plain words.
    Given a decision in a file that names the same entry twice in the same place
    When the user records that file as a decision, saying who they are and why
    Then the decision is rejected because an entry is named once and only once, naming the place in the file
    And the user is shown that fault in plain words, never a traceback
    And the command reports failure to whatever ran it

  @slice-50.18.1
  Scenario: A decision whose prose the shop cannot keep is refused
    Pins that text the shop cannot keep as written is refused in plain words, naming where it is, rather than altered quietly or ended in a traceback.
    Given a decision in a file whose prose has a line ending in a space before its last line
    When the user records that file as a decision, saying who they are and why
    Then the decision is rejected because the shop cannot keep prose in which a line before the last ends in a space, naming the place in the file
    And the user is shown that fault in plain words, never a traceback
    And the shop's knowledge base is unchanged
    And the command reports failure to whatever ran it

  @slice-50.17
  Scenario: Recording from a file given an empty name is refused
    Pins that a file named with nothing is refused as naming no file, rather than read from somewhere the user did not say.
    When the user records a decision from a file whose name is given empty, saying who they are and why
    Then the decision is rejected because the file it was given has an empty name, which names no place
    And the shop's knowledge base is unchanged
    And the command reports failure to whatever ran it
