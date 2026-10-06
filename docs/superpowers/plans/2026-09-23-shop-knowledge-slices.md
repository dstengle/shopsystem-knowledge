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
- Status: green

## Slice 52: shop-knol reaches kb v0.5.0 through contract v1, every answer unchanged
- Kind: enabling
- Check: `.venv/bin/pip show shopsystem-kb` -> Version 0.5.0; `grep -rn "kb_pb2\.\(Apply\|Init\|Journal\|Validate\|Refs\|Write\|Append\|Delete\)" src tests` -> nothing; `make test` -> every scenario that passed before the slice passes, except "One bad change in a batch leaves the shop untouched" (its step builds a batch that mixes kinds, which v1 cannot land; slice 56 takes it)
- Observable: everything a user could do on kb v0.3.0 they can do on v0.5.0, the same commands giving the same answers and refusals
- Unknown: whether every command maps onto its v1 call with its answer and its refusals unchanged
- Needs: the pin in pyproject.toml; the stand-in and the steps' oracles speak v1's messages (needed by every scenario that compares with kb's answer)
- Status: green

## Slice 53: shop-knol answers through a kb server exactly as through the store
- Kind: capability
- Scenarios: find-the-knowledge-base / Reading where the knowledge base found is a connection to a server hosting the store
- Observable: a user whose directory holds only the connection to a kb server reads the shop's knowledge as if the store were beside them
- Unknown: whether a kb server started by the test, inside its own temporary directory on a port of its own, serves shop-knol unchanged
- Needs: starting and stopping a real kb server from a step, within the suite's isolation rules (needed by this scenario and by slice 55's server rows)
- Status: blocked: awaiting a kb release that ships `kb serve` and a client that reaches a server through `kb/server.yaml` (kb v0.5.0 lists serving under Not yet)

## Slice 54: init furnishes an empty knowledge base it finds, and starts one only where none is found
- Kind: capability
- Scenarios: start-a-knowledge-base / With no directory named, an empty knowledge base kb finds from the working directory is furnished with the shop's types (both rows); start-a-knowledge-base / Naming a directory that holds an empty knowledge base furnishes it with the shop's types; start-a-knowledge-base / Where no knowledge base is found, the shop's knowledge sits in a place of its own inside the working directory; start-a-knowledge-base / Starting a knowledge base where the directory already holds one is refused; start-a-knowledge-base / With nothing naming another knowledge base, starting from inside one the shop already has is refused; start-a-knowledge-base / Starting a knowledge base from a removed directory, with nothing naming a knowledge base, ends in a plain refusal
- Observable: a user who works where kb's operator started an empty knowledge base runs `shop-knol init` and gets the shop's types in it, while a user with nothing found still gets a new one beside their work
- Unknown: how init tells whether kb finds a knowledge base from where it is, and loads the types into it instead of starting one
- Needs: none
- Status: green

## Slice 55: init refuses a knowledge base it cannot furnish
- Kind: capability
- Scenarios: start-a-knowledge-base / With no directory named, starting where finding the knowledge base is refused is refused for finding's reason (both rows); start-a-knowledge-base / Starting where the knowledge base to furnish holds something other than the shop's types is refused (both rows)
- Observable: init never furnishes a knowledge base already holding something else, saying what it holds, and stops for the reason finding gives
- Unknown: how init tells, through the contract alone, an empty knowledge base from one holding something else
- Needs: none
- Status: green

## Slice 55.1: init never furnishes twice
- Kind: capability
- Scenarios: start-a-knowledge-base / Starting where the knowledge base to furnish already holds the shop's types is refused (all three rows; its server row waits on slice 53)
- Observable: init refuses a knowledge base found through KB_ROOT, or named, that already holds the shop's types, instead of starting a second store beside it
- Unknown: none (slice 55 settled how a found knowledge base is told apart)
- Needs: slice 53's server for the outline's server row only
- Status: in progress: its server row waits on slice 53

## Slice 55.2: init furnishes a served empty store
- Kind: capability
- Scenarios: start-a-knowledge-base / With no directory named, an empty store kb reaches through a server is furnished with the shop's types
- Observable: a user reaching an operator's empty store through a server furnishes it as one in place
- Unknown: none once a kb server exists
- Needs: slice 53's server
- Status: blocked: awaiting slice 53

## Slice 56: A batch of creates lands as one, its new artifacts linked by keys
- Kind: capability
- Scenarios: make-several-changes-at-once / The user makes several changes at once; make-several-changes-at-once / A link written with a key a create in the batch carries names that create's artifact (both rows); make-several-changes-at-once / A link written with a key no create in the batch carries leaves the shop untouched; make-several-changes-at-once / Two creates carrying the same key leave the shop untouched; make-several-changes-at-once / One bad change in a batch leaves the shop untouched; make-several-changes-at-once / A batch whose prose the shop cannot keep leaves the shop untouched
- Observable: a user records a decision and a work item pointing at it in one batch, the history showing one change, and a bad key or a bad change refuses the whole batch
- Unknown: how a key a create carries, and a link written with it, reach kb
- Needs: none
- Status: green

## Slice 57: A batch of writes lands as one; a batch of mixed kinds, or a write carrying a key, is refused
- Kind: capability
- Scenarios: make-several-changes-at-once / The user applies a batch whose changes are all writes; make-several-changes-at-once / A write carrying a key leaves the shop untouched; make-several-changes-at-once / A batch mixing creates and writes leaves the shop untouched
- Observable: a user rewrites several artifacts as one change, and a batch kb could not land as one set is refused in plain words before anything lands
- Unknown: whether shop-knol's own refusal of a batch's kinds and keys reads as one refusal naming the batch and the key
- Needs: none
- Status: green

## Slice 58: The user sees and reads the shop's types through a command of their own
- Kind: capability
- Scenarios: use-the-shops-types / The user asks which types the shop holds; use-the-shops-types / The user reads one of the shop's types by its name; use-the-shops-types / Every artifact of the shop's seven types can carry an owner, a status and tags (all seven rows); use-the-shops-types / A process's step either defines a step in place or uses a shared step with settings of its own (both rows)
- Observable: a user runs `shop-knol types` to see the shop's seven types and `shop-knol types <name>` to read one, and every kind of thing carries an owner, a status and tags
- Unknown: what the types command shows of each type, and of one type, as the shop holds it
- Needs: none
- Status: green

## Slice 59: Markdown shows a field holding a mapping as a nested list
- Kind: capability
- Scenarios: publish-an-artifact / Markdown shows a field holding a mapping as a list nested under the field
- Observable: a role's field holding a mapping reads on its page as a list under the field
- Unknown: none
- Needs: none
- Status: green

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

## Log

- 2026-10-05 Batches 1 to 13 archived in `docs/superpowers/plans/archive/2026-09-23-shop-knowledge-slices-batches-1-13.md`; batch 13's last line: Suite `100 passed`.
- 2026-10-05 MIGRATED to capabilities (spec/ committed in 070886f, lines approved 2026-10-05). The 14 feature files became 16, one per capability under spec/capabilities/, each scenario moved verbatim with its tags, in its capability's line order: start-a-shop-knowledge-base split into start-a-knowledge-base and use-the-shops-types; read-back-what-the-shop-knows into find-the-knowledge-base and read-an-artifact; record-a-decision, revise-what-the-shop-knows, retire-what-the-shop-no-longer-uses, list-what-the-shop-has-recorded, follow-the-links-between-what-the-shop-knows, check-the-shops-knowledge-is-sound and publish-what-the-shop-knows renamed to record-an-artifact, revise-an-artifact, retire-an-artifact, list-what-the-shop-holds, follow-the-links, check-the-knowledge-base and publish-an-artifact. Test modules renamed with their features; no step definition changed; test_read_an_artifact.py binds both halves of read-back, whose finding scenarios share its Background steps; test_use_the_shops_types.py star-imports start_roles_and_tags. The feature half of every Scenarios line above is rewritten to the new names; batch plans are history and keep the old ones. Verified against the baseline: 100 passed, the same passing scenarios by title, the same count for each of the 40 slice tags. Unbacked lines approved at the gate go to formulating-features: init furnishing an empty knowledge base kb finds (and its refusals), `shop-knol types`, a server connection behaving as the store, the fields every shop artifact carries, a process's steps in place or shared, a mapping on a markdown page as a nested list.
- 2026-10-05 Suite: 37 failed, 94 passed (after the kb v0.5.0 spec and its formulation, e05a55b; on kb v0.3.0). Red: exactly the 37 new or changed scenarios of this batch (Examples rows counted), each on a step not yet defined.
- 2026-10-05 Batch 14 cut (slices 51 to 59) under the person's delegation (2026-10-05: "use your recommendations for any questions"). The ninth architecture review the batch 13 log named is not cut: under shopsystem-bdd 0.9.0 the batch's branch review checks shape and coupling, and the separate review runs only when the person asks. The parked driver split is slice 51, before the server work that grows the driver. Order: the split, then the pin the rest stands on, then by risk: the server harness, furnishing, telling what a found knowledge base holds, keys in a batch, a batch's kinds refused, the types command, a markdown case with no unknown.
- 2026-10-05 slice 51 green. Someone can now: grow tests/driver.py for a server, because kb's answers asked as oracles (`kb_answer`, `actor`, `printed`, `refused_as_kb_refuses`, `UNKEPT`, `refused_as_unkept`, `NO_STORE`) sit in tests/kb_oracle.py and the driver holds only launching shop-knol, isolation and the environment (driver.py 249 to 143 lines, kb_oracle.py 115; no tests module over 250).
  Surprised by: kb_oracle reads driver's `_default_cwd`, `_isolated` and `Removed` at call time through `import driver` (conftest monkeypatches `driver._default_cwd`); session_guard's own `import driver` became unused. CLAUDE.md's two sentences reworded to name kb_oracle. Suite `37 failed, 94 passed`, the same failing list.
  Open questions: none. Next: slice 52.
- 2026-10-05 slice 52 green. Someone can now: run every shop-knol command against kb v0.5.0 through contract v1 (`kb.init` for a start, Replace, Add, Remove, Check, History, Follow, BatchCreate or BatchReplace for `apply`), each answer keeping its keys; `pip show` gives 0.5.0 and no v0.3.0 message name is left under src/ or tests/.
  Surprised by: read-an-artifact's Given 'the older decision is tagged "seasonal"' built its state with a mixed batch (create a tag, write the decision), which v1 cannot land, so "The user asks for the links to be followed two steps" went red; the step now makes the same state with `create` then `write`. The clock stand-in fronts `kb.init` beside `connect`, or init's own entry is stamped from the machine's clock ("The user reviews the changes since a date" went red). `_answered` no longer takes `also`: a check's violations and a renderer's faults are refused through `_refused`, and CLAUDE.md's size-and-shape sentence says so. A mixed batch is now a traceback until slice 57. Suite `37 failed, 94 passed` before, `38 failed, 93 passed` after: the one addition is "One bad change in a batch leaves the shop untouched".
  Open questions: none. Next: slice 53.
- 2026-10-05 HAND-BACK slice 53, scenario "Reading where the knowledge base found is a connection to a server hosting the store": the scenario can't be made to fail on its Then line, only on setup (the Given "the shop's knowledge base is hosted by a server" describes a state kb v0.5.0 cannot produce), and going green needs a kb change.
  Evidence: `RuntimeError: kb serve exited 2: usage: kb [-h] {init,validate,export,import} ... kb: error: argument command: invalid choice: 'serve' (choose from 'init', 'validate', 'export', 'import')` (tests/driver.py `_answering`, from the Given's `server` fixture). kb v0.5.0 (e530e1f) has no `kb serve`, its `kb.client` is in-process only and reads no `kb/server.yaml`; its operate-a-store capability lists serving under "Not yet" ("Promoted when the served-store lines ... are formulated and built"). Neither kb's main nor batch23-storage has it either.
  Green in this slice: none. Red: "Reading where the knowledge base found is a connection to a server hosting the store".
  KB REQUEST: bump the pin to the kb release that ships reach-a-served-store and operate-a-store's `kb serve <root> --listen <host:port>` lines, with `kb.client.connect` reaching a server through `kb/server.yaml`. Slice 53 (and slice 55's server rows, and Review Focus 1 for Task 4) wait on it. Written and kept, red: the two Givens and the Then beside the find feature's steps (tests/read_back_from_elsewhere.py, a `server` fixture that stops the server at teardown), and in tests/driver.py `serve`, `stop` and `connection_in` (a real `kb serve` on 127.0.0.1 and a free port, from the shop's own directory, waited on until it takes connections); CLAUDE.md names the connection file in rule 1 and the step-definition rules. Nothing under src/ changed. Suite `38 failed, 93 passed` before and after, the same failing list.
- 2026-10-05 RE-SLICE after the HAND-BACK of slice 53 (5443cd6): no row of the hand-back table changes a Given, When or Then, so this skill re-orders alone. kb v0.5.0 specifies `kb serve` and the served-store lines but lists serving under Not yet: its command line has no `serve` and its client never reads `kb/server.yaml` (checked: `git -C ../shopsystem-kb show v0.5.0:src/kb/cli.py`). Slice 53 is blocked on a kb release that ships it (KB REQUEST, logged in the hand-back). Slice 55's two scenarios that need a server, the server-furnish scenario and the already-holds outline (its three rows share one tag), move to slice 55.1, blocked on 53. Slice 55 keeps finding refused and not empty. Order: 54, 55, 56, 57, 58, 59; 53 and 55.1 wait. The red step code for 53 (5443cd6) stays committed, never run against a server.
- 2026-10-05 HAND-BACK slice 54, scenario "Naming a directory that holds an empty knowledge base furnishes it with the shop's types": not a bdd-red-green stop condition. The implementer's own stop rule fired: a file would cross the 250-line limit. Every scenario is green, but `src/shop_knowledge/cli.py` holds 269 lines with the least code that makes them green: `_init` picks `_named` or `_found`, and `_empty` sends one List of kind `schema` as ids (`kb_requests.init_request`). CLAUDE.md says "split first", and a split means a new module and a module-map row (or init moved out of `cli.py`'s row). The brief does not decide that, so it is handed back rather than chosen here.
  Evidence: `wc -l src/shop_knowledge/*.py ... | awk '$1 > 250'` gives `269 src/shop_knowledge/cli.py` (245 before). `-m slice-54` gives `7 passed`. Suite `38 failed, 93 passed` before, `31 failed, 100 passed` after; only the seven slice-54 scenarios left the failing list.
  Green in this slice: all seven (both furnish rows, the named furnish, none found, already holds, inside one, removed directory). Red: none, but the size check fails. Slice 54 stays not green until the split is decided. Suggested split: move init's handler and helpers (`_init`, `_found`, `_named`, `_empty`, `_started`, `_absolute`, `_GONE`) to a new `start.py` row ("which knowledge base init furnishes, the one kb finds or is named when empty or a store it starts, and kb's refusal to start one as `Refused`"), with `cli._HANDLERS` naming it.
- 2026-10-05 slice 54 green. This resolves the HAND-BACK above, following the controller's ruling: init's finding, emptiness, furnishing and starting moved to a new module, `src/shop_knowledge/start.py`, with a CLAUDE.md row; `cli.py`'s row was adjusted. `cli.py` is 222 lines and `start.py` 71. Someone can now: run `shop-knol init` where kb's operator started an empty knowledge base, whether it is found upward, through KB_ROOT or named, and have it furnished with the shop's types; with nothing found, a new knowledge base is started beside their work.
  Surprised by:
  - Four of the seven scenarios needed only their Givens: none found, already holds, inside one, and removed directory. Today's init already did what they ask.
  - The removed-directory Then holds shop-knol's own "gone" words, not kb's, so `start._absolute` still refuses before kb is called.
  - `start.furnished` hands bootstrap's Create answers back to `cli._init`, so `_answered` stays the one way a kb answer is refused.
  - Suite `38 failed, 93 passed` before, `31 failed, 100 passed` after; only the slice's seven scenarios left the failing list.
  - Review Focus 1 (an unreachable server) is deferred with slice 53.
  Open questions: for Task 5 (slice 55), every finding refusal still falls through to starting a store in the working directory, including those with KB_ROOT set. When slice 55 refuses those instead, `driver.start` and the init Whens of slices 4, 47 and 50.x will break, because the suite's `env` sets KB_ROOT to the shop's directory before any store exists. Next: slice 55.
- 2026-10-05 slice 55 green. Someone can now: run `shop-knol init` with KB_ROOT naming a directory that holds no knowledge base, or a knowledge base other than the one they work in, and be refused in kb's own words with nothing started; and be refused, in plain words naming KB_ROOT and the types it holds, when the knowledge base to furnish already holds types that are not all the shop's.
  Surprised by:
  - Splitting `start._found` on the List's outcome broke previously green scenarios (16 on the two modules run: 12 of record-an-artifact, 4 of start-a-knowledge-base): `driver.start` and the feature's own init When ran init with the suite's KB_ROOT naming the shop's directory before any store existed. Both now run init with no KB_ROOT (`driver.unnamed`); no Given, When or Then changed.
  - A knowledge base holding all of the shop's types still falls through to `kb.init` in the working directory, so slice 54's "already holds" and "inside one" keep kb's words; the KB_ROOT-elsewhere case of that is slice 55.1's.
  - Suite `31 failed, 100 passed` before, `27 failed, 104 passed` after; only the slice's four scenarios left the failing list.
  - Review Focus 2: a Create refused partway leaves the types created before it, and a second `init` refuses the knowledge base as not empty, naming them; logged in the Backlog.
  Open questions: a knowledge base found upward (no KB_ROOT) holding types other than the shop's is refused with no name before its message, since no scenario says how to name it; `_absolute` still refuses a gone working directory before finding, even where KB_ROOT names a knowledge base. Next: slice 56.
- 2026-10-05 RE-SLICE after Task 5's review (5dcfa5c): with KB_ROOT naming a knowledge base elsewhere that already holds the shop's types, init starts a second store in the working directory and reports success (reproduced by the reviewer), against start-a-knowledge-base's Purpose and Implementation (a store is started only where none is found). The already-holds outline is buildable but for its server row, so slice 55.1 keeps it and runs now, its server row waiting on slice 53; the server-furnish scenario becomes slice 55.2, blocked on 53. No Given, When or Then changes.
- 2026-10-05 slice 55.1 in progress: its KB_ROOT and named-directory rows are green, and its server row waits on slice 53. That row fails in setup: `kb serve exited 2: ... invalid choice: 'serve'`. Someone can now: run `shop-knol init` with KB_ROOT naming a knowledge base elsewhere that already holds the shop's types, or name a directory holding one, and be refused in plain words naming it ("it already holds the shop's knowledge"), with nothing started and nothing changed.
  Surprised by:
  - The named row needed no Given of slice 54's kind. `_named` already reached the store there when kb refused to start one, so it now asks that store whether it holds the shop's types before passing kb's refusal on.
  - A KB_ROOT naming the working directory itself, and a knowledge base found upward, still fall through to `kb.init`, so slice 47's and 54's reasons stay in kb's words (decision/a-working-directory-holding-the-shops-knowledge-keeps-its-reasons).
  - Review Minor #1 fell out of the same change: `_found` now tests whether KB_ROOT is present, as kb does, so a set-but-empty KB_ROOT is refused in kb's words ("KB_ROOT names a directory that holds no store:") where init used to start a store in the working directory.
  - The server Given starts its own `kb serve` through `driver.serve`, since the read-an-artifact `server` fixture sits in a step module that no other step module may import.
  - Suite `27 failed, 104 passed` before, `25 failed, 106 passed` after; only the two rows left the failing list.
  Open questions: a named directory holding types other than the shop's is still refused in kb.init's words, not as not empty, since no scenario names it; a KB_ROOT naming a store the working directory sits inside, which kb finds as the same store, is refused as already holding the shop's knowledge rather than in kb's "inside" words, since the decision keeps kb's reasons only for the working directory itself. Next: slice 56.
- 2026-10-05 slice 56 green. Someone can now: record a decision and a work item pointing at it in one batch, the link written `@<key>` with a key the decision carries, wherever in the batch either stands, the history showing one change; a key no create carries, a key two creates share, a change that does not fit its type, or prose the shop cannot keep refuses the whole batch.
  Surprised by:
  - The production change is one field: `batch._item` carries a create's `key` into its `CreateItem`, and the `batch` shape names `key` as a string. Links written `@<key>` pass as written and kb puts the name in.
  - Of the seven, only the first scenario and the key-shared scenario needed the key carried to go green. The outline was red on its undefined Given, then green on the first scenario's change (with `batch.py` stashed it is red on its Then: kb refuses `'@weekly'`). The key-no-create scenario and the prose scenario were red only on undefined steps and green on their steps alone: kb's `ref` refusal passes through, and `document.read` refuses the prose before kb. With `batch.py` stashed, the key-no-create scenario stays green, because the link's key is carried by nothing either way.
  - "One bad change" was red on a traceback (its old mixed batch, which slice 57 refuses). Its step is now two creates, the second a work item with `owner` and `status` that do not fit, and its Then names that work item. No Gherkin changed.
  - kb words a key no create carries as `a link must land on a node of a kind the type allows; '@monthly' does not` under rule `ref`. The Thens compare the printed lines with kb's own answer to the same BatchCreate (`kb_answer`), and check that a `ref` fault names the key.
  - "The shop's history shows them as one change" now compares the batch's History with the ids the apply gave back, not a fixed list, so slice 57's writes scenario can read it too.
  - Suite `25 failed, 106 passed` before, `18 failed, 113 passed` after; only the slice's seven scenarios left the failing list. test_make_several_changes_at_once.py is 219 lines, so slice 57 will likely need a sibling step module (adrs/0035).
  - Review Focus 4: a link written `@` alone is refused in one line in kb's words, exit 1. A key given empty is taken as no key and the create lands (exit 0), never a traceback; logged in the Backlog.
  Open questions: whether a key given empty is a key (Backlog). Next: slice 57.
- 2026-10-05 slice 57 green. Someone can now: rewrite several artifacts as one change with a batch of writes, the history showing one change; a batch mixing creates and writes, or a write carrying a key, is refused in one plain line naming the batch file (and `changes/<n>/key`), before kb is called.
  Surprised by:
  - "The user applies a batch whose changes are all writes" was red only on its undefined Givens and went green on its steps alone: Task 2's `apply_request` already sends a BatchReplace for all writes. The other two were red on their Then (a mixed batch ended in a protobuf traceback; a keyed write landed, its key ignored).
  - The keyed-write refusal is shop-knol's own words raised in `batch.items`, not a JSON Schema rule (jsonschema's words name no key), so `shapes/batch.yaml` still allows `key` beside `write`; this is the form the Implementation line "allows `key` only beside `create`" takes. Both refusals' rule is empty, like `content`'s own-words siblings. `batch.items` takes the batch file's name, from the new `document.named`, which `document.read` uses too.
  - Steps went to a sibling module, `tests/batch_writes.py`, star-imported by the feature's test module alone (adrs/0035); the test module stays 220 lines.
  - Review Focus 3: `apply` of `changes: []` is one line in kb's words ("a set must hold at least one change"), exit 1, never a traceback (it holds no kind, so goes to kb as a BatchCreate).
  - Suite `18 failed, 113 passed` before, `15 failed, 116 passed` after; only the slice's three scenarios left the failing list.
  Open questions: none. Next: slice 58.

- 2026-10-05 slice 58 green. Someone can now: run `shop-knol types` to see the shop's seven types, `shop-knol types <name>` to read one as kb holds it, and record every kind of thing with an owner, a status and tags.
  Surprised by:
  - The listing's eleven scenarios: only "The user asks which types the shop holds" was red on its Then (the command was not there); the other ten were red on undefined steps and went green on their steps alone, as the brief expected, since the read and create paths already carried the behaviour.
  - The listing shows `name` (the id without its kind) and `title`, as a sequence; the seven are `bootstrap.SHOP_TYPES`, `TYPES` less `bootstrap.BASE`, so kb's own `schema/schema` and the base are left out of the listing only.
  - Steps went to three siblings, `tests/types_listed_and_read.py`, `tests/types_common_fields.py` and `tests/types_process_steps.py`, star-imported by the feature's test module alone.
  - Review Focus 5: `nonesuch` is one line in kb's words, exit 1; `a/b` the same; `schema` and `shop-artifact` are shown whole, exit 0 (logged in the Backlog); an empty name is refused by the argument.
  - Suite `15 failed, 116 passed` before, `4 failed, 127 passed` after; only the slice's eleven scenarios left the failing list.
  Open questions: whether `types schema` and `types shop-artifact` should be refused as not among the seven. Next: slice 59.
- 2026-10-05 slice 59 green. Someone can now: read a role's field holding a mapping on its markdown page as a list nested under the field.
  Surprised by: the renderer already nested a field group (adrs/0041), so no production code changed; the scenario was red only on its undefined Given and Then, and the two steps (in `tests/publish_as_markdown.py`) are the whole change. The Given uses the Background role's `harness` group as it is.
  Suite `4 failed, 127 passed` before, `3 failed, 128 passed` after; the three left are the kb-serve scenarios (slices 53, 55.1's server row, 55.2).
  Open questions: none. Next: none (batch 14's last slice).
- 2026-10-06 Whole-branch review of batch 14 (opus, a3d8729..0b3522c): suite `3 failed, 128 passed`, the 3 blocked on kb serve; size, imports, pin and feature files clean. Ready with fixes: the named not-empty refusal (formulated as a new row in 37abc45, for the fix wave); slice 55.1's server row needs more than kb serve (re-sliced above); CLAUDE.md's one-way-to-refuse sentence omits start's two refusals of kb's answers; `driver.serve` waits with no deadline. Feature files changed in this batch only by `@slice` tag moves in the two re-slices and the formulation commits, as the slicing rule allows; the batch plan's "tag lines included" is read as excepting the slicer's own tag moves.
- 2026-10-06 KB REQUEST (for kb's plan, with the kb serve request from slice 53's hand-back): (1) ship `kb serve` and a client that reaches a server through `kb/server.yaml`, as kb's spec already states; (2) publish where a found knowledge base is (its root or a server's address) so a client can name it in a refusal; (3) publish `kb.init`'s `execution` keyword, which shop-knowledge passes but kb's start-a-store does not name; (4) publish the id of the type that describes types (`schema/schema`), which init reads as the mark of an empty store; (5) publish `NotCanonical`'s `path` attribute, which shop-knowledge reads.
