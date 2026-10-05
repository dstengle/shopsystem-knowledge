---
id: capability/search-what-the-shop-knows
title: Search what the shop knows
narrator: the user, finding knowledge without knowing where it lives
rests_on:
  - decision/follow-and-search
  - capability/find-the-knowledge-base
formulated_as: features/search-what-the-shop-knows.feature
---

# Search what the shop knows

## Purpose

Finding knowledge by its words. Each result says where the words were found and shows a snippet, with the strongest result first. A search can be narrowed to one type, or widened to the fields as well as the prose.

## Behaviour

- When the user searches for text, each result names the section it matched and shows a snippet of it, and a result whose section mentions the text most often comes first.
- When the user searches for text within one type, the user is shown only results of that type.
- When the user searches for text in the fields as well as the prose, the results also include artifacts whose fields hold the text.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol search <text> [--type <type>] [--in sections\|fields\|all]` | Search |

- `--in sections` is used when `--in` is not given.
- The answer is a sequence in kb's order, with no wrapper key. Each entry has `id`, `type`, `title`, then `section` or `field` (whichever matched), then `snippet`.

## Not yet

Nothing deferred.
