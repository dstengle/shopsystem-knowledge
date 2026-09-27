# shop-knowledge batch 7: slices 42.2 to 50.1

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`. A capability task follows `shopsystem-bdd:bdd-red-green` over its scenarios. An enabling task is done when its check gives the required result. bdd-red-green's stop conditions, hand-back and checkpoint apply, and they override any step here that conflicts with them.

**Goal:** Eight slices in plan order. They finish every scenario the features hold and leave the code in the shape CLAUDE.md sets. This is the last batch of the plan. In order:
- the check's answer refused the one way (42.2);
- check the shop's knowledge is sound (44);
- start a knowledge base beside the shop's work, for no stated reason, and never twice (47);
- one bad change in a batch leaves the shop untouched (48);
- a whole read driven one way in the steps (48.1);
- the shop's roles and tags hold their shape (49);
- publish a role as an agent (50);
- what an argument means said once (50.1).

**Architecture:** shop-knowledge is the Python package `shop_knowledge`. Its `shop-knol` command calls kb through `kb.client.connect` with `kb.contract.kb_pb2` messages, and reads and prints YAML 1.2 through `kb.content`. kb is `shopsystem-kb` v0.2.0, installed from its git tag into this checkout's `.venv`. It is never edited here. `CLAUDE.md` sets the shape the code is held to. Its module map says where each change lands, and each task names the rule it implements once.

**This plan carries no code** (adrs/0011). The implementer writes every step definition and every line under `src/` red-green in the execution session. What each task gives instead:
- the slice and its scenarios or check;
- why each is red today, found by running it in this checkout and probing current behaviour;
- where the change lands, and which rule it implements once;
- the decisions the spec leaves open, each resting on a passage;
- what existing steps and fixtures to reuse, by name;
- the commands, with counts taken from the tags;
- the checkpoint to log.

**Tech Stack:** Python 3.11, setuptools (src layout), kb v0.2.0 (protobuf contract, in-process client), pytest 8 + pytest-bdd 8, `jsonschema`.

**Spec:** `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md`. Read these sections:
- The CLI: the command table rows for `validate`, `init`, `apply` and `render`, and the paragraph after the table.
- Bootstrap types: `role` "separates the harness contract fields from the corpus identity fields into two named field groups, so the `agent` renderer can copy one into frontmatter"; `tag` "is a title and description; a `tags` reference field on other types targets it".
- Renderers: "`agent` for `role`: `.claude/agents/<name>.md` with the harness field group as frontmatter and the prose sections as the body."

Also read `CLAUDE.md`, and in the slice plan: slices 42.2 to 50.2, and the slice 42.1 review entry at the end of its log. The decisions this plan relies on are in adrs/0029 to 0032. kb's contract is `.venv/lib/python3.11/site-packages/kb/contract/kb.proto`: `InitRequest`/`InitResponse`, `ValidateResponse` and `Stale`, `ApplyResponse`, and `Fault`.

## Global Constraints

- Feature files are read-only. Any diff under `features/` is a stop condition, and that includes tag lines. No task here moves a tag.
- Code only what a scenario asserts (bdd-red-green). An enabling task changes no behaviour a scenario pins. Where a scenario is silent, the code is silent too, and the silence goes into the checkpoint as an open question.
- kb is v0.2.0 in `.venv` and is never edited here. "shop-knowledge never touches kb's files or git. It calls the contract through the in-process client." A kb change a slice needs is not coded. It is logged in the slice plan as a request to bump the pin, and the slice stops. The probes for this plan found that none of these slices needs one. The empty batch's traceback is kb's, is fixed in kb's main (kb slice 97), waits on a kb tag and a pin bump, and is not touched here.
- Every rule in `CLAUDE.md` holds at the end of every task, and each is implemented once:
  - a kb answer's faults are refused only through `cli._answered`: Validate's from Task 1, Init's and bootstrap's from Task 3. A renderer's are the one exception, turned into `Rendered` faults and refused by `_render` through `_answered`;
  - a refusal is printed only by `main`, through the one printer;
  - a user's file, or the pipe, is read only in `cli._document`;
  - files are written only by `cli._write`;
  - what the user is shown is shaped only in `answers.py`, one public function per answer, each named in its CLAUDE.md row;
  - no module runs over 250 lines. If a task would take one past 250, stop and hand back.
- Spec lines every task keeps: "shop-knol never shows a traceback." "Errors are printed as returned by kb, with artifact, path, and message, and exit non-zero." "Every mutating command requires an actor and `-m`." (`init`: "needs an actor but no `-m`, its messages are fixed".) "Output is YAML by default."
- Work on `main` in this checkout (adrs/0009). `make test` runs the suite in `.venv`. While scenarios are red, its last line is make's own `Error 1`, so read pytest's summary line above it. After Task 7 nothing is red and make ends cleanly. Every command below runs from the checkout's root.
- Scratch files go under `.superpowers/batch7/`, which `.git/info/exclude` covers. It already holds:
  - `failing-now.txt`, the 12 failing ids, run 2026-09-27;
  - `help-now.txt`, the help of `shop-knol` and of all fourteen commands, each exit 0;
  - the planning probes `probe-init.sh`, `probe-kb.py`, `probe-cli.sh`, `probe-validate.py`, `probe-stale.py`, `probe-48.sh` and `probe-tb.sh`. They are throwaways: read them as evidence of what kb and shop-knol give, not as code to copy.
  Each task still writes its own baseline.
- Commits: `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`. The message ends with the Co-Authored-By line of the model that made the commit, e.g. `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`. Each task makes one commit, holding the slice's code, its steps and its checkpoint.
- pytest-bdd prints `PytestRemovedIn10Warning`s, two for each `target_fixture` step. That is the baseline, not a fault.
- **Counts.** The suite has 62 scenarios. `pytest --collect-only -q -m slice-N` (run 2026-09-27) selects 3 for slice 44, 5 for 47, 1 for 48, 2 for 49 and 1 for 50. It selects none for the enabling slices 42.2, 48.1 and 50.1. Failed and passed after each task:

  | after | failed | passed |
  |---|---|---|
  | before Task 1 (run 2026-09-27) | 12 | 50 |
  | 42.2 | 12 | 50 |
  | 44 | 9 | 53 |
  | 47 | 4 | 58 |
  | 48 | 3 | 59 |
  | 48.1 | 3 | 59 |
  | 49 | 1 | 61 |
  | 50 | 0 | 62 |
  | 50.1 | 0 | 62 |

- **GREEN** is the set of slices green before this batch. It is selected by `-m "slice-1 or slice-1.17 or slice-1.24 or slice-1.27 or slice-1.28 or slice-4 or slice-15 or slice-16 or slice-17 or slice-18 or slice-19 or slice-20 or slice-22 or slice-24 or slice-26 or slice-28 or slice-30 or slice-32 or slice-34 or slice-36 or slice-38 or slice-40 or slice-42"`, which gives `50 passed, 12 deselected` (run 2026-09-27). Each capability task adds its own tag to the expression, and every scenario it selects must pass.
- **The shape check** is run at the end of every task:

  ```bash
  grep -c "_refuse(" src/shop_knowledge/cli.py; grep -c "raise Refused" src/shop_knowledge/cli.py; grep -c "read_text" src/shop_knowledge/cli.py; grep -cE "argparse|add_parser|add_argument" src/shop_knowledge/cli.py; find src -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'; grep -lE "print\(|open\(|write_text" src/shop_knowledge/renderers/*.py; wc -l < src/shop_knowledge/cli.py
  ```

  Expected today: `2`, `8`, `1`, `0`, no module over 250 lines, no renderer listed, and `232`. From Task 1 on, the second number is `7`, since `_validate` no longer raises its own. No later task adds a `raise Refused`: Task 3 refuses Init's and bootstrap's answers through `_answered`. The slice 42.1 review estimated `cli.py`'s length after each task: about 231 after 42.2, 232 after 44, and 234 to 235 after 47, unchanged to the end. If a task finds `cli.py` would pass 250, stop and hand back. Do not squeeze lines to fit (slice 28's hand-back).
- **The arguments snapshot** shows that help did not change where a task says it must not:

  ```bash
  for c in "" init create read write append validate apply journal list refs search render delete snapshot; do .venv/bin/shop-knol $c -h; echo "exit $?"; done > .superpowers/batch7/help-$TAG.txt 2>&1
  ```

  Set `TAG` to the slice number, and diff against `.superpowers/batch7/help-now.txt`. Task 7 changes it in one way only: `agent` joins `render`'s renderer choices. Every other task changes nothing.

## Decisions that hold across the batch

1. **One public function per answer in `answers.py`,** named for what it gives and added to the CLAUDE.md row in the task that adds it. There is one new one: `checked` (validate, Task 2).
2. **kb's words pass through.** A refusal kb makes, of a start over a store, inside one, or of a change that does not fit its type, is printed as kb returns it: artifact, path and message ("Errors are printed as returned by kb"). A Then that says "rejected because ..." asserts kb's reason by a fragment of its message, as slice 42's Then does for "cannot be removed while".
3. **The steps observe through shop-knol.** A Then reads what the shop holds through `read`, `journal` or `list`. It reads a knowledge base's files only where no command shows the thing, and says so in a comment citing CLAUDE.md's Step definitions, as `_everything_under` in the publish module and `_defines_nothing` in the start module do.

## Review Focus

writing-plans asks for a test in the owning task for each line here. In this project tests are scenarios, and feature files are the human gate, so no test is added. Instead, each line goes into the owning task's checkpoint as a `QUESTION FOR THE SPEC`, with its reproduction, run after that task.

1. **A fault in a batch names a change by an artifact that does not exist** (owner: Task 4). A batch's create that does not fit is named by the name kb would have given it. Probed on 2026-09-27 (`probe-kb.py`): the second change, a create titled "Bad one", is refused as `decision/bad-one at owner: ...`, and there is no `decision/bad-one`. A user fixing the batch "in one pass" would expect the fault to say which change of the batch it is (the second). Reproduction after Task 4: apply a batch whose second change creates a decision with `owner: 3`, and read stderr.
2. **What is behind its type is not shown when the check also finds faults** (owner: Task 2). With faults, the check is a refusal: stderr only, nothing on stdout (adrs/0029). An artifact behind its type is then not shown at all. Reproduction after Task 2: write the decision type at version 2 through `shop-knol write schema/decision`, hand-break another decision, and run `shop-knol validate`. A user would expect to be told both.
3. **A non-role published as an agent** (owner: Task 7). `render agent tag/pricing --to o` writes an agent with an empty heading block and exits 0 (adrs/0031), as `render skill tag/pricing` writes a skill with no steps. A user would expect a refusal naming the type. Reproduction after Task 7: exactly that, then read the file.
4. **The agent's `tools` is written as a YAML list** (owner: Task 7). The harness field group is copied as kb gives it, so `tools: [Read]` becomes a sequence in the heading block. The bet renderers-match-the-harness says a rendered agent loads unchanged, and whether the harness takes a list there, or wants a comma-separated string, is not observed by the suite. No harness limit on an agent is checked, since no scenario asks for one ("fail rather than emit something it would reject"). Reproduction after Task 7: publish the Background's role and read the heading block.
5. **A reason given to `init` is refused** (owner: Task 3). `init` "needs an actor but no `-m`", and it takes none. `shop-knol init shop -m why` is refused as `shop-knol: unrecognized arguments: -m why`, exit 1 (probed 2026-09-27). A user who gives a reason out of habit might expect it to be taken, or told plainly that starting writes its own. Reproduction after Task 3: exactly that.

---

### Task 1: Slice 42.2, the check's answer is refused the one way every kb answer is

**Slice plan entry:** enabling, no unknown. Check:
- the same failing scenarios as before the slice (12 failed, 50 passed);
- `.venv/bin/python -c "import inspect,shop_knowledge.cli as c; assert 'Refused' not in inspect.getsource(c._validate)"` succeeds;
- `CLAUDE.md` names one place where a kb answer's faults are not refused through `_answered` directly, a renderer's, and not Validate's.

**Observable:** the check's faults and violations go through the one refusal of kb answers, so Task 2 extends that path rather than a second one.

**Why the check fails today:** `cli._validate` (cli.py:157-162) tests `response.faults or response.violations` and raises `Refused` itself. CLAUDE.md's Size and shape section names two places that differ, "Validate's answer is raised as `Refused` over its faults and violations together, and a renderer ...".

**Where it lands:**
- `src/shop_knowledge/cli.py`: `_answered` and `_validate`.
- `CLAUDE.md`: the sentence in Size and shape.
- Rule implemented once: "a kb answer's faults are refused in one way, `cli._answered`".

**Decisions** (adrs/0029):
1. **Validate's violations are refused as its faults.** `_answered` stays the one function that raises `Refused` over a kb answer. It takes the answer and, only when kb's answer carries more faults than its `faults` field, those faults as well. Only `_validate` passes them, `[*response.faults, *response.violations]`, in that order, as today. `_answered` still gives back the answer, which Task 2 shows.
2. **What a user sees does not change.** The slice 1.28 scenario's lines, their order and exit 1 stay as they are.

- [ ] **Step 1: Baseline.** `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch7/failing-42.2.txt; diff .superpowers/batch7/failing-42.2.txt .superpowers/batch7/failing-now.txt && echo same`: `same` (12). The `inspect` assertion fails.
- [ ] **Step 2: Change** `_answered` and `_validate` as decided, and CLAUDE.md's sentence so it names the renderer alone.
- [ ] **Step 3: Check.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort | diff - .superpowers/batch7/failing-42.2.txt && echo same`: `same`;
  - `make test`: `12 failed, 50 passed`;
  - `-m slice-1.28`: `1 passed`;
  - the `inspect` assertion succeeds;
  - `grep -n "Validate" CLAUDE.md`: no line says Validate's answer is raised apart;
  - the shape check: `2 7 1 0`, nothing listed, `cli.py` about 231;
  - arguments snapshot `TAG=42.2`: no diff.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 42.2 green.`, then `Check:` with each output, `Surprised by:`, and `Next: slice 44.` Set slice 42.2's Status to `green`.

---

### Task 2: Slice 44, check the shop's knowledge is sound

**Slice plan entry:** capability, no unknown. Scenarios, in check-the-shops-knowledge-is-sound (`@slice-44`, 3):
1. The user checks a sound knowledge base
2. The user checks a knowledge base with faults
3. The user is told what is behind its type

**Observable:** a user checks a sound knowledge base and is told nothing is wrong. They check one with two faults and see both, each with the artifact and place, while the command exits non-zero. Or they see a decision listed as behind its type and not as a fault.

**Why each is red today:**
- All three stop at their Given, `StepDefinitionNotFoundError` (run 2026-09-27): "a shop knowledge base where everything fits its type", "... where a decision is missing something its type requires and a work item points at something the shop does not hold", "... where a decision was last checked against an older version of the decision type".
- Underneath, probed with `probe-cli.sh` and `probe-stale.py`:
  - Scenario 1: `shop-knol validate` on a sound store prints nothing and exits 0, so there is nothing that tells the user.
  - Scenario 3: after the decision type is written at version 2, kb's answer carries `stale {artifact: "decision/old-one", schema_version: 1, current: 2}`, and shop-knol drops it, printing nothing with exit 0.
  - Scenario 2 already passes on code once its steps exist. Its two lines were probed with `probe-validate.py`: `decision/old-one at sections: the sections the type requires must all be present, in order; 'Rationale' is missing` and `work-item/w at decisions/0: a link must land on a node of a kind the type allows; 'decision/nothing' does not`, with exit 1.

**What kb gives:** `ValidateResponse` has `violations`, `faults` and `stale`. Each `Stale` is `artifact`, `schema_version` (the version last checked against) and `current`. kb refuses to create a decision missing a required section, or a work item pointing at nothing (`probe-cli.sh`, "work item pointing at nothing": refused, exit 1). So scenario 2's Given must break the files by hand. `shop-knol write schema/decision` with the type's own whole content at `version: 2` is taken (revision 2), and the decision recorded before it is then stale.

**Where it lands:**
- `src/shop_knowledge/answers.py`: `checked`, the check's answer as shown.
- `src/shop_knowledge/cli.py`: `_validate` shows it through `_show` once `_answered` has let the answer through.
- `CLAUDE.md`: the `answers.py` row names `checked`.
- `tests/test_check_the_shops_knowledge_is_sound.py`: three Givens and three Thens. The When, "the user checks the shop's knowledge", exists (`_check`).
- Rule implemented once: none new.

**Decisions** (adrs/0029):
1. **A sound check is shown.** A check that finds no fault shows `sound: true` and `behind:`, a sequence of each stale artifact as `artifact`, `schema_version` and `current`, empty when none is. It exits 0. "Told nothing is wrong" is `sound: true` with nothing on stderr and exit 0.
2. **What is behind its type is never a fault.** It is shown under `behind`, with `sound: true`, exit 0, and nothing on stderr. Scenario 3's "it is not listed as a fault" is stderr empty and exit 0.
3. **Faults are refused as today** (Task 1's path): one line per fault on stderr, nothing on stdout, exit 1. Stale artifacts are not shown beside faults (Review Focus 2).
4. **Scenario 2's Given.** Record a decision and a work item through shop-knol. Then edit both files by hand: the decision loses its Rationale section, and the work item's `decisions` names `decision/nothing`. A comment in the step says no shop-knol command can leave an artifact unfit, since kb refuses it (CLAUDE.md, Step definitions), as `_shop_with_a_file_mangled_by_hand` does with `kb.canonical`. Its Then asserts exactly two stderr lines, one naming the decision at `sections` and one the work item at `decisions/0`.
5. **Scenario 3's Given is made through shop-knol.** Record a decision, read `schema/decision` whole, and write its content back at `version: 2` with `shop-knol write`, dropping the read's identity fields (`id`, `type`, `schema_version`, `revision`, `title`), since a write carries content alone. Its Then asserts `behind` holds exactly the decision, `schema_version: 1` and `current: 2`.
6. **Scenario 1's Given** is a store with a decision recorded through shop-knol. Its Then reads `shown` and asserts `sound` is true and `behind` is empty.

**Reuse:**
- `tests/driver.py`: `start`, `record` and `knol`.
- `tests/conftest.py`: `env`, `shop`, `shown` and "the command reports failure to whatever ran it".
- This module: `_check`, and the `SECTIONS` and `canonical` hand-edit pattern of the slice 1.28 Given.

- [ ] **Step 1: Red.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch7/failing-44.txt; wc -l < .superpowers/batch7/failing-44.txt`: `12`;
  - `-m slice-44`: `3 failed, 59 deselected`, each on its Given.
- [ ] **Step 2: Scenarios 1 to 3** in turn, red then green. Scenario 1 goes red on code at `shown` (empty stdout). Scenario 2 may pass once its steps exist: see it red first on a wrong Then, then put the Then right, and log it (bdd-red-green). Scenario 3 goes red on code at the missing `behind`.
- [ ] **Step 3: Green.**
  - `-m slice-44`: `3 passed, 59 deselected`;
  - `make test`: `9 failed, 53 passed`;
  - GREEN plus `or slice-44`: `53 passed`;
  - the shape check: `2 7 1 0`, nothing listed, `cli.py` about 232;
  - arguments snapshot `TAG=44`: no diff.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 44 green.` in capability form, with:
  - `Evidence:` the three answers, stdout and stderr verbatim;
  - `Open questions:` Review Focus 2, with its reproduction;
  - `Next: slice 47.`

  Set slice 44's Status to `green`.

---

### Task 3: Slice 47, the shop's knowledge base sits beside the shop's work, is started by someone for no stated reason, and is not started twice

**Slice plan entry:** capability, no unknown. Scenarios, in start-a-shop-knowledge-base (`@slice-47`, 5):
1. Starting a knowledge base asks for no reason
2. Starting a knowledge base without saying who is refused
3. The shop's knowledge sits in a place of its own inside the directory it was started in
4. Starting a knowledge base where the directory already holds one is refused
5. Starting a knowledge base inside one the shop already has is refused

**Observable:** see slice 47's entry in the slice plan.

**Why each is red today:**
- Each stops at an undefined step (run 2026-09-27): scenario 1 at its When "... saying who they are and giving no reason", 2 at "the user starts a shop knowledge base in that directory", and 3, 4 and 5 at their Givens.
- Underneath, probed with `probe-init.sh` and `probe-kb.py`:
  - Scenario 4: a second `init` of a started directory exits 0 with nothing on stderr. kb refused Init (`a store is never started over another; '<root>' already has a store inside it`), and `cli._init` drops that answer and runs bootstrap anyway. bootstrap's Creates land in the store and add `schema/shop-artifact-2`, `schema/tag-2` and so on for all eight types. So both Thens fail: nothing is rejected, and the store changed.
  - Scenario 5: `init` of a directory inside the store exits 0 with nothing on stderr. kb refused it (`stores do not nest; '<dir>' is inside the store at '<root>'`), and the answer is dropped.
  - Scenarios 1, 2 and 3 already hold in code:
    - `init` takes no `-m`, and the history holds `initialise store` and eight `Define the shop's <type> type` entries;
    - with `KB_ACTOR` unset, `init` prints `every change must say which role made it, through KB_ACTOR as role or role:execution`, exits 1, and leaves the directory empty;
    - a directory holding `notes.txt` keeps it byte for byte beside a new `kb/`.

**Where it lands:**
- `src/shop_knowledge/bootstrap.py`: `load` gives back each Create's answer as it is made. It does not import `cli`.
- `src/shop_knowledge/cli.py`: `_init` passes Init's answer through `_answered`. Only then does it load the types, passing each answer through `_answered`.
- `tests/test_start_a_shop_knowledge_base.py`: the Givens, Whens and Thens below.
- Rule implemented once: "a kb answer's faults are refused in one way, `cli._answered`", now for Init and bootstrap, the last kb answers that did not keep it (slice 1.29's review).

**Decisions** (adrs/0030):
1. **The types are loaded only after Init answers without a fault.** A Create that is refused stops the load at that type. The answers are passed one by one, as bootstrap makes them, so none is made after a refusal.
2. **The refusals are kb's words** (decision 2 of the batch). Scenario 4's Then asserts stderr carries `already has a store`, and scenario 5's asserts `stores do not nest`. Each also asserts exit 1 and nothing on stdout.
3. **"Everything the shop already knows is still there, unchanged"** means that `shop-knol journal`'s answer, read before the When and after it, is the same. Take it in a fixture local to this module, named for what it holds.
4. **Scenario 5's directory** is `kb/schema` inside the started store: a directory kb made. The Given creates nothing inside the knowledge base, and its comment says it names a directory of kb's layout because no shop-knol command names one (CLAUDE.md, Step definitions).
5. **Scenario 3.** The Given writes a file and a subdirectory with a file in the shop directory before the start. The Then asserts the directory's entries after the start are exactly those plus `kb`, that `kb/store.yaml` exists, and that the earlier files are byte for byte the same. Its comment says no command shows where the store is kept.
6. **Scenario 1.** The When runs `init` with no `-m`, the way today's `_start_saying_who` does. It is its own step text, and it may call the same function. The Then asserts `result` exited 0 and that `shop-knol journal` holds one `create` for each of the shop's eight types (`schema/<type>` for each name in `THE_SHOPS_TYPES`), each with a message that is not empty. The user gave none. Its first Then, "the shop's knowledge base is started", asserts exit 0 and that `shop/kb/store.yaml` exists; a comment says no command shows where the store is kept.
7. **Scenario 2.** The Given is the conftest's "the user has not said which role they are". The Then asserts stderr is the one `_NO_ROLE` line, `every change must say which role made it`, and that `shop` holds no `kb/`.
8. **Not a scenario, settled by the rule:** after this task, `init` of a directory that does not exist is refused in kb's words, `a store is started in a directory that exists; '<dir>' does not`, with exit 1 (`probe-kb.py`). Today it exits 0 having started nothing. Log it as evidence.

**Reuse:**
- This module: `_an_empty_directory`, `_start_saying_who` (the When "..., saying who they are", used by scenarios 3, 4 and 5) and `THE_SHOPS_TYPES`.
- `tests/conftest.py`: `shop`, `env`, `_no_role`, "the command reports failure to whatever ran it" and `shown`.
- `tests/driver.py`: `start` and `knol`.

- [ ] **Step 1: Red.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch7/failing-47.txt; wc -l < .superpowers/batch7/failing-47.txt`: `9`;
  - `-m slice-47`: `5 failed, 57 deselected`, each on an undefined step.
- [ ] **Step 2: Scenarios** in feature order, red then green. Scenarios 1, 2 and 3 are expected to pass once their steps exist: see each red first on a wrong Then, then put the Then right, and log it. Scenario 4 goes red on code at "rejected because" (exit 0, stderr empty). Scenario 5 goes red on code the same way.
- [ ] **Step 3: Green.**
  - `-m slice-47`: `5 passed, 57 deselected`;
  - `-m slice-4`: `1 passed`;
  - `make test`: `4 failed, 58 passed`;
  - GREEN plus `or slice-44 or slice-47`: `58 passed`;
  - the shape check: `2 7 1 0`, nothing listed, `cli.py` about 234 to 235;
  - arguments snapshot `TAG=47`: no diff;
  - `mkdir -p .superpowers/batch7/s47 && cd .superpowers/batch7/s47 && KB_ACTOR=a ../../../.venv/bin/shop-knol init nope; echo "exit $?"`: kb's one line, `exit 1`.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 47 green.` in capability form, with:
  - `Evidence:` the two refusals and the `init nope` line, verbatim;
  - `Open questions:` Review Focus 5 with its reproduction; also that a Create refused mid-load leaves a store with only some types, which no scenario reaches;
  - `Next: slice 48.`

  Set slice 47's Status to `green`.

---

### Task 4: Slice 48, one bad change in a batch leaves the shop untouched

**Slice plan entry:** capability, no unknown. Scenario, in make-several-changes-at-once (`@slice-48`, 1): One bad change in a batch leaves the shop untouched.

**Observable:** a user applies a batch whose second change does not fit its type. The batch is refused with every fault, and none of it is in the shop.

**Why it is red today:** it stops at its Given, `StepDefinitionNotFoundError: Given "a batch whose second change does not fit its type"` (run 2026-09-27). Underneath, the code already holds (`probe-48.sh`). A batch that records the decision, then writes the work item with `owner: 3` and `decisions: [decision/nothing]`, prints two lines, `work-item/reprice-the-dairy-shelf at owner: 3 is not of type 'string'` and `work-item/reprice-the-dairy-shelf at decisions/0: a link must land on a node ...`, and exits 1. After it, `read decision/price-reviews-happen-weekly` is refused, the work item shows no references, and the history is unchanged. kb v0.2.0's Apply is all or nothing.

**Where it lands:**
- `tests/test_make_several_changes_at_once.py`: one Given and three Thens.
- Nothing under `src/`.
- Rule implemented once: none.

**Decisions:**
1. **The batch.** The first change is scenario 1's, recording the decision. The second writes the work item with two faults of its type, `owner` and `status` given as numbers, so both are plainly "does not fit its type" and "every fault" is two lines. The probe used `owner` and a link to nothing; `status` is a type fault of the same kind as the probed `owner`, and kb reported two schema faults of one change together in `probe-kb.py`.
2. **"Rejected because a change in it does not fit its type"**: exit 1, nothing on stdout, and every stderr line names the work item with a place.
3. **"None of the changes are in the shop"**: `shop-knol read` of the decision is refused, and `shop-knol read` of the work item shows no references and no `owner` or `status`.
4. **"Every fault, not only the first"**: exactly two stderr lines, one at `owner` and one at `status`.

**Reuse:**
- This module: the Background `_shop_with_a_work_item`, the When `_apply`, `WORK_ITEM`, `WEEKLY` and `SECTIONS`.
- `tests/driver.py`: `knol`.

- [ ] **Step 1: Red.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch7/failing-48.txt; wc -l < .superpowers/batch7/failing-48.txt`: `4`;
  - `-m slice-48`: `1 failed, 61 deselected`, on the Given.
- [ ] **Step 2: The scenario.** It is expected to pass once its steps exist: see it red first on a wrong Then, then put the Then right, and log it.
- [ ] **Step 3: Green.**
  - `-m slice-48`: `1 passed`;
  - `make test`: `3 failed, 59 passed`;
  - GREEN plus `or slice-44 or slice-47 or slice-48`: `59 passed`;
  - the shape check is unchanged from Task 3;
  - arguments snapshot `TAG=48`: no diff.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 48 green.` in capability form, with:
  - `Evidence:` stderr verbatim, and the two reads after;
  - `Open questions:` Review Focus 1 with its reproduction;
  - `Next: slice 48.1.`

  Set slice 48's Status to `green`.

---

### Task 5: Slice 48.1, a whole read the steps make is driven one way

**Slice plan entry:** enabling, no unknown. Check:
- the same failing scenarios as before the slice (3 failed, 59 passed);
- `grep -c "def _whole" tests/*.py | grep -v ":0"` gives no line;
- `grep -c "^def whole" tests/driver.py` gives `1`.

**Observable:** the steps that read an artifact whole find that read in the driver, beside `record`.

**Why the check fails today:** `_whole(env, name)` is written word for word in `tests/test_revise_what_the_shop_knows.py:30` and `tests/test_add_a_step_to_a_process.py:34`. Each runs `read <name> --whole`, asserts exit 0 with stderr as the message, and loads stdout. The driver has no whole read. Task 6 needs three more.

**Where it lands:**
- `tests/driver.py`: `whole(env, name)`, with the behaviour the two copies share, and a docstring.
- The two modules import it, and their `_whole` goes. The `before` fixtures and every step that called `_whole` call it.
- Nothing under `src/` changes.
- Rule implemented once: `driver.py` is the one place that drives shop-knol the way a user does (CLAUDE.md, Step definitions).

- [ ] **Step 1: Baseline.** `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch7/failing-48.1.txt; wc -l < .superpowers/batch7/failing-48.1.txt`: `3`. The first grep gives two lines, the second `0`.
- [ ] **Step 2: Move** the read into the driver and delete both copies.
- [ ] **Step 3: Check.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort | diff - .superpowers/batch7/failing-48.1.txt && echo same`: `same`;
  - `make test`: `3 failed, 59 passed`;
  - `-m "slice-24 or slice-40"`: `4 passed`;
  - the two greps: no line, and `1`;
  - the shape check is unchanged.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 48.1 green.`, then `Check:` with each output, `Surprised by:`, and `Next: slice 49.` Set slice 48.1's Status to `green`.

---

### Task 6: Slice 49, the shop's roles and tags hold their shape

**Slice plan entry:** capability, no unknown. Scenarios, in start-a-shop-knowledge-base (`@slice-49`, 2):
1. A role keeps its harness fields apart from its shop identity
2. Anything the shop knows can be tagged

**Observable:** a user records a role, and its harness fields sit in one named group and its shop identity in another. They tag a decision with a tag, so the decision names it while the tag's description is held once, on the tag.

**Why each is red today:**
- Each stops at its Given (run 2026-09-27): "a shop knowledge base" and "a shop knowledge base holding a tag "pricing" with a title and a description".
- Underneath, the code already holds (`probe-cli.sh`, "role" and "tag"). The role's whole read shows `harness` (`name`, `description`, `tools`, `model`) and `shop` (`responsible_for`, `answers_to`) as two mappings. A decision recorded with `tags: [tag/pricing]` reads whole with `tags: [tag/pricing]` and no description, and the tag's whole read holds the description.

**Where it lands:**
- `tests/test_start_a_shop_knowledge_base.py`: two Givens, two Whens and four Thens.
- Nothing under `src/`. Rule 5 holds: the types are data, and only the steps know the role's and tag's fields.
- Rule implemented once: none.

**Decisions:**
1. **"A shop knowledge base"** is a store started through `start`. It is its own step text in this module, since only this feature uses it.
2. **The role** is recorded with `record`, holding `harness` (name, description, tools) and `shop` (responsible_for, answers_to) and a section, the same shape `_holds_the_seven` records.
3. **"Kept as one named group"**: the whole read, through `driver.whole` (Task 5), holds `harness` as a mapping equal to what was recorded, and none of its keys at the top level. The same holds for `shop`.
4. **The tag** is recorded with title "Pricing" and a description, giving `tag/pricing`. "Tags a decision with pricing" records a decision carrying `tags: [tag/pricing]`: the Given holds no decision to write.
5. **"The decision names that tag"**: the decision's whole read has `tags == ["tag/pricing"]`. **"The tag's description is held once, on the tag"**: the tag's whole read holds it, and the description's text appears nowhere in the decision's whole read, as dumped.

**Reuse:**
- `tests/driver.py`: `start`, `record`, `whole` (Task 5) and `knol`.
- `tests/conftest.py`: `env` and `shop`.

- [ ] **Step 1: Red.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch7/failing-49.txt; wc -l < .superpowers/batch7/failing-49.txt`: `3`;
  - `-m slice-49`: `2 failed, 60 deselected`, each on its Given.
- [ ] **Step 2: Scenarios 1 and 2.** Both are expected to pass once their steps exist: see each red first on a wrong Then, then put the Then right, and log it.
- [ ] **Step 3: Green.**
  - `-m slice-49`: `2 passed`;
  - `make test`: `1 failed, 61 passed`, the one left being slice 50's;
  - GREEN plus `or slice-44 or slice-47 or slice-48 or slice-49`: `61 passed`;
  - the shape check is unchanged;
  - arguments snapshot `TAG=49`: no diff.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 49 green.` in capability form, with:
  - `Evidence:` both whole reads;
  - `Open questions:` whatever the scenarios leave silent, each with a reproduction;
  - `Next: slice 50.`

  Set slice 49's Status to `green`.

---

### Task 7: Slice 50, publish a role as an agent

**Slice plan entry:** capability, no unknown. Scenario, in publish-what-the-shop-knows (`@slice-50`, 1): The user publishes a role as an agent.

**Observable:** a user publishes a role into a directory and finds an agent whose heading block is the role's harness fields and whose body is its prose.

**Why it is red today:**
- It stops at its When, `StepDefinitionNotFoundError: When "the user publishes the role as an agent into a directory"` (run 2026-09-27).
- Underneath, `shop-knol render agent role/stock-keeper --to o` is refused: `shop-knol render: argument renderer: invalid choice: 'agent' (choose from 'diagram', 'markdown', 'skill')`, exit 1. No agent renderer exists.

**Where it lands:**
- `src/shop_knowledge/renderers/agent.py`: `render(client, name) -> Rendered`. It reads the role through `source.whole`, gives back `refused(faults)` when the read has faults, and names the file with `source.slug`, as `skill.py` and `diagram.py` do (adrs/0014).
- `src/shop_knowledge/renderers/__init__.py`: `"agent": agent.render` in `RENDERERS`. That makes `agent` a choice of `render`, with no change to `arguments.py` or `cli.py`.
- The section layout `markdown._sections` makes today moves to a module of its own under `renderers/`, used by both the markdown and agent renderers, with a row in CLAUDE.md's module map. This is the refactor step, after green, under bdd-red-green. The markdown scenario (`-m slice-20`) must still pass byte for byte.
- `tests/test_publish_what_the_shop_knows.py`: the When and the Then.
- Rules implemented once: 6 (the renderer reads and gives back; `cli._write` writes), and 5 (only the agent renderer knows a role's `harness` and `sections`).

**Decisions** (adrs/0031):
1. **Path**: `.claude/agents/<name>.md` under `--to`, where `<name>` is the role's name without its kind (`stock-keeper`). The spec: "`.claude/agents/<name>.md`".
2. **Heading block**: `---`, the `harness` mapping written with `kb.content.dumps`, `---`, then a blank line, as the skill's heading block is written. The spec: "with the harness field group as frontmatter".
3. **Body**: the role's sections laid out as the markdown page lays out its sections, each a heading and its body, with sections inside a level down, starting at level 1. No title heading comes before them. The spec: "the prose sections as the body".
4. **A missing `harness`** gives an empty heading block, not a refusal (Review Focus 3). No harness limit is checked (Review Focus 4).
5. **The Then** reads the one file under `target`. It splits the heading block from the body, loads the heading block with `kb.content.loads` and asserts it equals `ROLE["harness"]`. It asserts the body holds each of `ROLE["sections"]`' titles as a heading and its body text, and nothing from `ROLE["shop"]`. It also asserts the directory holds that one file and no other.

**Reuse:**
- This module: the Background `_shop_with_a_process_and_a_role`, `ROLE`, the fixture `target`, and the pattern of `_publish_as_a_skill` for the When.
- `tests/driver.py`: `knol`.

- [ ] **Step 1: Red.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch7/failing-50.txt; wc -l < .superpowers/batch7/failing-50.txt`: `1`;
  - `-m slice-50`: `1 failed, 61 deselected`, on the When.
- [ ] **Step 2: The scenario**, red then green. Its first red on code is `invalid choice: 'agent'`. Then refactor the shared section layout out of `markdown.py`.
- [ ] **Step 3: Green.**
  - `-m slice-50`: `1 passed`;
  - `-m "slice-17 or slice-18 or slice-19 or slice-20"`: `4 passed`;
  - `make test`: `62 passed`, and make ends without an error;
  - GREEN plus `or slice-44 or slice-47 or slice-48 or slice-49 or slice-50`: `62 passed`;
  - the shape check: `2 7 1 0`, nothing listed, `cli.py` unchanged from Task 3;
  - `grep -c "sections" CLAUDE.md`: the new module's row is there;
  - arguments snapshot `TAG=50`, diffed against `help-now.txt`: only `agent` added to `render`'s choices, in its usage line and `render -h`.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 50 green.` in capability form, with:
  - `Evidence:` the agent file verbatim;
  - `Open questions:` Review Focus 3 and 4, each with its reproduction;
  - `Next: slice 50.1.`

  Set slice 50's Status to `green`.

---

### Task 8: Slice 50.1, what an argument means is said once, and nothing is named for a use it does not have

**Slice plan entry:** enabling, no unknown. Check:
- the same failing scenarios as before the slice (none: 62 passed);
- `grep -cE 'or ""|is None|Path\(' src/shop_knowledge/kb_requests.py` gives `0`;
- `grep -c "Path(args.root)" src/shop_knowledge/cli.py` gives `0`;
- `.venv/bin/python -c "import shop_knowledge.cli as c, shop_knowledge.arguments as a; p=a.command_parser(); assert list(c._HANDLERS) == list(p._subparsers._group_actions[0].choices)"` succeeds;
- `grep -c "def locator" src/shop_knowledge/kb_requests.py` gives `0`, and neither the module's docstring nor its CLAUDE.md row names a helper `cli` does not call;
- `shop-knol -h` and every command's `-h` give byte for byte what they gave before.

**Observable:** a reader finds each argument's type and default where the argument is declared, and the handler table in the order the help lists the commands. The request module names only the helper the command line uses.

**Why the check fails today** (run 2026-09-27):
- The first grep gives `4`: `refs_request`'s `args.depth is None` and two `or ""`, `search_request`'s `or ""`, and `init_request`'s `Path(args.root)`. The last of these matches `Path\(` alone.
- `cli._init` has `Path(args.root)`, and the second grep gives `1`.
- The order assertion fails. The parser declares `init create read write append validate apply journal list refs search render delete snapshot`, and `_HANDLERS` lists `init create append delete read write validate apply journal list refs search snapshot render`.
- `kb_requests.locator` is public, and the module's docstring and CLAUDE.md's row say it serves `cli._read`, which calls only `is_whole` (`grep -n "kb_requests\.\(locator\|is_whole\)" src -r`: one line).

**Where it lands:**
- `src/shop_knowledge/arguments.py`: defaults and types.
- `src/shop_knowledge/kb_requests.py`: the requests map arguments to fields as given. `locator` becomes the module's own, and the docstring changes.
- `src/shop_knowledge/cli.py`: `_init` uses the root as parsed, and `_HANDLERS` follows the parser's order.
- `CLAUDE.md`: the `kb_requests.py` row names `is_whole` alone for `cli._read`.
- Rule implemented once: the module map's split, where `arguments.py` holds every command's arguments and `kb_requests.py` only turns them into requests.

**Decisions** (adrs/0032):
1. `refs --via` and `--type`, and `search --type`, default to `""`, as `journal`'s flags do. `refs --depth` defaults to `1`, and its help already says "(one when not said)". `init`'s root is typed as a path. `read --resolve` keeps `None`, since there "not given" means a glance and not a whole read.
2. **Help does not change.** argparse's default help formatter does not print defaults, and a `type` does not show in help. The snapshot proves it. The parser's command order stays as users see it, and `_HANDLERS` follows it.
3. **Behaviour does not change.** Every answer and refusal stays as it was, including `refs --depth -1` answering `[]` (a question in the slice 42.1 log).

- [ ] **Step 1: Baseline.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch7/failing-50.1.txt; wc -l < .superpowers/batch7/failing-50.1.txt`: `0`;
  - arguments snapshot with `TAG=50.1-before`;
  - the check's greps and the assertion fail as above.
- [ ] **Step 2: Change** as decided.
- [ ] **Step 3: Check.**
  - `make test`: `62 passed`;
  - each grep gives `0`, the assertion succeeds, and the docstring and row name `is_whole` alone;
  - arguments snapshot `TAG=50.1`, diffed against `50.1-before`: no diff;
  - the shape check: `2 7 1 0`, nothing listed, `cli.py` within a line of Task 7's.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 50.1 green.`, then `Check:` with each output, `Surprised by:`, and `Next: slice 50.2, the fifth architecture review, which runs after this batch's final review and before any further plan (adrs/0011).` Set slice 50.1's Status to `green`.

---

## After the batch

Slice 50.2, the fifth architecture review, is not a task here. Architecture reviews run before planning, never inside a plan (adrs/0011). It follows the eight slices of this batch and has three things to weigh:
- how `cli.py` held under 250 through the check and the start;
- whether the agent renderer and the shared section layout keep rule 5;
- whether a bump of kb's pin to the tag carrying kb slice 97 has landed, closing the empty batch's traceback.

Every scenario in `features/` is then green. What remains is the QUESTION FOR THE SPEC lines in the slice plan's log, for formulating-features and the human.
