---
id: capability/publish-a-shops-spec
title: Publish a shop's spec
narrator: the user, publishing a shop's spec into the shop's repository
rests_on:
  - decision/kb-is-the-source-of-the-spec
  - decision/every-decision-is-an-adr
  - decision/the-shops-types-model-the-bdd-spec
  - decision/renderers-are-client-code
  - decision/renderers-read-through-source
  - decision/a-decision-links-to-its-shop
  - decision/a-ledger-holds-only-the-shops-own-decisions
  - decision/capabilities-depend-on-capabilities
  - decision/a-capability-carries-its-reading-order
  - decision/capabilities-are-deprecated-then-retired
  - decision/a-constraint-is-tested-in-capabilities
  - decision/an-unreadable-file-stops-the-publish
depends_on:
  - capability/use-the-shops-types
  - capability/publish-an-artifact
formulated_as: features/publish-a-shops-spec.feature
---

# Publish a shop's spec

## Purpose

This capability covers publishing a shop's whole spec from the knowledge base into a directory: its index, its active and deprecated capabilities, its ledger, its decision records and the feature files formulating its capabilities, and deleting the files it published earlier that nothing published now stands behind. It is not publishing one artifact on its own (publish-an-artifact), and it is not moving a shop's existing files into the knowledge base. Like every publisher it only reads the knowledge base, and it writes nothing, and deletes nothing, when it refuses anything.

## Behaviour

- When the user publishes a shop's spec into a directory, the directory holds `spec/index.md` from the shop, and the knowledge base is unchanged.
- When the user publishes a shop's spec into a directory, the directory holds `spec/capabilities/<name>.md` for each capability linking to the shop whose status is active or deprecated.
- When the user publishes a shop's spec into a directory, the directory holds `spec/decisions.md`, the ledger of the shop's own decisions, those linking to it, in number order.
- When the user publishes a shop's spec into a directory, the directory holds `features/<name>.feature` for each feature formulating one of the shop's capabilities.
- When the user publishes a shop's spec into a directory, the directory holds `adrs/<number>-<name>.md` for each of the shop's decisions.
- When the user publishes a shop's spec, the index lists the shop's capabilities in their order, the dotted numbers compared part by part as numbers.
- When the user publishes a shop's spec holding a deprecated capability, the directory holds its page, the page says it is deprecated, and its line in the index says it is deprecated.
- When the user publishes a shop's spec holding a retired capability, the directory holds no page and no feature file for it, and the index does not list it.
- When the user publishes a shop's spec, a capability's file is named from its title, lower-cased, with every straight (`'`) and curly (`’`) apostrophe dropped wherever it appears, every run of characters other than the unaccented letters a to z and the digits 0 to 9 made one `-`, and no `-` at either end, and the feature formulating it takes the same name.
- When the user publishes a shop's spec, a decision's record is named from its number, padded with zeros to at least four digits and written in full where it is longer, then its title made into a name the way a capability's is.
- When the user publishes a shop's spec, every file it writes carries a line saying it was published from the knowledge base and is not to be edited by hand; in `spec/index.md` and `spec/decisions.md` the line names the shop and the shop's revision, and in every other file it names the capability, feature or decision the file is published from and that artifact's revision; in a capability's file the line comes directly after the frontmatter, which stays first in the file, and in every other file it is the first line.
- When the user publishes a shop's spec, every entry in its ledger is a decision the knowledge base holds.
- When the user publishes a shop's spec into a directory holding files published earlier, every file under `spec/capabilities/`, `features/` and `adrs/` that carries a published-from line and that this publish does not write is deleted, a file left behind by an artifact published this time under a new name among them, and no other file is deleted.
- When the user publishes a shop's spec into a directory, a file under `spec/capabilities/`, `features/` or `adrs/` that has no published-from line, at a name this publish does not write, is left as it was.
- If two of the shop's capabilities would be published under one file name, publishing is refused because they would share a file, naming both, and nothing is written or deleted.
- If two of the shop's decisions would be published under one file name, publishing is refused because they would share a file, naming both, and nothing is written or deleted.
- If two of the shop's decisions carry one number, publishing is refused because a number names one decision, naming both, and nothing is written or deleted.
- If two of the shop's capabilities carry one order, publishing is refused because an order places one capability, naming both, and nothing is written or deleted.
- If a capability of the shop rests on a decision of another shop, publishing is refused because a capability rests only on its own shop's decisions, naming the capability and the decision, and nothing is written or deleted.
- If a scenario's `uses` names a capability that is not among its capability's dependencies, publishing is refused because a scenario uses only what its capability depends on, naming the scenario and the capability it uses, and nothing is written or deleted.
- If an active or deprecated capability of the shop depends on a retired capability, in any shop, publishing is refused because it depends on a retired capability, naming both, and nothing is written or deleted.
- If a constraint of the shop is tested in a retired capability, publishing is refused because that capability is retired, naming the constraint and the capability, and nothing is written or deleted.
- If two features formulate one of the shop's capabilities, publishing is refused because they would share a file, naming both, and nothing is written or deleted.
- If a table in a feature formulating one of the shop's capabilities has rows of different widths, publishing is refused because a table's rows must each have one cell per column, naming the scenario, and nothing is written or deleted.
- If, among the files publishing may delete, one cannot be read, publishing is refused because that file cannot be read, naming the file, and nothing is written or deleted.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol render spec <shop> --to <dir>` | client-side rendering, reading through Read, List and Follow |

- `spec` is a publisher made from the `shop` type. The directory it writes into is the root of the shop's repository.

| file | from |
|---|---|
| `spec/index.md` | the shop |
| `spec/capabilities/<name>.md` | each capability of the shop |
| `spec/decisions.md` | the ledger: the shop's own decisions |
| `features/<name>.feature` | each feature formulating one of the shop's capabilities |
| `adrs/<number>-<name>.md` | each of the shop's decisions |

- The shop's capabilities are those linking to it whose status is `active` or `deprecated`, in `order`. The shop's decisions are those linking to it. They are the ledger's entries, the decisions published as ADR records, and the decisions whose numbers are judged for collisions.
- The published-from line is an HTML comment in markdown, and a `#` comment in a feature file, ahead of the `# formulated from` line.
- A capability's frontmatter `id`, its `rests_on`, its `depends_on`, and a ledger entry's heading are the names the knowledge base holds (`capability/<slug>`, `decision/<slug>`). The `<name>` made from a title names files only.
- `spec/index.md`: `# <shop title>`; `## Purpose`; `## Constraints carried`, one bullet per constraint, `- **<title>.** <says> Tested in <names>.`, the names those of its `tested_in`, joined with commas and a final "and"; `## Composition (reading order)`, a numbered line per capability in `order`, `<n>. [<name>](capabilities/<name>.md): <gist>`, ending ` (deprecated)` where the capability is deprecated; then the shop's other sections in order.
- `spec/capabilities/<name>.md`: frontmatter `id`, `title`, `narrator`, `status: deprecated` where the capability is deprecated, `rests_on` (a list of decision names), `depends_on` (a list of capability names) after `rests_on`, `formulated_as` (`features/<name>.feature`, where a feature formulates it); `# <title>`; `## Purpose`; `## Behaviour`, one bullet per line's `says`, in the order the capability holds them; `## Implementation, may change` where the capability has it; `## Not yet`, one bullet per deferral, `- **<title>.** <defers> Promoted when <trigger>.`
- `spec/decisions.md`: `# Decisions`, then one entry per decision of the shop, in number order. Each entry is `## <decision name>`, the statement, then `date:`, `revisit_when:` where it has one, `supersedes:` where it has one, and `source: adrs/<number>-<name>.md`.
- `adrs/<number>-<name>.md`: `# <number> <title>`, `<number>` padded as in the file name; a paragraph `<date>. <Purpose>`; the Rationale as the next paragraph; then `Supersedes <number>.` and `Extends <number>.` lines, padded the same way, where it has them.
- `features/<name>.feature`: `# formulated from spec/capabilities/<name>.md`; `Feature: <title>`; `  Narrator: <the capability's narrator>`; a `Background:` where it has steps; then each scenario in order: its labels on one line, `Scenario:` (or `Scenario Outline:` where it has examples) and its title, its description, its steps, a step's table with its columns padded to one width, a docstring between `"""` lines, and `Examples:` with its table padded the same way. Two-space indentation, as the shop's feature files are written today.
- Deleting reads the published-from line of each file under `spec/capabilities/`, `features/` and `adrs/` in the directory. Files elsewhere in the directory are not deleted; `spec/index.md` and `spec/decisions.md` are written over. A file there that cannot be read is a fault on that file, as an operating-system error on a path is.

## Not yet

- **Moving a shop's real spec into the knowledge base.** An agent drafts each shop's create batches from its files (handles for Behaviour lines included, and an ADR drafted for every decision that has none, from its source), and publishing the shop reproduces its files but for differences the person approves once. Promoted when kb publishes a validate-only mode on its batch calls and the pin is bumped to it, and shopsystem-bdd releases its writer agents' tools and draft form, integrating-a-proposal's apply step, formulating-features' apply step, and the capability format's note of the published-from line.
- **Checking that a shop's committed files match a fresh publish.** A make target in each shop's repository can do it with `render spec`. Promoted when a shop's committed files are found to differ from a fresh publish.
- **Product-level decisions in a shop's ledger.** The lead shop's decisions, listed in another shop's ledger. Promoted when a shop needs one in practice.
- **`depends_on` in shopsystem-bdd's capability format.** A request to shopsystem-bdd: the capability format defines `depends_on` (the capabilities a capability builds on, in its own context or another) beside `rests_on` (decisions). Promoted when shopsystem-bdd releases a capability format that defines it.
