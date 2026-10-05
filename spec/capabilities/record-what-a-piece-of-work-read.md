---
id: capability/record-what-a-piece-of-work-read
title: Record what a piece of work read
narrator: an agent doing a piece of work
rests_on:
  - decision/history-filters-and-snapshot
formulated_as: features/record-what-a-piece-of-work-read.feature
---

# Record what a piece of work read

## Purpose

Anchoring a piece of work in time, so that later changes cannot rewrite what it was working from. The agent records which version of each artifact it read, as one entry in the history. Reviewing that history is not part of this capability (review-who-changed-what).

## Behaviour

- When an agent records, for its piece of work, the artifacts it read, the history holds one entry naming each of them with the version read.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol snapshot --execution <id> <ids...> -m <why>` | Snapshot |

- `snapshot` is a mutating command. It asks for an actor and a message before any call.
- Its actor is `KB_ACTOR`'s role, with `--execution` as the piece of work; this replaces any execution `KB_ACTOR` names.
- The answer is `entry`, the name of the history entry kb made.

## Not yet

Nothing deferred.
