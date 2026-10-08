---
id: capability/use-the-shops-types
title: Use the shop's types
narrator: the user, working with the shop's kinds of thing
rests_on:
  - decision/types-are-readable
  - decision/types-have-a-command-of-their-own
  - decision/ten-types-on-a-shop-artifact-base
  - decision/role-splits-harness-from-identity
  - decision/a-tag-is-an-artifact
  - decision/the-shops-types-model-the-bdd-spec
  - decision/short-fields-for-progressive-disclosure
  - decision/a-decision-links-to-its-shop
  - decision/a-capability-carries-its-reading-order
  - decision/capabilities-depend-on-capabilities
  - decision/capabilities-are-deprecated-then-retired
formulated_as: features/use-the-shops-types.feature
---

# Use the shop's types

## Purpose

This capability covers what the user can do with the shop's ten types:
- see which types the shop holds, through a command for the shop's types that is separate from the commands for artifacts;
- read one of them, through the same command;
- record things whose shape the types give, such as a role's two groups of fields, a tag held once and named elsewhere, a process's steps, and a shop's spec: its product, the shop itself, its capabilities, its decisions and the features formulating them.

The types arrive when a knowledge base is set up (start-a-knowledge-base). Defining or changing a type is not offered. How a type is enforced is kb's job, and it surfaces as a refusal of a change (record-an-artifact).

## Behaviour

- When the user asks which types the shop holds, the user is shown each of the shop's types.
- When the user reads one of the shop's types by its name, the user is shown that type as the shop holds it.
- Every artifact of the shop's ten types can carry an owner, a status and tags, among the fields every shop artifact carries.
- When the user records a role, the fields the harness needs are kept as one named group, and the fields that say who the role is in the shop are kept as another.
- When the user tags a decision with a tag the shop holds, the decision names that tag, and the tag's description is held once, on the tag itself.
- A process's steps each either define a step in place, or use a shared step with settings of their own.
- When the user reads a product, a shop, a capability, a decision or a feature at a glance, each field it shows is one short line or a link, as it was recorded.
- When the user reads an artifact holding parts at a glance, each part is shown by its title.
- When the user records an artifact holding parts, each part's name is minted from its title.
- If the user records a gist or a statement longer than 200 characters, the change is refused because it does not fit its type.
- If the user records a gist or a statement that holds a line break, the change is refused because it does not fit its type.
- If the user records a part whose title is longer than 80 characters, the change is refused because it does not fit its type.
- If the user records a part whose title holds a line break, the change is refused because it does not fit its type.
- If the user records a scenario whose `uses` points at anything but a capability, the change is refused because it does not fit its type.
- When the user records a feature, each of its scenarios names the one Behaviour line it formulates, as a link into a capability's Behaviour lines.
- When the user records a scenario with labels, each label is kept as a plain word, not as a link to a tag.
- When the user records a capability that depends on capabilities of its own shop and of other shops, the capability names each capability it depends on.
- If the user records a capability whose status is not active, deprecated or retired, the change is refused because it does not fit its type.
- If the user records a capability whose order is not one or more whole numbers joined by dots, such as 3 or 3.1.2, the change is refused because it does not fit its type.
- When the user sets a capability's status to retired while other capabilities or scenarios depend on it, in any shop, the capability is recorded as retired.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol types` | lists the shop's types |
| `shop-knol types <name>` | reads one of the shop's types |

- The command's name may change. `create`, `write`, `list` and `read` are not the way to the types.
- The types are schema artifacts in kb's schema language: `product`, `shop`, `capability`, `decision`, `feature`, `work-item`, `role`, `process`, `step` and `tag`.
- `role`, `process`, `step`, `tag` and `work-item` stay as they were. `feature` is replaced, `decision` is reshaped, and `product`, `shop` and `capability` are new.
- All ten build on the `shop-artifact` base schema (owner, status, tags) through kb's composition mechanism, so the common fields are declared once.
- The shop's schemas are the ten types and the `shop-artifact` base, eleven in all.
- `role` has two named field groups: `harness` (the harness contract fields) and the corpus identity fields.
- `tag` is a title and a description. Other types target it through a `tags` reference field.
- `process` declares a `steps` part collection. Each item either defines a step inline, or carries `uses: <ref to step>` and `with: <bindings>`.
- kb v0.5.0 refuses a type that puts kb's keywords where kb does not read them, or a `ref` that does not state its whole shape. Each of the eight schemas of the earlier seven-type set was created in a fresh v0.5.0 store and accepted as it was.
- Long prose lives in sections and in a part's own body fields, read one at a time or whole.
- The short lines are written into the types and checked by kb: a `gist` or a `statement` is at most 200 characters, a part's `title` at most 80, and neither holds a line break.

| type | glance fields | other fields | sections | parts |
|---|---|---|---|---|
| product | `gist` | | Purpose | |
| shop | `product` → product, `gist` | `narrator` | Purpose, Order of building, Testing | `constraints`: `title`, `says`, `pinned_in` → capability, many |
| capability | `shop` → shop, `gist` | `narrator`, `order`, `rests_on` → decision, many, `depends_on` → capability, many | Purpose; an `Implementation, may change` section may follow | `behaviour`: `title`, `says` (one EARS line); `not_yet`: `title`, `defers`, `trigger` |
| decision | `statement`, `date`, `supersedes` → decision, `shop` → shop | `number`, `revisit_when`, `extends` → decision, many | Purpose, Rationale | |
| feature | `formulates` → capability | `background`: steps | | `scenarios`: `title`, `description`, `formulates` → a capability's behaviour line, `uses` → capability, many, `labels` (Gherkin tags), `steps`, `examples` |

- Every section listed for a type is required, save the capability's `Implementation, may change`, which may follow: a product requires Purpose; a shop, Purpose, Order of building and Testing; a capability, Purpose; a decision, Purpose and Rationale; a feature has no sections. A missing required section is refused as a change that does not fit its type (record-an-artifact).
- Required fields:
  - product: `gist`;
  - shop: `product`, `gist`;
  - capability: `shop`, `gist`, `narrator`, `order`, `status`;
  - decision: `statement`, `date`, `number`, `shop`;
  - feature: `formulates`;
  - a `behaviour` item: `title`, `says`;
  - a `not_yet` item: `title`, `defers`, `trigger`;
  - a `constraints` item: `title`, `says`;
  - a scenario: `title`, `formulates`, `steps`;
  - a step: `keyword`, `text`.
- Every other field is optional: a shop's `narrator`; a capability's `rests_on` and `depends_on`; a decision's `supersedes`, `extends` and `revisit_when`; a constraint's `pinned_in`; a scenario's `description`, `uses`, `labels` and `examples`; a step's `table` and `docstring`.
- Each link is held in one direction only, and kb answers it from either end. A shop holds no list of its decisions or of its capabilities.
- A decision's `shop` is one link, to the one shop it belongs to. A shop's decisions are the decisions linking to it.
- A capability's `order` is a dotted number (`3`, `3.1`, `3.1.2`), sorted numerically part by part. A shop's capabilities are the capabilities linking to it, in `order`.
- A capability's `depends_on` names the capabilities it builds on, in its own shop or any other. It is kept apart from `rests_on`, which holds decisions only.
- A scenario is part of its capability. Its `uses` names the dependencies that scenario exercises, in the scenario's own shop or another; that each is among its capability's `depends_on` is checked when the shop's spec is published (publish-a-shops-spec).
- A capability's `status` is one of `active`, `deprecated` or `retired`:
  - `active`: part of the shop's contract;
  - `deprecated`: its removal from spec and code is under way in its own shop;
  - `retired`: gone from spec and code, and kept in the knowledge base as the record.
- The other types keep `status` as free text.
- A decision's `date` is a day, `YYYY-MM-DD`. Its `number` is a whole number, given by whoever records it as the shop's next; it is the number its ADR file carries.
- A scenario's step is `keyword` (Given, When, Then, And or But), `text`, and optionally a `table` (rows of cells, the first row the header) or a `docstring`. `examples` is a table, the first row the header.
- `labels` are plain words such as `@slice-55.3`.
- A scenario's `formulates` is one link into a capability's `behaviour` part: `capability/<name>#behaviour/<line>`. A scenario has no field that can point at a scenario.

## Not yet

- **Defining or changing a type.** This would be product-local or user-local extensions: additional schema and renderer sets that shop-knowledge loads, which kb never learns of. When it comes, it belongs to the shop's types command, not to `create` or `write`. Promoted when a product or a user wants types or renderers of its own.
- **Validation that kb's schema language cannot express.** If needed, it would run client-side before the call and would not be binding. Promoted when such a validation is needed.
- **Scenario status over time.** It will be a ledger, modelled later; it will not be a field on the scenario or on a work item. Promoted when assignment cannot be tracked without one, or at the crossover.
- **The slice plan as types.** Slices, the backlog and the log, held as artifacts that point at scenarios; the spec's types do not change when they come. Promoted when the slice plan is to be held in the knowledge base.
- **The product's own concerns.** A lead shop holds the product's own concerns; beyond the `product` artifact itself, none is modelled. Promoted when a product's own concerns are to be held in the knowledge base.
- **Removing a capability as a lifecycle in the workflow.** A request to shopsystem-bdd: integration deprecates the capability (its lines are removed), formulation removes its scenarios, and slicing cuts a removal slice whose check is that no step definition or code serves only the removed scenarios and the suite is green; retiring it is the last step. Promoted when shopsystem-bdd releases that lifecycle.
- **A lifecycle for decisions beyond `supersedes`.** Promoted when a decision needs a state `supersedes` cannot express.
