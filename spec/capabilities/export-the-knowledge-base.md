---
id: capability/export-the-knowledge-base
title: Export the knowledge base
narrator: the user, keeping a readable copy of the shop's knowledge
rests_on:
  - decision/rendered-and-exported-after-every-change
depends_on:
  - capability/find-the-knowledge-base
  - capability/name-an-artifact
formulated_as: features/export-the-knowledge-base.feature
---

# Export the knowledge base

## Purpose

This capability covers writing kb's export of the knowledge base, whole or one context's, into an empty directory, so it can be committed as the readable copy of the shop's knowledge and imported into any store. Recovering a lost server is not part of it: that is the operator's backup, history included.

## Behaviour

- When the user exports the knowledge base into an empty directory, the directory holds kb's export of the whole knowledge base.
- When the user exports one context into an empty directory, the directory holds kb's export of that context.
- When the user exports, the user is shown the position in the history the export reflects.
- If the user exports into a directory that is not empty, the export is refused because the directory is not empty, naming the directory, and nothing is written.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol export <dir>`, whole or selected by context | kb's streamed export call |

## Not yet

- **Exporting what changed since a position.** Only what changed since an earlier export's position is written. Promoted when kb adds it to its export call and the pin is bumped to it.
- **Which types a shop commits in its export and which it leaves to the backup.** Until then the spec types are all committed. Promoted when types such as transcripts arrive.
- **Rendering and exporting after every round of changes.** A request to shopsystem-bdd: after every round of changes applied, the controller publishes with `render spec`, exports with `shop-knol export`, and commits both. Promoted when shopsystem-bdd releases it.
