---
id: capability/revise-an-artifact
title: Revise an artifact
narrator: the user, revising what the shop has recorded
rests_on:
  - decision/a-part-is-named-with-a-hash
  - decision/actor-and-message-asked-once
  - decision/yaml-1-2-the-way-kb-reads
formulated_as: features/revise-an-artifact.feature
---

# Revise an artifact

## Purpose

Replacing a recorded artifact's wording, either whole or one section of it, so that its version moves on. A revision is held to the same rules about what the shop can keep as a new record. A refused revision leaves the artifact as it was. Adding an item to a collection is not part of this capability (add-a-step-to-a-process).

## Behaviour

- When the user replaces an artifact from a file, saying which role they are and why, the shop holds the new wording, and the artifact is at a later version than before.
- When the user replaces one section of an artifact from a file, saying which role they are and why, only that section changes, and the rest of the artifact reads as before.
- If a file replacing an artifact, or one section of it, holds prose in which a line before the last ends in a space, the revision is refused because the shop cannot keep that prose as written, naming the place in the file, and the artifact reads as before at the version it had.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol write <locator> --from <file or -> -m <why>` | Replace |

- A locator is a name, or a name followed by `#` and a place inside it (kb's link notation). shop-knol never computes a place from a section's title.
- A whole write's file is passed as given, so kb refuses a title in it. A part's file holds the part as kb holds it; for a section, that is `title` and `body`.
- The file is checked against the `content` shape.
- The actor and message are asked for as in record-an-artifact: before any file is read or kb is called, each lack its own fault.
- The answer shows `id` (the locator's name) and `revision`.

## Not yet

- **An expected revision** on a replacement, on an addition (add-a-step-to-a-process) or on a removal (retire-an-artifact), using kb's rule `revision`. Promoted when two users revising one artifact lose a change.
