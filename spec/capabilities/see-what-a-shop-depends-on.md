---
id: capability/see-what-a-shop-depends-on
title: See what a shop depends on
narrator: the user, checking whether a shop's capabilities lean on capabilities being removed
rests_on:
  - decision/capabilities-depend-on-capabilities
  - decision/capabilities-are-deprecated-then-retired
  - capability/use-the-shops-types
  - capability/find-the-knowledge-base
formulated_as: features/see-what-a-shop-depends-on.feature
---

# See what a shop depends on

## Purpose

This capability covers seeing which of a shop's published capabilities depend on a capability that is deprecated or retired, in any shop, and which of their scenarios use it. It reports; it never refuses for what it finds. Refusing to publish a capability that depends on a retired one is publish-a-shops-spec, and following every link into a capability is follow-the-links.

## Behaviour

- When the user asks what a shop depends on, the user is shown each of the shop's active or deprecated capabilities that depends on a deprecated or retired capability, in any shop, with the capability it depends on, that capability's shop and its status, and the scenarios of the depending capability whose `uses` name it.
- Where some of the shop's capabilities depend on a retired capability, when the user asks what the shop depends on, the user is answered, and the command is not refused.
- When none of the shop's published capabilities depends on a deprecated or retired capability, the user is shown none.
- If the user asks what a shop depends on and the knowledge base does not hold that shop, the answer is refused because that shop is not there, naming it.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol dependencies <shop>` | Read, List and Follow, over the shop's capabilities, the capabilities they depend on, and the scenarios using those |

- The shop's published capabilities are found as publishing finds them: linking to the shop, active or deprecated, in `order`.
- The scenarios shown are those of the features formulating the depending capability.
- Where none is found, the answer is an empty list.
- A shop the knowledge base does not hold is refused as `coverage` refuses it.

## Not yet

Nothing deferred.
