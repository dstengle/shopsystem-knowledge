---
id: capability/follow-the-links
title: Follow the links
narrator: the user, seeing how the shop's knowledge hangs together
rests_on:
  - decision/follow-and-search
  - decision/capabilities-depend-on-capabilities
depends_on:
  - capability/find-the-knowledge-base
formulated_as: features/follow-the-links.feature
---

# Follow the links

## Purpose

Seeing what an artifact points at and what points at it. The answer can be narrowed by link and by type, and can reach further than one step, showing the route to each thing reached. Filling links in while reading one artifact is not part of this capability (read-an-artifact).

## Behaviour

- When the user follows the links out of an artifact, the user is shown what it points at.
- When the user follows the links into an artifact, the user is shown what points at it.
- When the user follows the links into an artifact, only through one link and only from one type, the user is shown only what points at it through that link from that type.
- When the user follows the links out of an artifact two steps, the user is shown everything reached within two steps, and the route taken to each.
- When the user follows the links into a capability, the user is shown each capability that depends on it and each feature whose scenarios' `uses` name it, in any shop.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol refs <locator> --inbound\|--outbound [--via <field>] [--type <type>] [--depth <n>]` | Follow |

- One of the two directions is required. With no `--depth`, one step is followed.
- The answer is a sequence, nearest first as kb gives it, with no wrapper key. Each entry has the reached artifact's `id`, `type` and `title`; `via` (the link of the last step); its stub's fields; and `route`, the steps taken, each as `field` and `id`.

## Not yet

Nothing deferred.
