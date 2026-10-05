---
id: capability/record-an-artifact
title: Record an artifact
narrator: the user, recording something new in the shop's knowledge
rests_on:
  - decision/ids-minted-by-kb
  - decision/actor-from-kb-actor
  - decision/actor-and-message-asked-once
  - decision/yaml-1-2-the-way-kb-reads
  - decision/user-files-checked-against-shapes
formulated_as: features/record-an-artifact.feature
---

# Record an artifact

## Purpose

Recording a new artifact of one of the shop's types, from a file or from piped input. The artifact gets a name the shop mints, starts at its first version, and is attributed to a role and optionally to a piece of work. The content arrives exactly as written. A record is refused when it lacks who or why, does not fit its type, or holds text the shop would have to guess at or alter. Revising, adding to and batching are not part of this capability; each has a capability of its own.

## Behaviour

- When the user records a file as a decision, saying which role they are and why, the user is shown the name the decision was given, which the user did not choose, and the shop reads the decision back by that name at its first version.
- When the user records a decision whose title is already used by one the shop holds, the user is shown a name of its own for the new decision (the name already taken, with a number added), and the decision recorded earlier still reads back by the name it had.
- When the user pipes a decision in instead of naming a file, the shop holds it just as if it had come from a file.
- Where `KB_ACTOR` names a role and a piece of work, a record the user makes is attributed to that role and that piece of work.
- If the user records without saying which role they are, the record is refused because every change must say which role made it.
- If the user records without a message, the record is refused because every change must carry a message.
- If a file does not fit the type it is recorded as, the record is refused because it does not fit that type, naming the artifact and the place in it that is at fault.
- When the user records a file whose title is written as a date, the title reads back as the text that was written, and the name the artifact is given is made from that text.
- When the user records a file whose title is written as a yes, the title reads back as the text that was written, and the name the artifact is given is made from that text.
- If a file names the same entry twice in the same place, the record is refused because an entry is named once and only once, naming the place in the file.
- If a file holds prose in which a line before the last ends in a space, the record is refused because the shop cannot keep that prose as written, naming the place in the file, and the knowledge base is unchanged.
- If the user records from a file whose name is given empty, the record is refused because that file's name is empty, which names no place, and the knowledge base is unchanged.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol create <type> --from <file or -> -m <why>` | Create |

- The actor comes from `KB_ACTOR`, as `role` or `role:execution-id`, and the message from `-m`. Both are asked for before any file is read or kb is called. Unset and empty count the same. Each one lacking is its own fault with no artifact (rule `actor` or `message`), and both are reported when both are lacking. `-m` is not required at the argument level.
- `--from -` reads standard input.
- The file is checked against the `content` shape, which is an object.
- The answer shows the `id` kb chose.

## Not yet

Nothing deferred.
