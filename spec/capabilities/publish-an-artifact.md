---
id: capability/publish-an-artifact
title: Publish an artifact
narrator: the user, publishing what the shop knows into files
rests_on:
  - decision/renderers-are-client-code
  - decision/renderers-read-through-source
  - decision/the-agent-renderer
  - decision/an-agents-limits-are-its-names
  - decision/agent-renderer-refuses-a-non-role-and-checks-limits
  - decision/markdown-page-laid-out-from-content-model
  - decision/markdown-lays-out-lists-and-tables
  - decision/markdown-spells-yes-no-and-nothing-in-words
  - decision/an-empty-list-is-an-empty-value
  - decision/renderers-match-the-harness
  - decision/markdown-projection-reads-well-enough
formulated_as: features/publish-an-artifact.feature
---

# Publish an artifact

## Purpose

This capability covers publishing one artifact into files in a directory:
- a process as a skill or a diagram;
- a role as an agent;
- any artifact as a markdown page that stays well-formed and never shows a value the way a program prints it.

Each publisher other than markdown takes only the type it is made from. Skills and agents are held to the limits the harness publishes. Publishing only reads from the shop, and writes nothing when it refuses.

## Behaviour

- When the user publishes a process as a skill into a directory, the directory holds a skill whose heading block is the process's identity and whose body is its steps, with each reused step written out in full, and the knowledge base is unchanged.
- When the user publishes a role as an agent into a directory, the directory holds an agent whose heading block is the role's harness fields and whose body is the role's prose.
- When the user publishes a process as a diagram into a directory, the directory holds a diagram of the process's steps and their branches.
- When the user publishes an artifact as markdown into a directory, the directory holds a page with its identity as a heading, its fields as a list, its sections at their levels and its parts as tables.
- When the user publishes an artifact as markdown, a list of mappings is shown as a table with one column for each key, a list of plain values as a bullet list, and nothing on the page is a programming language's representation of a value.
- When the user publishes an artifact as markdown, a yes or a no is shown as the word yes or no, an empty value (an empty list among them) is shown as nothing, and nothing on the page is a programming language's representation of a value.
- When the user publishes an artifact as markdown, whatever its values hold, every table row has one cell for each column, no line ends in a space, and every value the artifact holds is shown on the page.
- When the user publishes an artifact as markdown, a field holding a mapping is shown as a list nested under the field.
- If the user publishes an artifact as a kind of file that is not made from its type, publishing is refused because that kind is not made from the artifact's type, naming the type, and nothing is written to the directory.
- If a skill would go beyond the limits the harness publishes, the skill is refused because it goes beyond those limits, and nothing is written to the directory.
- If an agent would go beyond the limits the harness publishes, the agent is refused because it goes beyond those limits, and nothing is written to the directory.
- If the user publishes into a directory whose name is given empty, publishing is refused because that directory's name is empty, which names no place, and nothing is written to the working directory.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol render <renderer> <id> --to <dir>` | client-side rendering |

**All renderers**

- Renderers are client code, invoked only by `shop-knol render`. Each reads through the contract and gives back the files to write, or faults. The command writes the files only when the renderer refused nothing.
- A renderer reads the whole artifact at depth 0, with links left as names.
- Renderers name pages and links from IRIs, through the one module that owns them (name-an-artifact).
- `<name>` below is the artifact's name without its kind.

**skill, agent and diagram**

- `skill` (from `process`) writes `SKILL.md` in Anthropic's frontmatter-plus-body shape, in a directory named `<name>`.
- `agent` (from `role`) writes `.claude/agents/<name>.md`. Its heading block is the role's `harness` group as kb gives it, written through `kb.content`. Its body is the role's sections, laid out as the markdown page lays out sections, starting at heading level 1.
- `agent` refuses an artifact that is not a role, as `skill` and `diagram` refuse one that is not a process.
- `diagram` (from `process`) writes `<name>.mmd`, generated from the steps and branches.
- An agent's limits are the two the harness's subagent documentation publishes: `harness.name` may not contain `:` and may not start with `-`. Each limit broken is one fault, with rule `harness-limit`, path `harness.name`, and a message naming the limit and where it was published. No length limit is checked.

**markdown**

- `markdown` (from any type) writes `<name>.md`. No schema is read, and no type is named. Only `sections` is told apart from fields.
- The heading is `# <title>`, using the title from the read's answer.
- Fields are listed in the order kb gives them, as `- **<field>**: <value>`. A field group's fields are nested two spaces in. A link is shown as its name.
- A list of plain values is the field's name, then one bullet per value, nested one level in.
- A field holding a list of mappings (a part collection among them) is taken out of the field list and laid out after it, before the sections. It is the field's name in bold on its own line, then a table:
  - one column per key, in the order the keys first appear across the items;
  - one row per item;
  - an empty cell where an item lacks the key.
- Each section is a heading one level below its holder, starting at level 2. Its body has trailing whitespace stripped. The section layout is shared with the agent renderer.
- Where a block cannot sit (in a table cell, or in a list of mappings inside a field group), a value is laid out inline:
  - a plain value's lines are joined by a space;
  - a mapping becomes `key: value` pairs joined by `, `;
  - a list's items are joined by `; `, each laid out inline in turn.
- A yes is `yes` and a no is `no`. An empty value, an empty list included, is nothing: `- **owner**:` in the field list, an empty cell in a table, and nothing between the separators inline. `True`, `False`, `None`, `true`, `false` and `null` never appear as a value.

## Not yet

- **Renderer sets for product-local or user-local types.** Promoted when a product or a user wants types or renderers of its own; see use-the-shops-types.
