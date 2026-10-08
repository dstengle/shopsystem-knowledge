---
id: capability/read-an-artifact
title: Read an artifact
narrator: the user, reading back one artifact by its name
rests_on:
  - decision/read-levels-and-json
  - decision/json-where-a-command-offers-it
depends_on:
  - capability/find-the-knowledge-base
formulated_as: features/read-an-artifact.feature
---

# Read an artifact

## Purpose

This capability covers reading one artifact by its name at a chosen level:
- at a glance, the default;
- one section;
- whole, with links left as names;
- whole, with links filled in to a depth the reader chooses.

The answer can be taken as JSON. Finding artifacts without knowing their names is not part of it; listing, following links and searching each have a capability of their own.

## Behaviour

- When the user reads an artifact, the user is shown its name, its title and the few fields the shop shows for its type, a stub of each thing it points at, and how many things point back at it, and of what kind.
- When the user reads one section of an artifact by its title, the user is shown that section and nothing else.
- When the user reads an artifact whole, the user is shown every field, every section and every part it holds, and what it points at is shown by name only.
- When the user reads an artifact whole, asking for what it points at to be filled in without saying how far, each thing it points at is shown in place of its pointer as the shop holds it now, and what those things point at is shown by name only.
- When the user reads an artifact whole, asking for what it points at to be filled in two steps, each thing it points at is shown in place of its pointer, and so is each thing those point at.
- When the user reads an artifact asking for JSON, the user gets the same answer as the default, written as JSON.
- If the stored file of the artifact being read cannot be read, the read is refused because that file cannot be read, naming the file.
- If the user reads an artifact whose name is given empty, the read is refused because that artifact's name is empty, which names no place.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol read <locator> [--section <title>] [--whole] [--resolve [<depth>]] [--json]` | Read, with the level asked as one of summary, whole with a depth, or section |

- A locator is a name, or a name followed by `#` and a place inside it (kb's link notation).
- With none of the level flags, the read asks for the summary level.
- `--section <title>` is a section read, using the title as given.
- `--whole` is a whole read at depth 0, with links as names.
- `--resolve [<depth>]` is a whole read at that depth, with links filled in. `--resolve` alone means depth 1.
- `--resolve` implies `--whole`. `--section` wins when given with either.
- A whole read shows kb's identity, then its content. A section read shows what kb gives and nothing else.
- `--json` is taken by `read` alone.

## Not yet

Nothing deferred.
