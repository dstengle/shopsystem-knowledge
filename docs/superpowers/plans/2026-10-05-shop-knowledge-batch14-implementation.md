# shop-knowledge batch 14: slices 51 to 59, on kb v0.5.0

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, in slice order, with one commit per slice. Tasks 1 and 2 are enabling slices checked by their checks. Tasks 3 to 9 are capability slices, built one scenario at a time under shopsystem-bdd:bdd-red-green.

**This plan carries no code** (adrs/0011).

**Goal:** every approved scenario is green, with shop-knowledge on kb v0.5.0 (contract v1). The work, in order:
- 51 moves the steps' oracles of kb's answers out of the driver;
- 52 pins v0.5.0 and moves every call to v1, with every answer unchanged;
- 53 serves shop-knol through a real kb server;
- 54 and 55 make `init` furnish an empty knowledge base that kb finds, and refuse the ones it cannot furnish;
- 56 and 57 make a batch one kind of change, with keys linking new artifacts;
- 58 adds the types command;
- 59 covers markdown's nested mapping.

**Spec:** `spec/`: `index.md` (Constraints carried, Mechanisms), and the capabilities `start-a-knowledge-base`, `find-the-knowledge-base`, `make-several-changes-at-once`, `use-the-shops-types` and `publish-an-artifact`; `spec/decisions.md` from `decision/types-are-readable` on. kb's side: shopsystem-kb at tag v0.5.0, `src/kb/contract/kb.proto` and its `spec/index.md` (what kb publishes). Read CLAUDE.md, and adrs/0035, 0044, 0047, 0048 and 0049.

## Global Constraints

**Change control**
- Feature files are read-only, tag lines included.
- kb is v0.3.0 until Task 2 pins v0.5.0, and is never edited here. A change needed from kb is logged as a KB REQUEST and the slice stops.
- Every rule in CLAUDE.md holds. Task 2 rewords rule 1 to name `kb.init` and `kb.NotStarted`; Task 3 adds the connection file's form (`kb/server.yaml` and its `address`), which kb publishes, as something only `tests/driver.py` may write.
- shop-knol's commands, flags and answer keys do not change (decision/the-command-line-survives-contract-v1): an answer still says `type`, and a printed fault still reads `artifact at place: message`.

**Where to work**
- Work on `main`, and run every command from the checkout's root.
- Scratch goes under `.superpowers/batch14/`. Never create a file outside this repository's `.superpowers/` (or a test's own temporary directory), and never export `GIT_*` variables. `/home/vscode` is shared with the kb checkout.

**Review and model**
- Each task's `Review:` and `Model:` lines say how the controller dispatches it. `Review: per-task` with `Model: opus` for a task that touches the published contract, concurrency, data integrity or a stored knowledge base; `Review: batch-end` with `Model: sonnet` for the rest. A batch-end task gets no task review: the batch's branch review covers it.

**Commits**
- Commit with `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`, the message ending with the model's Co-Authored-By line.
- One commit per slice, each holding its checkpoint in the slice plan's Log and its Status set to green.
- The implementer never pushes.

**Counts**
- The suite collects 131 scenarios (Examples rows counted) and gives `94 passed, 37 failed` today (2026-10-05, after c3134dc).
- The tags select 53: 1; 54: 7; 55: 8; 56: 7, of which 1 ("One bad change in a batch leaves the shop untouched") passes today; 57: 3; 58: 11; 59: 1.

| after | failed | passed |
|---|---|---|
| 51 | 37 | 94 |
| 52 | 37 or 38 | 94 or 93 ("One bad change" may go red: its step builds a batch of mixed kinds) |
| 53 | blocked (re-sliced 2026-10-05) | |
| 54 | 31 | 100 |
| 55 | 27 | 104 |
| 56 | 20 | 111 |
| 57 | 17 | 114 |
| 58 | 6 | 125 |
| 59 | 5 | 126 (the 5 left: slice 53's 1 and slice 55.1's 4, waiting on kb serve) |

**Checks**
- Record the failing list at each slice's start with `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort`, and compare at its end: only the slice's own scenarios may leave it.
- `wc -l src/shop_knowledge/*.py src/shop_knowledge/renderers/*.py tests/*.py tests/*/*.py | awk '$1 > 250'` lists nothing at each slice's end.
- `grep -rn "^from kb\|^import kb" src tests | grep -v "kb.client\|kb.content\|kb.contract\|^.*import kb$\|from kb import \(init\|NotStarted\)"` lists nothing from Task 2 on.

## Review Focus

Inputs no scenario covers that are most likely to bite. For each, the owning task probes it by hand once the slice is green, records what happened in its checkpoint, and logs a misbehaviour as a Backlog line with its reproduction. It writes no scenario for it (CLAUDE.md: no behaviour no scenario asks for).
1. `init` where kb finds a connection to a server that cannot be reached: one plain line in kb's words, exit 1, never a traceback (Task 4, after Task 3's server exists).
2. `init` furnishing a knowledge base where kb refuses a Create partway through: what the knowledge base holds afterwards, and whether a second `init` then calls it "not empty" (Task 5).
3. `apply` with a batch holding no changes: refused in one line, never a traceback (Task 7).
4. A key given empty, or a link written as `@` alone: kb's refusal passed through, never a traceback (Task 6).
5. `types <name>` for a name that is not one of the shop's seven (`schema`, `shop-artifact`, `nonesuch`): one line, never a traceback (Task 8).

---

### Task 1: Slice 51, the steps' oracles of kb's answers sit in a module of their own

Review: batch-end. Model: sonnet.

**Check:** `wc -l tests/*.py` shows no module over 250 lines, and `tests/driver.py` holds none of `NO_STORE`, `actor`, `kb_answer`, `_kb_answer_from_gone`, `_ASK_KB`, `printed`, `refused_as_kb_refuses`, `UNKEPT` or `refused_as_unkept`. `make test` gives the same `94 passed, 37 failed`, the same failing list.

**Why now:** batch 13's fix wave parked this split (the slice plan's archive, its last log lines). `tests/driver.py` is at 249 lines and holds four concerns. Task 3 grows it with the server.

**Where it lands:** a new helper module beside `tests/driver.py`, imported plainly by every step module that used those names (it is not a step module, so adrs/0035's star-import rule does not apply). `driver.py` keeps launching shop-knol, isolation and the environment. CLAUDE.md's Step definitions section names `driver.kb_answer` and `driver.printed`: reword those sentences to name the new module. Add no row to the module map, which covers `src/` only.

**Steps:**
- [ ] Record the failing list.
- [ ] Move the names, with what only they use; update every import.
- [ ] Reword CLAUDE.md's two sentences.
- [ ] Run the check and the size check.
- [ ] Checkpoint and commit.

### Task 2: Slice 52, shop-knol reaches kb v0.5.0 through contract v1, every answer unchanged

Review: per-task. Model: opus.

**Check:** `.venv/bin/pip show shopsystem-kb` gives `Version: 0.5.0`. `grep -rn "kb_pb2\.\(Apply\|Init\|Journal\|Validate\|Refs\|Write\|Append\|Delete\)" src tests` lists nothing. `make test` passes every scenario that passed before the slice, except perhaps "One bad change in a batch leaves the shop untouched" (Task 6 takes it).

**Why red today:** the pin is `@v0.3.0`. Every call uses v0.3.0's rpc and message names.

**Where it lands:**
- `pyproject.toml`: the pin `@v0.5.0`. Reinstall with `.venv/bin/pip uninstall -y shopsystem-kb && make dev`.
- `src/shop_knowledge/kb_requests.py`: each command's request in v1's messages.
  - `kind` where v0.3.0 said `type`; `place` where it said `path`.
  - One `Signature` (role, execution, message) where a request carried an `Actor` and a message.
  - Read's level as one of `summary`, `whole` with a depth, or `section` with a title. No flag means summary. `--whole` is whole at depth 0. `--resolve [n]` is whole at depth n. `--section` wins.
  - `refs` → Follow, `journal` → History, `validate` → Check, `write` → Replace, `append` → Add, `delete` → Remove. `apply` → BatchCreate when every change is a create, BatchReplace when every change is a write. Task 7 owns refusing a mixed batch, so do nothing more for it here.
- `src/shop_knowledge/batch.py`: a batch read into the items of one BatchCreate or one BatchReplace. Its module-map row says "the operations of one Apply": reword it.
- `src/shop_knowledge/cli.py`: `_answered` refuses on the response's refusal (`WhichOneof("outcome")`) and hands `result` on. `init` starts a store with `kb.init(root, role)` in shop-knol's own process, and turns `kb.NotStarted`'s faults into the one refusal (rule 4).
- `src/shop_knowledge/answers.py`: each answer from v1's result messages (`Created`, `Artifact`, `Checked`, `Replaced`, `Added`, `Removed`, `BatchCreated`/`BatchReplaced`, `Entries`, `Followed`, `Found`, `Listed`, `Recorded`), keeping every key it shows today. `Artifact.kind` and `Stub.kind` are shown as `type`.
- `src/shop_knowledge/bootstrap.py`: each type's Create in v1's shape (`kind="schema"`, a `Signature`).
- `src/shop_knowledge/renderers/source.py` and the renderers: Read in v1's shape; faults from `refusal.faults`.
- `src/shop_knowledge/document.py`, `shape.py`: a Fault's `place`.
- Tests:
  - the stand-in (`tests/stand_in/sitecustomize.py`), and every step that writes the messages it answers with, in v1's response shapes (a refusal as `refusal=Refusal(faults=…)`);
  - the oracle module from Task 1: `kb_answer` asks v1's calls, and for a start uses `kb.init` and catches `kb.NotStarted`;
  - conftest's session guard's own call to kb;
  - `tests/clock/sitecustomize.py`, if its use of `connect` changes.
- CLAUDE.md rule 1: name `kb.init` and `kb.NotStarted`. adrs/0013: a dated line, "kb v0.5.0 is tagged and pinned; contract v1".

**Decisions already made:**
- Answers keep shop-knol's keys (decision/the-command-line-survives-contract-v1).
- Check's violations are its result, not a refusal: `validate` prints them on stderr and `sound: false` with `behind:` on stdout, exit 1, as today (decision/a-failing-check-still-shows-what-is-behind).

**Steps:**
- [ ] Record the failing list.
- [ ] Bump the pin and reinstall; run the suite and record what broke.
- [ ] Move `src/`, then the stand-in and oracles, to v1 until the check passes.
- [ ] Reword CLAUDE.md rule 1, the batch.py row, and adrs/0013.
- [ ] Run the check, the size check and the import check.
- [ ] Checkpoint (with the suite line before and after) and commit.

### Task 3: Slice 53, shop-knol answers through a kb server exactly as through the store

Review: per-task. Model: opus.

**Scenarios** (`@slice-53`, 1): find-the-knowledge-base / Reading where the knowledge base found is a connection to a server hosting the store.

**Why red today:** its two Givens are not defined: "the shop's knowledge base is hosted by a server" and "the user is working in a folder deep inside a directory holding a connection to that server".

**Where it lands:**
- `src/`: nothing is expected to change (adrs/0049). If anything does, stop and hand back.
- `tests/driver.py`: starting a real `kb serve <root> --listen 127.0.0.1:<port>` subprocess on a free port, inside the test's own temporary directory, under the allowlisted environment; waiting until it answers; stopping it when the test ends (a fixture with teardown); writing the connection file, `<directory>/kb/server.yaml` with its `address`. That file's form is what kb publishes (kb's `spec/index.md`, Constraints carried). The driver is the one place a root's `kb/` is named (CLAUDE.md, Step definitions). Add the sentence about the connection file there, and to CLAUDE.md rule 1's test clause.
- The Givens go beside the find feature's steps (`tests/read_back_from_elsewhere.py`, which `tests/test_read_an_artifact.py` star-imports). They reuse the feature's Background, which seeds the decision in a store. The served store is that one.
- The When "the user reads the decision" and its Then exist in `tests/test_read_an_artifact.py` (or its sibling). Reuse them, and compare with the answer read straight from the store.

**Decisions already made:**
- Testing reaches only a server it started, on a port of its own, inside its own temporary directory (decision/shop-knol-reaches-kb-wherever-kb-finds-it).
- No test reaches a store outside its temporary directory, and the session guard stays as it is.

**Steps:**
- [ ] Record the failing list; run `-m slice-53` and see it red on the undefined Given.
- [ ] Red-green the scenario.
- [ ] Run `-m slice-53`, then the whole suite.
- [ ] Checkpoint and commit.

### Task 4: Slice 54, init furnishes an empty knowledge base it finds, and starts one only where none is found

Review: per-task. Model: opus.

**Scenarios** (`@slice-54`, 7):
- start-a-knowledge-base / With no directory named, an empty knowledge base kb finds from the working directory is furnished with the shop's types (both rows)
- Naming a directory that holds an empty knowledge base furnishes it with the shop's types
- Where no knowledge base is found, the shop's knowledge sits in a place of its own inside the working directory
- Starting a knowledge base where the directory already holds one is refused
- With nothing naming another knowledge base, starting from inside one the shop already has is refused
- Starting a knowledge base from a removed directory, with nothing naming a knowledge base, ends in a plain refusal

**Why red today:** their Givens are undefined. Some name a knowledge base kb's operator started empty; some add "nothing names a (different) knowledge base" to an existing Given. Once the Givens exist, furnishing fails: init always starts a store, and kb refuses a directory that already has one.

**Where it lands:** `cli.py`'s init handler, `bootstrap.py` (unchanged in what it loads), `kb_requests.py` for any request init now makes. Steps go in `tests/start_refused.py` and `tests/test_start_a_knowledge_base.py`. An operator-started empty store is made in a step with `kb.init` (published) under a role of the step's own, never by writing files. "Nothing names a knowledge base" means the allowlisted environment has no `KB_ROOT`. Assert that rather than unsetting anything by hand.

**Decisions** (each rests on the line or ledger entry named):
- **No directory named.** init first asks kb to find a knowledge base from the working directory: connect with no root, then one read-only call. The answer decides:
  - **Found and empty:** load the shop's types into it through Create, and start nothing. This is decision/init-furnishes-the-knowledge-base-kb-finds.
  - **Found and holding the shop's types,** found upward (no `KB_ROOT`), or through a `KB_ROOT` that names the working directory itself: start with `kb.init(<working directory>)` so that kb's own refusal reaches the user, "already has a store inside it" or "is inside a store". That keeps slice 47's reasons in kb's words (decision/a-working-directory-holding-the-shops-knowledge-keeps-its-reasons). Task 5 owns the other found cases.
  - **Nothing found:** kb's finding refusal (rule `store`) while no `KB_ROOT` is set and the working directory exists means start with `kb.init(<working directory>)`, then load the types.
  - **Any other finding refusal** (`KB_ROOT` set, or the working directory gone) is refused for finding's reason, in kb's words. Task 5 covers the `KB_ROOT` rows. The removed-directory scenario is here.
- **Empty** means the knowledge base holds no type but kb's own: a List of kind `schema` as ids answers `schema/schema` alone. No artifact of another kind can exist without its type, so this answers for content too (start-a-knowledge-base Behaviour; the types are data, rule 5). init knows the shop's eight schema names from `bootstrap.TYPES`.
- **A directory named.** Start with `kb.init(<root>)`. If kb refuses because the directory already has a store inside it, connect to that root and furnish it when it is empty. Any other refusal of kb's (inside a store, the directory missing) reaches the user in kb's words. A named directory found holding something is Task 5's.
- History: the start entry is kb's ("initialise store"). The types are recorded under init's fixed messages, as today.

**Steps:**
- [ ] Record the failing list; run `-m slice-54` and see each red.
- [ ] Red-green one scenario at a time, starting with the furnish rows.
- [ ] Run `-m slice-54`, then the whole suite.
- [ ] Probe Review Focus 1, and record it.
- [ ] Checkpoint and commit.

### Task 5: Slice 55, init refuses a knowledge base it cannot furnish, and furnishes one through a server

Review: per-task. Model: opus.

**Re-sliced 2026-10-05 (after slice 53's hand-back):** kb v0.5.0 cannot serve a store, so the already-holds outline and the server-furnish scenario moved to slice 55.1, blocked on slice 53. This task builds slice 55 alone; the "Already holds the shop's types" decision and the server Givens below wait for 55.1.

**Scenarios** (`@slice-55`, 4):
- start-a-knowledge-base / With no directory named, starting where finding the knowledge base is refused is refused for finding's reason (both rows)
- Starting where the knowledge base to furnish holds something other than the shop's types is refused (both rows)

**Why red today:** their Givens are undefined. Once they exist:
- init has no refusal of its own for a found knowledge base holding the shop's types or something else;
- a server is reached for the first time by init.

**Where it lands:** `cli.py`'s init handler, and the refusal built where init's other refusals are (`refusal.Refused`, rule 4). The server Givens reuse Task 3's driver fixture.

**Decisions:**
- **Already holds the shop's types,** where found through `KB_ROOT` naming somewhere other than the working directory, through a server, or in a named directory: shop-knol's own refusal, in plain words naming the knowledge base, "it already holds the shop's knowledge". A knowledge base holding the shop's types and other things too is refused the same way (decision/init-edge-cases-settled-by-principle). Name it as the user can find it: the `KB_ROOT` value, the named directory, or the server's address.
- **Not empty,** with not all of the shop's types present: shop-knol's own refusal, "it is not empty", naming what it holds: the kinds of the types it holds besides kb's own (start-a-knowledge-base: "naming what it holds"). For the content row, the types are what is named.
- The rule names of shop-knol's own refusals here are its own, like `actor` and `message`. A Then compares with what `printed` makes of the step's expected Fault, never with kb's words.
- **Finding refused:** kb's refusal passed through. The Then compares with the oracle's `kb_answer` for the same call under the same environment (CLAUDE.md, Step definitions).

**Steps:**
- [ ] Record the failing list; run `-m slice-55` and see each red.
- [ ] Red-green: finding refused, then not empty, then already holds, then the server rows.
- [ ] Run `-m slice-55`, then the whole suite.
- [ ] Probe Review Focus 2, and record it.
- [ ] Checkpoint and commit.

### Task 5.1: Slice 55.1, init never furnishes twice

Review: per-task. Model: opus.

**Added 2026-10-05 by a re-slice after Task 5's review.**

**Scenarios** (`@slice-55.1`, 3): start-a-knowledge-base / Starting where the knowledge base to furnish already holds the shop's types is refused (three rows: through KB_ROOT, through a server, in a named directory). The server row cannot pass until slice 53 (kb v0.5.0 has no `kb serve`); it stays red, failing in setup, and is named in the checkpoint.

**Why red today:** the KB_ROOT row: init starts a second store in the working directory and exits 0 (start.py's finding falls through to starting when the found knowledge base holds the shop's types and KB_ROOT names somewhere else). The named-directory row: its Given is undefined, or init furnishes or refuses in kb's words instead.

**Where it lands:** `src/shop_knowledge/start.py`, in the same branch slice 55 split. Steps beside slice 55's (`tests/start_not_empty.py` or `tests/start_refused.py`); the server row's Given may reuse Task 3's server Givens and stays red.

**Decisions:** as Task 5's "Already holds the shop's types" decision: shop-knol's own refusal, in plain words naming the knowledge base as the user can find it (the KB_ROOT value, or the named directory), "it already holds the shop's knowledge". A knowledge base holding the shop's types and other things too is refused the same way (decision/init-edge-cases-settled-by-principle). A KB_ROOT naming the working directory itself keeps slice 47's reasons in kb's words (decision/a-working-directory-holding-the-shops-knowledge-keeps-its-reasons). Use the same naming form as slice 55's not-empty refusal.

**Steps:**
- [ ] Record the failing list; run `-m slice-55.1`.
- [ ] Red-green the KB_ROOT row, then the named row.
- [ ] Run `-m slice-55.1` (2 passed, 1 failed: the server row), then the whole suite.
- [ ] Checkpoint and commit; slice 55.1's Status stays `in progress: its server row waits on slice 53`.

### Task 6: Slice 56, a batch of creates lands as one, its new artifacts linked by keys

Review: per-task. Model: opus.

**Scenarios** (`@slice-56`, 7):
- make-several-changes-at-once / The user makes several changes at once
- A link written with a key a create in the batch carries names that create's artifact (both rows)
- A link written with a key no create in the batch carries leaves the shop untouched
- Two creates carrying the same key leave the shop untouched
- One bad change in a batch leaves the shop untouched
- A batch whose prose the shop cannot keep leaves the shop untouched

**Why red today:**
- The first and the prose scenario: their Given changed to "a batch that records a decision and a work item pointing at it", which is undefined.
- The key scenarios: their Givens are undefined.
- "One bad change" is green on v0.3.0 only because its step builds a mixed batch. After Task 2 it may be red. Its step's batch becomes two creates, the second not fitting its type. Its Gherkin is unchanged, and its Then names the second create's artifact instead of the work item.

**Where it lands:**
- `src/shop_knowledge/batch.py`: a create's `key` carried into its `CreateItem`. A link in content written `@<key>` is passed as written; kb puts the name in.
- `src/shop_knowledge/shapes/batch.yaml`: `key` as a string beside `create`.
- The steps in `tests/test_make_several_changes_at_once.py`. If that module grows past the limit, move one concern's steps to a sibling (adrs/0035). "The shop's history shows them as one change" asks the oracle for History by the batch's name.

**Decisions:**
- A key no create carries, and two creates sharing a key, are kb's refusals passed through (make-several-changes-at-once, Implementation). The Thens compare with the oracle's answer for the same BatchCreate.
- The decision and work item linked by key (decision/the-batch-scenarios-record-two-linked-creates). "Both changes are in the shop" means both are read back, and the work item's link names the decision's minted name.

**Steps:**
- [ ] Record the failing list; run `-m slice-56`.
- [ ] Red-green: the first scenario, the outline, the two key refusals, "One bad change", then prose.
- [ ] Run `-m slice-56`, then the whole suite.
- [ ] Probe Review Focus 4, and record it.
- [ ] Checkpoint and commit.

### Task 7: Slice 57, a batch of writes lands as one; a batch of mixed kinds, or a write carrying a key, is refused

Review: batch-end. Model: sonnet.

**Scenarios** (`@slice-57`, 3):
- make-several-changes-at-once / The user applies a batch whose changes are all writes
- A write carrying a key leaves the shop untouched
- A batch mixing creates and writes leaves the shop untouched

**Why red today:** their Givens are undefined. After Task 2, a mixed batch or a keyed write has no refusal of shop-knol's own.

**Where it lands:** `src/shop_knowledge/batch.py`. Reading the batch's changes raises `refusal.Refused`:
- for a batch whose changes are not all one kind: one fault naming the batch file, "a batch holds one kind of change";
- for a write carrying a key: one fault naming the file and the place (`changes/<n>/key`), "only a create carries a key".

Both are in plain words (index: shop-knol's own refusals). They are raised before kb is called. Steps go in the feature's test module or its sibling.

**Decisions:**
- The keyed-write refusal is shop-knol's own words, raised in `batch.py`. A JSON Schema rule would give jsonschema's words, which name no key, so the shape does not refuse `key` beside `write`. Record this in the checkpoint as the form the Implementation line "allows `key` only beside `create`" takes.
- The two refusals' rule names are shop-knol's own, like `content` (index, Mechanisms).
- A batch with no changes is Review Focus 3. It holds no kind, so whatever it gets must be one line and no traceback.

**Steps:**
- [ ] Record the failing list; run `-m slice-57`.
- [ ] Red-green each scenario.
- [ ] Run `-m slice-57`, then the whole suite.
- [ ] Probe Review Focus 3, and record it.
- [ ] Checkpoint and commit.

### Task 8: Slice 58, the user sees and reads the shop's types through a command of their own

Review: batch-end. Model: sonnet.

**Scenarios** (`@slice-58`, 11):
- use-the-shops-types / The user asks which types the shop holds
- The user reads one of the shop's types by its name
- Every artifact of the shop's seven types can carry an owner, a status and tags (seven rows)
- A process's step either defines a step in place or uses a shared step with settings of its own (two rows)

**Why red today:** there is no `types` command, and the new steps are undefined. The outlines' behaviour likely exists already; red-green shows whether it does.

**Where it lands:** a `types` subcommand with an optional name:
- its arguments in `arguments.py`;
- its requests in `kb_requests.py` (`types_request`): a List of kind `schema` as stubs, or a whole Read of `schema/<name>` at depth 0;
- its handler in `cli.py`;
- its answers in `answers.py`: add `types` and `type_` (or names of the same style) to the module map row's list of answers.

Steps go in `tests/test_use_the_shops_types.py` or a sibling. The module star-imports `tests/start_roles_and_tags.py`, so reuse "a shop knowledge base" from there.

**Decisions:**
- **The listing** shows the shop's seven types, not the `shop-artifact` base and not kb's own `schema/schema` (use-the-shops-types Purpose: "the shop's seven types"). Each is shown as its name without its kind and its title, as a sequence with no wrapper key, like `list`.
  - The seven are `bootstrap.TYPES` less the base. Name which entry is the base in `bootstrap.py` beside `TYPES`, so no other module knows a type (rule 5).
- **Reading one** (`types <name>`) shows the type as kb holds it: kb's identity, then its content, as `read --whole` shows an artifact. A name kb holds no type for is kb's refusal passed through.
- **Owner, status and tags** are fields of the shop-artifact base. The outline records each kind from a file and reads it back whole. A tag carrying a tag of its own is fine, since the base allows it.

**Steps:**
- [ ] Record the failing list; run `-m slice-58`.
- [ ] Red-green: the listing, reading one, then each outline.
- [ ] Run `-m slice-58`, then the whole suite.
- [ ] Probe Review Focus 5, and record it.
- [ ] Checkpoint and commit.

### Task 9: Slice 59, markdown shows a field holding a mapping as a nested list

Review: batch-end. Model: sonnet.

**Scenarios** (`@slice-59`, 1): publish-an-artifact / Markdown shows a field holding a mapping as a list nested under the field.

**Why red today:** its Given "the role holds a field holding a mapping" and its Then are undefined. The page may already nest a field group (adrs/0041; the markdown renderer nests a group's fields two spaces in). Red-green shows whether it does.

**Where it lands:**
- Steps go in `tests/publish_as_markdown.py`, which `tests/test_publish_an_artifact.py` star-imports, or in `tests/markdown_pages.py` for an expected page.
- The role's `harness` group is a field holding a mapping, so the Given may use the publish feature's Background role as it is.
- If the renderer must change, the change is in `renderers/markdown.py` or `renderers/sections.py`.

**Steps:**
- [ ] Record the failing list; run `-m slice-59`.
- [ ] Red-green.
- [ ] Run the whole suite: `131 passed`.
- [ ] Checkpoint and commit.

---

After Task 9 the controller runs the whole-branch review (shopsystem-bdd:bdd-branch-reviewer) over `c3134dc..HEAD`, then the one fix wave, then pushes main (adrs/0036).
