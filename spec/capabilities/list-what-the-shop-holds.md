---
id: capability/list-what-the-shop-holds
title: List what the shop holds
narrator: the user, who knows the kind of thing but no name
rests_on: []
depends_on:
  - capability/find-the-knowledge-base
formulated_as: features/list-what-the-shop-holds.feature
---

# List what the shop holds

## Purpose

Seeing everything of one kind, optionally narrowed by what a field says, either as entries to pick from or as bare names to feed another command. Reading one of them is not part of this capability (read-an-artifact).

## Behaviour

- When the user lists one type, the user is shown every artifact of that type, each with its name and title.
- When the user lists one type, asking for those whose field holds a given value, the user is shown only the artifacts that match.
- When the user lists one type, asking for names only, the user is shown the names and nothing else.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol list --type <type> [--where k=v ...] [--ids]` | List |

- The answer has no wrapper key.

## Not yet

Nothing deferred.
