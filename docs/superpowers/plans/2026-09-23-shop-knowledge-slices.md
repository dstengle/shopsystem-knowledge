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

## Slice 60: The shop's ten types
- Kind: capability
- Scenarios: start-a-knowledge-base / The user starts a knowledge base and the shop's types are ready; use-the-shops-types / The user asks which types the shop holds; use-the-shops-types / Every artifact of the shop's ten types can carry an owner, a status and tags (all rows)
- Observable: a new knowledge base holds products, shops, capabilities, the reshaped decision and the new feature beside the five kept types, and each of the ten carries an owner, a status and tags
- Unknown: whether the reshaped decision, whose required shop needs a shop and a product, can stand in for every decision today's scenarios record without changing what any of them says
- Needs: every existing scenario that records a decision gives it the reshaped decision's required fields (statement, date, number, shop) as step data only, per integration answer 2; no Given, When or Then changes
- Status: green

## Slice 61: Publish a shop's index
- Kind: capability
- Scenarios: publish-a-shops-spec / The user publishes a shop's spec and the directory holds its index
- Observable: the user publishes a shop into a directory and finds spec/index.md laid out from the shop, its constraints and its reading order, with the knowledge base unchanged
- Unknown: whether a publisher made from a shop can read the shop's other artifacts through the contract and give back files in more than one directory
- Needs: none
- Status: planned

## Slice 62: Short fields and links into Behaviour lines
- Kind: capability
- Scenarios: use-the-shops-types / The user reads a product, a shop, a capability, a decision or a feature at a glance (all rows); The user reads an artifact holding parts at a glance; The user records an artifact holding parts; The user records a gist or a statement longer than 200 characters (all rows); The user records a gist or a statement that holds a line break (all rows); The user records a part whose title is longer than 80 characters; The user records a part whose title holds a line break; The user records a scenario whose uses points at anything but a capability; The user records a feature; The user records a scenario with labels
- Observable: the user records a feature whose scenarios link into a capability's Behaviour lines, sees parts by title at a glance, and is refused a gist, statement or part title that is too long or breaks a line
- Unknown: whether a link into a capability's Behaviour line, given in a file the user records, is kept and shown back through shop-knol as the link it was given
- Needs: none
- Status: planned

## Slice 63: Publish a shop's capabilities
- Kind: capability
- Scenarios: publish-a-shops-spec / The user publishes a shop's spec and the directory holds a file for each capability; The user publishes a shop's spec and a capability's file is named from its title (all rows)
- Observable: the user publishes a shop and finds one file per capability, named from its title, with frontmatter, Purpose, Behaviour, Implementation and Not yet
- Unknown: whether a capability page can keep its frontmatter first and lay out its sections with the layout the markdown and agent publishers share
- Needs: none
- Status: planned

## Slice 64: Publish a shop's decisions
- Kind: capability
- Scenarios: publish-a-shops-spec / The user publishes a shop's spec and the directory holds its ledger; The user publishes a shop's spec and the directory holds a record for each decision; The user publishes a shop's spec and a decision's record is named from its number and title (all rows); The user publishes a shop's spec and every ledger entry is a decision the knowledge base holds; The user publishes a shop's spec whose capabilities rest on a decision of another shop
- Observable: the user publishes a shop and finds its ledger, listing its own decisions and then those of other shops its capabilities rest on, and one numbered record per decision of its own
- Unknown: how a publisher finds the decisions of other shops that a shop's capabilities rest on, and those shops' names, through the contract
- Needs: none
- Status: planned

## Slice 65: Publish a shop's feature files
- Kind: capability
- Scenarios: publish-a-shops-spec / The user publishes a shop's spec and the directory holds a feature file for each formulated capability
- Observable: the user publishes a shop and finds a Gherkin feature file for each formulated capability, its scenarios, labels, steps, tables and examples laid out as the shop writes them
- Unknown: whether a feature's scenarios, as parts holding steps, tables, docstrings and examples, lay out as Gherkin the shop's own feature files would accept as written
- Needs: none
- Status: planned

## Slice 66: See what is formulated
- Kind: capability
- Scenarios: see-what-is-formulated / The user asks what is formulated in a shop, and is shown each line no scenario formulates; The user asks what is formulated in a shop, and is shown each line more than one scenario formulates; Where some of the shop's lines have no scenario, the user asks what is formulated and is answered, not refused; Every one of the shop's lines is formulated by exactly one scenario, and the user is shown none unformulated and none formulated twice; The user asks what is formulated in a shop the knowledge base does not hold
- Observable: the user asks shop-knol coverage for a shop and is shown the Behaviour lines no scenario formulates and those more than one does
- Unknown: how to count the scenarios that formulate each of a shop's Behaviour lines through the contract, given a link into a part counts as a link into its artifact
- Needs: none
- Status: planned

## Slice 67: The published-from line and publishing refusals
- Kind: capability
- Scenarios: publish-a-shops-spec / The user publishes a shop's spec and every file it writes carries the published-from line (all rows); Publishing is refused when a capability names the shop but is not in the shop's reading order; Publishing is refused when a capability in the shop's reading order names another shop; Publishing is refused when two of the shop's capabilities would be published under one file name; Publishing is refused when two of the shop's decisions would be published under one file name; Publishing is refused when two of the shop's decisions carry one number; Publishing is refused when two features formulate one of the shop's capabilities; Publishing is refused when a scenario's uses points at a capability of its own shop
- Observable: every file a publish writes says it was published from the knowledge base and must not be edited, and a shop whose spec would publish inconsistently is refused with nothing written
- Unknown: none
- Needs: none
- Status: planned

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
- 2026-10-07 Suite: 132 passed, 21 failed at f965ec0 in 12.8 s; failing: the new and changed scenarios of use-the-shops-types and start-a-knowledge-base (publish-a-shops-spec and see-what-is-formulated not yet collected)
- 2026-10-07 Probe: kb v0.6.0, a schema with maxLength 200 and pattern ^[^\n]*$ on gist -> a 201-character gist refused (rule maxLength, place gist), a gist holding a line break refused (rule pattern)
- 2026-10-07 Probe: kb v0.6.0, a feature scenario's formulates ref with parts: true -> capability/checkout#behaviour/show-the-price accepted; #behaviour/nope refused (rule ref, place scenarios/0/formulates); a glance at the capability shows the part's title and counts the feature inbound
- 2026-10-07 Probe: kb v0.6.0, Read whole at locator place behaviour/show-the-price -> the whole capability comes back, not the one item (no scenario relies on reading one part)
- 2026-10-07 Probe: kb v0.6.0 BatchCreateRequest and BatchReplaceRequest fields -> items, signature only: no validate-only mode
- 2026-10-07 REQUEST kb: a validate-only mode on BatchCreate and BatchReplace, checking a batch as it would land and landing nothing (adrs/0053; spec/capabilities/make-several-changes-at-once.md Not yet). No slice of batch 16 waits on it.
- 2026-10-07 REQUEST shopsystem-bdd: capability-writer and feature-formulator read kb through a read-only shop-knol allowlist (read, list, refs, search, types) and draft shop-knol apply batch files; integrating-a-proposal's and formulating-features' apply steps validate, gate, apply creates then writes, publish with render spec, and commit; the capability format notes the published-from line (adrs/0052, 0053). Moving a shop's real spec into kb waits on it.
- 2026-10-07 QUESTION FOR THE SPEC: publish-a-shops-spec, a decision named by the decisions of two shops: refused (a decision belongs to one shop, naming both shops, nothing written), or allowed (each shop publishes it as its own, each judging its numbers apart)? No principle decides it; for the person. No slice of batch 16 depends on it.
- 2026-10-07 Slice 67 gains publish-a-shops-spec / Publishing is refused when a capability of the shop rests on a decision no shop names (line added 2026-10-07 under the person's delegation, settled by principle; formulated by the small-change path)
- 2026-10-07 Slice 60's Unknown, re-read after decision/a-shop-names-its-decisions: whether the reshaped decision (statement, date and number required, no shop link) can stand in for every decision today's scenarios record without changing what any of them observes; its Needs reads statement, date and number only
- 2026-10-07 slice 60 green. Someone can now: start a knowledge base holding the shop's ten types (product, shop, capability, the reshaped decision and the new feature beside the five kept), and record each with an owner, a status and tags.
  Surprised by: kb's Replace takes a decision's whole content, so the four steps that write a whole decision (batch_writes, review-who-changed-what, revise-an-artifact, read-an-artifact's tagging of the older decision) give statement, date and number too, beside the creates. Type-order probe (.superpowers/batch16/slice60/probe_order.py, fresh v0.6.0 stores): kb accepts a link whose targets name a kind not yet defined, so shop and capability load in either order; TYPES is shop-artifact, tag, product, shop, capability, decision, work-item, feature, role, step, process. 16 test modules gained decision fields, all from tests/decision_fields.py (decided(n)). Needing nothing but data: every existing scenario that records a decision, and the decision and feature rows of the ten-types outline (the work item, role, process, step and tag rows needed nothing); the two Thens that count the types needed new step text. Types carry title as required beside the listed fields, as every existing type does; no length or line-break limits yet (slice 62).
  Open questions: none. Next: slice 61.
- 2026-10-07 Suite: 137 passed, 16 failed at e6044f0 in 13.7 s; failing: slice 62's 16 rows of use-the-shops-types
