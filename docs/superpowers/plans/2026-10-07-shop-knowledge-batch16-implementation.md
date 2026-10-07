# shop-knowledge batch 16: slices 60 to 67, the shop's types hold the shopsystem-bdd spec

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, in slice order, with one commit per slice. Every task is a capability slice, built one scenario at a time under shopsystem-bdd:bdd-red-green.

**This plan carries no code** (adrs/0011).

**Goal:** a product's knowledge base holds each shop's spec as the shop's types (product, shop, capability, the reshaped decision and the new feature, beside the five kept types). `shop-knol render spec <shop> --to <dir>` publishes a shop's `spec/`, `features/` and `adrs/` from it, and `shop-knol coverage <shop>` shows which Behaviour lines are formulated. Every scenario approved for batch 16 is green, and no scenario green today goes red.

**Architecture:** types are data (`src/shop_knowledge/types/*.yaml`, loaded by `bootstrap.py` at init). The `spec` publisher is a renderer made from `shop`. Unlike today's renderers, which read one artifact, it reads the shop's other artifacts through the contract. It is split by concern across modules under `renderers/`, each with its row in CLAUDE.md's module map. `coverage` is a new command whose reading lives in a module of its own.

**Tech stack:** Python 3.11, pytest-bdd, kb v0.6.0 (contract v1) through `kb.client.connect`, `kb.content`, `kb.contract.kb_pb2`.

**Spec:**
- `spec/capabilities/`: `use-the-shops-types.md`, `start-a-knowledge-base.md`, `publish-a-shops-spec.md`, `see-what-is-formulated.md`, each read whole.
- `spec/index.md`: Constraints carried, and the shared mechanisms. Note the line on `coverage` and `render spec` reading through Read, List and Follow.
- `spec/decisions.md`, from `decision/the-shops-types-model-the-bdd-spec` to its end.
- The note `docs/superpowers/specs/2026-10-07-spec-system-types-design.md`, for context only. The spec decides; the note does not.
- adrs/0051 to 0056.
- Read CLAUDE.md first.

## Global Constraints

**Change control**
- Feature files are read-only, tag lines included.
- kb is v0.6.0 and is never edited here. A change needed from kb is logged as a `REQUEST kb:` line in the slice plan, and the slice stops.
- Every rule in CLAUDE.md holds, the size limit of 250 lines a module included. A new concern gets a new module and a row in CLAUDE.md's module map, in the same commit.
- An existing scenario's Given, When and Then never change. Its step data may change only as Task 1 says.
- A slice that cannot go green without changing what a scenario says hands back (`HAND-BACK` in the slice plan's log, under bdd-red-green) and stops. It is never "fixed" in the feature file.

**Where to work**
- Work on `main`, and run every command from the checkout's root.
- Scratch goes under `.superpowers/batch16/`, and only there or in a test's own temporary directory. Never export `GIT_*` variables. `/home/vscode` is shared with the kb checkout.

**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/` (`plan` for the slice plan's status and log, `features` for counts).

**Review and model**
- Each task's `Review:` and `Model:` lines say how the controller dispatches it:
  - `Review: per-task` with `Model: opus` for a task that touches the published contract, data integrity or what `init` furnishes;
  - `Review: batch-end` with `Model: sonnet` for the rest. A batch-end task gets no task review: the batch's branch review covers it.

**Commits**
- Commit with `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`, the message ending with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- One commit per slice, holding its checkpoint in the slice plan's Log and its Status set to green.
- The implementer never pushes.

**Counts**
- The suite collected 153 scenario rows at f965ec0 (Examples rows counted) and gave `132 passed, 21 failed` in 12.8 s. The 21 failures are slice 60's 5 red rows and slice 62's 16.
- publish-a-shops-spec and see-what-is-formulated are not collected until a test module binds them: Task 2 binds the first (31 rows) and Task 7 the second (5 rows).
- Rows by tag: 60: 12 (7 green today: the decision, feature, work item, role, process, step and tag rows of the ten-types outline pass against the old types; that must still hold after Task 1); 61: 1; 62: 16; 63: 8; 64: 8; 65: 1; 66: 5; 67: 13.

| after | collected | failed | passed |
|---|---|---|---|
| 60 | 153 | 16 | 137 |
| 61 | 184 | 46 | 138 |
| 62 | 184 | 30 | 154 |
| 63 | 184 | 22 | 162 |
| 64 | 184 | 14 | 170 |
| 65 | 184 | 13 | 171 |
| 66 | 189 | 13 | 176 |
| 67 | 189 | 0 | 189 |

**Checks**
- Compare the failing list at a slice's start and end, with `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort`. Only the slice's own scenarios may leave it; none may join it.
- `wc -l src/shop_knowledge/*.py src/shop_knowledge/renderers/*.py tests/*.py tests/*/*.py | awk '$1 > 250 && $2 != "total"'` lists nothing at each slice's end.
- This lists nothing at each slice's end: `grep -rn "^from kb\|^import kb" src tests | grep -v "kb.client\|kb.content\|kb.contract\|^.*import kb$\|from kb import \(init\|NotStarted\)\|kb.testing"`.
- `grep -rln "jsonschema" src` lists only `src/shop_knowledge/shape.py`.

## Review Focus

These are inputs no scenario covers that are most likely to bite. Once its slice is green, the owning task probes each one by hand in a scratch directory under `.superpowers/batch16/` and records what happened in its checkpoint. A misbehaviour becomes a Backlog line with its reproduction. No scenario is written for any of them (CLAUDE.md: no behaviour that no scenario asks for).
1. **A title that makes an empty file name** (all punctuation, or only letters outside a to z, such as `Café ®` → `caf`; `®` alone → nothing) when publishing a shop. Expected: a plain refusal naming the artifact, never a file named `.md` or `0007-.md`, and never a traceback. Owner: Task 4.
2. **A capability whose `rests_on` names a decision the knowledge base does not hold**, the link left dangling by the stand-in. Expected: publishing refuses in kb's words, or in plain words naming the decision, and writes nothing. Owner: Task 5.
3. **Publishing into a directory that already holds an older spec** with a capability since removed from the shop. Expected: the published files are written over. Whether the removed capability's file stays is recorded, not changed: no line says it. Owner: Task 4.
4. **`coverage` named a non-shop** (a capability's name, or a decision's). Expected: a plain one-line refusal, exit 1, never a traceback or an empty answer. Owner: Task 7.
5. **A scenario part with a docstring holding `"""`, or a table cell holding `|`**, published as a feature file. Expected: the file stays parseable by the `features` script (`python3 <Scripts>/features --dir <dir>/features count`), or the problem is a Backlog line. Owner: Task 6.

---

### Task 1: Slice 60, the shop's ten types

**Review:** per-task
**Model:** opus
**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (tag `slice-60`, 12 rows):
- start-a-knowledge-base / The user starts a knowledge base and the shop's types are ready;
- use-the-shops-types / The user asks which types the shop holds;
- use-the-shops-types / Every artifact of the shop's ten types can carry an owner, a status and tags (10 rows).

**Why each is red today**
- The "types are ready" Then now lists products, shops and capabilities. Its step in `tests/test_start_a_knowledge_base.py` still matches the old seven-type text, so the new step is undefined.
- "asks which types": the Then says "ten types", and `tests/types_listed_and_read.py` defines only the seven-type Then (`THE_SEVEN`).
- The outline's product, shop and capability rows: `tests/types_common_fields.py`'s `BY_KIND` has no entry for them, and the bootstrap set has no such types.
- The decision, feature, work item, role, process, step and tag rows pass today against the old types. They must still pass once the decision and feature types are reshaped.

**Where the change lands**
- `src/shop_knowledge/types/`: new `product.yaml`, `shop.yaml` and `capability.yaml`; `decision.yaml` reshaped; `feature.yaml` replaced. Each is written as use-the-shops-types' Implementation table and field lists say:
  - the glance fields are the type's `summary`;
  - links carry kb's full `ref` shape;
  - `formulates` on a scenario has `parts: true`, and every other link has `parts: false`;
  - the required sections and fields are exactly those listed;
  - every type builds on `kb:schema/shop-artifact`.
- In this slice the types carry **no length or line-break limits**. Task 3's scenarios ask for those (slices are trimmed).
- `src/shop_knowledge/bootstrap.py`: `TYPES` holds the eleven names, the base first. The docstrings saying "seven" now say "ten".
- `shop` and `capability` link each other (`reading_order` and `shop`). Probe in scratch whether kb v0.6.0 accepts a type whose link targets a kind not yet defined, and order `TYPES` by what the probe shows. If kb refuses both orders of a cycle, log `REQUEST kb:` and stop.
- CLAUDE.md: the `bootstrap.py` row ("the base the seven build on") and the rule 5 wording, wherever they count the types.

**Decisions the lines leave open, decided**
- A decision carries no link to a shop (`decision/a-shop-names-its-decisions`). A shop's `decisions` is an optional many-link.
- `date` is a string with a `YYYY-MM-DD` pattern, and `number` is an integer with a minimum of 1. The spec says "a whole number" and "a day"; zero and negative numbers are not the shop's next.

**Needs (step data only)**
- Every existing scenario that records a decision gives it `statement`, `date` and `number` beside what it gives today. No Given, When or Then changes, and no decision gains a link it lacks today. The modules recording decisions are listed by `grep -rln '"decision"' tests/`.
- Give the shared data one home: a helper module beside `tests/driver.py`, imported plainly, never star-imported (CLAUDE.md, Step definitions). Every module that records a decision takes its required fields from there.
- Keep each `statement` free of the words any search scenario looks for (search-what-the-shop-knows), and keep every number distinct within a scenario.
- If any existing scenario's observable changes because of the reshape (a search hit, a glance's fields, a fault set, a fault count), that is a hand-back, not a step change.

**Steps to reuse:**
- `start` and `record` (`tests/driver.py`);
- the `shop`, `started_shop`, `env`, `shown` and `result` fixtures (`tests/conftest.py`);
- `BY_KIND` gains the product, shop and capability rows. A shop needs a product and a capability needs a shop, so build those through `record` first.

**Verify:**
- `.venv/bin/python -m pytest -q -m slice-60` → 12 passed.
- The whole suite → `137 passed, 16 failed`, the failing list being exactly slice 62's 16 rows.

**Checkpoint:** `plan log` one line covering: what the type-order probe showed, how many test modules gained decision fields, and any scenario that needed nothing but data. Then `plan status 60 green`.

---

### Task 2: Slice 61, publish a shop's index

**Review:** batch-end
**Model:** sonnet
**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenario** (tag `slice-61`, 1 row): publish-a-shops-spec / The user publishes a shop's spec and the directory holds its index.

**Why red:** no test module binds `publish-a-shops-spec.feature`, so it is not collected. Once a module binds it (this task), all 31 rows are red on undefined steps, and `render` offers no `spec` renderer.

**Where the change lands**
- A new renderer module, `src/shop_knowledge/renderers/spec.py`, named `spec` in `RENDERERS` (`renderers/__init__.py`). It takes `(client, name)` like every renderer and gives back a `Rendered`.
- It reads the shop whole, through `renderers/source.py`'s `whole`, and refuses a non-shop the way the other renderers refuse a type they are not made from (`source.refusal`, made from `shop`).
- It reads each capability in `reading_order` whole, for its title and gist.
- The index's layout (`spec/index.md`, as publish-a-shops-spec's Implementation gives it) is a module of its own, `renderers/spec_index.py`, so later tasks add pages beside it, not inside it. Shared helpers:
  - the title-to-file-name rule: a module of its own, `renderers/names.py`, which Task 4 extends;
  - the section layout: `renderers/sections.py`'s `laid_out` and `heading`, for the shop's own sections after Composition.
- "Pinned in <names>": names are capability file names from `names.py`, joined with commas and a final "and".
- CLAUDE.md: a module-map row per new module, and the `renderers/` row's mention of what a renderer reads ("an artifact") widened to "an artifact, and, for `spec`, the shop's other artifacts".

**Decisions open, decided**
- This task writes `spec/index.md` only. The other files arrive in their own slices.
- A capability is "of the shop" when it is in `reading_order`. Tasks 4 and 8 add the cross-check with each capability's `shop` link.

**Steps:**
- Bind the feature from a new `tests/test_publish_a_shops_spec.py`.
- The shop the scenarios share is built by a helper module of its own (for example `tests/spec_shop.py`: a product, a shop with constraints, sections and a reading order, capabilities with Behaviour and Not yet, decisions, features), imported plainly. When this feature's steps outgrow one module, the steps of one concern move to a sibling module that the test module alone star-imports (adrs/0035).
- "the knowledge base is unchanged" and its `observed` and `before` fixtures are in `tests/conftest.py`.
- The publish steps of `tests/test_publish_an_artifact.py` show how a render's directory and its `result` are read.

**Verify:**
- `.venv/bin/python -m pytest -q -m slice-61` → 1 passed.
- The whole suite → `138 passed, 46 failed`, the 30 new failures being publish-a-shops-spec's other rows.

**Checkpoint:** `plan log`, then `plan status 61 green`.

---

### Task 3: Slice 62, short fields and links into Behaviour lines

**Review:** batch-end
**Model:** sonnet
**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (tag `slice-62`, 16 rows), all in use-the-shops-types:
- the glance outline (5 rows);
- the parts glance;
- part names minted from titles;
- gist or statement over 200 characters (2 rows), and with a line break (2 rows);
- a part title over 80 characters, and with a line break;
- a scenario's `uses` pointing at anything but a capability;
- recording a feature;
- labels.

**Why red:** every step is undefined. The 200, 80 and line-break refusals also need the limits in the types.

**Where the change lands**
- `types/product.yaml`, `shop.yaml`, `capability.yaml`, `decision.yaml` and `feature.yaml` get the limits:
  - `gist` and `statement`: `maxLength: 200` and a pattern forbidding a line break;
  - every part item's `title` (behaviour, not_yet, constraints, scenarios): `maxLength: 80` and the same pattern.
  - The slice plan's log has the probe showing kb refuses both as rule `maxLength` and rule `pattern`.
- No code under `src/` beyond the types is expected. A glance already shows part titles, and part ids are minted by kb.
- New step definitions: a sibling module of `tests/test_use_the_shops_types.py` (for example `tests/types_spec_kinds.py`), star-imported by that test module alone. Building a capability, a shop and a product reuses Task 2's helper module.

**Decisions open, decided**
- "Refused because it does not fit its type": the Then compares with kb's own words for the same call (`kb_oracle.kb_answer`), never spelled out in the step (CLAUDE.md, Step definitions).
- "Each part's name is minted from its title": compare with the item id kb gives in `create`'s answer and in a whole read. Never spell the slug rule in the step.
- "As it was recorded": the glance's fields equal what the file gave, and links are left as names.

**Verify:**
- `.venv/bin/python -m pytest -q -m slice-62` → 16 passed.
- The whole suite → `154 passed, 30 failed`.

**Checkpoint:** `plan log`, then `plan status 62 green`.

---

### Task 4: Slice 63, publish a shop's capabilities

**Review:** batch-end
**Model:** sonnet
**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (tag `slice-63`, 8 rows):
- publish-a-shops-spec / … a file for each capability;
- … a capability's file is named from its title (7 rows).

**Why red:** undefined steps, and the publisher writes only the index.

**Where the change lands**
- A capability page module, `renderers/spec_capabilities.py`, laid out as publish-a-shops-spec's Implementation gives it.
  - The frontmatter is written through `kb.content` (rule 3) and comes first.
  - `formulated_as` appears only where a feature formulates the capability: this task finds features through List of kind `feature` filtered by `formulates`. Probe that List filters on a link field; if it does not, read the features and filter.
  - `Not yet` items are laid out as `- **<title>.** <defers> Promoted when <trigger>.`
- `renderers/names.py` gains the full rule of the capability-name line:
  - lower-case;
  - drop `'` and `’` wherever they appear;
  - every run of characters other than a to z and 0 to 9 becomes one `-`;
  - strip `-` from both ends.
- `renderers/spec.py` adds each capability's page to the `Rendered` files.

**Decisions open, decided**
- Lower-casing follows Python's `str.lower`. A character that lower-cases into a to z (the Kelvin sign) is then kept as that letter. No line says otherwise, and the formulator listed it as an unmentioned case.

**Verify:**
- `.venv/bin/python -m pytest -q -m slice-63` → 8 passed.
- The whole suite → `162 passed, 22 failed`.

**Checkpoint:** `plan log` (including Review Focus 1 and 3), then `plan status 63 green`.

---

### Task 5: Slice 64, publish a shop's decisions

**Review:** batch-end
**Model:** sonnet
**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (tag `slice-64`, 8 rows):
- the ledger;
- a record for each decision;
- a decision's record named from its number and title (4 rows);
- every ledger entry is a decision the knowledge base holds;
- a decision of another shop.

**Why red:** undefined steps; no ledger or record pages yet.

**Where the change lands**
- A ledger-and-records module, `renderers/spec_decisions.py`. It lays out `spec/decisions.md` and `adrs/<number>-<name>.md` as publish-a-shops-spec's Implementation gives them:
  - number padding: `str(n).zfill(4)`-like, written in full where longer;
  - `Supersedes` and `Extends` padded the same way.
- The shop's own decisions are those its `decisions` names, in number order.
- Decisions of other shops are those its capabilities' `rests_on` name that the shop does not. Each one's shop is the shop whose `decisions` names it. Find it with Follow (IN, via `decisions`, kind `shop`) on the decision, and order by that shop's name, then number.
- `renderers/names.py` gives the decision file name.

**Decisions open, decided**
- A ledger entry's `supersedes:` names the superseded decision by its kb name.
- A decision a capability rests on that no shop names is refused in Task 8. This task does not handle it.

**Verify:**
- `.venv/bin/python -m pytest -q -m slice-64` → 8 passed.
- The whole suite → `170 passed, 14 failed`.

**Checkpoint:** `plan log` (including Review Focus 2), then `plan status 64 green`.

---

### Task 6: Slice 65, publish a shop's feature files

**Review:** batch-end
**Model:** sonnet
**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenario** (tag `slice-65`, 1 row): … a feature file for each formulated capability.

**Why red:** undefined steps; no Gherkin layout.

**Where the change lands**
- A Gherkin layout module, `renderers/gherkin.py`, laying out a feature from its fields and `scenarios` parts as publish-a-shops-spec's Implementation gives it:
  - two-space indentation;
  - labels on one line above the scenario;
  - `Scenario Outline:` where the scenario has `examples`;
  - a table's columns padded to the widest cell, with `| ` and ` |`;
  - a docstring between `"""` lines.
- A feature file is named from its capability's file name.

**Decisions open, decided**
- The scenario's `formulates` and `uses` are not written into the file. No line asks for them, and Gherkin has no place for them.
- The Then compares the published file with what the shop's own `features` script parses: the scenario count and the titles. It never compares bytes with a hand-written expectation.

**Verify:**
- `.venv/bin/python -m pytest -q -m slice-65` → 1 passed.
- The whole suite → `171 passed, 13 failed`.

**Checkpoint:** `plan log` (including Review Focus 5), then `plan status 65 green`.

---

### Task 7: Slice 66, see what is formulated

**Review:** batch-end
**Model:** sonnet
**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (tag `slice-66`, 5 rows): all of see-what-is-formulated.

**Why red:** no test module binds the feature, and there is no `coverage` command.

**Where the change lands**
- `arguments.py`: a `coverage` command taking one shop name, which may not be given empty (`_named`).
- `cli.py`: a `_coverage` handler, which shows the answer as YAML.
- A new module, `src/shop_knowledge/coverage.py`, with a row in CLAUDE.md's module map. It reads, through the client it is given:
  - the shop (kb's refusal of a name it does not hold is passed through, raised as `refusal.Refused`, so "refused because that shop is not there, naming it" is kb's own fault);
  - the capabilities in its reading order, and each one's Behaviour items;
  - the features formulating them.
- It answers `{unformulated: [...], formulated_twice: [...]}`. Each entry is the line's link `capability/<name>#behaviour/<line>` with its capability's title and the line's title. An empty list is an empty value (adrs/0045).

**Decisions open, decided**
- A scenario outline counts once, whatever its Examples rows.
- A scenario of another shop's feature formulating this shop's line counts. "More than one scenario formulates" names no shop.
- Lines come in reading order, then the capability's own order.

**Steps:** bind the feature from a new `tests/test_see_what_is_formulated.py`, reusing Task 2's shop-building helper module.

**Verify:**
- `.venv/bin/python -m pytest -q -m slice-66` → 5 passed.
- The whole suite → `176 passed, 13 failed`.

**Checkpoint:** `plan log` (including Review Focus 4), then `plan status 66 green`.

---

### Task 8: Slice 67, the published-from line and publishing refusals

**Review:** batch-end
**Model:** sonnet
**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (tag `slice-67`, 13 rows):
- the published-from outline (5 rows);
- the eight refusals: not in reading order; in reading order but naming another shop; two capabilities on one file name; two decisions on one file name; two decisions on one number; a decision no shop names; two features on one capability; `uses` into its own shop.

**Why red:** undefined steps; no published-from line; no consistency checks.

**Where the change lands**
- **The published-from line**, added by each page module:
  - an HTML comment in markdown, a `#` comment in a feature file;
  - it names the shop and the shop's revision in `spec/index.md` and `spec/decisions.md`, and the artifact and its revision elsewhere;
  - it comes directly after the frontmatter in a capability page, and first elsewhere (before `# formulated from` in a feature file);
  - wording: `published from the knowledge base: <name>@<revision>; do not edit by hand`.
- **The consistency checks**, in a module of their own, `renderers/spec_faults.py`:
  - each check gives `kb_pb2.Fault`s in plain words, naming what is at fault (`artifact` set);
  - `spec.py` gives back `refused(faults)` when there are any, so nothing is written (rule 6), and `cli._render` refuses them as today;
  - "A capability names the shop": List of kind `capability` filtered by `shop`, compared with `reading_order`.
- Every refusal is shop-knol's own, worded in plain words (index: "shop-knol's own refusals are in plain words"). Each Then checks the reason and the names, never the whole message.

**Decisions open, decided**
- Every fault found is given at once, as kb gives every fault at once. No line asks for the first only.
- Two decisions sharing one file name always share a number too. Both faults are given.

**Verify:**
- `.venv/bin/python -m pytest -q -m slice-67` → 13 passed.
- The whole suite → `189 passed, 0 failed`.

**Checkpoint:** `plan log`, then `plan status 67 green`.
