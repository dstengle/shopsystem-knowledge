# shop-knowledge on kb v0.5.0

Proposal, integrated into spec/ on 2026-10-05.

Date: 2026-10-05. Decided by the person in this session. Rests on kb's contract v1 note
(shopsystem-kb, docs/superpowers/specs/2026-10-01-kb-contract-v1-design.md) and kb's spec at v0.5.0.

## What changes

shop-knowledge pins kb v0.5.0, which publishes contract v1 as one breaking release. Every rpc is renamed or
reshaped, and one thing a client could do is gone: a set that mixes kinds of change.

### A batch holds one kind of change

kb lands a set of one kind of change only, so `shop-knol apply` takes a batch of one kind:

- A batch whose changes are all creates lands as one set of creates; a batch whose changes are all writes lands as
  one set of replacements. Either lands whole or not at all, and the history shows it as one change.
- A create in a batch may carry a key of the user's choosing, unique in the batch. A link written `@` and that key,
  anywhere in the batch, names the artifact that create makes, so new artifacts in one batch can point at each
  other. A key no create in the batch carries is refused as a link landing on nothing, naming the key.
- A batch that mixes creates and writes is refused because a batch holds one kind of change, naming the batch, and
  none of its changes are in the shop.

The approved scenario "The user makes several changes at once" records a decision and points an existing work item
at it: a create and a write. Its meaning changes: the batch records a decision and a work item pointing at it, two
creates linked by a key. Its Thens stand (both are in the shop; the history shows one change). The batch whose prose
the shop cannot keep is the same batch, and changes the same way.

### Starting a store leaves the wire

kb has no Init rpc. A client starts a store in its own process with `kb.init(root, role)`, which raises
`kb.NotStarted` with the faults when it refuses. `shop-knol init` starts a store this way where it starts one, and
loads the shop's types through Create as before. This makes buildable what start-a-knowledge-base already says:
where kb finds an empty knowledge base that kb's operator started, in place or through a server, init loads the
shop's types into it without starting anything.

### Nothing else the user sees changes

The commands, their flags and their answers stay as they are: `write`, `append`, `delete`, `refs`, `journal` and
`validate` keep their names and their answers keep their keys (an answer still says `type`, not kb's `kind`). Under
them, each command maps to v1's call: Create, Replace, Add, Remove, BatchCreate, BatchReplace, Read (a level asked
as one of summary, whole with a depth, or section), List, Follow, Search, History, Snapshot and Check. Every
response is a result or a refusal, never both; a change carries one signature (role, piece of work, message); a
place inside an artifact is kb's `place`.

### The shop's types

kb v0.5.0 refuses a type that puts kb's keywords where kb does not read them, or a `ref` that does not state its
whole shape. The shop's eight schemas were each created in a fresh v0.5.0 store and accepted as they are; nothing
changes in them.

### What kb publishes, for shop-knowledge's own rule

The published surface shop-knowledge may use gains `kb.init` and `kb.NotStarted` (kb's index, Constraints carried).
shop-knowledge's rule that it knows kb only through what kb publishes names them.

## Not taken up

- An expected revision on a replacement, an addition or a removal (kb's rule `revision`). Promoted when two users
  revising one artifact lose a change.
- Batches of additions or of removals. Promoted when a user needs several steps added, or several artifacts retired,
  as one change.
- Moving a knowledge base made by an earlier kb into a v0.5.0 store is the operator's `kb import`, not a shop-knol
  command.
