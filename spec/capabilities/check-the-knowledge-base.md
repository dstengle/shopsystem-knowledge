---
id: capability/check-the-knowledge-base
title: Check the knowledge base
narrator: the user, or a script, checking the shop's knowledge is sound
rests_on:
  - decision/a-failing-check-still-shows-what-is-behind
  - capability/find-the-knowledge-base
formulated_as: features/check-the-knowledge-base.feature
---

# Check the knowledge base

## Purpose

This capability covers one check over the whole knowledge base. It names every fault at once, each with where it is. It reports what is behind its type separately from faults. Only faults make the shop unsound. A check with no single knowledge base to check gives no answer at all. Fixing what the check finds is not part of this capability.

## Behaviour

- When the user checks a knowledge base where everything fits its type, the user is told nothing is wrong.
- If the check finds faults, every fault is listed, each naming the artifact and the place in it that is at fault, and the command reports failure to whatever ran it.
- When the user checks a knowledge base where an artifact was last checked against an older version of its type, that artifact is listed as behind its type and not as a fault.
- If the check finds faults while another artifact is behind its type, the faults are listed, and the other artifact is listed as behind its type and not as a fault.
- If a stored file in the knowledge base cannot be read, that file is listed as a fault naming the file, and everything else the shop knows is checked and listed alongside it.
- If no single knowledge base can be found to check, the check is refused for the reason finding the knowledge base gives, and the user is shown no answer from a check: neither that nothing is wrong, nor anything as behind its type.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol validate` | Check |

- A check that finds no fault shows `sound: true` and `behind:` on stdout, and exits 0.
- A check that finds faults prints them on stderr, one line each, and exits 1. It also shows `sound: false` and `behind:` on stdout.
- `behind:` lists each artifact kb reports as stale, under kb's own field names: `artifact`, `schema_version` and `current`. It is empty when nothing is behind.
- An artifact behind its type is never a fault and never on stderr.

## Not yet

Nothing deferred.
