# shop-knowledge batch 9: slices 50.5 to 50.9

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, in slice order. The capability tasks (2, 3 and 4) are built under shopsystem-bdd:bdd-red-green, one scenario at a time. Its stop conditions, hand-back and checkpoint apply, and they override any step here that conflicts with them.

**Goal:** The behaviour commit 1133296 added to the feature files, settled by the spec and adrs/0037, 0038 and 0039, in plan order:
- the publish feature's markdown steps move to a module of their own before they grow (50.5, enabling);
- markdown lays out each kind of value as markdown (50.6);
- an agent the harness would reject is not published (50.7);
- the knowledge base starts where the user works, and elsewhere only when they name the place (50.8);
- the sixth architecture review (50.9, enabling).

**Architecture:** shop-knowledge is the Python package `shop_knowledge`, and its `shop-knol` command is a client of kb v0.2.1. Its scenarios are driven by pytest-bdd 8.1 step definitions under `tests/`: one `test_<feature>.py` per feature file, with sibling modules a test module star-imports (adrs/0035), the shared steps and fixtures in `tests/conftest.py`, and the one way of driving shop-knol in `tests/driver.py`. Across the batch the code changes in three places:
- the markdown renderer (`src/shop_knowledge/renderers/markdown.py`);
- the agent renderer and the harness's limits (`renderers/agent.py`, `renderers/limits.py`);
- the `init` argument (`arguments.py`).

**This plan carries no code** (adrs/0011). The implementer writes every change in the execution session. What each task gives instead:
- the slice and its scenarios or check;
- the observable and the unknown it settles;
- why each scenario or check is red today, found by running it in this checkout;
- where the change lands by CLAUDE.md's module map, and the rule it implements once;
- the decisions the spec leaves open, each resting on a passage;
- what existing steps and fixtures to reuse, by name;
- the commands, with counts from the tags;
- the checkpoint to log.

**Tech Stack:** Python 3.11, pytest 8 + pytest-bdd 8.1, kb v0.2.1 (`kb.content` for YAML, `kb.contract.kb_pb2` for faults).

**Spec:** `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md`, its command table's `shop-knol init [<root>]` row and its Renderers section. Read CLAUDE.md alongside it, and in the slice plan slices 50.5 to 50.9 and the 2026-09-27 log entry that cut them. The decisions this plan rests on are adrs/0035, 0037, 0038, 0040, 0041 and 0042.

## Global Constraints

- Feature files are read-only, tag lines included. The tags `@slice-50.6`, `@slice-50.7` and `@slice-50.8` are already written. Any diff under `features/` is a stop condition.
- kb is v0.2.1 in `.venv` and is never edited here (CLAUDE.md, rule 2).
- Every rule in CLAUDE.md holds at the end of every task. No module under `src/` or `tests/` goes past 250 lines (adrs/0034).
- Work on `main` in this checkout (adrs/0009). Run every command from the checkout's root. While scenarios are red, `make test`'s last line is make's own error, so read pytest's summary above it.
- Scratch files and probes go under `.superpowers/batch9/`, which `.git/info/exclude` covers (it excludes `.superpowers/`). Never under `/tmp`.
- Commits: `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`. The message ends with the Co-Authored-By line of the model that made the commit. Each task makes one commit, holding the slice's change and its checkpoint. When the batch is done, push: `git push origin main` (adrs/0036).
- pytest-bdd prints `PytestRemovedIn10Warning`s, two for each `target_fixture` step. That is the baseline, not a fault.
- **Counts.** The suite collects 66 scenarios (`.venv/bin/python -m pytest --collect-only -q | grep -c ::`, run 2026-09-27). What the tags select:
  - `-m slice-50.6` selects 2, both rows of the markdown outline;
  - `-m slice-50.7` selects 1;
  - `-m slice-50.8` selects 1;
  - `-m "slice-4 or slice-47 or slice-50.8"` selects 7, the named-place scenario and the six rewritten start scenarios, which keep their tags;
  - `-m slice-20` selects 1, `-m slice-50` 1, `-m slice-18` 1.

  The test modules collect as follows: `tests/test_publish_what_the_shop_knows.py` 8, `tests/test_start_a_shop_knowledge_base.py` 9.

  | after | failed | passed |
  |---|---|---|
  | before Task 1 (run 2026-09-27) | 10 | 56 |
  | 50.5 | 10 | 56 |
  | 50.6 | 8 | 58 |
  | 50.7 | 7 | 59 |
  | 50.8 | 0 | 66 |
  | 50.9 | 0 | 66 |

  Every one of the ten fails today on `StepDefinitionNotFoundError`, none on an assertion. So each is seen red on its own assertion only once its steps exist, and the checkpoint says so.
- **The size check**, run at the start and end of every task: `find src tests -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'`. Today it lists nothing. `tests/test_publish_what_the_shop_knows.py` is 193 lines, `tests/test_start_a_shop_knowledge_base.py` 182, `src/shop_knowledge/cli.py` 233, `renderers/markdown.py` 45.

## Review Focus

writing-plans asks for a test in the owning task for each line here. In this project tests are scenarios, and feature files are the human gate, so no test is added. Each line goes into the owning task's checkpoint instead: a failure mode as a thing checked, or a behaviour as a `QUESTION FOR THE SPEC` with its reproduction.

1. **A `|` in a value breaks a markdown table** (owner: Task 2). adrs/0041 joins a value's lines inside a cell, but says nothing of a pipe. No scenario holds one. Reproduction, after Task 2: add a step whose `does` is `Count a | b.` to a process in a throwaway store under `.superpowers/batch9/`, then `render markdown` it. The row gains a cell. A person would expect the pipe shown as written. QUESTION FOR THE SPEC, unless the layout escapes it as `\|`, which is markdown and not behaviour of its own. Log which it is.
2. **Other types' lists of mappings** (owner: Task 2). The scenarios cover a process's steps and a role's tags. After Task 2, render as markdown in a throwaway store:
   - a feature, whose `scenarios` are a list of mappings;
   - a decision with an empty `tags` list.

   Check that the first is a table, and that the second holds no repr, `[]` included. An empty list laid out as its field's name with nothing under it is a QUESTION FOR THE SPEC. Log what it shows.
3. **An agent whose name breaks only one limit** (owner: Task 3). The scenario's role breaks both published limits. After Task 3, render a role named `-steward` and one named `shop:steward`. Each gives exactly its one fault line and writes nothing. The slice 50 role, `stock-keeper`, still publishes: `-m slice-50` passes.
4. **`init` with `KB_ROOT` naming another directory** (owner: Task 4). adrs/0042 says init never reads `KB_ROOT`. From an empty directory under `.superpowers/batch9/`, run `KB_ACTOR=a KB_ROOT=<another empty directory> shop-knol init`. It starts `kb/` in the working directory and leaves the other directory empty. Log what it does.
5. **`init ""` still starts in the working directory** (owner: Task 4, carried from the slice 50.2 review). Now that the argument is optional, `KB_ACTOR=a shop-knol init ""` from an empty directory still exits 0 and makes `kb/` there, since `""` is typed as the path `.`. It stays a QUESTION FOR THE SPEC with this reproduction, rerun after Task 4.

---

### Task 1: Slice 50.5, the publish feature's markdown steps sit apart from its other steps

**Slice plan entry:** enabling, no unknown. Check:
- `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` gives the same ten failing scenarios as before the slice, and the summary gives `56 passed, 10 failed`;
- `.venv/bin/python -m pytest --collect-only -q tests/test_publish_what_the_shop_knows.py | grep -c ::` gives `8`;
- the size check lists nothing;
- `grep -l "import \*" tests/*.py` lists exactly three modules: `tests/test_publish_what_the_shop_knows.py`, `tests/test_read_back_what_the_shop_knows.py` and `tests/test_start_a_shop_knowledge_base.py`;
- no new module under `tests/` is named `test_*`;
- `git diff --stat -- src features` is empty.

**Observable:** a reader finds the publish feature's markdown steps in a module of their own beside its test module. The markdown and agent steps that Tasks 2 and 3 add then keep every module under 250 lines.

**Why the check fails today** (run 2026-09-27):
- `grep -l "import \*" tests/*.py` lists two modules, not three.
- The publish test module is 193 lines. Tasks 2 and 3 add about 60 to it: two Givens and three Thens for markdown, one Given, a fixture and a Then for the agent. That crosses 250, and CLAUDE.md says "When a change would cross the limit, split first".

**Where it lands:**
- A new module beside `tests/test_publish_what_the_shop_knows.py`, `tests/publish_as_markdown.py`. It holds the markdown When `_publish_as_markdown` and the Then `_a_page`, today's lines 148 to 173.
- The test module star-imports it, with the comment the other two star imports carry.
- Rule implemented once: CLAUDE.md's "No module over 250 lines… split first", as adrs/0035 splits a feature's steps.

**Decisions:**
1. **The concern is markdown.** It is the concern Task 2 grows. The agent's steps stay in the test module with the skill's, since they share `_heading_block_and_body` and `ROLE`.
2. **No constant is copied, and the sibling never imports its test module** (adrs/0035, circular import). The moved steps use only fixtures by name, `env`, `target` and `result`, which pytest resolves wherever the step is defined. So the sibling imports only `knol` from the driver and pytest-bdd's decorators.
3. **The sibling's docstring** names the feature it serves and says it holds the markdown scenarios' steps, as `tests/start_roles_and_tags.py` does.

**Reuse:** `tests/read_back_from_elsewhere.py` and `tests/start_roles_and_tags.py` as the pattern.

- [ ] **Step 1: Baseline.** Run `mkdir -p .superpowers/batch9; .venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch9/failing-50.5.txt; wc -l < .superpowers/batch9/failing-50.5.txt`. It gives `10`. The size check lists nothing.
- [ ] **Step 2: Move** the two steps and add the star import. Then run `.venv/bin/python -m pytest -q -m slice-20`, which gives `1 passed`. Comment out the star import for one run: slice 20 fails on `StepDefinitionNotFound`. Then restore it.
- [ ] **Step 3: Check.** Run each command of the slice's check. The failing list diffs empty against `.superpowers/batch9/failing-50.5.txt`.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 50.5 green.`, then:
  - `Check:` with each output, and both modules' line counts after;
  - `Surprised by:`;
  - `Next: slice 50.6.`

  Set slice 50.5's Status to `green`.

---

### Task 2: Slice 50.6, markdown lays out each kind of value as markdown

**Slice plan entry:** capability. Scenario: publish-what-the-shop-knows / Markdown lays out each kind of value as markdown, both rows (`@slice-50.6`, 2 scenarios).

**Observable:**
- A user publishes a process as markdown and finds its steps as a table with a column for each thing a step says.
- A user publishes a role with tags and finds its tags as a bullet list.
- No value on either page is written the way a program prints it.

**Unknown:** whether every value kb's content model holds can be laid out as markdown from the content alone, with no schema read and no type named. That includes a part collection, and the lists and mappings inside its items.

**Why it is red today** (run 2026-09-27): both rows fail on `StepDefinitionNotFoundError`, on "Given the process holds steps that each say more than one thing" and "Given the role holds more than one tag". Behind the missing steps, a probe in a throwaway store showed what the renderer does:
- `render markdown` of the Background's process gives one field line, `- **steps**: {'id': 'check-it', 'title': 'Check it', 'uses': ..., 'with': [{'name': 'shelf', 'value': 'dairy'}]}, {...}`. That is Python reprs joined with commas. The steps come back from kb's whole read as the content's `steps` list, each item with the `id` kb minted.
- `render markdown` of a role with two tags gives `- **tags**: tag/stock, tag/dairy`.

The cause is `markdown._value`, which joins a list's items with `str()` and prints anything else with `str()`.

**Where it lands:**
- `src/shop_knowledge/renderers/markdown.py` alone, whose row in the module map is the page. The layout of values is the markdown renderer's own, so nothing moves to `renderers/sections.py`, which is the prose layout shared with the agent. The module stays well under 250 lines. Each layout (the field list, the table, the inline value) is a function of its own at one level (CLAUDE.md, Size and shape).
- The steps go in `tests/publish_as_markdown.py`, from Task 1.
- Rule implemented once: CLAUDE.md rule 5, types are data. The layout reads the content's shape (mapping, list of mappings, list of plain values, plain value) and never a field's name. adrs/0038 says no repr is ever shown.

**Decisions** (adrs/0041, filling in the spec's Renderers passage "Every value is laid out as markdown: a list of mappings is a table with one column per key, a list of scalars is a bullet list, a mapping is a nested definition list"):
1. **A list of plain values** is the field's bold name as a list item, then one bullet a value nested one level in, as a mapping's fields nest today.
2. **A list of mappings among the page's fields** comes out of the field list. It is laid out after the list and before the sections, in the order kb gives the fields:
   - the field's name in bold on a line of its own, a blank line, then a table;
   - one column per key, in the order the keys first appear across the items; the header names the keys as kb gives them, over a `---` separator row;
   - one row an item, with an empty cell where an item lacks the key.

   For the Background's process that is the columns `id`, `title`, `uses`, `with`, `does`, `branches`, and four rows. Its field list is empty, so the page is the heading, then the steps table.
3. **Inline, where a block cannot sit.** That is a table cell, or a list of mappings inside a field group. A plain value's lines are joined by a space, with its trailing newline dropped. A mapping is its `key: value` pairs joined by `, `, and a list's items are joined by `; `, each laid out inline in turn. So `with` shows `name: shelf, value: dairy`. `branches` shows `when: the shelf is short, go_to: order-more; when: it is not, go_to: stop`.
4. **A mapping** keeps today's layout: its bold name, then its fields nested. That is the spec's "nested definition list", as slice 20 accepted it.
5. **Slice 20's Then changes its expected page, not its line.** `_a_page` expects the role's `tools` as `  - **tools**` with `    - Read` under it, the bullet list of Decision 1, where today it expects `  - **tools**: Read`. Its docstring's "a list of plain values joined" becomes "a list of plain values as a bullet list". The Then line in the feature file ("the fields as a list…") does not change. adrs/0038 decides the layout, so this is the renderer meeting the spec. It is not a scenario changing meaning. Slice 20 goes red when Decision 1 lands and green when its expectation follows. Log both runs.
6. **The steps of the outline:**
   - One parsed When, "the user publishes the {thing} as markdown into a directory", replaces today's literal role When, so no two steps match one line. It publishes the Background's process by the `process_name` fixture, and the role as `role/stock-keeper`, as today.
   - "Given the process holds steps that each say more than one thing" changes nothing. It reads the Background's process whole and asserts that every step holds more than one thing.
   - "Given the role holds more than one tag" records two tags through the driver. Then it replaces the Background role's content through `shop-knol write`, as a user does. The new content is `ROLE` without its title, plus the two tags' names under `tags`. A whole write replaces the content, and `title` is not content (compare `test_revise_what_the_shop_knows.py`'s `_replace_the_decision`).
   - The two Thens are literal, one per row: "that directory holds a page showing its steps as a table with one column for each thing a step says" and "that directory holds a page showing its tags as a bullet list". Each asserts the command succeeded, that the one file under the directory is the page (`restock-a-shelf.md`, `stock-keeper.md`), and the exact lines of the table, or of the tags field and its bullets.
   - "And nothing on the page is a programming language's representation of a value" reads the one page in the directory. It asserts that none of `{'`, `['`, `'}`, `']`, `{"`, `["` appears on it.

   The Thens and the Given read `ROLE` and `process_name` from the test module by fixture where they can. `ROLE` itself is a constant of the test module, and the sibling cannot import it (Task 1, Decision 2). So the tag Given asks for the role's content through a fixture the test module gives, `role_content`, returning `ROLE`. The alternative, moving `ROLE` to the sibling, would make the test module depend on the star import for its own Background.

**Reuse:**
- `tests/driver.py`: `knol`, `record`, `whole`.
- The test module: the Background Given (`process_name`), and the fixtures `target` and `result`.
- `tests/conftest.py`: `shown` is not needed, since each Then reads the file.

- [ ] **Step 1: Baseline.** Run `.venv/bin/python -m pytest -q -m slice-50.6`. It gives `2 failed`, on `StepDefinitionNotFoundError`. The size check lists nothing.
- [ ] **Step 2: Red, the process row.** Write its Given, the parsed When and its two Thens. Run `.venv/bin/python -m pytest -q -m slice-50.6 -k process`. It fails on an assertion: the table is missing, and the repr Then fails on `{'`. Log the first failing line. Run `-m slice-20` too, which still gives `1 passed` through the parsed When.
- [ ] **Step 3: Green, the process row.** Lay out a list of mappings as a table and a value inline in a cell. The process row passes, and `-m slice-20` still passes.
- [ ] **Step 4: Red, the role row.** Write its Given and Then. It fails on the tags line, `- **tags**: tag/…, tag/…`.
- [ ] **Step 5: Green, the role row, and slice 20.** Lay out a list of plain values as bullets. `-m slice-20` goes red on `tools`. Log that run, then change `_a_page`'s expectation as Decision 5 says.
- [ ] **Step 6: Check.**
  - `.venv/bin/python -m pytest -q -m slice-50.6` gives `2 passed`;
  - `-m "slice-20 or slice-17 or slice-18 or slice-19 or slice-50"` gives `5 passed`;
  - `.venv/bin/python -m pytest -q` gives `58 passed, 8 failed`, and the eight are the start scenarios and the agent;
  - the size check lists nothing;
  - `git diff --stat -- features` is empty.
- [ ] **Step 7: Review Focus 1 and 2.** Run the probes in a throwaway store under `.superpowers/batch9/`, and log what each shows.
- [ ] **Step 8: Checkpoint and commit.** Log `- 2026-09-27 slice 50.6 green.`, then:
  - `Check:` with each output and `markdown.py`'s line count;
  - `Seen red:` each Then, and slice 20's run;
  - `Surprised by:`;
  - `Settled:` the unknown, in one sentence;
  - `Open questions:` from Review Focus 1 and 2;
  - `Next: slice 50.7.`

  Set slice 50.6's Status to `green`.

---

### Task 3: Slice 50.7, an agent the harness would reject is not published

**Slice plan entry:** capability. Scenario: publish-what-the-shop-knows / An agent the harness would reject is not published (`@slice-50.7`, 1 scenario).

**Observable:** a user publishing a role whose harness name the harness would not load is told which limit it breaks, and finds nothing written.

**Unknown:** whether the agent renderer can hold a role's harness fields to the limits the harness publishes for an agent, before anything is written, the way the skill renderer holds a process's body to its limit.

**Why it is red today** (run 2026-09-27):
- It fails on `StepDefinitionNotFoundError`, on "Given a role whose harness fields run past the limits the harness publishes".
- Behind it, a probe: a role with `harness.name: shop:steward`, published with `render agent`, exits 0 and writes `.claude/agents/shop-steward.md`. `renderers/agent.py` checks nothing, and `renderers/limits.py` holds only `skill`.

**Which limits** (spike, 2026-09-27, logged in the slice plan). The harness's subagent documentation, code.claude.com/docs/en/sub-agents, publishes two limits an agent file can break through a role's harness fields:
- its `name` may not contain `:`, which is reserved for plugin-scoped names, and the harness does not load such a file;
- its `name` may not start with `-`.

It publishes no length limit on the name, the description or the body. The 1500-character description and `Stock Keeper!` in the slice 50.2 reproduction break no published limit.

**Where it lands:**
- `src/shop_knowledge/renderers/limits.py`: the agent's limits, beside the skill's, with where they were published in the module's docstring (its module map row).
- `src/shop_knowledge/renderers/agent.py`: it checks the role's harness fields before it builds the file, and gives back the faults refused, as `skill._skill` does.
- `cli._render` refuses them through `_answered`, unchanged.
- The steps go in `tests/test_publish_what_the_shop_knows.py`.
- Rules implemented once: CLAUDE.md rule 6 (a renderer writes nothing; the command writes only when nothing was refused) and rule 4 (the refusal is a `Fault` printed by the one printer, one line each, exit 1).

**Decisions** (adrs/0040, resting on the spec's "`skill` and `agent` validate their output against the limits the harness publishes and fail rather than emit something it would reject"):
1. **Both published limits are checked, one fault each**, in the order the documentation gives them: the `:` first, then the leading `-`.
2. **Each fault:** `artifact` is the role's name, `path` is `harness.name`, `rule` is `harness-limit`. The messages are:
   - `an agent's name holds no ":", the limit the harness publishes; this one is <name>`;
   - `an agent's name does not start with "-", the limit the harness publishes; this one is <name>`.

   The wording follows the skill's.
3. **The scenario's role breaks both**, so the one scenario asks for both limits. It is recorded in the Given (the Background has started the shop) with the title `Shop steward`, so its name is `role/shop-steward`. Its `harness.name` is `-shop:steward`, its description `Keeps the shop.`, and its `shop.responsible_for` `The shop`. The Then asserts stderr is exactly these two lines and the exit is not 0:
   - `role/shop-steward at harness.name: an agent's name holds no ":", the limit the harness publishes; this one is -shop:steward`
   - `role/shop-steward at harness.name: an agent's name does not start with "-", the limit the harness publishes; this one is -shop:steward`
4. **Which role the When publishes.** Today's `_publish_as_an_agent` names `role/stock-keeper` itself. It takes a fixture, `role_name`, instead. The test module gives it as `role/stock-keeper`, and this scenario's Given overrides it with `target_fixture="role_name"`, as `start_in` is overridden in the start feature. Slice 50's scenario keeps passing unchanged.
5. **The limits are checked on the role's harness group as kb gives it**, before the heading block is written. No length is checked, since none is published.

**Reuse:**
- The test module: `target`, `_publish_as_an_agent` (made to take `role_name`), and the Then "nothing is written to the directory" (`_nothing_written`).
- `tests/driver.py`: `record`.
- `_rejected_for_the_limits` is the pattern for the new Then.

- [ ] **Step 1: Baseline.** Run `.venv/bin/python -m pytest -q -m slice-50.7`. It gives `1 failed`, on `StepDefinitionNotFoundError`. `-m slice-50` gives `1 passed`.
- [ ] **Step 2: Red.** Write the Given, the fixture and the Then. The scenario fails on the Then: exit 0, and the agent file written.
- [ ] **Step 3: Green.** Add the agent's limits and the check. `-m slice-50.7` and `-m slice-50` each pass.
- [ ] **Step 4: Check.**
  - `.venv/bin/python -m pytest -q -m "slice-50.7 or slice-50 or slice-18"` gives `3 passed`;
  - `.venv/bin/python -m pytest -q` gives `59 passed, 7 failed`, and the seven are the start scenarios;
  - the size check lists nothing;
  - `git diff --stat -- features` is empty.
- [ ] **Step 5: Review Focus 3.** Run the probes, and log them.
- [ ] **Step 6: Checkpoint and commit.** Log `- 2026-09-27 slice 50.7 green.`, then:
  - `Check:`;
  - `Seen red:`;
  - `Surprised by:`;
  - `Settled:`. This answers the QUESTION FOR THE SPEC logged at slice 50.2 about the agent's limits; say so;
  - `Next: slice 50.8.`

  Set slice 50.7's Status to `green`.

---

### Task 4: Slice 50.8, the shop's knowledge base starts where the user works, and elsewhere only when they name the place

**Slice plan entry:** capability. Scenarios: start-a-shop-knowledge-base / The user starts a knowledge base somewhere else on purpose by naming the place (`@slice-50.8`). With it go the six start scenarios rewritten in commit 1133296, which keep their tags: one under `@slice-4` and five under `@slice-47`. `-m "slice-4 or slice-47 or slice-50.8"` selects 7.

**Observable:** a user starts the shop's knowledge base from the directory they work in without naming one. They are refused there as before where one exists or where they are inside one. They start one elsewhere only by naming the place.

**Unknown:** whether a knowledge base started from the working directory, with no directory named, is made and refused just as one started by naming it.

**Why it is red today** (run 2026-09-27):
- All seven fail on `StepDefinitionNotFoundError`, on the Givens that now begin "the user is working in…".
- Behind them, probes in a throwaway store:
  - `KB_ACTOR=shopkeeper shop-knol init` with no directory is refused by argparse, `shop-knol init: the following arguments are required: root`, since `arguments.py` declares `root` positional and required;
  - `init .` starts one;
  - `init .` again is refused `a store is never started over another; '.' already has a store inside it`;
  - `init .` from inside `kb/schema` is refused `stores do not nest; '.' is inside the store at …`.

  So kb makes and refuses a store from a relative root as it does from a named one. The unknown is narrowed to the default and the refusals' wording.

**Where it lands:**
- `src/shop_knowledge/arguments.py`, the one place an argument's meaning is declared (adrs/0032). `root` becomes optional and defaults to the working directory. The help says `<root>` is the working directory unless one is named.
- `kb_requests.init_request` and `cli._init` do not change. They already send and connect to `args.root`.
- `tests/test_start_a_shop_knowledge_base.py`: the steps.
- `tests/driver.py`: `start`.
- Rule implemented once: adrs/0032, an argument's meaning said where it is declared, and CLAUDE.md's Step definitions, "drive shop-knol the way a user does".

**Decisions** (adrs/0037 and 0042, resting on the spec's command table, "`<root>` defaults to the working directory, since the shop's knowledge sits beside the shop's work; the argument exists only to start a knowledge base somewhere else on purpose"):
1. **The default is the working directory as an absolute path**, taken when the command line is parsed. kb's refusals then name the directory the user is in, not `.`. The Thens only look for `already has a store` and `stores do not nest`, so this is not asserted. Log the refusal lines seen.
2. **init never reads `KB_ROOT`.** `KB_ROOT` finds a store that exists, and init makes one (adrs/0042). Nothing changes in `_client`.
3. **The suite starts a knowledge base the way the user now does.** `driver.start` runs `init` from the shop's directory without naming it (adrs/0037, "Tests set the working directory rather than passing one"). Its signature stays, since some twenty Givens call it. `test_review_who_changed_what.py`'s founder start names the shop, which still works. `_started_and_noted` goes through `start`, so it now starts from the shop's directory too. Only the named-place When names a directory on purpose.
4. **The Givens:**
   - "the user is working in an empty directory for the shop's knowledge" asserts the shop's directory is empty, as `_an_empty_directory` does.
   - "…holding work of the shop's that is not its knowledge" writes the shop's work, as `_a_directory_with_work` does, and gives `shops_work`.
   - "…that already holds the shop's knowledge" starts one and notes the journal, `_started_and_noted`.
   - "…that sits inside the shop's knowledge" does the same and gives `start_in` as `kb/schema`, as today.
   - "the user is working in one directory, and another directory is empty" makes `tmp_path / "elsewhere"` and gives it as `elsewhere`. The user works in the shop's directory.

   The Givens and Whens the feature no longer uses (every step text without "the user is working in" or "without naming a directory") are renamed to the new texts, not kept beside them. `grep -c "in that directory" tests/test_start_a_shop_knowledge_base.py` gives 0 afterwards.
5. **The Whens run `init` from the directory worked in, naming none:** `knol(env, "init", cwd=start_in)` through the module's `_init`, which now takes the directory as the working directory. That holds for "…there without naming a directory, saying who they are", "…saying who they are and giving no reason", and "…there without naming a directory" (no role). "the user starts a shop knowledge base in the other directory by naming it, saying who they are" runs `init <elsewhere>` from the shop's directory. The env keeps `KB_ROOT`, since the Thens' `journal` and `record` need it.
6. **The new Thens:**
   - "the shop's knowledge is kept in a place of its own inside the named directory" asserts that `elsewhere` holds `kb/` alone and that `elsewhere/kb/store.yaml` is a file, reading the directory as `_kept_in_its_own_place` does, with its comment.
   - "the directory they are working in holds no knowledge base" asserts the shop's directory has no `kb/`, as `_holds_none` does.

**Reuse:**
- The test module: `_init`, `start_in`, `known_before`, `_started_and_noted`, `shops_work`, and every Then of slices 4 and 47, unchanged.
- `tests/driver.py`: `knol` (its `cwd`) and `start`.
- `tests/conftest.py`: `shop`, `env`, and the Thens "the command reports failure to whatever ran it" and "the user has not said which role they are".

- [ ] **Step 1: Baseline.** Run `.venv/bin/python -m pytest -q -m "slice-4 or slice-47 or slice-50.8"`. It gives `7 failed`, each on `StepDefinitionNotFoundError`.
- [ ] **Step 2: Red.** Rename the Givens and Whens and write the new ones. With `init`'s root still required, the six start scenarios that run init with no directory fail on the argparse refusal. The one refused for no role fails too, since argparse speaks first. The named-place scenario passes: naming a directory already works. Log which fail and on what. The named-place scenario is not seen red on the code. Its Thens are seen red by breaking each assertion for one run.
- [ ] **Step 3: Green.** Make `root` optional with the default of Decision 1. The seven pass.
- [ ] **Step 4: The driver.** Change `driver.start` as Decision 3 says. The whole suite still passes.
- [ ] **Step 5: Check.**
  - `.venv/bin/python -m pytest -q -m "slice-4 or slice-47 or slice-50.8"` gives `7 passed`;
  - `.venv/bin/python -m pytest -q` gives `66 passed`, and `make test` ends cleanly;
  - `.venv/bin/python -m shop_knowledge init -h` shows `root` as optional;
  - the size check lists nothing;
  - `git diff --stat -- features` is empty.
- [ ] **Step 6: Review Focus 4 and 5.** Run the probes, and log them.
- [ ] **Step 7: Checkpoint and commit.** Log `- 2026-09-27 slice 50.8 green.`, then:
  - `Check:`;
  - `Seen red:`;
  - `Surprised by:`;
  - `Settled:`;
  - `Open questions:` Review Focus 5 with its reproduction;
  - `Next: slice 50.9.`

  Set slice 50.8's Status to `green`.

---

### Task 5: Slice 50.9, sixth architecture review

**Slice plan entry:** enabling, no unknown. Check: an Opus review of the code and the step definitions against CLAUDE.md is in the slice plan's log, after the six slices implemented since slice 50.2 (50.3 to 50.8), and every refactor it calls for is a slice of its own with a check.

**Observable:** anyone can read whether the markdown layout, the agent's limits and the init default kept the code in the shape CLAUDE.md sets.

**Why the check fails today:** no such entry is in the log. The last review is slice 50.2's.

**Where it lands:** the slice plan's log, and new enabling slices numbered after 50.9 if any refactor is called for. Nothing under `src/`, `tests/` or `features/`.

**Decisions** (adrs/0010):
1. **What the review reads:**
   - CLAUDE.md;
   - the module map against `src/`, the new layout in `renderers/markdown.py` and the agent's limits in `renderers/limits.py` among them;
   - the three rules this batch touched: rule 4, one way to refuse, for the agent's faults; rule 5, types are data, for the markdown layout; rule 6, renderers only read;
   - the size limit;
   - the step definitions' rules, the new sibling `tests/publish_as_markdown.py` and the start steps' working directory among them.
2. **Every finding is placed.** A finding that breaks a rule becomes a refactor slice with a measurable check. One that no rule settles is logged as not called for, or as a QUESTION FOR THE SPEC.
3. **The review runs on the most capable model**, as slices 19.1, 30.1, 42.1 and 50.2 did, and it writes nothing but the log.

- [ ] **Step 1: Review.** Dispatch the review with CLAUDE.md, the diff since slice 50.2's commit, and the questions above. Read it, and verify each finding against the code before logging it.
- [ ] **Step 2: Log.** Add `- 2026-09-27 slice 50.9 review.` with `Met:`, `Not met:`, the refactors cut, `Not called for:`, and the questions still open.
- [ ] **Step 3: Cut** each refactor as a slice numbered after 50.9, with its check. Commit, then push: `git push origin main`.

  Set slice 50.9's Status to `green`.

---

## After the batch

Every slice in the plan is green unless the review cut more. What remains:
- the QUESTION FOR THE SPEC lines in the slice plan's log, for formulating-features and the human, among them `init ""` and whatever Review Focus 1 and 2 turn up;
- the refactor slices the sixth review cuts, if any.
