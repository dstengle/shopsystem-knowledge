# shop-knowledge batch 8: slices 50.3 and 50.4

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`. Both are enabling slices: a task is done when its check gives the required result. bdd-red-green's stop conditions, hand-back and checkpoint apply, and they override any step here that conflicts with them.

**Goal:** The two refactors the fifth architecture review (slice 50.2) calls for, in plan order:
- every When that runs shop-knol gives what it ran, and every whole read a step makes goes through the driver (50.3);
- no step definition module is over 250 lines (50.4).

No behaviour changes, no scenario is added and no feature file is touched. After this batch the plan holds no slice that is not green.

**Architecture:** shop-knowledge is the Python package `shop_knowledge`, and its `shop-knol` command is a client of kb v0.2.0. Its scenarios are driven by pytest-bdd 8.1 step definitions under `tests/`, one `test_<feature>.py` per feature file, with the shared steps and fixtures in `tests/conftest.py` and the one way of driving shop-knol in `tests/driver.py`. Both tasks change only `tests/` and, in Task 2, `CLAUDE.md`. Nothing under `src/` or `features/` changes.

**This plan carries no code** (adrs/0011). The implementer writes every change in the execution session. What each task gives instead:
- the slice and its check;
- why the check fails today, found by running it in this checkout;
- where the change lands, and which rule it implements once;
- the decisions left open, each resting on a passage;
- what existing steps and fixtures to reuse, by name;
- the commands, with counts;
- the checkpoint to log.

**Tech Stack:** Python 3.11, pytest 8 + pytest-bdd 8.1, kb v0.2.0 (`kb.content` for YAML in the steps).

**Spec:** `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md`. These slices change no behaviour it describes. Read `CLAUDE.md` instead, "Size and shape" and "Step definitions", and in the slice plan: slices 50.2 to 50.4 and the slice 50.2 review entry at the end of its log. The decisions this plan rests on are adrs/0034 and 0035.

## Global Constraints

- Feature files are read-only, tag lines included. Any diff under `features/` is a stop condition.
- Nothing under `src/` changes. `git diff --stat -- src features` is empty at the end of each task.
- No behaviour changes. Every scenario that passes before a task passes after it, and none is added, removed or renamed.
- kb is v0.2.0 in `.venv` and is never edited here. The empty batch's traceback is kb's. It waits on a kb tag and a pin bump and is not touched here.
- Every rule in `CLAUDE.md` holds at the end of every task. Under `src/` no module goes past 250 lines, since nothing there changes. Under `tests/` the limit holds from Task 2 on (adrs/0034).
- Work on `main` in this checkout (adrs/0009). Run every command from the checkout's root. The suite is green, so `make test` ends cleanly with pytest's `62 passed`.
- Scratch files go under `.superpowers/batch8/`, which `.git/info/exclude` covers (it excludes `.superpowers/`). Each task writes its own baseline there.
- Commits: `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`. The message ends with the Co-Authored-By line of the model that made the commit. Each task makes one commit, holding the slice's change and its checkpoint.
- pytest-bdd prints `PytestRemovedIn10Warning`s, two for each `target_fixture` step. That is the baseline, not a fault.
- **Counts.** The suite has 62 scenarios (`.venv/bin/python -m pytest --collect-only -q | grep -c ::`, run 2026-09-27), and all pass before and after each task. No slice tag selects either enabling slice. The test modules each task touches collect as follows (run 2026-09-27):
  - `tests/test_read_back_what_the_shop_knows.py`: 12 (tags 1, 1.27 and 22);
  - `tests/test_start_a_shop_knowledge_base.py`: 8 (tags 4, 47 and 49; `-m slice-49` selects its 2 role and tag scenarios);
  - `tests/test_record_a_decision.py`: 10 (tags 1, 1.17, 1.24, 26 and 28).

  | after | failed | passed |
  |---|---|---|
  | before Task 1 (run 2026-09-27) | 0 | 62 |
  | 50.3 | 0 | 62 |
  | 50.4 | 0 | 62 |

- **The size check**, run at the start and end of every task:

  ```bash
  find src tests -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'
  ```

  Today it lists `276 tests/test_read_back_what_the_shop_knows.py`, `251 tests/test_record_a_decision.py` and `251 tests/test_start_a_shop_knowledge_base.py`. After Task 2 it lists nothing.

## Decisions that hold across the batch

1. **The steps keep saying what they say.** A refactored step asserts what it asserted before, through a different route. A Then that checked a string in a whole read's stdout checks the same string in the document the driver gives back. No assertion is loosened or dropped. The run proves nothing was lost only if each changed step is also seen red once by breaking its assertion for one run (bdd-red-green's "seen red" for a refactor), and the checkpoint says so.
2. **The driver is not widened.** `driver.record` keeps its signature and its return, the id, since some thirty Givens call it. A When that must give `result` runs the command itself through `driver.knol`, as `test_record_a_decision.py`'s `_record_it` does.

## Review Focus

writing-plans asks for a test in the owning task for each line here. In this project tests are scenarios, and feature files are the human gate, so no test is added. Each line goes into the owning task's checkpoint instead: a failure mode as a thing checked, a behaviour as a `QUESTION FOR THE SPEC` with its reproduction.

1. **A step moved to a sibling module and not reached** (owner: Task 2). Under pytest-bdd 8.1 a step in a sibling module reaches a feature's test module only through a star import. A plain `import` leaves it unregistered, and the scenario fails with `StepDefinitionNotFound` (spike, 2026-09-27, logged in the slice plan). The file counts above catch it: 12 and 8 passed.
2. **A sibling module collected as tests** (owner: Task 2). A module named `test_*` is collected by pytest and would register its steps a second time in a module with no scenarios. The check's `ls tests/*.py` catches it.
3. **A name brought in by the star import shadows one of the test module's own** (owner: Task 2). A star import brings in every public name of the sibling, its constants and the driver names it imports among them. A sibling constant named like one of the test module's, `DECISION` for example, rebinds it in whichever order the lines run. Keep each constant in the one module that uses it, and check with `grep -n "^[A-Z_]* = " tests/<sibling>.py` against the test module's own.
4. **The agent renderer checks no harness limit** (owner: Task 2's checkpoint, carried from the slice 50.2 review). QUESTION FOR THE SPEC. Reproduction: record a role with `harness.name: Stock Keeper!`, a 1500-character description and a 700-line section, then run `shop-knol render agent role/stock-keeper --to out`. It exits 0 and writes a 707-line agent headed `name: Stock Keeper!`. The spec says `agent` fails rather than emit something the harness would reject.
5. **`init ""` starts a store in the working directory** (owner: Task 2's checkpoint, carried from the slice 50.2 review). QUESTION FOR THE SPEC. Reproduction: from an empty directory, run `KB_ACTOR=a shop-knol init ""`. It exits 0, and `kb/` is now in the working directory. A user might expect a refusal naming the empty root.

---

### Task 1: Slice 50.3, every When that runs shop-knol gives what it ran, and every whole read a step makes goes through the driver

**Slice plan entry:** enabling, no unknown. Check:
- `.venv/bin/python -m pytest -q` gives `62 passed`, as before the slice;
- `grep -h -A3 "^@when" tests/*.py | grep -o 'target_fixture="[a-z_]*"' | sort | uniq -c` gives one line, `42 target_fixture="result"`;
- `grep -n '"--whole"' tests/*.py` gives two lines: `tests/driver.py`, and the When of `test_read_back_what_the_shop_knows.py` that is the user's whole read;
- `grep -c "does not exist yet" tests/*.py | grep -v ":0"` gives no line;
- `git diff --stat -- src features` is empty.

**Observable:** a reader finds every When that runs shop-knol handing on what it ran as `result`, and every whole read a Then makes going through the driver's one way. No comment says a command is missing that the shop now has.

**Why the check fails today** (run 2026-09-27):
- The uniq count gives three lines: `1 target_fixture="decision"`, `40 target_fixture="result"` and `1 target_fixture="role"`. The two strays were added in slice 49 in `tests/test_start_a_shop_knowledge_base.py`:
  - `_records_a_role` (line 193), "the user records a role, saying who they are and why", runs `create` through `driver.record` and gives the id as `role`. `_kept_as_one_group`, `_harness_group` and `_shop_group` take `role`.
  - `_tags_a_decision` (line 231), "the user tags a decision with "pricing", saying who they are and why", does the same and gives the id as `decision`. `_decision_names_tag` and `_description_held_once` take `decision`.
- The whole-read grep gives four lines. The two besides the check's are in `tests/test_record_a_decision.py`:
  - line 222, in `_earlier_still_reads_back` ("the decision recorded earlier still reads back by the name it had"). It runs `read <name> --whole`, asserts exit 0 and loads stdout. Its last assertion looks for `Monthly was enough once.` in the raw stdout.
  - line 244, in `_holds_the_piped_decision` ("the shop holds the decision just as if it had come from a file"), which does the same.
  Slice 48.1 made `driver.whole` the one way, but its check counted only functions named `_whole`, so these slipped by.
- `tests/test_read_back_what_the_shop_knows.py:150`, in `_older_decision_tagged_seasonal`, says `apply` is used "since `write` does not exist yet". `write` has existed since slice 36.

**Where it lands:**
- `tests/test_start_a_shop_knowledge_base.py`: the two Whens give `result`, and the Thens that took `role` or `decision` read the id from what the command showed.
- `tests/test_record_a_decision.py`: the two Thens read whole through `driver.whole`.
- `tests/test_read_back_what_the_shop_knows.py`: the stale clause of the comment goes.
- Nothing else. Rule implemented once: CLAUDE.md's Step definitions, "A When that runs shop-knol gives what it ran as the fixture `result`", and `driver.py` as the one way a step reads whole.

**Decisions:**
1. **The Whens run `create` themselves.** Each writes its content to a file under `tmp_path` and runs `knol(env, "create", <type>, "--from", <file>, "-m", <message>)`, giving the result, as `_record_it` in `test_record_a_decision.py` does (Decision 2 above). The content and message stay as they are today: the role `Stock keeper` with `THE_HARNESS_FIELDS`, `THE_SHOP_IDENTITY` and its one section, message `Describe the stock keeper`, and the decision `Price reviews happen weekly` tagged with the Given's `tag`, message `Record weekly reviews`.
2. **The Thens take the id from `shown`.** The conftest fixture `shown` asserts the command succeeded and loads its stdout, and `shown["id"]` is the name kb gave. `_kept_as_one_group` then takes the role's name from its caller. `_description_held_once` and `_decision_names_tag` keep `tag`, a Given's fixture, which the rule does not cover.
3. **The whole reads keep every assertion.** `_earlier_still_reads_back` checks the title, the revision and the monthly rationale's body, the last in the document's `sections` and no longer in the raw stdout (Decision 1 above). `_holds_the_piped_decision` checks what it checks now. `loads` stays imported in the module, since other steps use it.
4. **The read-back comment keeps its reason.** The step still drives shop-knol as a user does, and a batch is a fair way to create a tag and write the decision as one change. Only the clause "since `write` does not exist yet" goes, so the comment says what the step does and nothing false.

**Reuse:**
- `tests/conftest.py`: the fixture `shown`.
- `tests/driver.py`: `knol` and `whole`. `record` stays for the Givens.
- `tests/test_record_a_decision.py`: `_record_it`, as the pattern for a When that writes and creates.
- `tests/test_start_a_shop_knowledge_base.py`: `THE_HARNESS_FIELDS`, `THE_SHOP_IDENTITY`, `TAG_DESCRIPTION`, and the Given `_a_base_holding_a_tag`, which gives `tag`.

- [ ] **Step 1: Baseline.**
  - `mkdir -p .superpowers/batch8; .venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch8/failing-50.3.txt; wc -l < .superpowers/batch8/failing-50.3.txt` gives `0`;
  - the check's three greps give what "Why the check fails today" says;
  - the size check lists the three modules.
- [ ] **Step 2: Change** the two Whens and their Thens, then the two whole reads, then the comment. See each changed Then red once by breaking its assertion for one run, then restore it.
- [ ] **Step 3: Check.**
  - `.venv/bin/python -m pytest -q` gives `62 passed`;
  - `.venv/bin/python -m pytest -q -m slice-49` gives `2 passed, 60 deselected`;
  - `.venv/bin/python -m pytest -q tests/test_record_a_decision.py` gives `10 passed`;
  - `.venv/bin/python -m pytest -q tests/test_read_back_what_the_shop_knows.py` gives `12 passed`;
  - the three greps give `42 target_fixture="result"`, the two lines, and no line;
  - `git diff --stat -- src features` is empty;
  - the size check. `tests/test_record_a_decision.py` is expected under 250 (about 247). The other two stay over, which is Task 2's.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 50.3 green.`, then:
  - `Check:` with each output, and each module's line count after;
  - `Surprised by:`;
  - `Next: slice 50.4.`

  Set slice 50.3's Status to `green`.

---

### Task 2: Slice 50.4, no step definition module is over 250 lines

**Slice plan entry:** enabling, no unknown. Check:
- `.venv/bin/python -m pytest -q` gives `62 passed`;
- `.venv/bin/python -m pytest --collect-only -q | grep -c ::` gives `62`;
- `find src tests -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'` lists nothing;
- `grep -l "import \*" tests/*.py` lists exactly `tests/test_read_back_what_the_shop_knows.py` and `tests/test_start_a_shop_knowledge_base.py`;
- no new module under `tests/` is named `test_*`;
- `grep -n "250" CLAUDE.md` shows the size rule naming `src/` and `tests/`, and CLAUDE.md's Step definitions section says where a feature's steps go when one module cannot hold them;
- `git diff --stat -- src features` is empty.

**Observable:** a reader finds no module under `src/` or `tests/` over the limit. CLAUDE.md says the limit covers both, and how a feature's steps are split when they outgrow one module.

**Why the check fails today** (run 2026-09-27, before Task 1):
- The size check lists `tests/test_read_back_what_the_shop_knows.py` at 276 and `tests/test_start_a_shop_knowledge_base.py` at 251. `test_record_a_decision.py` at 251 is Task 1's to bring under. After Task 1 the read-back module is about 275, and the start module is a few lines over 251, since its two Whens now write their files themselves. Measure both at Step 1.
- `grep -l "import \*" tests/*.py` lists nothing.
- CLAUDE.md's "No module over 250 lines" names no directory, and its Step definitions section does not say how one feature's steps are split.

**Where it lands:**
- A new module beside `tests/test_read_back_what_the_shop_knows.py` holds the steps of the five scenarios about where the knowledge base is found. That is the five Givens that give `workdir` and their Thens, today lines 196 to 276:
  - `_working_deep_inside_the_shop`, `_decision_from_above`;
  - `_working_elsewhere_naming_the_shop`, `_decision_from_kb_root`;
  - `_working_elsewhere_naming_nothing`, `_rejected_no_store`;
  - `_kb_root_names_an_empty_directory`, `_rejected_kb_root_holds_none`;
  - `_kb_root_names_another_store`, `_rejected_two_stores`.
  The test module star-imports it.
- A new module beside `tests/test_start_a_shop_knowledge_base.py` holds the steps of slice 49's two scenarios, role and tag. That is today's lines 184 to 251 as Task 1 left them: the Given "a shop knowledge base" (used by the role scenario alone), `THE_HARNESS_FIELDS`, `THE_SHOP_IDENTITY`, `TAG_DESCRIPTION`, the role and tag Givens, Whens and Thens, and `_kept_as_one_group`. The test module star-imports it.
- `CLAUDE.md`: the size rule says it covers `src/` and `tests/` (adrs/0034). The Step definitions section says where a feature's steps go when one module cannot hold them (adrs/0035).
- Rule implemented once: "No module over 250 lines. When a change would cross the limit, split first", read with adrs/0034, and "the rest sit beside the scenarios they serve".

**Decisions** (adrs/0035):
1. **The names.** The read-back sibling is `tests/read_back_from_elsewhere.py`. The start sibling is `tests/start_roles_and_tags.py`. Neither starts with `test_`, so pytest does not collect them. Each opens with a docstring naming the feature it serves and the scenarios whose steps it holds, as `conftest.py` and `driver.py` open with theirs.
2. **One importer each.** Each sibling is star-imported by its feature's test module alone. A plain import does not register the steps (spike, 2026-09-27). The star import carries a comment saying so, so no one "tidies" it into a plain import.
3. **What stays.** The fixture `workdir` and the When `_read_the_decision` that reads it stay in the read-back test module, with the Background's `decision_id`, `DECISION` and `OLDER`, which the rest of that module uses. The moved Givens ask for `decision_id` and `workdir` as fixtures by name, as they do now, and pytest resolves them per scenario wherever each step is defined. A sibling never imports from its test module, since the test module imports it first and the import would be circular. So the two moved Thens that compare `shown["id"]` against `DECISION` compare it against the Background's `decision_id` fixture, the name the Background recorded, which is the same value (the Background returns `record`'s id for `Price reviews happen weekly`). No constant is copied (Review Focus 3). In the start module, `_init`, `THE_SHOPS_TYPES`, `_NO_ROLE` and every step of slices 4 and 47 stay.
4. **Split, not squeezed.** No line is joined, no blank line or docstring dropped to fit (slice 28's hand-back). Both modules end well under the limit: about 195 and 185 lines.
5. **CLAUDE.md's words.** One sentence in "Size and shape" says the limit covers every module under `src/` and `tests/`. One bullet in "Step definitions" says that when one feature's steps outgrow a module, the steps of one of its concerns go to a module beside it, not named `test_*`, which the feature's test module alone star-imports. Nothing else in CLAUDE.md changes, and the module map, which is `src/`'s, gains no row.

**Reuse:**
- `tests/conftest.py`: `shop`, `env`, `shown`, and the shared Thens. They stay where they are. The moved steps use them as they do now.
- `tests/driver.py`: `knol`, `start`, `record`, `whole`. Each sibling imports the driver names it uses itself.

- [ ] **Step 1: Baseline.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch8/failing-50.4.txt; wc -l < .superpowers/batch8/failing-50.4.txt` gives `0`;
  - the size check lists the read-back and start modules, and their counts go into the checkpoint;
  - `grep -l "import \*" tests/*.py` lists nothing.
- [ ] **Step 2: Split** the read-back module, then run `.venv/bin/python -m pytest -q tests/test_read_back_what_the_shop_knows.py`, which gives `12 passed`. Then split the start module and run `.venv/bin/python -m pytest -q tests/test_start_a_shop_knowledge_base.py`, which gives `8 passed`. To see that the moved steps are really reached through the sibling, comment out the star import for one run: the scenarios whose steps moved then fail on `StepDefinitionNotFound` (5 in read-back, 2 in start). Then restore it.
- [ ] **Step 3: Edit `CLAUDE.md`** as Decision 5 says.
- [ ] **Step 4: Check.**
  - `.venv/bin/python -m pytest -q` gives `62 passed`, and `make test` ends cleanly;
  - `.venv/bin/python -m pytest --collect-only -q | grep -c ::` gives `62`;
  - the size check lists nothing;
  - `grep -l "import \*" tests/*.py` lists the two test modules;
  - `ls tests/*.py` shows the two siblings, neither named `test_*`;
  - `grep -n "^[A-Z_]* = " tests/read_back_from_elsewhere.py tests/start_roles_and_tags.py` names no constant also assigned in its test module;
  - `grep -n "250" CLAUDE.md` shows the rule naming `src/` and `tests/`;
  - `git diff --stat -- src features` is empty.
- [ ] **Step 5: Checkpoint and commit.** Log `- 2026-09-27 slice 50.4 green.`, then:
  - `Check:` with each output and each module's line count after;
  - `Surprised by:`;
  - `Open questions:` Review Focus 4 and 5, each with its reproduction, run after this task;
  - `Next: none. Every slice in the plan is green. What remains is the QUESTION FOR THE SPEC lines in the log, for formulating-features and the human, and the kb pin bump for the empty batch's traceback.`

  Set slice 50.4's Status to `green`.

---

## After the batch

No architecture review follows: two slices are fewer than the six adrs/0010 counts, and neither touches `src/`. The plan is then complete. What remains:
- the QUESTION FOR THE SPEC lines in the slice plan's log;
- the request to bump kb's pin to the tag that releases kb slice 97, which closes the empty batch's traceback, the one place rule 4 is broken.
