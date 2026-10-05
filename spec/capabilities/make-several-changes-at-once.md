---
id: capability/make-several-changes-at-once
title: Make several changes at once
narrator: the user, landing changes that only make sense together
rests_on:
  - decision/user-files-checked-against-shapes
  - decision/actor-and-message-asked-once
formulated_as: features/make-several-changes-at-once.feature
---

# Make several changes at once

## Purpose

Applying a batch of changes that land together as one change in the history, or not at all. When any change in the batch is refused, every fault is reported at once.

## Behaviour

- When the user applies a batch, saying which role they are and why, every change in it is in the shop, and the history shows them as one change.
- If a change in a batch does not fit its type, the batch is refused because a change in it does not fit its type, none of its changes are in the shop, and the user is shown every fault in the batch.
- If a batch holds prose in which a line before the last ends in a space, the batch is refused because the shop cannot keep that prose as written, naming the place in the batch, and none of its changes are in the shop.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol apply --from <batch> -m <why>` | Apply |

- A batch is read into the operations of one Apply, in the order written.
- The `batch` shape leaves additional properties open. It checks `create` and `write` as strings, and `content` as an object, under a `oneOf` of two required-lists.
- The actor and message are asked for as in record-an-artifact.

## Not yet

Nothing deferred.
