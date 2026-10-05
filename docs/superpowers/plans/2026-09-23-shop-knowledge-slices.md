# shop-knowledge slices

shop-knowledge's living plan. Until kb 0.1 it was the one plan for both
this repository and kb, as both specs' "Order of building" say; on
2026-09-24, with kb tagged `v0.1.0` and pinned here, every slice made only
of kb scenarios moved to kb's own plan,
`shopsystem-kb/docs/superpowers/plans/2026-09-24-kb-slices.md`, with its
number, tags, status, and log entries. The numbers here skip those that
moved; a number is never reused across the two plans, and a slice in the
other plan is named with its repository, as in "kb slice 21". Slices 0 and
1 check or run scenarios in both repositories and stay here; their
Scenarios lines still say which repository each scenario runs in.

From here each repository plans alone. A kb change this repository needs
is a request to bump the pin: the shop-knowledge slice that needs it waits
until kb has released it under a new tag and this repository pins that
tag.

Slice 0 is the enabling slice the skeleton stands on: both checkouts run
their feature suites and this repository imports kb from the checkout
beside it. Slice 1 is the walking skeleton the specs define. Slices 1.1 to
1.28 were the three cuts kb 0.1 waited on, most of them now in kb's plan, each ordered the same way: the
slices that settle one unknown by the size of it, then those with none.
Then the tag. Then slices 2 to 20, which each settle one
unknown, ordered by the size of it. Then the slices with no unknown:
scenarios that share a feature and step definitions bundle into one slice,
and the slices are ordered by value, kb's slice ahead of the shop-knowledge
slice that needs it. An architecture review is an enabling slice cut after
every six implemented slices, counting enabling slices and the refactors a
review cuts. The first review's refactors were placed as dotted slices right
after it; from the second on, each refactor a review calls for is placed by
its risk among the slices not yet begun, like any finding, and precedes a
slice only if that slice needs it.

The order of the sections in this file is the order of the work, and the
numbers read in that order. A slice placed after the plan was cut takes
its place by its unknown among the slices not yet begun, and those slices
are renumbered and their tags rewritten to match, within this repository
only.

## Slice 51: The steps' oracles of kb's answers sit in a module of their own
- Kind: enabling
- Check: `wc -l tests/*.py` -> no module over 250 lines, and the module that launches shop-knol holds none of the helpers that ask kb for its own answer or build the lines shop-knol is expected to print; `make test` -> the same 94 passed and the same 37 failed as before the slice
- Observable: a step that needs kb's own answer to compare with takes it from one module whose only concern that is, so the driver can grow for a server without crossing the size limit
- Unknown: none
- Needs: none
- Status: planned

## Slice 52: shop-knol reaches kb v0.5.0 through contract v1, every answer unchanged
- Kind: enabling
- Check: `.venv/bin/pip show shopsystem-kb` -> Version 0.5.0; `grep -rn "kb_pb2\.\(Apply\|Init\|Journal\|Validate\|Refs\|Write\|Append\|Delete\)" src tests` -> nothing; `make test` -> every scenario that passed before the slice passes, except "One bad change in a batch leaves the shop untouched" (its step builds a batch that mixes kinds, which v1 cannot land; slice 56 takes it)
- Observable: everything a user could do on kb v0.3.0 they can do on v0.5.0, the same commands giving the same answers and refusals
- Unknown: whether every command maps onto its v1 call with its answer and its refusals unchanged
- Needs: the pin in pyproject.toml; the stand-in and the steps' oracles speak v1's messages (needed by every scenario that compares with kb's answer)
- Status: planned

## Slice 53: shop-knol answers through a kb server exactly as through the store
- Kind: capability
- Scenarios: find-the-knowledge-base / Reading where the knowledge base found is a connection to a server hosting the store
- Observable: a user whose directory holds only the connection to a kb server reads the shop's knowledge as if the store were beside them
- Unknown: whether a kb server started by the test, inside its own temporary directory on a port of its own, serves shop-knol unchanged
- Needs: starting and stopping a real kb server from a step, within the suite's isolation rules (needed by this scenario and by slice 55's server rows)
- Status: planned

## Slice 54: init furnishes an empty knowledge base it finds, and starts one only where none is found
- Kind: capability
- Scenarios: start-a-knowledge-base / With no directory named, an empty knowledge base kb finds from the working directory is furnished with the shop's types (both rows); start-a-knowledge-base / Naming a directory that holds an empty knowledge base furnishes it with the shop's types; start-a-knowledge-base / Where no knowledge base is found, the shop's knowledge sits in a place of its own inside the working directory; start-a-knowledge-base / Starting a knowledge base where the directory already holds one is refused; start-a-knowledge-base / With nothing naming another knowledge base, starting from inside one the shop already has is refused; start-a-knowledge-base / Starting a knowledge base from a removed directory, with nothing naming a knowledge base, ends in a plain refusal
- Observable: a user who works where kb's operator started an empty knowledge base runs `shop-knol init` and gets the shop's types in it, while a user with nothing found still gets a new one beside their work
- Unknown: how init tells whether kb finds a knowledge base from where it is, and loads the types into it instead of starting one
- Needs: none
- Status: planned

## Slice 55: init refuses a knowledge base it cannot furnish, and furnishes one through a server
- Kind: capability
- Scenarios: start-a-knowledge-base / With no directory named, starting where finding the knowledge base is refused is refused for finding's reason (both rows); start-a-knowledge-base / Starting where the knowledge base to furnish already holds the shop's types is refused (all three rows); start-a-knowledge-base / Starting where the knowledge base to furnish holds something other than the shop's types is refused (both rows); start-a-knowledge-base / With no directory named, an empty store kb reaches through a server is furnished with the shop's types
- Observable: init never furnishes twice, never furnishes a knowledge base already holding something else (saying what it holds), stops for the reason finding gives, and furnishes a served empty store as one in place
- Unknown: how init tells, through the contract alone, an empty knowledge base from one holding the shop's types or something else
- Needs: slice 53's server (for the server rows)
- Status: planned

## Slice 56: A batch of creates lands as one, its new artifacts linked by keys
- Kind: capability
- Scenarios: make-several-changes-at-once / The user makes several changes at once; make-several-changes-at-once / A link written with a key a create in the batch carries names that create's artifact (both rows); make-several-changes-at-once / A link written with a key no create in the batch carries leaves the shop untouched; make-several-changes-at-once / Two creates carrying the same key leave the shop untouched; make-several-changes-at-once / One bad change in a batch leaves the shop untouched; make-several-changes-at-once / A batch whose prose the shop cannot keep leaves the shop untouched
- Observable: a user records a decision and a work item pointing at it in one batch, the history showing one change, and a bad key or a bad change refuses the whole batch
- Unknown: how a key a create carries, and a link written with it, reach kb
- Needs: none
- Status: planned

## Slice 57: A batch of writes lands as one; a batch of mixed kinds, or a write carrying a key, is refused
- Kind: capability
- Scenarios: make-several-changes-at-once / The user applies a batch whose changes are all writes; make-several-changes-at-once / A write carrying a key leaves the shop untouched; make-several-changes-at-once / A batch mixing creates and writes leaves the shop untouched
- Observable: a user rewrites several artifacts as one change, and a batch kb could not land as one set is refused in plain words before anything lands
- Unknown: whether shop-knol's own refusal of a batch's kinds and keys reads as one refusal naming the batch and the key
- Needs: none
- Status: planned

## Slice 58: The user sees and reads the shop's types through a command of their own
- Kind: capability
- Scenarios: use-the-shops-types / The user asks which types the shop holds; use-the-shops-types / The user reads one of the shop's types by its name; use-the-shops-types / Every artifact of the shop's seven types can carry an owner, a status and tags (all seven rows); use-the-shops-types / A process's step either defines a step in place or uses a shared step with settings of its own (both rows)
- Observable: a user runs `shop-knol types` to see the shop's seven types and `shop-knol types <name>` to read one, and every kind of thing carries an owner, a status and tags
- Unknown: what the types command shows of each type, and of one type, as the shop holds it
- Needs: none
- Status: planned

## Slice 59: Markdown shows a field holding a mapping as a nested list
- Kind: capability
- Scenarios: publish-an-artifact / Markdown shows a field holding a mapping as a list nested under the field
- Observable: a role's field holding a mapping reads on its page as a list under the field
- Unknown: none
- Needs: none
- Status: planned

## Satisfied by existing behaviour

- none

## Backlog

- 2026-09-28 `read <id> --section ""` answers the summary and `journal --artifact ""` the whole history, where "a name given empty names no place" would refuse them; these arguments default to `""`, so telling "given empty" apart needs another default. No capability line names them yet (from batch 13's review, routed to formulation).
- 2026-09-28 A relative `--from` or `--to` named from a removed working directory is refused in the operating system's words (`d.yaml: No such file or directory`), where the directory being gone is the cause. No line names it (from batch 13's review).

## Log

- 2026-10-05 Batches 1 to 13 archived in `docs/superpowers/plans/archive/2026-09-23-shop-knowledge-slices-batches-1-13.md`; batch 13's last line: Suite `100 passed`.
- 2026-10-05 MIGRATED to capabilities (spec/ committed in 070886f, lines approved 2026-10-05). The 14 feature files became 16, one per capability under spec/capabilities/, each scenario moved verbatim with its tags, in its capability's line order: start-a-shop-knowledge-base split into start-a-knowledge-base and use-the-shops-types; read-back-what-the-shop-knows into find-the-knowledge-base and read-an-artifact; record-a-decision, revise-what-the-shop-knows, retire-what-the-shop-no-longer-uses, list-what-the-shop-has-recorded, follow-the-links-between-what-the-shop-knows, check-the-shops-knowledge-is-sound and publish-what-the-shop-knows renamed to record-an-artifact, revise-an-artifact, retire-an-artifact, list-what-the-shop-holds, follow-the-links, check-the-knowledge-base and publish-an-artifact. Test modules renamed with their features; no step definition changed; test_read_an_artifact.py binds both halves of read-back, whose finding scenarios share its Background steps; test_use_the_shops_types.py star-imports start_roles_and_tags. The feature half of every Scenarios line above is rewritten to the new names; batch plans are history and keep the old ones. Verified against the baseline: 100 passed, the same passing scenarios by title, the same count for each of the 40 slice tags. Unbacked lines approved at the gate go to formulating-features: init furnishing an empty knowledge base kb finds (and its refusals), `shop-knol types`, a server connection behaving as the store, the fields every shop artifact carries, a process's steps in place or shared, a mapping on a markdown page as a nested list.
- 2026-10-05 Suite: 37 failed, 94 passed (after the kb v0.5.0 spec and its formulation, e05a55b; on kb v0.3.0). Red: exactly the 37 new or changed scenarios of this batch (Examples rows counted), each on a step not yet defined.
- 2026-10-05 Batch 14 cut (slices 51 to 59) under the person's delegation (2026-10-05: "use your recommendations for any questions"). The ninth architecture review the batch 13 log named is not cut: under shopsystem-bdd 0.9.0 the batch's branch review checks shape and coupling, and the separate review runs only when the person asks. The parked driver split is slice 51, before the server work that grows the driver. Order: the split, then the pin the rest stands on, then by risk: the server harness, furnishing, telling what a found knowledge base holds, keys in a batch, a batch's kinds refused, the types command, a markdown case with no unknown.
