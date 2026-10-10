---
id: capability/make-several-changes-at-once
title: Make several changes at once
narrator: the user, landing changes that only make sense together
rests_on:
  - decision/a-batch-holds-one-kind-of-change
  - decision/only-a-create-carries-a-key
  - decision/the-batch-scenarios-record-two-linked-creates
  - decision/user-files-checked-against-shapes
  - decision/actor-and-message-asked-once
  - decision/the-user-names-what-they-create
depends_on:
  - capability/name-an-artifact
formulated_as: features/make-several-changes-at-once.feature
---

# Make several changes at once

## Purpose

This capability covers applying a batch of creates, or a batch of replacements. The batch lands together as one change in the history, or not at all. Each create carries the name of the artifact it makes, and may name its parts. New artifacts in a batch of creates can point at each other by the IRIs their creates carry, or through a key one of them carries. When any change in the batch is refused, every fault is reported at once. A batch never mixes creates with writes, and batches of additions or removals are not part of this capability.

## Behaviour

- When the user applies a batch whose changes are all creates, saying which role they are and why, every artifact it creates is in the shop, and the history shows them as one change.
- When the user applies a batch of creates, saying which role they are and why, each artifact it creates is held under the name its create carries.
- When the user applies a batch of creates naming some of their parts, each part named is known by the name the user gave it.
- When the user applies a batch of creates in which a link names the IRI that one of its creates carries, that link names the artifact that create makes.
- When the user applies a batch whose changes are all writes, saying which role they are and why, the shop holds the new wording of every artifact the batch replaces, and the history shows them as one change.
- When the user applies a batch of creates in which a link, anywhere in the batch, is written with a key of the user's choosing that one of its creates carries, that link names the artifact that create makes.
- If a create in a batch carries no name, the batch is refused because every artifact is named by the user, and none of its changes are in the shop.
- If a create in a batch carries a name the shop already holds, the batch is refused because that name is taken, naming it, and none of its changes are in the shop.
- If two creates in a batch carry one name, the batch is refused because that name is taken, naming it, and none of its changes are in the shop.
- If a link in a batch is written with a key that no create in the batch carries, the batch is refused because the link lands on nothing, naming the key, and none of its changes are in the shop.
- If two creates in a batch carry the same key, the batch is refused because a key names one create in the batch, naming the key, and none of its changes are in the shop.
- If a write in a batch carries a key, the batch is refused because only a create carries a key, naming the key, and none of its changes are in the shop.
- If a batch mixes creates and writes, the batch is refused because a batch holds one kind of change, naming the batch, and none of its changes are in the shop.
- If a change in a batch does not fit its type, the batch is refused because a change in it does not fit its type, none of its changes are in the shop, and the user is shown every fault in the batch.
- If a batch holds prose in which a line before the last ends in a space, the batch is refused because the shop cannot keep that prose as written, naming the place in the batch, and none of its changes are in the shop.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol apply --from <batch> -m <why>`, every change a create | BatchCreate |
| `shop-knol apply --from <batch> -m <why>`, every change a write | BatchReplace |

- A batch is read into the changes of one BatchCreate or one BatchReplace, in the order written.
- A create carries its artifact's name, taken as any name is (name-an-artifact); a link in a batch names an IRI, short or full.
- A link to a create's key is written `@` followed by the key.
- The `batch` shape checks `create` and `write` as strings, and `content` as an object, under a `oneOf` of two required-lists. It allows `key` only beside `create`. Apart from that, it leaves additional properties open.
- kb's refusal of two creates carrying one key is passed through in kb's words.
- The actor and message are asked for as in record-an-artifact.

## Not yet

- **Batches of additions or of removals.** Promoted when a user needs several steps added, or several artifacts retired, as one change.
- **Checking a batch without landing it.** A validate-only mode on the batch calls, so a batch is checked and nothing lands. A write that links to an artifact the same round creates can only be checked once the creates have landed. It is a request to kb. Promoted when kb publishes a validate-only mode on its batch calls and the pin is bumped to it.
- **Batches without keys.** `@key` goes from a batch, links in a batch naming IRIs alone. Promoted when kb drops `@key` from its sets and the pin is bumped to it.
