# shop-knowledge batch 5: slices 28.1, 28 (the pipe) and 30

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`. A capability task follows `shopsystem-bdd:bdd-red-green` over its scenarios. An enabling task is done when its check gives the required result. bdd-red-green's stop conditions, hand-back and checkpoint apply, and they override any step here that conflicts with them.

**Goal:** Three slices in plan order, which pick up after batch 4's hand-back at slice 28:
- the command line's arguments move out of `cli.py`, so the handlers have room under the 250-line limit (28.1);
- a decision can be piped into `create` (the rest of slice 28);
- what the shop has recorded can be listed (30).

**Architecture:** shop-knowledge is the Python package `shop_knowledge`. Its `shop-knol` command calls kb through `kb.client.connect` with `kb.contract.kb_pb2` messages, and reads and prints YAML 1.2 through `kb.content`. kb is `shopsystem-kb` v0.2.0, installed from its git tag into this checkout's `.venv`. It is never edited here. `CLAUDE.md` sets the shape the code is held to. Its module map says where each change lands, and each task names the rule it implements once.

**This plan carries no code** (adrs/0011). The implementer writes every step definition and every line under `src/` red-green in the execution session. What each task gives instead:
- the slice and its scenarios or check;
- why each is red today, found by running it in this checkout;
- where the change lands, and which rule it implements once;
- the decisions the spec leaves open, each resting on a passage;
- what existing steps and fixtures to reuse, by name;
- the commands, with counts taken from the tags;
- the checkpoint to log.

**Tech Stack:** Python 3.11, setuptools (src layout), kb v0.2.0 (protobuf contract, in-process client), pytest 8 + pytest-bdd 8, `jsonschema`.

**Spec:** `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md`, section The CLI (the command table: `create <type> --from <file or ->`, `list --type <type> [--where k=v ...] [--ids]`). `CLAUDE.md`. Slice plan `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`:
- slices 28, 28.1 and 30;
- the slice 28 HAND-BACK entry and the RE-SLICE entry after it, at the end of its log.

Batch 4's plan, `docs/superpowers/plans/2026-09-27-shop-knowledge-batch4-implementation.md`, Tasks 8 and 9, holds the decisions this plan carries over. They are restated below so that this plan stands alone. kb's contract: `.venv/lib/python3.11/site-packages/kb/contract/kb.proto` (`ListRequest`, `ListResponse`, `Stub`).

## Global Constraints

- Feature files are read-only. Any diff under `features/` is a stop condition, and that includes tag lines: slice 28's pipe scenario keeps `@slice-28`.
- Code only what a scenario asserts (bdd-red-green). Where a scenario is silent, the code is silent too, and the silence goes into the checkpoint as an open question.
- kb is v0.2.0 in `.venv` and is never edited here. "shop-knowledge never touches kb's files or git. It calls the contract through the in-process client." A kb change a slice needs is not coded. It is logged in the slice plan as a request to bump the pin, and the slice stops. The probes for this plan found that none of these slices needs one.
- Every rule in `CLAUDE.md` holds at the end of every task, and each is implemented once:
  - a kb answer's faults are refused only through `cli._answered`;
  - a refusal is printed only by `main`, through the one printer, from a `Refused`;
  - a user's file, or the text piped in instead of one, is read only in `cli._document`;
  - files are written only by `cli._write`;
  - no module runs over 250 lines. If a task would take one past 250, stop and hand back.
- "shop-knol never shows a traceback." "Errors are printed as returned by kb, with artifact, path, and message, and exit non-zero." "Every mutating command requires an actor and `-m`." "Output is YAML by default and `--json` for the same structure."
- Work on `main` in this checkout (adrs/0009). `make test` runs the suite in `.venv`. While scenarios are red, its last line is make's own `Error 1`, so read pytest's summary line above it. Every command below runs from the checkout's root.
- Scratch files for checks go under `.superpowers/batch5/`. `.superpowers/` is in `.git/info/exclude`. `.superpowers/batch5/failing-now.txt` already holds the 31 failing ids from the planning run. Each task still writes its own baseline.
- Commits: `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`. The message ends with the Co-Authored-By line of the model that made the commit, e.g. `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`. Each task makes one commit, holding the slice's code, its steps and its checkpoint.
- pytest-bdd prints `PytestRemovedIn10Warning`s, two for each `target_fixture` step. That is the baseline, not a fault.
- **Counts.** The suite has 62 scenarios. `pytest --collect-only -q -m slice-N` selects 3 for slice 28 (two already green, one red), 3 for slice 30, and none for slice 28.1. Failed and passed after each task:

  | after | failed | passed |
  |---|---|---|
  | before Task 1 (run 2026-09-27) | 31 | 31 |
  | 28.1 | 31 | 31 |
  | 28 | 30 | 32 |
  | 30 | 27 | 35 |

  After Task 3, the 27 left are exactly those tagged 32 or later. `-m "slice-32 or slice-34 or slice-36 or slice-38 or slice-40 or slice-42 or slice-44 or slice-47 or slice-48 or slice-49 or slice-50"` collects 27.
- **GREEN** is the set of slices green before this batch. It is selected by `-m "slice-1 or slice-1.17 or slice-1.24 or slice-1.27 or slice-1.28 or slice-4 or slice-15 or slice-16 or slice-17 or slice-18 or slice-19 or slice-20 or slice-22 or slice-24 or slice-26"`, which gives 29 passed (run 2026-09-27). Each task adds its own tag to the expression, and every scenario it selects must pass. Slice 28's two green scenarios join the expression with slice 28's tag in Task 2.
- **The shape check** is run at the end of every task:

  ```bash
  grep -c "_refuse(" src/shop_knowledge/cli.py; grep -c "if response.faults:" src/shop_knowledge/cli.py; grep -c "read_text" src/shop_knowledge/cli.py; grep -cE "argparse|add_parser|add_argument" src/shop_knowledge/cli.py; find src -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'; grep -lE "print\(|open\(|write_text" src/shop_knowledge/renderers/*.py
  ```

  Expected: `2`, `1`, `1`, then `0` from Task 1 on (it is `29` before Task 1: the argparse import, the parser's constructor, and every `add_parser`/`add_argument` line), no module over 250 lines, and no renderer listed. `_validate` raising its own `Refused` is the one exception CLAUDE.md names, until slice 42.2.
- **The arguments snapshot** is how Task 1 shows that behaviour no scenario pins did not change, and how Tasks 2 and 3 show what they added:

  ```bash
  for c in "" init create read write validate apply journal render; do .venv/bin/shop-knol $c -h; echo "exit $?"; done > .superpowers/batch5/help-$TAG.txt 2>&1; .venv/bin/shop-knol nosuch >> .superpowers/batch5/help-$TAG.txt 2>&1; echo "exit $?" >> .superpowers/batch5/help-$TAG.txt
  ```

  Set `TAG` to a name for the run, e.g. `before`, `28.1` or `30`. Task 1 compares `before` with `28.1`, and the diff must be empty. Task 3 adds `list` to the loop, since `list -h` exists only after it.

## Decisions that hold across the batch

1. **The arguments sit apart from the handlers** (slice 28.1, adrs/0021). A new module, `src/shop_knowledge/arguments.py`, builds the parser. It holds every subparser with its flags and help, `prog="shop-knol"`, and the renderer names from `RENDERERS` as `render`'s choices. It knows no handler.
   - `cli.py` keeps `main`, one handler per command, `_run`, `_by`, `_MUTATING`, `_client`, `_document`, `_answered`, `_show`, and the printer.
   - `cli.py` finds a command's handler by its name (`args.command`, the subparsers' existing `dest`) in one table of its own, in place of `set_defaults(handler=...)`.
   - A new command adds its arguments to `arguments.py`, and its handler and one table entry to `cli.py`.
   - `arguments.py` is named for what it owns, as `answers.py` is (adrs/0017). Its row in CLAUDE.md's module map: it owns "`shop-knol`'s arguments: one subparser per command, its flags and help". It never holds "handlers, kb calls, printing".
   - The `cli.py` row drops "its arguments" and keeps the rest.
2. **A pipe is read where a file is read** (slice 28). The spec's command table gives `--from <file or ->`. `cli._document` reads standard input when the source is `-`, and it checks the text against its shape exactly as it checks a file. So `create`, `write` and `apply` all take a pipe. See Review Focus 5 for `apply`.
3. **What `list` shows** (slice 30, carried from batch 4 Task 9):
   - By default, a sequence with one entry per artifact: `id`, `type`, `title`, then the stub's fields. This is the shape `answers.glance` gives a reference, without `field`.
   - With `--ids`, the sequence of names and nothing else.
   - There is no wrapper key: the answer to "list" is the list itself.

## Review Focus

writing-plans asks for a test in the owning task for each line here. In this project tests are scenarios, and feature files are the human gate, so no test is added. Instead, each line goes into the owning task's checkpoint as a `QUESTION FOR THE SPEC`, with its reproduction, run after that task. Lines 1 to 4 were raised in batch 4 and are still open. They are restated with their reproductions.

1. **An empty batch ends in a traceback** (owner: Task 2, whose `_document` change lets `apply` read a pipe as well as a file). This was found while probing for this plan. In a started knowledge base, `printf 'changes: []\n' > b.yaml; shop-knol apply --from b.yaml -m why` prints a traceback that ends in `subprocess.CalledProcessError` from kb's `store.commit` (git has nothing to commit) and exits 1. That breaks rule 4. The fault is in kb v0.2.0, which should refuse an Apply with no operations, so it is logged as a request to bump the pin once kb refuses it. shop-knol could instead refuse it itself, with `minItems: 1` on the batch shape's `changes`. No scenario pins either choice, so the choice is the spec's. A user would expect one plain line saying the batch holds no change.
2. **`list --ids` is YAML, not bare lines** (owner: Task 3). Everything printed goes through `kb.content`, which writes a top-level sequence as `- decision/a` lines. So `shop-knol list --type decision --ids | xargs -n1 shop-knol read` passes `-` as a name. The scenario says "names only, to feed another command". A user would expect one name to a line, or a `--json` array.
3. **"Superseded" is a status the user writes, not the link** (owner: Task 3). kb's List narrows by an artifact's own fields. Reproduction after Task 3: record two decisions, the second with `supersedes` pointing at the first and neither with a status. Then `shop-knol list --type decision --where status=superseded` answers an empty sequence. A user would expect the link to count.
4. **argparse still refuses in its own way** (owner: Task 3). Reproductions after Task 3: `shop-knol list` with no `--type`, and `shop-knol list --type decision --json`. Each prints argparse's usage on stderr and exits 2, where rule 4 says one plain line and exit 1. Task 1 keeps this behaviour byte for byte (the arguments snapshot). Changing it is not a refactor.
5. **`apply` takes a pipe the spec does not give it** (owner: Task 2). The spec's table says `create`, `write` and `append` take `--from <file or ->`, and `apply` takes `--from <batch>`. Reading the pipe once, in `_document`, gives all three that take `--from` the pipe. Reproduction after Task 2: `printf 'changes: []\n' | shop-knol apply --from - -m why` reaches kb (and Review Focus 1). A user would expect either every `--from` to take `-` or `apply` to refuse it plainly.

---

### Task 1: Slice 28.1, the command line's arguments sit apart from its handlers

**Slice plan entry:** enabling, no unknown. Check:
- the same 31 failing scenarios as before the slice (31 failed, 31 passed);
- the arguments snapshot is byte for byte the same before and after, exit codes included;
- `grep -cE "argparse|add_parser|add_argument" src/shop_knowledge/cli.py` gives 0;
- `wc -l < src/shop_knowledge/cli.py` is under 210;
- the module that now holds the arguments holds no handler, no kb call and no `print`, and CLAUDE.md's module map has a row for it.

**Observable:** slice 28's pipe and slice 30's list each add a few lines to the module holding the handlers without it reaching the 250-line limit.

**Why the check fails today:**
- `cli.py` is 250 lines;
- the grep gives 29 (run 2026-09-27): `import argparse` on line 6, and the constructor and every `add_parser`/`add_argument` line inside `_parser` (lines 50 to 100, 51 lines with its closing `return`);
- CLAUDE.md has no row for an arguments module.

Moving `_parser` and its import out, and adding a name-to-handler table, leaves `cli.py` near 200 lines. That was estimated by reading, not by building. That is about 48 lines free for slice 28 (about 4) and slice 30 (a handler of about 8). Slices 32 to 42 add six more commands. Slice 30.1, the review, decides whether the handlers need a further split before them.

**Where it lands:**
- New `src/shop_knowledge/arguments.py`: the parser, moved whole (decision 1). Its docstring says what it owns.
- `src/shop_knowledge/cli.py`:
  - `main` builds the parser from `arguments`;
  - `_run` looks the handler up by `args.command` in the table (decision 1);
  - `import argparse` goes, and `RENDERERS` stays for `_render`.
- `pyproject.toml`'s entry point `shop-knol = "shop_knowledge.cli:main"` is unchanged.
- `CLAUDE.md`: the module map gains the `arguments.py` row and the `cli.py` row drops "its arguments" (decision 1). Nothing else in CLAUDE.md changes: `cli._document` and `cli._answered` keep their names and module.
- Rule implemented once: the module map's "a new concern gets a new module and a row here". Declaring the arguments is one concern, and slice 30 and every later command add theirs there.

**Decisions:**
- The parser is built by one public function, since `cli.py` calls it. Its name reads as what it gives.
- The table maps each command's name to its handler. It is one table, beside `_MUTATING`, which already keys on `args.command`, so that both say which commands exist in the same terms.
- `_MUTATING` stays in `cli.py`. It decides whether the actor is asked (adrs/0020), which is the environment's concern, not the arguments'.
- No handler, helper or answer moves in this slice. Anything else the check does not need is left for slice 30.1.

**Reuse:** nothing in `tests/` changes. No test imports `cli._parser` (`grep -rn "_parser\|cli\." tests/` finds none). All 31 passing scenarios guard the move, since each drives `shop-knol` as a subprocess.

- [ ] **Step 1: Baseline.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch5/failing-28.txt; wc -l < .superpowers/batch5/failing-28.txt`: `31`.
  - Run the arguments snapshot with `TAG=before`.
  - Run the shape check (expected `2 1 1 29`, nothing listed) and `wc -l < src/shop_knowledge/cli.py` (`250`).
- [ ] **Step 2: Move** the parser to `arguments.py`, and put the table in `cli.py`.
- [ ] **Step 3: Map.** Edit the CLAUDE.md rows.
- [ ] **Step 4: Check.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort | diff - .superpowers/batch5/failing-28.txt && echo same`: `same`;
  - `make test`: `31 failed, 31 passed`;
  - the arguments snapshot with `TAG=28.1`, then `diff .superpowers/batch5/help-before.txt .superpowers/batch5/help-28.1.txt`: no output;
  - the shape check: `2 1 1 0`, nothing listed;
  - `wc -l < src/shop_knowledge/cli.py`: under 210;
  - `grep -cE "print|Request|connect|_pb2|handler" src/shop_knowledge/arguments.py`: `0` (no kb call, no printing, and no handler bound with `set_defaults(handler=...)`);
  - `grep -c "arguments.py" CLAUDE.md`: `1`.
- [ ] **Step 5: Checkpoint and commit.** Log `- 2026-09-27 slice 28.1 green.`, then:
  - what moved and the new module's line count;
  - `Check:` with each output;
  - `Surprised by:`;
  - `Next: slice 28, its pipe scenario.`

  Set slice 28.1's Status to `green`. adrs/0021 is already committed with this plan. If the move had to differ from it, amend it.

---

### Task 2: Slice 28, the pipe: the user pipes a decision in instead of naming a file

**Slice plan entry:** capability, no unknown. Slice 28's other two scenarios went green in batch 4. This task finishes the slice. Scenario, in record-a-decision (`@slice-28`, 3 selected, 1 red):
- The user pipes a decision in instead of naming a file

**Observable:** a user pipes a decision from another command into `create` with `--from -`, and the shop holds it as if it had come from a file.

**Why it is red today:**
- It stops at its first step: `StepDefinitionNotFoundError: Given "a decision produced by another command"`. None of its three steps is defined.
- Underneath that, `tests/driver.py`'s `knol` takes no `input`. Batch 4's decision 6 gave it `cwd` then, but not yet `input`.
- Underneath that, `create decision --from -` with text on stdin answers `-: No such file or directory` on stderr and exits 1 (probed 2026-09-27). `_document` opens `-` as a path, the operating system refuses it, and `_run` turns the `OSError` into a fault.

Batch 4's attempt at the steps is in `.superpowers/batch4/s28-scenario1-attempt.diff`. Its Then asserts a deliberately wrong title so as to see red. Read it as a sketch, not as code to apply.

**Where it lands:**
- `cli._document` (decision 2). When the source is `-`, it reads standard input in place of the file. The read stays inside the existing `try`, so text that is not UTF-8 or not canonical is refused the way a file's is, with no code of its own.
- `tests/driver.py`: `knol` takes `input`, the text piped to the subprocess, and passes it to `subprocess.run`. Nothing else in the driver changes.
- `tests/test_record_a_decision.py`: the scenario's three steps. They sit beside the scenarios they serve, since no other feature uses them.
- Rule implemented once: "A file a user gives is read, and checked against its shape, in one place, `cli._document`". The pipe is that same place's other source.

**Decisions:**
1. **A fault about piped text names its source `standard input`, not `-`** (carried from batch 4 Task 8, decision 1). The printer prints `<artifact> at <path>: <message>`, and `standard input at sections: …` says where the fault is in words a user reads. So the name `_document` gives the source in a fault, and in the shape check's violations, is `standard input` when the source is `-`. That covers `UnicodeDecodeError`, `NotCanonical` and `shape.violations`. No scenario asserts the wording, so the checkpoint shows one real line (Step 4).
2. **"Just as if it had come from a file"** (batch 4 Task 8, decision 2). The Then asserts that `create` exits 0 and prints an `id`. It then reads that id with `read --whole` and finds the title and both sections as piped, at revision 1, which is what "the shop holds the decision under that name" checks for a file.
3. **"Produced by another command"**: the Given gives the text another command would print, the decision's content through `kb.content.dumps`. It is not a file on disk. The When pipes that text to `create decision --from - -m <why>` with `KB_ACTOR` as `env` sets it ("saying who they are and why").

**Reuse:**
- `tests/test_record_a_decision.py`: `OLDER` for the content (the scenario's Background records nothing, so its title is free). Also the shape of `_reads_back_by_name` and `_first_version` for the Then's read.
- `tests/driver.py`: `knol`, with its new `input`.
- `tests/conftest.py`: `env`, and Given "a shop knowledge base holding the shop's types" from the Background.
- The When gives `result`.

- [ ] **Step 1: Red.** `.venv/bin/python -m pytest -q -m slice-28`: `1 failed, 2 passed, 59 deselected`. The failure is the undefined Given.
- [ ] **Step 2: Steps.** Define the three steps and give `knol` its `input`. Confirm the scenario goes red for the reason above (`-: No such file or directory`), then on a wrong Then once `_document` reads the pipe.
- [ ] **Step 3: Green.**
  - `-m slice-28`: `3 passed, 59 deselected`;
  - `make test`: `30 failed, 32 passed`;
  - GREEN plus `or slice-28`: `32 passed`;
  - the shape check: `2 1 1 0`, nothing listed;
  - `grep -n stdin src/shop_knowledge/cli.py` shows lines inside `_document` only;
  - `wc -l < src/shop_knowledge/cli.py`: at most 250;
  - the arguments snapshot with `TAG=28`, diffed against `help-28.1.txt`: no output.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 28 green.` in capability form, with:
  - `Evidence:` the piped decision's `create` answer and its `read --whole`; and the stderr of `printf 'title: x\nsections: 3\n' | shop-knol create decision --from - -m why` in a started knowledge base, which shows decision 1's name;
  - `Open questions:` Review Focus 1 and 5, each with its reproduction run after this task;
  - `Next: slice 30.`

  Set slice 28's Status to `green`.

---

### Task 3: Slice 30, list what the shop has recorded

**Slice plan entry:** capability, no unknown. Observable: a user lists the decisions with name and title, narrows them by a field, or takes the names alone. Scenarios, in list-what-the-shop-has-recorded (`@slice-30`, 3):
1. The user lists every decision
2. The user lists the decisions that match a field
3. The user lists only the names, to feed another command

**Why each is red today:**
- All three stop at the Background: `StepDefinitionNotFoundError: Given "a shop knowledge base holding three decisions, one of them superseded"`. `tests/test_list_what_the_shop_has_recorded.py` holds only `scenarios(...)` (3 lines).
- Underneath that, `shop-knol list` is refused by argparse: `invalid choice: 'list' (choose from 'init', 'create', 'read', 'write', 'validate', 'apply', 'journal', 'render')`, exit 2 (probed 2026-09-27).

**What kb gives, probed on 2026-09-27** (the probe ran in `.superpowers/batch5/probe`, and matches batch 4's):
- `ListRequest` has `type`, `fields` (a map of strings) and `form` (`STUBS`, the default, or `IDS`).
- `ListResponse` has `stubs`, `ids` and `faults`.
- `List(type="decision")` gives stubs in the order the store holds them. Each stub has `id`, `type`, `title` and `fields`, canonical YAML (`"{}\n"` for a decision with no glance field set).
- `fields={"status": "superseded"}` narrows to the one whose `status` is `superseded`.
- A kind the store lacks is refused with a fault that names no artifact.

**Where it lands:**
- `src/shop_knowledge/arguments.py` (from Task 1): a `list` subparser. `--type` is required, as the spec's table has no brackets around it. `--where FIELD=VALUE` is repeatable, and `--ids` asks for names only.
- `src/shop_knowledge/cli.py`: a handler making one `List` call, refused through `_answered` and shown through `_show`, with one table entry. `list` changes nothing, so it is not in `_MUTATING` and asks no actor.
- `src/shop_knowledge/answers.py`: the listed stubs, and the names (decision 3). These are its public functions, named for what they give, as `glance` and `history` are.
- CLAUDE.md: the `answers.py` row's list of public functions gains the new ones.
- Rule implemented once: none new. The handler uses `_answered`, `_show` and `answers` as every command does.

**Decisions** (carried from batch 4 Task 9):
1. **What `list` shows**: decision 3 above. The Thens read `kb.content.loads(stdout)` as a sequence. A stub's `fields` are loaded with `kb.content.loads` and spread after `id`, `type` and `title`, as `answers.glance` does for a reference.
2. **`--where FIELD=VALUE`** is split at the first `=` into kb's `fields` map, and each repetition narrows further. A `--where` with no `=` is not pinned by any scenario, so it is not refused beyond what kb says. Log what it does.
3. **The superseded decision** carries `status: superseded`, from shop-artifact's `status` ("the fields every shop artifact carries, such as owner, status, and tags"). The newest decision's `supersedes` points at it. The When is `list --type decision --where status=superseded` (Review Focus 3).
4. **The Background** records three decisions, each with both sections: the superseded one, the one superseding it, and one unrelated. It gives their ids as a fixture, so each Then compares names, not counts alone.
5. **"Each with its name and title"**: the Then for scenario 1 asserts that every entry's `id` and `title` match the three recorded, and nothing more. The fields are shown but not asserted.
6. **"Three names and nothing else"**: the Then for scenario 3 asserts that the loaded answer is a sequence of exactly the three ids, each a string.

**Reuse:**
- `tests/driver.py`: `start`, `record` and `knol`.
- `tests/conftest.py`: `env` and `shop`.
- Each When gives `result`.
- A `shown` fixture that asserts exit 0 and loads stdout serves all three Thens. `tests/test_read_back_what_the_shop_knows.py` has one of that shape (`shown`), but it is local to that module. Define this module's own beside the scenarios, because CLAUDE.md puts a fixture in `conftest.py` only when more than one feature shares it. Moving `shown` to `conftest.py` is a refactor for slice 30.1 to weigh.
- Content: the Background writes its three decisions as dicts in this module, as `OLDER` and `WEEKLY` are written in `test_record_a_decision.py`.

- [ ] **Step 1: Red.** `.venv/bin/python -m pytest -q -m slice-30`: `3 failed, 59 deselected`, each on the Background Given.
- [ ] **Step 2: Scenarios 1, 2, 3** in turn, red then green.
- [ ] **Step 3: Green.**
  - `-m slice-30`: `3 passed, 59 deselected`;
  - `make test`: `27 failed, 35 passed`;
  - GREEN plus `or slice-28 or slice-30`: `35 passed`;
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | wc -l`: `27`. Each of them belongs to a slice tagged 32 or later, and the Counts constraint's expression collects exactly 27;
  - the shape check: `2 1 1 0`, nothing listed;
  - `wc -l < src/shop_knowledge/cli.py`: at most 250;
  - the arguments snapshot, with `list` added to the loop and `TAG=30`. Diffed against `help-28.txt`, the only differences are `list` in the top-level usage and choices, and the new `list -h` block.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 30 green.` in capability form, with:
  - `Evidence:` the three answers, verbatim;
  - `Open questions:` Review Focus 2, 3 and 4, each with its reproduction run after this task, and what `--where status` (no `=`) does;
  - `Next: slice 30.1, the third architecture review, which runs before the next plan (adrs/0011).`

  Set slice 30's Status to `green`.

---

## After the batch

Slice 30.1, the third architecture review, is not a task here. Architecture reviews run before planning, never inside a plan (adrs/0011). It follows the ten slices since 19.1, as its check now says. It has three things to weigh:
- `cli.py`'s headroom before slices 32 to 42 add six commands;
- the `shown` fixture defined in two modules;
- Review Focus 1, the empty batch that ends in a traceback.
