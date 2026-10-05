---
id: capability/use-the-shops-types
title: Use the shop's types
narrator: the user, working with the shop's kinds of thing
rests_on:
  - decision/types-are-readable
  - decision/types-have-a-command-of-their-own
  - decision/seven-types-on-a-shop-artifact-base
  - decision/role-splits-harness-from-identity
  - decision/a-tag-is-an-artifact
  - decision/seven-types-close-the-loop
formulated_as: features/use-the-shops-types.feature
---

# Use the shop's types

## Purpose

This capability covers what the user can do with the shop's seven types:
- see which types the shop holds, through a command for the shop's types that is separate from the commands for artifacts;
- read one of them, through the same command;
- record things whose shape the types give, such as a role's two groups of fields, a tag held once and named elsewhere, and a process's steps.

The types arrive when a knowledge base is set up (start-a-knowledge-base). Defining or changing a type is not offered. How a type is enforced is kb's job, and it surfaces as a refusal of a change (record-an-artifact).

## Behaviour

- When the user asks which types the shop holds, the user is shown each of the shop's types.
- When the user reads one of the shop's types by its name, the user is shown that type as the shop holds it.
- Every artifact of the shop's seven types can carry an owner, a status and tags, among the fields every shop artifact carries.
- When the user records a role, the fields the harness needs are kept as one named group, and the fields that say who the role is in the shop are kept as another.
- When the user tags a decision with a tag the shop holds, the decision names that tag, and the tag's description is held once, on the tag itself.
- A process's steps each either define a step in place, or use a shared step with settings of their own.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol types` | lists the shop's types |
| `shop-knol types <name>` | reads one of the shop's types |

- The command's name may change. `create`, `write`, `list` and `read` are not the way to the types.
- The types are schema artifacts in kb's schema language: `decision`, `feature`, `work-item`, `role`, `process`, `step` and `tag`.
- All seven build on a `shop-artifact` base schema through kb's composition mechanism, so the common fields are declared once.
- The shop's schemas are the seven types and the `shop-artifact` base, eight in all.
- `role` has two named field groups: `harness` (the harness contract fields) and the corpus identity fields.
- `tag` is a title and a description. Other types target it through a `tags` reference field.
- `process` declares a `steps` part collection. Each item either defines a step inline, or carries `uses: <ref to step>` and `with: <bindings>`.
- kb v0.5.0 refuses a type that puts kb's keywords where kb does not read them, or a `ref` that does not state its whole shape. Each of the shop's eight schemas was created in a fresh v0.5.0 store and accepted as it is; nothing changes in them.

## Not yet

- **Defining or changing a type.** This would be product-local or user-local extensions: additional schema and renderer sets that shop-knowledge loads, which kb never learns of. When it comes, it belongs to the shop's types command, not to `create` or `write`. Promoted when a product or a user wants types or renderers of its own.
- **Validation that kb's schema language cannot express.** If needed, it would run client-side before the call and would not be binding. Promoted when such a validation is needed.
- **Scenario status over time.** It will be a ledger, modelled later; it will not be a field on the scenario or on a work item. Promoted when assignment cannot be tracked without one, or at the crossover.
