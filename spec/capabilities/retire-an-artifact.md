---
id: capability/retire-an-artifact
title: Retire an artifact
narrator: the user, tidying away what the shop no longer uses
rests_on:
  - decision/append-and-delete
formulated_as: features/retire-an-artifact.feature
---

# Retire an artifact

## Purpose

Taking an artifact out of the shop for good when nothing depends on it. While something still points at it, retiring is refused, and the user is shown what depends on it, so tidying never breaks a link.

## Behaviour

- When the user retires an artifact nothing points at, saying which role they are and why, the shop no longer holds it.
- If something in the shop still points at an artifact, retiring it is refused because something still points at it, and the user is shown everything that points at it.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol delete <locator> -m <why>` | Remove |

- The actor and message are asked for as in record-an-artifact.
- The answer shows `id` (the locator's name) and `revision`.
- A removal kb refuses because the artifact is still pointed at prints one line for each thing that points at it, as kb names them.

## Not yet

Nothing deferred.
