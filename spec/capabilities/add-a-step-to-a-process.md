---
id: capability/add-a-step-to-a-process
title: Add a step to a process
narrator: the user, building up a process a step at a time
rests_on:
  - decision/append-and-delete
  - decision/shared-steps-get-used
  - decision/ids-minted-by-kb
formulated_as: features/add-a-step-to-a-process.feature
---

# Add a step to a process

## Purpose

Adding a step to the end of a process, under a name the shop gives it. The step is either written in place, or borrowed from a shared step with settings of its own, without altering that step or the other processes that use it. Rewriting or removing a step is not part of this capability (revise-an-artifact).

## Behaviour

- When the user adds a step written in place to a process, saying which role they are and why, the new step is the last step of the process, and the user is shown the name the new step is known by.
- When the user adds a step to a process that uses a shared step with settings of its own, saying which role they are and why, the process runs the shared step at that point with those settings, and the shared step and every other process using it are unchanged.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol append <name>#<collection> --from <file or -> -m <why>` | Append |

- The locator is read as `write`'s is.
- The file is checked against the `content` shape.
- The actor and message are asked for as in record-an-artifact.
- The answer shows `id`, as `<name>#<collection>/<item>` from the item name kb gives back, and `revision`.

## Not yet

Nothing deferred.
