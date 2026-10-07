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

## Satisfied by existing behaviour

- none

## Backlog

- 2026-09-28 `read <id> --section ""` answers the summary and `journal --artifact ""` the whole history, where "a name given empty names no place" would refuse them; these arguments default to `""`, so telling "given empty" apart needs another default. No capability line names them yet (from batch 13's review, routed to formulation).
- 2026-09-28 A relative `--from` or `--to` named from a removed working directory is refused in the operating system's words (`d.yaml: No such file or directory`), where the directory being gone is the cause. No line names it (from batch 13's review).
- 2026-10-05 A knowledge base whose furnishing stopped at a refused Create cannot be finished by `init`: it keeps the shop's types created before the refusal, and a second `init` refuses it as not empty, naming them. Reproduction: an operator-started store named by KB_ROOT, `init` run with the stand-in (`driver.answering`) answering the Create titled `Decision` with a refusal, then `init` again without it: exit 1, `<KB_ROOT>: it is not empty: it holds the types decision, shop-artifact, tag` (decision is there because the stand-in asks the real kb first). No capability line says what a half-furnished knowledge base is (slice 55's Review Focus 2 probe, routed to formulation).
- 2026-10-05 A create in a batch given `key: ""` lands as a create carrying no key: the batch shape takes it as a string and contract v1's `CreateItem.key` cannot tell empty from absent, so kb is never asked. Reproduction: `shop-knol apply` of a batch holding one decision create with `key: ""`: exit 0, the decision created. A link written `@` alone is refused in kb's words (`work-item/start-weekly-price-reviews at decisions/0: a link must land on a node of a kind the type allows; '@' does not`, exit 1). No line says whether an empty key is a key (slice 56's Review Focus 4 probe, routed to formulation).
- 2026-10-05 `types shop-artifact` and `types schema` are shown whole, as kb holds them, exit 0: the command passes kb's read through and names no one of the seven as the only ones readable. Review Focus 5 asked for one line; only `nonesuch` (and a path such as `a/b`) is refused in one line, in kb's words. Reproduction: `shop-knol types schema` in a started knowledge base.
- 2026-10-06 init over a store kb cannot read hides the damage behind kb.init's reason: garbage in the store's database, then `shop-knol init` from a directory below it prints "stores do not nest" where `list` prints that the database cannot be read (start's finding does not tell a damaged store from a found one). From batch 14's branch review.
- 2026-10-06 A removed working directory with KB_ROOT naming an empty store: `shop-knol init` says the directory is gone, where find-the-knowledge-base answers from KB_ROOT. Also a question for the spec (from batch 14's branch review).
- 2026-10-06 A store found upward that holds other types is refused "it is not empty: …" with nothing naming the knowledge base: how init names one found upward is for formulation (from batch 14's branch review).
- 2026-10-06 The stand-in's `from_kb` would turn a refusal answer into a result (`tests/stand_in/sitecustomize.py`); no step writes that combination (from Task 2's review).
- 2026-10-06 KB_ROOT naming the knowledge base the user works inside is refused "it already holds the shop's knowledge" (a ruling under the person's delegation), where the "inside" line could also apply: for the person to confirm, with an Examples row (from Task 5.1's review).
- 2026-10-07 init with nothing named, where kb finds a connection to a server hosting a store holding types other than the shop's, is refused as not empty but names no knowledge base: stderr is 'it is not empty: it holds the types recipe, supplier' (the Fault's artifact empty), while the already-holds refusal of a served store names its address. Reproduction: .superpowers/batch15/probe55-1/scripts/probe.py <empty scratch dir> (kb.init a store, the operator creates schema Recipe and Supplier, kb.testing.served(store, office), shop-knol init from office with KB_ROOT unset). Whether it should name the address as already-holds does is for the person; the not-empty outline has no server row.
- 2026-10-07 init over a damaged connection to a server hides the damage behind kb.init's reason: a garbage kb/server.yaml in the working directory, then `shop-knol init` prints 'a store goes in a place of its own, and <dir> already holds something in that place' where `list --type schema --ids` prints that the connection cannot be read or names no address. Same class as the damaged-store entry. (slice 55.2's Review Focus 4 probe)
- 2026-10-07 If the session guard refuses in the xdist workers only, each worker shows a "node down" traceback and the run exits 5 instead of one line and exit 4 (session_guard.py pytest_sessionstart). Reproduction: a scratch plugin pointing only the workers' guard at a store, then `make test` (slice 52.1's log). From batch 15's review.
- 2026-10-07 The served-store fixture's serve() does not forward kb.testing.served's clock, so a scenario that sets the day (driver.at) and writes through a server would be stamped with the machine's day. No scenario does today. From batch 15's review.
- 2026-10-07 tests/start_not_empty.py's _noted does not check the exit code of the journal read it records, so a failed before-read makes "nothing changes" compare empty with empty for the KB_ROOT and named-directory rows. From batch 15's review.
- 2026-10-07 init._reached_at compares where().root with the named root even when where() found nothing (root "" resolves to the process's working directory); harmless today since the List is refused and kb.init's refusal re-raised, but the intent is obscure: return False when where() carries faults. Reproduction: `shop-knol init <dir>` with a garbage connection in <dir>, naming `.` versus another path. From batch 15's fix-wave re-review.
- 2026-10-07 Probe stores from earlier batches sit inside the checkout under .superpowers/ (batch4 to batch14, r5): a shop-knol run started inside one finds it, and the suite's guard looks upward only. Clean them up, or keep probes in the test temp dir. From batch 15's fix-wave re-review.

## Log
- 2026-10-07 Batch batch15 archived to archive/2026-09-23-shop-knowledge-slices-batch15.md; last 2026-10-07 Suite: 134 passed, 0 failed at 09bc387 in 10.7 s
- 2026-10-07 Suite: 134 passed, 0 failed at 09bc387 in 10.7 s
