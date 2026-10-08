# Shop links held once, capability dependencies, and a capability lifecycle

Date: 2026-10-08. Status: approved in conversation. Decisions: adrs/0058 to 0062.

A proposal against `spec/`, following batch 16's review with the person. It corrects three choices batch 16
made under delegation and adds a lifecycle for capabilities.

## Links are held once

kb answers a link from either end, so each fact is stored in one direction only.

- **A decision links to its shop.** `decision.shop` → shop, one, required, and shown at a glance. `shop.decisions`
  goes. A shop's decisions are the decisions linking to it. A decision can no longer belong to two shops or to
  none.
- **A capability carries its place in the reading order.** `capability.order` is a dotted number (`3`, `3.1`,
  `3.1.2`), required, sorted numerically part by part, so a capability can be inserted without renumbering.
  `shop.reading_order` goes. A shop's capabilities are the capabilities linking to it, in `order`.

What approved scenarios observe changes where a decision now points at its shop:

- follow-the-links: following the links out of a decision shows the older decision **and its shop**. Two steps out
  shows the older decision, the tag "pricing", the shop and the shop's product.
- read-an-artifact: a decision's glance has a stub of its shop beside the older decision and the tag.

## A capability declares what it depends on

- `capability.depends_on` → capability, many, optional: the capabilities it builds on, in its own shop or any
  other. It is kept apart from `rests_on`, which holds decisions only.
- A scenario is part of its capability. Its `uses` names the dependencies that scenario exercises. Each must be
  among its capability's `depends_on`. `uses` may now point into the scenario's own shop.
- Who depends on a capability, in any shop, is a query: the capabilities whose `depends_on` links to it, and the
  scenarios whose `uses` does.
- A capability's page shows `depends_on` in its frontmatter, as capability names, after `rests_on`.

## A capability's lifecycle

A capability's `status` is one of `active`, `deprecated` or `retired`, and is required. The other types keep
`status` as free text.

- `active`: part of the shop's contract.
- `deprecated`: its removal from spec and code is under way in its own shop. Still published: its page's
  frontmatter carries `status: deprecated`, and its line in the index's Composition ends `(deprecated)`.
- `retired`: gone from spec and code, and kept in the knowledge base as the record. Not published: no page, no
  feature file, no line in the index.
- Retiring is the shop's own act on its public contract. kb accepts it whatever depends on the capability
  elsewhere. Other shops find out when they publish or ask, and act on their own schedule.
- Removing a capability is three short steps, each checked: deprecate it, remove its spec and code through the
  shop's normal work, retire it. Making the code-removal step part of the workflow is a request to shopsystem-bdd
  (below).

## Publishing a shop's spec, changed

- The shop's capabilities are those linking to it whose status is `active` or `deprecated`, in `order`.
- The ledger lists only the shop's own decisions (those linking to it), in number order. The line about another
  shop's decisions, and the `<shop name>:` form of `source:`, go.
- Publishing deletes the files it published earlier that no published artifact now stands behind. Under
  `spec/capabilities/`, `features/` and `adrs/` in the directory, it deletes exactly the files whose
  published-from line names an artifact not published this time. A file without a published-from line is never
  touched.
- Refused, naming what is at fault, with nothing written or deleted:
  - two of the shop's capabilities with the same `order`;
  - a capability of the shop resting on a decision of another shop;
  - a scenario whose `uses` names a capability not among its capability's `depends_on`;
  - a published capability (active or deprecated) depending on a retired capability, in any shop.
- These refusals go: a capability not in the reading order; a capability in the reading order naming another
  shop; a decision of another shop's ordering in the ledger; a decision no shop names (it no longer fits its
  type); a scenario's `uses` pointing into its own shop.

## Seeing what a shop depends on

`shop-knol dependencies <shop>` answers the shop's published capabilities that depend on a deprecated or retired
capability, in any shop. Each comes with the capability it depends on, that capability's shop and its status, and
the scenarios whose `uses` name it. It answers, and never refuses, for what it finds. A shop the knowledge base
does not hold is refused as `coverage` refuses it.

## Seeing what is formulated, changed

`coverage` counts the Behaviour lines of the shop's capabilities as publishing finds them: linking to the shop,
active or deprecated, in `order`.

## Requests (outside this repository)

- **shopsystem-bdd:** removing a capability is a lifecycle in the workflow. Integration deprecates it (its lines are
  removed), formulation removes its scenarios, and slicing cuts a removal slice whose check is that no step
  definition or code serves only the removed scenarios and the suite is green. Retiring it is the last step.

## Not in this proposal

- Product-level decisions (the lead shop's) in a shop's ledger. Promoted when a shop needs one in practice.
- A lifecycle for decisions beyond `supersedes`.
