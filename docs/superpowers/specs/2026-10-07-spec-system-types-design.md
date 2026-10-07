# The shop's types hold the shopsystem-bdd spec

Date: 2026-10-07. Status: approved in conversation; integration under the person's delegation (adrs/0056).
Decisions: adrs/0051 to 0055.

A proposal against `spec/`. It reshapes the shop's types so a product's knowledge base holds what
shopsystem-bdd produces for each shop: the context's index, its capabilities, its decision records and its
feature files. It adds a publisher that writes a shop's spec into files, and a command that shows which
Behaviour lines are formulated. It does not move any shop's real spec into kb (that waits for
shopsystem-bdd, below).

## Terms

- A **shop** manages one bounded context. A **product** is a group of shops; a **lead shop** holds the
  product's own concerns. One product's knowledge base holds every one of its shops.
- A scenario in one shop never points at a scenario in another. It may point at a capability in another shop.

## The types

`role`, `process`, `step`, `tag` and `work-item` stay as they are. `feature` is replaced, `decision` is
reshaped, and `product`, `shop` and `capability` are new. All of them build on the `shop-artifact` base
(owner, status, tags), which stays. The shop's types are then ten, on the base.

Progressive disclosure is a rule of every type (adrs/0055):

- the fields a type shows at a glance are each one short line, or a link;
- every part carries a short `title`, which is what a glance shows of it and what its name is minted from;
- long prose lives in sections and in a part's own body fields, read one at a time or whole.

"One short line" is written into the types and checked by kb: a gist or a statement is at most 200
characters, a part's title at most 80, and neither holds a line break.

| type | glance fields | other fields | sections (required first) | parts |
|---|---|---|---|---|
| product | `gist` | | Purpose | |
| shop | `product` → product, `gist` | `narrator` (optional), `reading_order` → capability, many, in order | Purpose, Order of building, Testing | `constraints`: `title`, `says`, `pinned_in` → capability, many |
| capability | `shop` → shop, `gist` | `narrator`, `rests_on` → decision, many | Purpose; an `Implementation, may change` section may follow | `behaviour`: `title`, `says` (one EARS line); `not_yet`: `title`, `defers`, `trigger` |
| decision | `statement`, `date`, `supersedes` → decision | `number`, `shop` → shop, `revisit_when` (optional), `extends` → decision, many | Purpose, Rationale | |
| feature | `formulates` → capability | `background`: steps | | `scenarios`: `title`, `description` (optional), `formulates` → a capability's behaviour line, `uses` → capability, many, `labels` (Gherkin tags), `steps`, `examples` (optional) |

- A decision's `date` is a day, `YYYY-MM-DD`. Its `number` is a whole number, given by whoever records
  it as the shop's next; it is the number its ADR file carries.
- A scenario's step is `keyword` (Given, When, Then, And or But), `text`, and optionally a `table` (rows of
  cells, the first row the header) or a `docstring`. `examples` is a table, the first row the header.
- `labels` are plain words such as `@slice-55.3`, not links to `tag` artifacts.
- A scenario's `formulates` is one link into a capability's `behaviour` part:
  `capability/<name>#behaviour/<line>`.

## Publishing a shop's spec

A new publisher, `spec`, made from the `shop` type, writes a shop's whole spec into a directory, the root of
the shop's repository. Like every publisher it only reads, and writes nothing when it refuses anything.

| file | from |
|---|---|
| `spec/index.md` | the shop |
| `spec/capabilities/<name>.md` | each capability of the shop |
| `spec/decisions.md` | the ledger: the shop's decisions and the decisions its capabilities rest on |
| `features/<name>.feature` | each feature formulating one of the shop's capabilities |
| `adrs/<number>-<name>.md` | each of the shop's decisions |

- A capability's `<name>` is its title in lower case, apostrophes dropped, every other run of characters
  that are not letters or digits made one `-`, with none at either end. Its feature takes the same name.
  A decision's `<name>` is made the same way from its title, and `<number>` is its number in four digits.
- Every file begins with a line saying it was published from the knowledge base, naming the artifact and
  its revision, and that it is not to be edited by hand (an HTML comment in markdown, a `#` comment in a
  feature file, ahead of the `# formulated from` line).
- `spec/index.md`: `# <shop title>`; `## Purpose`; `## Constraints carried`, one bullet per constraint,
  `- **<title>.** <says> Pinned in <names>.`, the names joined with commas and a final "and";
  `## Composition (reading order)`, a numbered line per capability in `reading_order`,
  `<n>. [<name>](capabilities/<name>.md): <gist>`; then the shop's other sections in order.
- `spec/capabilities/<name>.md`: frontmatter `id`, `title`, `narrator`, `rests_on` (a list of decision
  names), `formulated_as` (`features/<name>.feature`, where a feature formulates it); `# <title>`;
  `## Purpose`; `## Behaviour`, one bullet per line's `says`, in the order the capability holds them;
  `## Implementation, may change` where the capability has it; `## Not yet`, one bullet per deferral,
  `- **<title>.** <defers> Promoted when <trigger>.`
- `spec/decisions.md`: `# Decisions`, then one entry per decision in number order: `## <decision name>`,
  the statement, then `date:`, `revisit_when:` where it has one, `supersedes:` where it has one, and
  `source: adrs/<number>-<name>.md`. Every entry is a decision the knowledge base holds; none stands alone.
- `adrs/<number>-<name>.md`: `# <number> <title>`; a paragraph `<date>. <Purpose>`; the Rationale as the
  next paragraph; then `Supersedes <number>.` and `Extends <number>.` lines where it has them.
- `features/<name>.feature`: `# formulated from spec/capabilities/<name>.md`; `Feature: <title>`;
  `  Narrator: <the capability's narrator>`; a `Background:` where it has steps; then each scenario in
  order: its labels on one line, `Scenario:` (or `Scenario Outline:` where it has examples) and its title,
  its description, its steps, a step's table with its columns padded to one width, a docstring between
  `"""` lines, and `Examples:` with its table padded the same way. Two-space indentation, as the shop's
  feature files are written today.

The publisher refuses, naming what is at fault, and writes nothing, where:

- a capability names the shop but is not in the shop's `reading_order`, or one in `reading_order` names
  another shop;
- two of the shop's capabilities, or two of its decisions, would be published under one file name;
- two of the shop's decisions carry one number;
- a scenario's `uses` points at a capability of its own shop.

## Seeing what is formulated

`shop-knol coverage <shop>` answers, for the shop's capabilities, the Behaviour lines no scenario
formulates and the lines more than one scenario formulates, each as the link to the line with its
capability's title and the line's title. A line with no scenario is normal between integration and
formulation, so this answers; it never refuses for it.

## Starting a knowledge base

`init` furnishes the new set of types, the ten and the base. Nothing else about starting changes. No
knowledge base in use holds artifacts of the old `feature` or `decision` types, so none is converted.

## How kb gets written (outside this repository)

The writer agents of shopsystem-bdd draft `shop-knol apply` batch files and read kb through a read-only
allowlist (`shop-knol read`, `list`, `refs`, `search`, `types`). The controller validates the drafts before
the gate, applies the creates and then the writes after it, publishes the shop's spec and commits it. This
needs:

- **from kb:** a validate-only mode on the batch calls, so a batch is checked before the gate and nothing
  lands. A write that links to an artifact the round creates can only be checked once the creates have
  landed. kb removed mixed-kind batches on purpose, so none is asked for.
- **from shopsystem-bdd:** the writer agents' tools and draft form, integrating-a-proposal's apply step,
  formulating-features' apply step, and the capability format's note of the published-from line.

Each is a request logged in this repository's plan. Moving a shop's real spec into kb waits for both: an
agent drafts each shop's create batches from its files (handles for Behaviour lines included, and an ADR
drafted for every decision that has none, from its source), and publishing the shop reproduces its files
but for differences the person approves once.

## Not in this proposal

- The slice plan as types (slices, backlog, log). Slices point at scenarios, so the spec's types do not
  change when they come.
- The product's own concerns beyond the `product` artifact itself.
- Checking that a shop's committed files match a fresh publish; a make target in each shop's repository
  can do it with `render spec`.
