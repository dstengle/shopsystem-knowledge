# shop-knowledge batch 12: slices 50.16.1 to 50.16.6

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, in slice order. All six are enabling slices. Each is checked by its check, and the suite gives the same answer before and after it: `80 passed, 21 failed`. The 21 are the capability slices planned after this batch.

**Goal:** make shop-knowledge's step definitions know kb only through what kb publishes (adrs/0047, kb adrs/0018). Keep every test away from live data. Clear the seventh architecture review's refactors. In plan order:
- **50.16.1** a stand-in for kb at the contract boundary, and no step touching kb's storage or internals;
- **50.16.2** no test reaching a knowledge base outside its own temporary directory;
- **50.16.3** no Then relying on kb's fault order;
- **50.16.4** no Then spelling kb's fault wording;
- **50.16.5** markdown pages built in one module with no step;
- **50.16.6** the batch 11 minors.

The eighth architecture review (50.16.7) follows the batch and runs before the next plan (adrs/0010, 0011).

**Architecture:**
- `shop-knol` runs as a subprocess per command, driven by `tests/driver.py`.
- shop-knol reaches kb through `kb.client.connect()` in `cli._client` (and `connect(root)` in `cli._init`).
- `tests/clock/` is put on the subprocess's `PYTHONPATH` by `driver.at` when a scenario says what day it is. It has a `sitecustomize.py` that Python loads at start-up. That is the one existing way the steps change shop-knol's process without `src/` knowing.

**This plan carries no code** (adrs/0011). The implementer writes every change. What each task gives: the check, why it fails today, where the change lands and the rule it keeps, the decisions already made, what to reuse, and the commands.

**Tech Stack:** Python 3.11, pytest 8 + pytest-bdd 8.1, kb v0.2.1 (`kb.content`, `kb.contract.kb_pb2`, `kb.client`).

**Spec:** `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md`, its Testing section as amended in e23a0c3:

> shop-knowledge knows kb only through what kb publishes, in its tests as in its code; where a scenario needs kb in a state no contract call can produce, a stand-in for kb at the contract boundary answers with kb's contract messages. No test reaches a knowledge base outside its own temporary directory.

Read CLAUDE.md, adrs/0035, 0047 and kb's adrs/0018 (`/home/vscode/shopsystem-kb/adrs/0018-the-published-contract.md`). In the slice plan, read slices 50.16.1 to 50.16.6 and the 2026-09-27 log entries from "Slice 50.16, seventh architecture review" on. The review's full report is `.superpowers/batch12/arch-review-50.16.md`, scratch outside git. Its sections 4 to 6 give each refactor's detail, and this plan repeats what a task needs.

## Global Constraints

- Feature files are read-only, tag lines included. Any diff under `features/` is a stop condition. No Given, When or Then line changes: a step's text stays, and only its body changes.
- Nothing under `src/` changes in this batch (`git diff --stat -- src` empty after every task), except the docstrings named in Task 6.
- kb is v0.2.1 and is never edited here. What kb publishes (kb adrs/0018): `kb.contract` (the messages), `kb.client.connect`, `kb.content` (`loads`, `dumps`, `text`), and fault `rule` names. Nothing else of kb is used by a step or a helper. Until the kb release carrying kb's slices 100 and 102 is pinned (slice 50.23), two exceptions stand:
  - `src/` still takes `NotCanonical` from `kb.canonical`;
  - `tests/clock/sitecustomize.py` still replaces kb's clock.
- Every rule in CLAUDE.md holds at the end of every task. No module under `src/` or `tests/` goes past 250 lines.
- Work on `main` (adrs/0009). Run every command from the checkout's root. Scratch files go under `.superpowers/batch12/`, never `/tmp`.
- Commits use `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`, the message ending with the model's Co-Authored-By line. One commit per task, holding the slice's change and its checkpoint in the slice plan's log, with its Status set to green. Push when the batch is done (adrs/0036).
- The baseline: `.venv/bin/python -m pytest -q` gives `80 passed, 21 failed` (run 2026-09-27). The 21 are:
  - slices 50.17 to 50.22's seven;
  - 50.18.1's five, 50.18.2's six red rows and 50.18.3's three.

  `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch12/failing-before.txt` records them. After each task the same command gives the same file (`diff` empty).
- `PytestRemovedIn10Warning`s are the baseline.
- The size check: `find src tests -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'` lists nothing, before and after each task.

## Review Focus

Each line goes into the owning task's checkpoint, as a thing checked.

1. **The stand-in never answers a scenario that did not ask for it** (owner: Task 1). With the stand-in's module on the path but told nothing, every call reaches the real kb. Show this with a throwaway run of the whole suite with the stand-in always on the path. The suite still gives `80 passed, 21 failed`. Log it.
2. **The stand-in cannot reach a real store** (owner: Task 2). The stand-in delegates to the real client, so Task 2's guard covers it too. Log that the guard's throwaway store in the checkout's parent stops a stand-in scenario as well.
3. **A developer's own `KB_ROOT` or `KB_ACTOR`** (owner: Task 2). Run the suite with `KB_ROOT` set in the shell to a throwaway store under `.superpowers/batch12/`. The suite neither reads nor writes it. Check its journal before and after, through kb's own `connect(root)` and `Journal`. Log it.
4. **Faults the stand-in gives are visibly not kb's** (owner: Task 4). A stand-in's fault message is written by the step, so a Then that checks "printed as kb returned it" compares with what the stand-in gave, never with kb's words. Log each Then's source of truth.

---

### Task 1: Slice 50.16.1, the steps know kb only through what kb publishes, with a stand-in for kb where the contract cannot reach

**Check:** as the slice plan's entry says:
- the suite unchanged;
- `grep -rn "kb import canonical\|kb\.canonical\|kb\.store\|kb\.values\|store.yaml\|/ \"schema\"\|\"schema\")\|read_bytes\|_everything_under" tests` gives nothing;
- `grep -rln "kb.journal" tests` gives only `tests/clock/sitecustomize.py`;
- `grep -rn '/ "kb" /' tests` gives nothing;
- the kb imports under `tests/` are only `kb.client`, `kb.content` and `kb.contract`;
- `git diff --stat -- features src` is empty;
- CLAUDE.md's Step definitions section and rule 1 say what adrs/0047 says.

**Why it fails today (read 2026-09-27):**
- **Hand-edits of stored files.** Each reaches kb's layout, and some use `kb.canonical`:
  - `tests/test_check_the_shops_knowledge_is_sound.py`: `_shop_with_a_file_mangled_by_hand` (lines 20-30), `_shop_with_two_faults` (64-75), `_without_its_rationale` (77-82), used by `_shop_with_a_fault_and_a_decision_behind`;
  - `tests/test_read_back_what_the_shop_knows.py`: `_decision_file_mangled_by_hand` (80-81).
- **Storage observed.** `tests/test_start_a_shop_knowledge_base.py`:
  - reads `kb/schema` at 82-83 (`_defines_nothing`) and 168;
  - checks `kb/store.yaml` at 98, 139 and 210.
- **Every byte compared.** `tests/test_publish_what_the_shop_knows.py`'s `_everything_under` (22-24, 45, 115) compares every byte under `kb/`, `.git` included.

**Where the change lands (CLAUDE.md, adrs/0047):**
- **The stand-in** is a module under `tests/`, beside `tests/clock/`, put on shop-knol's `PYTHONPATH` by one function of `tests/driver.py`, the one way the steps drive shop-knol. Its surface:
  - At start-up it puts itself in front of `kb.client.connect`, a name kb publishes. For any call a scenario told it to answer, it answers with a `kb_pb2` message the step described. Every other call goes to the real client unchanged.
  - The scenario tells it what to answer through something the driver sets for that process, such as an environment variable naming a file the step wrote.
  - It knows only `kb.client`, `kb.contract` and `kb.content`.
  - Nothing under `src/` knows it exists.

  How the answers are described and matched to calls is the implementer's choice. Keep it to what these scenarios need:
  - a `ValidateResponse` carrying given violations, beside the real check's stale list where the scenario also has something behind its type;
  - a `ReadResponse` carrying a given fault for one named artifact.
- **The check and read-back Givens** record what they can through shop-knol against the real kb, as today. What no contract call can produce (a file that cannot be read, an artifact unfit for its type, a link that points at nothing) they give through the stand-in instead of editing files. The Given's text says someone edited a file by hand: that is the state of the world the user sees, and the stand-in gives kb's answer for that state. The faults the stand-in gives are written by the step, in the step's own words, never kb's (Task 4, Review Focus 4).
- **The start feature's steps observe through shop-knol:**
  - `_defines_nothing` lists the types with `shop-knol list --type schema --ids`;
  - the "store is started" Thens check that a shop-knol command run from that directory, with `KB_ROOT` unset, finds the store;
  - the "inside the shop's knowledge" Given (168) works in `kb/` itself. The contract's Init row names `kb/`, the subdirectory of the root.
  - `_holds_none` (123) checks that `kb/` does not exist. The Init row names that directory, so the check may stay, with a comment saying why.
- **The publish feature's "the shop's knowledge base is unchanged"** compares, before and after, what shop-knol shows: `shop-knol journal`, and the whole reads of the published artifacts. `_still_there` does the same elsewhere, and can be reused.
- **Helpers:** where any step still needs to name a place kb's contract names (`<root>/kb/`), that name lives in `tests/driver.py` alone.
- **CLAUDE.md:**
  - The Step definitions section says what adrs/0047 says. Replace "They may use kb's in-process client, or read and hand-edit a knowledge base's files, only to set up or observe what no shop-knol command yet does" with: they use kb only through what kb publishes; a state no contract call can produce comes from the stand-in; they never read or write a knowledge base's files.
  - Rule 1 says the same holds for `tests/`.
  - The module map gets no row, since `tests/` has none; the Step definitions section names the stand-in's module.

**Decisions already made:**
- The stand-in answers with contract messages and delegates everything else (adrs/0047).
- Its faults are the step's own words.
- `kb/` as the root's subdirectory is contract (kb's Init row).
- The clock stays until 50.23.

**Reuse:** `driver.knol`, `driver.record`, `driver.start`, `driver.whole`, `driver.at` (the pattern for putting a directory on the path), `_still_there`, and the existing When "the user checks the shop's knowledge".

- [ ] **Step 1:** Record the failing list (`failing-before.txt`). Run the size check and each grep of the check, and log the before values.
- [ ] **Step 2:** Build the stand-in and its driver function. Move the read-back Given to it first, then run `-m slice-1.27`, which gives `1 passed`. Show it can fail: a throwaway stand-in answer with a different fault turns the Then red. Log it, then revert.
- [ ] **Step 3:** Move the three check Givens to the stand-in:
  - `-m "slice-1.28 or slice-42 or slice-44 or slice-42.2 or slice-50.13"` stays green, with the count logged in Step 1;
  - `kb.canonical` goes from the module.
- [ ] **Step 4:** Move the start feature's and the publish feature's observations to shop-knol commands. `-m "slice-4 or slice-47 or slice-50.8 or slice-17 or slice-19"` stays green, with the count logged in Step 1.
- [ ] **Step 5:** Update CLAUDE.md.
- [ ] **Step 6:** Run Review Focus 1.
- [ ] **Step 7:** The failing list is unchanged. Run every command of the check.
- [ ] **Step 8:** Checkpoint, set the status to green, commit.

### Task 2: Slice 50.16.2, no test reaches a knowledge base outside its own temporary directory

**Check:** as the slice plan's entry says:
- the suite is unchanged;
- a throwaway `kb/store.yaml` in the checkout's parent directory makes the suite refuse to start, saying why;
- a throwaway call of the driver with no working directory is refused.

**Why it fails today:**
- `driver.knol`'s `cwd` defaults to `None`, so the process starts where pytest runs (the checkout).
- The read-back feature's `workdir` fixture is `None` unless a Given moves the user.
- Every scenario has `KB_ROOT` naming its temporary shop, and the three steps that unset it move the user into a temporary directory. So no test reaches a real store today, but only by convention.
- A store in the checkout's parents (`/home/vscode/kb/`, say, beside the shop's work) would be found by any future step that unset `KB_ROOT` and ran from the checkout.

**Where the change lands:**
- `tests/driver.py`: every shop-knol run has a working directory under the test's temporary directory, and running with none is refused. `conftest.py` can give the scenario's temporary directory as the default.
- The read-back `workdir` fixture's default becomes a directory under the test's temporary directory, not `None`. The scenarios' meaning is unchanged, since `KB_ROOT` names the shop.
- `tests/conftest.py` holds a session-start guard. It refuses to run, saying why, when a knowledge base can be found from the checkout or from the system's temporary directory, looking upward as the store is found. It knows `kb/` only as the contract names it: the root's subdirectory holding a store, whatever kb puts inside it. The guard may call kb's published client from each directory and treat an answer that is not a no-store refusal as a found store. It may not open `store.yaml` (adrs/0047).
- The environment every scenario starts from copies the developer's shell. `KB_ROOT` and `KB_ACTOR` from the shell must never reach a scenario unchanged (Review Focus 3).

**Reuse:** `env`, `shop`, `tmp_path`.

- [ ] **Step 1:** Run the size check and record the failing list.
- [ ] **Step 2:** Add the guard. Show it working, by making the throwaway store in the checkout's parent and running the suite, then remove the store. Log it.
- [ ] **Step 3:** Change the driver and `workdir`. Show the refusal with a throwaway call, then revert it. Log it.
- [ ] **Step 4:** Run Review Focus 2 and 3.
- [ ] **Step 5:** The failing list is unchanged. Checkpoint, set the status to green, commit.

### Task 3: Slice 50.16.3, the steps hold kb only to a fault order kb states

**Check:** as the slice plan's entry says. The Thens that read fault lines by position:
- `tests/test_check_the_shops_knowledge_is_sound.py`'s `_unreadable_listed`, `_the_rest_listed` and `_both_listed`, which Task 1 may have reshaped;
- `tests/test_make_several_changes_at_once.py` around lines 86-88.

They compare as a set, or find each line by its artifact. A throwaway reversal of `cli._refuse`'s loop leaves them green. Log it, then revert.

**Why it fails today:** neither spec states an order, and these Thens index lines by position.

- [ ] **Step 1:** Record the failing list. Make the reversal and see which Thens go red. Log it, then revert.
- [ ] **Step 2:** Reshape those Thens. Run the reversal again, and it stays green. Revert it.
- [ ] **Step 3:** The failing list is unchanged. Checkpoint, set the status to green, commit.

### Task 4: Slice 50.16.4, the steps never spell kb's fault wording

**Check:** as the slice plan's entry says:
- the suite is unchanged;
- the Thens of the review's coupling point 17 check what the shop's spec owns: one line, the artifact and the place, printed as kb returned it;
- a throwaway rewording of one kb fault message in `.venv` leaves them green. Log it, then restore it with `make dev`.

**Unknown:** whether every Then that reads kb's words today can get the same words from kb itself for the same state.

**Why it fails today:** these Thens spell kb's wording:
- `tests/read_back_from_elsewhere.py` lines 55, 72 and 93-96;
- `tests/test_check_the_shops_knowledge_is_sound.py` 39 and 44, unless Task 1 already moved these to stand-in words;
- `tests/test_read_back_what_the_shop_knows.py` 86;
- `tests/test_record_a_decision.py` 82, 87-90 and 174;
- `tests/test_start_a_shop_knowledge_base.py` 175 and 182;
- `tests/test_retire_what_the_shop_no_longer_uses.py` 53 and 59.

Re-read each line number, since Tasks 1 to 3 move lines.

**Where the change lands:**
- Where the real kb gives the fault, the Then asks kb's published client (`kb.client.connect`, with the same working directory, `KB_ROOT` and request) for the same state's answer, and compares shop-knol's line with it.
- Where a helper in `tests/driver.py` does this for several features, it is said once there. A shared step goes in `conftest.py`.
- Where the stand-in gave the fault, the Then compares with what the stand-in gave (Review Focus 4).
- A `rule` name kb publishes may be asserted, where the Then has one to hand.

**Decisions already made:** kb's `rule` names are contract and its wording is not (kb adrs/0018). The shop's spec says errors are "printed as returned by kb".

- [ ] **Step 1:** Record the failing list, and list each Then with its line and its source of truth.
- [ ] **Step 2:** Reshape the Thens, one feature at a time, each feature's scenarios staying green.
- [ ] **Step 3:** Make the throwaway rewording, run the suite, restore with `make dev`, and log it. Run Review Focus 4.
- [ ] **Step 4:** The failing list is unchanged. Checkpoint, set the status to green, commit.

### Task 5: Slice 50.16.5, the markdown pages the publish steps expect are built in one module that holds no step

**Check:** as the slice plan's entry says. The review's R1:
- `grep -n "from publish_as_markdown" tests/*.py` gives nothing;
- `grep -c "@given\|@when\|@then"` on the new helper module gives 0;
- one page reader, which `_a_page_of` and `_every_value_shown` both use;
- `grep -c '"| check-it' tests/publish_as_markdown.py` gives 0, because `_steps_as_a_table` compares with the page the helper builds;
- a throwaway `_step_holding(steps, "no-such-step", x=1)` raises. Log it, then revert.

**Why it fails today:** `tests/markdown_well_formed.py:10` imports helpers from its sibling step module. adrs/0035 says a sibling is star-imported by its feature's test module alone. `_every_value_shown` repeats `_a_page_of`. `_steps_as_a_table` spells out a page `_process_page` builds. `_step_holding` passes silently on an unknown id.

**Where the change lands:** a new helper module under `tests/`, holding no step and imported plainly, as `driver.py` is. It holds `_write_over`, `_role_page`, `_process_page`, `_row`, `_STEP_ROWS`, `_step_holding` and the one page reader. Name it for what it holds (e.g. `markdown_pages.py`). CLAUDE.md's Step definitions section says where such helpers go, if it does not already.

- [ ] **Step 1:** Record the failing list.
- [ ] **Step 2:** Move the helpers. `-m "slice-20 or slice-50.6 or slice-50.11 or slice-50.14 or slice-50.18.2"` gives the same passed/failed split, with the count logged.
- [ ] **Step 3:** Run every command of the check.
- [ ] **Step 4:** Checkpoint, set the status to green, commit.

### Task 6: Slice 50.16.6, the batch 11 review's minor findings are tidied

**Check:** as the slice plan's entry says. The review's R2:
- `grep -n "startswith(decisions" tests/test_check_the_shops_knowledge_is_sound.py` gives nothing;
- `grep -rn "_after_the_colon" src tests` gives nothing;
- `grep -n "_MADE_FROM\|^def _a(" tests/test_publish_what_the_shop_knows.py` gives nothing;
- `grep -n "renderer's to say" src/shop_knowledge/renderers/source.py` gives nothing;
- `_a_failing_checks_answer` opens with a docstring;
- `_role_page`'s and `renderers/source.py`'s docstrings each name what the code does.

**Where the change lands:**
- **`_not_a_fault`:** matches the artifact a fault line names exactly (before ` at ` or `:`).
- **The renamed helper:** `markdown._after_the_colon` is renamed for what it does, both after a colon and after a bullet's dash. This is the one change under `src/`: a name and a docstring, with behaviour unchanged.
- **The type-refusal Then:** it spells its three expected lines, one per outline row. These lines are shop-knowledge's own wording (`source.refusal`), not kb's.
- **`renderers/source.py`'s module docstring:** it says `refusal` decides what stops a render.
- **`_role_page`'s docstring:** it says plainly what `extra` is.

- [ ] **Step 1:** Record the failing list.
- [ ] **Step 2:** Make the changes. Run `-m "slice-50.13 or slice-50.14 or slice-50.15 or slice-50.18.2"` and log the split.
- [ ] **Step 3:** Run every command of the check. `git diff --stat -- src` shows only `renderers/markdown.py` and `renderers/source.py`.
- [ ] **Step 4:** Checkpoint, set the status to green, commit.

## After the batch

- [ ] Run the final whole-branch review on the most capable model against this plan, CLAUDE.md and adrs/0047. The reviewer greps `src/` and `tests/` for every kb import and every name of kb's storage themselves.
- [ ] Log the findings and rulings. Push.
- [ ] Then slice 50.16.7, the eighth architecture review, before the next plan.
