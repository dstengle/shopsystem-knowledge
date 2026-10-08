---
id: capability/see-what-is-formulated
title: See what is formulated
narrator: the user, checking which of a shop's Behaviour lines its scenarios formulate
rests_on:
  - decision/the-shops-types-model-the-bdd-spec
  - decision/a-capability-carries-its-reading-order
  - decision/capabilities-are-deprecated-then-retired
  - capability/use-the-shops-types
  - capability/find-the-knowledge-base
formulated_as: features/see-what-is-formulated.feature
---

# See what is formulated

## Purpose

This capability covers seeing, for one shop's capabilities, which Behaviour lines no scenario formulates and which more than one scenario formulates. It reports; it is not a check, and a line with no scenario is never a refusal. Publishing the shop's feature files is publish-a-shops-spec.

## Behaviour

- When the user asks what is formulated in a shop, the user is shown each of the shop's Behaviour lines that no scenario formulates, as the link to the line with its capability's title and the line's title.
- When the user asks what is formulated in a shop, the user is shown each of the shop's Behaviour lines that more than one scenario formulates, as the link to the line with its capability's title and the line's title.
- Where some of the shop's Behaviour lines have no scenario formulating them, when the user asks what is formulated in the shop, the user is answered, and the command is not refused.
- When every one of the shop's Behaviour lines is formulated by exactly one scenario, the user is shown that none is unformulated and none is formulated twice.
- If the user asks what is formulated in a shop the knowledge base does not hold, the answer is refused because that shop is not there, naming it.
- Where a capability linking to the shop is retired, when the user asks what is formulated in the shop, none of that capability's Behaviour lines is shown.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol coverage <shop>` | Read, List and Follow, over the shop's capabilities and the scenarios formulating their lines |

- The shop's capabilities are found as publishing finds them: linking to the shop, active or deprecated, in `order`. Lines are listed in that order.
- A line is shown as its link, `capability/<name>#behaviour/<line>`.
- Where none is unformulated and none is formulated twice, the answer is two empty lists.

## Not yet

Nothing deferred.
