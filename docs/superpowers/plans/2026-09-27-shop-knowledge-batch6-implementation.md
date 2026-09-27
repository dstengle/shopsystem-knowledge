# shop-knowledge batch 6: slices 32 to 42

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`. A capability task follows `shopsystem-bdd:bdd-red-green` over its scenarios. An enabling task is done when its check gives the required result. bdd-red-green's stop conditions, hand-back and checkpoint apply, and they override any step here that conflicts with them.

**Goal:** Ten slices in plan order, taking shop-knol from nine commands to fourteen and keeping its code in the shape CLAUDE.md sets. In order:
- follow the links (32);
- a fixture every feature shares (32.1);
- search (34);
- review by role, piece of work or date (36);
- requests built apart from handlers (36.1);
- argument errors refused like any other refusal (36.2);
- names that say what the code does (36.3);
- record what a piece of work read (38);
- add a step to a process (40);
- retire what the shop no longer uses (42).

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

**Spec:** `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md`, section The CLI. Its command table gives:
- `shop-knol refs <locator> --inbound|--outbound [--via f] [--type t] [--depth n]` (Refs);
- `shop-knol search <text> [--type t] [--in sections|fields|all]` (Search);
- `shop-knol journal [--artifact] [--actor] [--execution] [--since]` (Journal);
- `shop-knol snapshot --execution <id> <ids...>` (Snapshot);
- `shop-knol append <locator> --from <file or ->` (Append);
- `shop-knol delete <locator>` (Delete).

Also read `CLAUDE.md`, and in the slice plan: slices 32 to 42, and the slice 30.1 review entry at the end of its log. The decisions this plan relies on are in adrs/0019 to 0026. kb's contract is `.venv/lib/python3.11/site-packages/kb/contract/kb.proto`: `RefsRequest`, `Reached`, `Hop`, `SearchRequest`, `Match`, `JournalRequest`, `Entry`, `Snapshotted`, `SnapshotRequest`, `AppendRequest`, `DeleteRequest`.

## Global Constraints

- Feature files are read-only. Any diff under `features/` is a stop condition, and that includes tag lines. No task here moves a tag.
- Code only what a scenario asserts (bdd-red-green). An enabling task changes no behaviour a scenario pins. Where a scenario is silent, the code is silent too, and the silence goes into the checkpoint as an open question.
- kb is v0.2.0 in `.venv` and is never edited here. "shop-knowledge never touches kb's files or git. It calls the contract through the in-process client." A kb change a slice needs is not coded. It is logged in the slice plan as a request to bump the pin, and the slice stops. The probes for this plan found that none of these slices needs one. The empty batch's traceback is kb's, is being fixed there (kb slice 97), and is not touched here.
- Every rule in `CLAUDE.md` holds at the end of every task, and each is implemented once:
  - a kb answer's faults are refused only through `cli._answered` (Validate's until slice 42.2);
  - a refusal is printed only by `main`, through the one printer;
  - a user's file, or the pipe, is read only in `cli._document`;
  - files are written only by `cli._write`;
  - what the user is shown is shaped only in `answers.py`, one public function per answer, each named in its CLAUDE.md row;
  - no module runs over 250 lines. If a task would take one past 250, stop and hand back.
- Spec lines every task keeps: "shop-knol never shows a traceback." "Errors are printed as returned by kb, with artifact, path, and message, and exit non-zero." "Every mutating command requires an actor and `-m`." "Output is YAML by default."
- Work on `main` in this checkout (adrs/0009). `make test` runs the suite in `.venv`. While scenarios are red, its last line is make's own `Error 1`, so read pytest's summary line above it. Every command below runs from the checkout's root.
- Scratch files go under `.superpowers/batch6/`, which `.git/info/exclude` covers. It already holds the planning run's `failing-now.txt` (27 ids) and `help-now.txt`. Each task still writes its own baseline. The planning probe, `.superpowers/batch6/probe.py`, is a throwaway. Read it as evidence of what kb gives, not as code to copy.
- Commits: `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`. The message ends with the Co-Authored-By line of the model that made the commit, e.g. `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`. Each task makes one commit, holding the slice's code, its steps and its checkpoint.
- pytest-bdd prints `PytestRemovedIn10Warning`s, two for each `target_fixture` step. That is the baseline, not a fault.
- **Counts.** The suite has 62 scenarios. `pytest --collect-only -q -m slice-N` selects 4 for slice 32, 3 for 34, 3 for 36, 1 for 38, 2 for 40 and 2 for 42. It selects none for the enabling slices 32.1, 36.1, 36.2 and 36.3. Failed and passed after each task:

  | after | failed | passed |
  |---|---|---|
  | before Task 1 (run 2026-09-27) | 27 | 35 |
  | 32 | 23 | 39 |
  | 32.1 | 23 | 39 |
  | 34 | 20 | 42 |
  | 36 | 17 | 45 |
  | 36.1 | 17 | 45 |
  | 36.2 | 17 | 45 |
  | 36.3 | 17 | 45 |
  | 38 | 16 | 46 |
  | 40 | 14 | 48 |
  | 42 | 12 | 50 |

  After Task 10, the 12 left are exactly those tagged 44 or later. `-m "slice-44 or slice-47 or slice-48 or slice-49 or slice-50"` collects 12.
- **GREEN** is the set of slices green before this batch. It is selected by `-m "slice-1 or slice-1.17 or slice-1.24 or slice-1.27 or slice-1.28 or slice-4 or slice-15 or slice-16 or slice-17 or slice-18 or slice-19 or slice-20 or slice-22 or slice-24 or slice-26 or slice-28 or slice-30"`, which gives 35 passed (run 2026-09-27). Each capability task adds its own tag to the expression, and every scenario it selects must pass.
- **The shape check** is run at the end of every task:

  ```bash
  grep -c "_refuse(" src/shop_knowledge/cli.py; grep -c "if response.faults:" src/shop_knowledge/cli.py; grep -c "read_text" src/shop_knowledge/cli.py; grep -cE "argparse|add_parser|add_argument" src/shop_knowledge/cli.py; find src -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'; grep -lE "print\(|open\(|write_text" src/shop_knowledge/renderers/*.py; wc -l < src/shop_knowledge/cli.py
  ```

  Expected: `2`, `1`, `1`, `0`, no module over 250 lines, no renderer listed, then `cli.py`'s length. The slice 30.1 review estimated that length after each task, by reading the handlers of today and kb's requests: about 229 after 32, 238 after 34, 241 after 36, under 205 after 36.1, and about 220 after 42. If a task finds `cli.py` would pass 250, stop and hand back. Do not squeeze lines to fit (slice 28's hand-back).
- **The arguments snapshot** shows that help did not change where a task says it must not, and what a task added where it adds a command:

  ```bash
  for c in "" $COMMANDS; do .venv/bin/shop-knol $c -h; echo "exit $?"; done > .superpowers/batch6/help-$TAG.txt 2>&1
  ```

  `COMMANDS` is the commands that exist at that point. Before Task 1 that is `init create read write validate apply journal list render`, and each task that adds a command appends it. Set `TAG` to the slice number.

## Decisions that hold across the batch

1. **Answers without a wrapper.** `refs`, `search` and `list` answer "what is there" questions. Each shows a sequence and nothing around it, as `list` does (batch 5, decision 3). A command that makes a change shows a mapping, as `create`, `write` and `apply` do.
2. **One public function per answer in `answers.py`,** named for what it gives and added to the CLAUDE.md row in the task that adds it: `reached` (refs, Task 1), `matched` (search, Task 3), `recorded` (snapshot, Task 8), `appended` (append, Task 9), `deleted` (delete, Task 10). `change` gains `read` in Task 8.
3. **Mutating commands.** `snapshot`, `append` and `delete` join `init`, `create`, `write` and `apply` in `cli._MUTATING`, so `_by` asks for the actor and `-m` before any call (adrs/0020). This is also what keeps kb v0.2.0's traceback on an empty Snapshot or Delete message out of reach. The probe for this plan found that `Snapshot` with `message=""` ends in `subprocess.CalledProcessError` from kb's git commit.
4. **Where a request is built.** Before Task 5, a new handler builds its request in `cli.py`, as the handlers of today do. From Task 5 on, requests are built in the module Task 5 makes (adrs/0022). Tasks 8 to 10 build theirs there.

## Review Focus

writing-plans asks for a test in the owning task for each line here. In this project tests are scenarios, and feature files are the human gate, so no test is added. Instead, each line goes into the owning task's checkpoint as a `QUESTION FOR THE SPEC`, with its reproduction, run after that task.

1. **Reviewing a role's changes shows what that role did to start the store** (owner: Task 4). In a store the shopkeeper started, `journal --actor shopkeeper` answers the store's start and every type the start defined (nine entries: `schema/schema` and the eight types) before the shopkeeper's first decision. The probe found this on 2026-09-27: the first entry for role `shopkeeper` is `create schema/schema`, "initialise store". Task 4's Background starts the store under another role (Task 4, decision 1), so the scenario sees only the recording. A user who started their own shop would expect to see their own decisions, not nine entries of setup. Reproduction after Task 4: start a store with `KB_ACTOR=shopkeeper`, record one decision, and run `shop-knol journal --actor shopkeeper`.
2. **The narrowed links show nothing narrowed away** (owner: Task 1). In follow's Background, nothing but the two work items points at the decision. So `refs --inbound --via decisions --type work-item` and `refs --inbound` give the same answer, and "nothing else" is not observed excluding anything. Reproduction after Task 1: in the Background's store, diff the two answers. A user would expect the narrowing to be shown dropping something.
3. **`snapshot`'s `--execution` and `KB_ACTOR`'s execution can disagree** (owner: Task 8). With `KB_ACTOR=agent:one` and `--execution two`, the entry is made under `two` (adrs/0025). A user would expect either one source for the piece of work or a refusal when they differ. Reproduction after Task 8: run exactly that, then `journal --execution one` and `journal --execution two`.
4. **A step added with a title already used** (owner: Task 9). kb names an item from its title. Appending a second step titled "Tidy" to a process that has one names it by kb's rule for a taken name, which no scenario here shows. Reproduction after Task 9: append the same file twice and read the process whole. A user would expect a name of its own, as slice 28 shows for a decision.
5. **`--json` is on `read` alone** (owner: Task 3, raised in batch 4 and still open). The spec says output is "YAML by default and `--json` for the same structure". `refs`, `search`, `journal` and `list` take no `--json`. After Task 6, `shop-knol search restocking --json` is one plain line and exit 1, where before Task 6 it was usage and exit 2. A user would expect JSON.

---

### Task 1: Slice 32, follow the links from the command line

**Slice plan entry:** capability, no unknown. Scenarios, in follow-the-links-between-what-the-shop-knows (`@slice-32`, 4):
1. The user sees what a decision points at
2. The user sees what points at a decision
3. The user narrows the links to one kind of link and one kind of thing
4. The user follows the links two steps out

**Observable:** a user follows the links out of a decision and sees the older decision. Following them in, they see both work items. Narrowed to one link and one kind, they see both work items and nothing else. Two steps out, they see the older decision and the tag, each with the route taken.

**Why each is red today:**
- All four stop at the Background: `StepDefinitionNotFoundError: Given "a shop knowledge base where a decision supersedes an older decision"` (run 2026-09-27). `tests/test_follow_the_links_between_what_the_shop_knows.py` holds only `scenarios(...)`.
- Underneath that, `shop-knol refs` is refused by argparse, `invalid choice: 'refs'`, with exit 2.

**What kb gives, probed on 2026-09-27** (`.superpowers/batch6/probe.py`):
- `Refs` at depth 0, the proto default, reaches nothing: an empty answer and no fault.
- At depth 1, outward from the newer decision, it reaches the older decision alone. The stub's `field` is `supersedes`, and the route is one hop (`supersedes`, the older decision's name).
- Inward at depth 1 with `via="decisions"` and `type="work-item"`, it reaches the two work items, each by `decisions`.
- Outward at depth 2, it reaches the older decision and then `tag/pricing`, whose route is two hops (`supersedes`, then `tags`). Nearest comes first.

**Where it lands:**
- `src/shop_knowledge/arguments.py`: a `refs` subparser.
  - A locator.
  - One of `--outbound`/`--inbound`, in a required, mutually exclusive group.
  - `--via FIELD`, `--type TYPE`, and `--depth N` (int).
- `src/shop_knowledge/cli.py`: a handler that makes one `Refs` call, refuses through `_answered` and shows through `_show`, plus one table entry. Not mutating.
- `src/shop_knowledge/answers.py`: `reached` (adrs/0024).
- `CLAUDE.md`: the `answers.py` row names `reached`.
- `tests/test_follow_the_links_between_what_the_shop_knows.py`: the Background's three Givens, four Whens and five Thens.
- Rule implemented once: none new.

**Decisions** (adrs/0024):
1. **No `--depth` asks for one step.** The spec's table leaves depth optional. kb reaches nothing at 0, and scenarios 1 to 3 say "points at" and "points at a decision", which is one step.
2. **What is shown**: a sequence in kb's order. Each entry is the reached artifact's `id`, `type` and `title`, then `via` (the stub's `field`, the link of the last step), then the stub's fields loaded with `kb.content.loads`, as `answers.listed` spreads them, then `route`, a sequence of `field` and `id` for each hop.
3. **The When lines map to flags**:
   - "out of the decision" is `--outbound`;
   - "into the decision" is `--inbound`;
   - "only through the link a work item uses, and only from work items" is `--inbound --via decisions --type work-item`, since `decisions` is the work-item type's link to a decision (`types/work-item.yaml`);
   - "two steps" is `--depth 2`.
4. **"Sees the route taken to each of them"**: the Then asserts both routes hop by hop. The older decision's is `[(supersedes, older)]`. The tag's is `[(supersedes, older), (tags, tag/pricing)]`.
5. **"Both work items and nothing else"**: the Then asserts the set of reached names is exactly the two work items (Review Focus 2).

**Reuse:**
- `tests/driver.py`: `start`, `record` and `knol`.
- `tests/conftest.py`: `env` and `shop`.
- Each When gives `result`.
- The Background's content: the same shapes `_shop_with_a_linked_decision` in `tests/test_read_back_what_the_shop_knows.py` writes (a tag, an older decision, a newer one with `supersedes`, two work items with `decisions`). Here, though, the tag is on the older decision ("the older decision is tagged pricing"). Write the dicts in this module.
- A `shown` fixture that asserts exit 0 and loads stdout. Define it in this module, word for word as the read-back and list modules have it. Task 2 takes all three into the conftest.

- [ ] **Step 1: Red.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch6/failing-32.txt; wc -l < .superpowers/batch6/failing-32.txt`: `27`.
  - `.venv/bin/python -m pytest -q -m slice-32`: `4 failed, 58 deselected`, each on the Background Given.
  - Arguments snapshot with `TAG=before`.
- [ ] **Step 2: Scenarios 1 to 4** in turn, red then green. Scenario 1's first red on code is argparse's `invalid choice: 'refs'`.
- [ ] **Step 3: Green.**
  - `-m slice-32`: `4 passed, 58 deselected`;
  - `make test`: `23 failed, 39 passed`;
  - GREEN plus `or slice-32`: `39 passed`;
  - the shape check: `2 1 1 0`, nothing listed, `cli.py` at most 250 (about 229);
  - arguments snapshot with `refs` appended and `TAG=32`, diffed against `before`: only `refs` in the usage and choices, and the new `refs -h` block.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 32 green.` in capability form, with:
  - `Evidence:` the four answers, verbatim;
  - `Open questions:` Review Focus 2, with its reproduction;
  - `Next: slice 32.1.`

  Set slice 32's Status to `green`.

---

### Task 2: Slice 32.1, what a command showed is read by one fixture every feature shares

**Slice plan entry:** enabling, no unknown. Check:
- the same failing scenarios as before the slice (23 failed, 39 passed);
- `grep -c "def shown" tests/*.py | grep -v ":0"` gives one line, `tests/conftest.py:1`.

**Observable:** the steps of slices 34 to 42 find one `shown` fixture in the shared conftest.

**Why the check fails today:** after Task 1, `shown` is defined three times: in `tests/test_read_back_what_the_shop_knows.py`, `tests/test_list_what_the_shop_has_recorded.py` and `tests/test_follow_the_links_between_what_the_shop_knows.py`. The first two are word for word the same apart from their docstrings (read on 2026-09-27). CLAUDE.md: "Fixtures and steps shared by more than one feature live in `tests/conftest.py`."

**Where it lands:**
- `tests/conftest.py`: `shown`, taking `result`, asserting exit 0 with stderr as the message, and giving `kb.content.loads(result.stdout)`. Its docstring says it serves every Then that expects the command to have succeeded.
- The three modules: their own `shown` goes, and any import only it used goes with it.
- Nothing under `src/` changes.
- Rule implemented once: CLAUDE.md's "Fixtures and steps shared by more than one feature live in `tests/conftest.py`."

**Decisions:** the conftest's `shown` has the behaviour both of today's copies share. No Then that reads `shown` changes.

- [ ] **Step 1: Baseline.** `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch6/failing-32.1.txt; wc -l < .superpowers/batch6/failing-32.1.txt`: `23`. The grep gives three lines.
- [ ] **Step 2: Move** `shown` into the conftest, and delete the three copies.
- [ ] **Step 3: Check.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort | diff - .superpowers/batch6/failing-32.1.txt && echo same`: `same`;
  - `make test`: `23 failed, 39 passed`;
  - the grep gives `tests/conftest.py:1`;
  - the shape check is unchanged from Task 1.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 32.1 green.`, then `Check:` with each output, `Surprised by:`, and `Next: slice 34.` Set slice 32.1's Status to `green`.

---

### Task 3: Slice 34, search what the shop knows

**Slice plan entry:** capability, no unknown. Scenarios, in search-what-the-shop-knows (`@slice-34`, 3):
1. The user searches the prose
2. The user searches within one kind of thing
3. The user searches the fields as well as the prose

**Observable:** a user searches for a word and sees each result with the section it matched and a snippet, the heaviest first. Narrowed to decisions, they see the two decisions and not the process. Including the fields, they also see a decision whose title carries the word.

**Why each is red today:**
- All three stop at the Background: `StepDefinitionNotFoundError: Given "a shop knowledge base where two decisions and a process mention restocking in their prose"` (run 2026-09-27). The module holds only `scenarios(...)`.
- Underneath that, `shop-knol search` is refused by argparse, `invalid choice`.

**What kb gives, probed on 2026-09-27:**
- `Search(text="restocking")` looks in sections by default (`Scope.SECTIONS` is 0). Each `Match` has a `stub` (without `field`), the `section` title and the `snippet`. Matches come in kb's order: "the one holding the words most often first" (the proto's comment).
- A process may carry `sections` beside its steps, and a Purpose section on one is matched. The probe created `process/close-up` with a Purpose saying "Restocking before close.", and kb accepted and matched it.
- `scope=ALL` also matches a decision whose title alone holds the word. That match has `field: "title"` and no `section`, and its snippet is the title.
- A step's `does` inside `steps` is not prose that Search reaches in sections scope. So the Background's process mentions restocking in a section, not in a step.

**Where it lands:**
- `arguments.py`: a `search` subparser. `text`, then `--type TYPE`, then `--in` with the choices `sections`, `fields` and `all`, default `sections`.
- `cli.py`: a handler making one `Search` call, the scope mapped from `--in`, plus one table entry. Not mutating.
- `answers.py`: `matched` (adrs/0024), plus its CLAUDE.md row entry.
- `tests/test_search_what_the_shop_knows.py`: the Background, three Whens and four Thens.

**Decisions** (adrs/0024):
1. **What is shown**: a sequence in kb's order. Each entry is `id`, `type` and `title`, then `section` when the match is in a section, or `field` when it is in a field, then `snippet`.
2. **The Background**, to make every Then observable:
   - a decision that says "restocking" several times in one section;
   - a second decision that says it once;
   - a process with one step and a Purpose section that says it once;
   - a third decision whose title carries the word and whose prose does not.

   The third is what scenario 3 finds, and scenarios 1 and 2 must not show it. The Background's line names only the first three. The fourth is the "decision whose title mentions restocking" that scenario 3's Then presupposes, so it belongs in the Background, where every scenario shares it.
3. **The When lines map to flags**: "searches for restocking" is `search restocking`; "among decisions only" adds `--type decision`; "in the fields as well as the prose" adds `--in all`.
4. **"The one that mentions restocking most often in a section comes first"**: the Then asserts that the first entry is the decision that says it several times.
5. **"Each result names the section it matched and shows a snippet"**: every entry has a non-empty `section` and a `snippet` holding the word, case ignored.
6. **"The two decisions and not the process"**: the set of names is exactly the two prose decisions.
7. **"Also sees a decision whose title mentions restocking"**: the title decision is among the names, and so are the three found in prose.

**Reuse:** `start`, `record` and `knol`; `env` and `shop`; `shown` (from Task 2). Each When gives `result`.

- [ ] **Step 1: Red.** `-m slice-34`: `3 failed, 59 deselected`, each on the Background.
- [ ] **Step 2: Scenarios 1, 2, 3** in turn, red then green.
- [ ] **Step 3: Green.**
  - `-m slice-34`: `3 passed, 59 deselected`;
  - `make test`: `20 failed, 42 passed`;
  - GREEN plus `or slice-32 or slice-34`: `42 passed`;
  - the shape check: `2 1 1 0`, nothing listed, `cli.py` at most 250 (about 238);
  - arguments snapshot with `search` appended, diffed against `32`: only `search` added.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 34 green.`, with:
  - `Evidence:` the three answers;
  - `Open questions:` Review Focus 5, and whether a match inside a part (a step's `does`) should be found. Run `search` for a word only a step's `does` holds and log what it shows;
  - `Next: slice 36.`

  Set slice 34's Status to `green`.

---

### Task 4: Slice 36, review by role, piece of work, or date

**Slice plan entry:** capability, no unknown. Scenarios, in review-who-changed-what (`@slice-36`, 3; slice 16's scenario in the same feature is green):
1. The user reviews what one role did
2. The user reviews what one piece of work did
3. The user reviews the changes since a date

**Observable:** a user reviews the shopkeeper's changes and sees only the recording of the decision. Reviewing a piece of work's changes, they see only the agent's revision. Reviewing the changes since yesterday, they see only today's revision.

**Why each is red today:**
- The Background is defined (slice 16), and each scenario stops at its When: `StepDefinitionNotFoundError: When "the user reviews the changes made by the shopkeeper"`, `"... made for that piece of work"` and `"... since 2026-09-22"` (run 2026-09-27).
- Underneath that, `shop-knol journal` takes only `--artifact`, so `--actor`, `--execution` and `--since` are refused by argparse, `unrecognized arguments`.

**What kb gives, probed on 2026-09-27:**
- `JournalRequest` has `role`, `execution`, `since` and `batch` beside `artifact`.
- `role="shopkeeper"` answers every entry the shopkeeper made, including the store's start and its type definitions, when the shopkeeper started the store.
- `since="2999-01-01"` answers nothing.
- `since="yesterday"` is refused with a fault with rule `since` and no artifact: "a time is written in ISO 8601, as 2026-09-22 or 2026-09-22T09:00:00Z; 'yesterday' is not".
- `execution="e1"` answers only that piece of work's entries.

**Where it lands:**
- `arguments.py`: `journal` gains `--actor ROLE`, `--execution ID` and `--since WHEN`, each defaulting to empty.
- `cli.py`: `_journal` passes them to `JournalRequest` (`--actor` as `role`). No new handler and no new answer: `answers.history` shows the entries.
- `tests/test_review_who_changed_what.py`:
  - three Whens and three Thens;
  - the Background Given `_recorded_then_revised` starts the store under another role (decision 1).

**Decisions** (adrs/0025):
1. **Who started the store.** The Background says "the shopkeeper recorded a decision on 2026-09-21 and an agent revised it today". It does not say who started the knowledge base. Today's step starts it under `env`'s `KB_ACTOR`, `shopkeeper`, so the shopkeeper's history also holds nine start entries, and scenario 1's "only the recording of the decision" could not hold. So the step starts the store under a role of its own that the Background does not name, e.g. `KB_ACTOR=founder`, at the same moment. Slice 16's scenario filters by artifact, so it is unaffected. It must stay green, and GREEN checks that. The question for the spec is Review Focus 1.
2. **The When lines map to flags**: "made by the shopkeeper" is `--actor shopkeeper`; "made for that piece of work" is `--execution reprice-dairy` (the module's `PIECE_OF_WORK`); "since 2026-09-22" is `--since 2026-09-22`, passed as the user writes it.
3. **The Thens** read `changes` from `shown` and assert the whole list, as slice 16's Then does:
   - scenario 1: exactly one change, `create` of the decision by the shopkeeper;
   - scenarios 2 and 3: exactly one change, the agent's `write` of the decision, dated today.

**Reuse:**
- The Background, `_today` and `_recorded_then_revised`, from slice 16, with decision 1's change.
- `WEEKLY` and `PIECE_OF_WORK`.
- `shown` (Task 2), `env` and `knol`.
- Slice 16's Then `_both_changes` shows the tuple form to compare.

- [ ] **Step 1: Red.** `-m slice-36`: `3 failed, 59 deselected`, each on its When (slice 16's scenario carries its own tag).
- [ ] **Step 2: Scenarios 1, 2, 3** in turn, red then green. Scenario 1 first goes red on its Then over the start entries, before decision 1's change to the Background. Log that red.
- [ ] **Step 3: Green.**
  - `-m slice-36`: `3 passed, 59 deselected`, and `-m slice-16`: `1 passed`;
  - `make test`: `17 failed, 45 passed`;
  - GREEN plus `or slice-32 or slice-34 or slice-36`: `45 passed`;
  - the shape check: `2 1 1 0`, nothing listed, `cli.py` at most 250 (about 241);
  - arguments snapshot diffed against `34`: only the `journal -h` block changes.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 36 green.`, with:
  - `Evidence:` the three answers;
  - `Open questions:` Review Focus 1, with its reproduction;
  - `Next: slice 36.1.`

  Set slice 36's Status to `green`.

---

### Task 5: Slice 36.1, each command's request to kb is built apart from its handler

**Slice plan entry:** enabling, no unknown. Check:
- the same failing scenarios as before the slice (17 failed, 45 passed);
- `grep -cE "kb_pb2\.[A-Za-z]*Request\b|kb_pb2\.Locator\(" src/shop_knowledge/cli.py` gives `0`;
- `wc -l < src/shop_knowledge/cli.py` is under 205;
- the module that now builds the requests holds no `print(`, no `connect` and no call on a client;
- CLAUDE.md's module map has a row for it.

**Observable:** `cli.py` keeps room under 250 through slices 38 to 50.

**Why the check fails today** (after Task 4):
- `cli.py` is about 241 lines;
- the grep counts every request and locator built in the handlers and their helpers: `_init`, `_create`, `_locator`, `_read_request`, `_validate`, `_apply`, `_journal`, `_list`, and Tasks 1 and 3's `refs` and `search` handlers.

**Where it lands** (adrs/0022):
- New `src/shop_knowledge/kb_requests.py`. Its docstring: each command's arguments turned into the request it sends kb. It holds one public function per command that calls kb, named `<command>_request`: `init_request`, `create_request`, `write_request`, `read_request`, `validate_request`, `apply_request`, `journal_request`, `list_request`, `refs_request` and `search_request`.
  - Each takes the parsed arguments, with `args.by` already set by `_run`. Those that send a file's content also take the document `cli._document` read.
  - It holds what `_locator`, `_is_whole` and `_read_request` do today, the list's `--where` split and form, the create's title split off the content, and the refs depth default.
  - `apply_request` calls `batch.operations`, which is unchanged.
  - It imports `kb.contract`, `kb.content` and `batch`, and never `kb.client`.
- `src/shop_knowledge/cli.py`: each handler calls its request function, makes its call, refuses through `_answered` and shows. `_read` still chooses which answer shapes the read. It needs to know whether the read was whole, so the helper that says so is public in the new module, and `cli` uses it.
- `CLAUDE.md`:
  - a row for `kb_requests.py`: it owns "each command's arguments as the request it sends kb, one public function per command", and never holds "kb calls, printing, reading files";
  - the `cli.py` row keeps "one handler per command making the kb calls that command maps to".
- `renderers/source.py` keeps its own `ReadRequest`. A renderer reads through `source`, not through the command line's requests.
- Rule implemented once: the module map's "a new concern gets a new module and a row here". Turning arguments into a request is one concern, the mirror of `answers.py`.

**Decisions:**
1. **The module's name.** It is `kb_requests.py`, not `requests.py`, so that no reader takes it for the third-party `requests` library. Slice 36.3 is about names that hide other names, and this one would.
2. **`_by` stays in `cli.py`.** The actor comes from the environment, which is `cli.py`'s by its row. The request functions read `args.by` and never read `os.environ`.
3. **Nothing else moves.** `_document`, `_answered`, `_show`, `_write`, the printer and the handler table stay where they are.

**Reuse:** nothing in `tests/` changes. Every scenario drives `shop-knol` as a subprocess, so all 45 passing ones guard the move.

- [ ] **Step 1: Baseline.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch6/failing-36.1.txt; wc -l < .superpowers/batch6/failing-36.1.txt`: `17`;
  - the grep's count, and `wc -l`;
  - arguments snapshot with `TAG=36.1-before`.
- [ ] **Step 2: Move** the requests, handler by handler, running `make test` after each.
- [ ] **Step 3: Map.** Add the CLAUDE.md row.
- [ ] **Step 4: Check.**
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort | diff - .superpowers/batch6/failing-36.1.txt && echo same`: `same`;
  - `make test`: `17 failed, 45 passed`;
  - the grep: `0`;
  - `wc -l < src/shop_knowledge/cli.py`: under 205;
  - `grep -cE "print\(|connect|client" src/shop_knowledge/kb_requests.py`: `0`;
  - `grep -c "kb_requests.py" CLAUDE.md`: `1`;
  - the shape check: `2 1 1 0`, nothing listed;
  - arguments snapshot with `TAG=36.1`, diffed against `36.1-before`: no output.
- [ ] **Step 5: Checkpoint and commit.** Log `- 2026-09-27 slice 36.1 green.`, with what moved and both modules' line counts, `Check:`, `Surprised by:`, and `Next: slice 36.2.` Set slice 36.1's Status to `green`. If the move had to differ from adrs/0022, amend it.

---

### Task 6: Slice 36.2, an argument shop-knol cannot take is refused the one way every refusal is

**Slice plan entry:** enabling, no unknown. Check:
- the same failing scenarios as before the slice (17 failed, 45 passed);
- each of these prints exactly one line on stderr, with no `usage:`, prints nothing on stdout, and exits 1:
  - `shop-knol`
  - `shop-knol nosuch`
  - `shop-knol list`
  - `shop-knol list --type decision --json`
  - `shop-knol read decision/x --resolve two`
  - `shop-knol create decision`
- `shop-knol -h`, and `-h` for every command, give byte for byte what they gave before, with exit 0.

**Observable:** a mistyped command or flag is one plain line and exit 1, as rule 4 states.

**Why the check fails today** (probed 2026-09-27):
- `shop-knol nosuch` prints a three-line usage block, then `shop-knol: error: argument command: invalid choice: 'nosuch' (choose from ...)`, and exits 2.
- `shop-knol list` prints `usage: shop-knol list [-h] --type TYPE ...`, then `shop-knol list: error: the following arguments are required: --type`, and exits 2.
- `read x --resolve two` gives `argument --resolve: invalid int value: 'two'` after its usage, with exit 2.
- `list --type decision --json` gives `unrecognized arguments: --json` after the top-level usage, with exit 2.
- `create decision` gives `the following arguments are required: --from`, with exit 2.
- `main` calls `parse_args` outside its `try`, and argparse prints and exits by itself.

**Spike, run while planning and thrown away:** an `argparse.ArgumentParser` subclass whose `error` raises, in place of printing and exiting, is used by `add_subparsers` for every subparser. It raised for all five kinds: an unknown command, a missing required argument, a value of the wrong type, an unrecognized argument, and no command. Each time it carried argparse's own message, and the parser's `prog` named the subcommand (`x a: the following arguments are required: --n`).

**Where it lands** (adrs/0023):
- `src/shop_knowledge/arguments.py`:
  - the parser class whose `error` raises;
  - the exception it raises, which carries the `prog` of the parser that refused and argparse's message. It is defined here, since `arguments.py` must not import `cli`, which imports it.
  - `command_parser` builds with that class.
- `src/shop_knowledge/cli.py`: `main` parses inside its handling. It turns the exception into one `kb_pb2.Fault`, with the artifact the `prog` and the message argparse's, and prints it through the same `_refuse` call that prints a `Refused`, so `grep -c "_refuse("` stays `2`. Exit 1.
- `CLAUDE.md`: rule 4 already says this and needs no change. The `arguments.py` row adds that it refuses an argument it cannot take by raising, and never prints.
- Rule implemented once: rule 4, for arguments, in the one place arguments are declared.

**Decisions** (adrs/0023):
1. The line is `<prog>: <argparse's message>`, what the printer gives for a fault with that artifact and no path. For example, `shop-knol list: the following arguments are required: --type`.
2. `-h` and `--help` are not refusals. argparse's help action prints and exits 0 without calling `error`, and that stays as it is.
3. No wording of argparse's is rewritten. "In plain words" is met by one line with no usage block. Rewording would be behaviour no scenario or rule asks for.

**Reuse:** none in `tests/`. No scenario runs an argument error. Slice 26's missing `-m` is `_by`'s refusal, not argparse's, since `-m` is optional at the argument level (adrs/0020).

- [ ] **Step 1: Baseline.**
  - failing ids to `.superpowers/batch6/failing-36.2.txt` (`17`);
  - arguments snapshot with `TAG=36.2-before` (commands `init create read write validate apply journal list render refs search`);
  - the six argument errors, each with its stderr line count and exit code, to `.superpowers/batch6/argerrors-before.txt`. Each is `exit 2` with a `usage:` line.
- [ ] **Step 2: Make the change.**
- [ ] **Step 3: Check.**
  - failing ids diff: `same`;
  - `make test`: `17 failed, 45 passed`;
  - for each of the six: `.venv/bin/shop-knol <args> 2>err >out; echo $?; wc -l < err; wc -c < out; grep -c "usage:" err` gives `1`, `1`, `0`, `0`;
  - arguments snapshot with `TAG=36.2`, diffed against `36.2-before`: no output;
  - the shape check: `2 1 1 0`, nothing listed, `cli.py` under 210.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 36.2 green.`, with the six lines verbatim, `Check:`, `Surprised by:`, and `Next: slice 36.3.` Set slice 36.2's Status to `green`. In the slice plan's log, mark the argparse question raised at slices 20.1, 22 and 30 answered by rule 4 through this slice.

---

### Task 7: Slice 36.3, no name in the code says less or other than it does

**Slice plan entry:** enabling, no unknown. Check:
- the same failing scenarios as before the slice (17 failed, 45 passed);
- `grep -cE "^\s+validate = " src/shop_knowledge/arguments.py` gives `0`;
- `grep -c "def _show(document: dict," src/shop_knowledge/cli.py` gives `0`;
- `grep -cE "def knol\(.*\binput\b" tests/driver.py` gives `0` (the keyword `input=` passed on to `subprocess.run` stays);
- `.venv/bin/python -c "import inspect,shop_knowledge.cli as c; assert 'shape =' not in inspect.getsource(c._read)"` succeeds;
- every public function of `answers.py` is named in its CLAUDE.md row, and the row and the module's docstring say it gives lists as well as dicts.

**Why the check fails today** (read 2026-09-27; line numbers before this batch):
- `arguments.py:35` assigns `validate = commands.add_parser(...)`, and nothing reads it;
- `cli.py:64` hints `document: dict`, while `answers.listed` and `answers.names`, and after Tasks 1 and 3 `reached` and `matched`, give it lists;
- `tests/driver.py` `knol(env, *args, cwd=None, input=None)` hides the built-in `input`;
- `cli._read`'s local `shape` hides the module `shape` that `cli` imports;
- the CLAUDE.md `answers.py` row lists nine functions and misses `whole` and `section`. The module's docstring says "plain dicts".

**Where it lands:**
- `arguments.py`: `validate`'s subparser is added without the assignment.
- `cli.py`: `_show`'s hint is `dict | list`. `_read`'s local is named for what it holds: the answer function.
- `tests/driver.py`: `knol`'s parameter is `piped`, and its one caller, `tests/test_record_a_decision.py`'s pipe When, passes it by that name. The docstring says "with `piped` on its standard input".
- `answers.py`: the docstring says plain dicts and lists.
- `CLAUDE.md`: the row names every public function in `answers.py` at this point (`glance`, `whole`, `section`, `change`, `history`, `created`, `written_over`, `applied`, `listed`, `names`, `reached`, `matched`, `written`).
- Rule implemented once: none. This is tidying that makes the names true.

**Decisions:** no behaviour, output or help text changes. The arguments snapshot must be byte for byte the same.

- [ ] **Step 1: Baseline.** Failing ids to `.superpowers/batch6/failing-36.3.txt` (`17`). Arguments snapshot with `TAG=36.3-before`. Run each grep of the check, and record what it gives.
- [ ] **Step 2: Make the five changes.**
- [ ] **Step 3: Check.** Every line of the check. The arguments snapshot diffed against `36.3-before` gives no output. `make test`: `17 failed, 45 passed`. The shape check: `2 1 1 0`, nothing listed.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 36.3 green.`, with `Check:`, `Surprised by:`, and `Next: slice 38.` Set slice 36.3's Status to `green`.

---

### Task 8: Slice 38, record what a piece of work read

**Slice plan entry:** capability, no unknown. Scenario, in record-what-a-piece-of-work-read (`@slice-38`, 1): An agent records what it read.

**Observable:** an agent records, for its piece of work, the decision and the process it read, and the shop's history holds one entry naming each with the version read.

**Why it is red today:**
- It stops at the Background: `StepDefinitionNotFoundError: Given "a shop knowledge base holding a decision and a process"` (run 2026-09-27). The module holds only `scenarios(...)`.
- Underneath that, there is no `snapshot` command.
- `answers.change` shows no `read`, so even once a snapshot is made, `journal` would not show what it named.

**What kb gives, probed on 2026-09-27:**
- `Snapshot(actor=agent:e1, artifacts=[decision, process], message="read")` answers `entry`, the entry's name.
- `Journal(execution="e1")` answers one entry with `op: "snapshot"`, no `artifact`, and `read`: each `Snapshotted` with `artifact`, `revision` (1 for both) and `digest`.
- `message=""` ends in kb's git traceback (decision 3 of the batch keeps it out of reach).

**Where it lands:**
- `arguments.py`: a `snapshot` subparser: `--execution ID` (required, since the spec's table has no brackets around it), the names (`nargs="+"`), and `-m`.
- `kb_requests.py`: `snapshot_request`. The actor is `args.by`'s role, with `--execution` as its execution (adrs/0025).
- `cli.py`: a handler, one table entry, and `snapshot` in `_MUTATING`.
- `answers.py`: `recorded`, the entry's name under `entry`. `change` gains `read`, each read artifact's `artifact` and `revision`, shown only when the entry read something (adrs/0025). CLAUDE.md row: `recorded`.
- `tests/test_record_what_a_piece_of_work_read.py`: the Background, the When and the Then.
- Rule implemented once: none new. The request is built where every request is (Task 5).

**Decisions** (adrs/0025):
1. **The When** runs `snapshot --execution <piece> <decision> <process> -m <why>` with `KB_ACTOR=agent`. "The agent records, for its piece of work" gives the role and the piece. A mutating command requires `-m`, so the step gives one, though the line does not say "why". Slice 28's `test_record_a_decision.py` When "records that file as a decision" does the same.
2. **The Then** runs `journal --execution <piece>` and asserts, through `shown`, exactly one change, whose `read` is the decision and the process, each at revision 1, the version the Background left them at. The digest is not shown and not asserted. No scenario asks for it.
3. **"The shop's history"** is observed through `shop-knol journal`, as a user would, and not through kb in process.

**Reuse:** `start`, `record` and `knol`; `env` and `shop`; `shown`. Each When gives `result`. Background content: a decision's dict as `tests/test_record_a_decision.py`'s `OLDER`, and a process with one inline step, written in this module.

- [ ] **Step 1: Red.** `-m slice-38`: `1 failed, 61 deselected`, on the Background.
- [ ] **Step 2: The scenario**, red then green. After the command exists, see it red on the Then while `change` shows no `read`.
- [ ] **Step 3: Green.**
  - `-m slice-38`: `1 passed`;
  - `make test`: `16 failed, 46 passed`;
  - GREEN plus slices 32, 34, 36 and 38: `46 passed`;
  - slice 16's and 36's scenarios still pass (in GREEN), so every entry that read nothing is shown as before;
  - the shape check: `2 1 1 0`, nothing listed, `cli.py` at most 250;
  - arguments snapshot with `snapshot` appended: only `snapshot` added.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 38 green.`, with:
  - `Evidence:` the snapshot's answer and the journal entry;
  - `Open questions:` Review Focus 3, with its reproduction;
  - `Next: slice 40.`

  Set slice 38's Status to `green`.

---

### Task 9: Slice 40, add a step to a process

**Slice plan entry:** capability, no unknown. Scenarios, in add-a-step-to-a-process (`@slice-40`, 2):
1. The user adds a step written in place
2. The user adds a step that reuses a shared step

**Observable:** a user adds a step written in place. It is the last step, and they are told its name. Or they add a step that uses a shared step with its own settings. The process runs it there with those settings, and the shared step and its other users are unchanged.

**Why each is red today:**
- Both stop at the Background: `StepDefinitionNotFoundError: Given "a shop knowledge base holding a process with two steps"` (run 2026-09-27).
- Underneath that, there is no `append` command.

**What kb gives, probed on 2026-09-27:**
- `Append(locator=process#steps, content={title, does})` answers `id: "tidy"`, the item's name made from its title, and the process's new `revision`. The item is added last.
- A step with `uses: step/check-the-stock` and `with: [{name: shelf, value: dairy}]` appends the same way.
- The new item's place is `steps/<its name>`. A Write to `process/...#steps/tidy` succeeded, and to `steps/2` it was refused, "holds nothing at 'steps/2'".
- An Append whose locator names no collection is refused: "an item is added to a collection, and '' in 'process/...' is not one".
- A process whose step uses the shared step shows among the step's links in (`Refs` inward, via `uses`).

**Where it lands:**
- `arguments.py`: an `append` subparser: a locator, `--from FILE` (required, taking `-` like every `--from`), and `-m`.
- `kb_requests.py`: `append_request`. The locator is read as `write`'s is (adrs/0019), and the content is the document `cli._document` read, against the `content` shape.
- `cli.py`: a handler, one table entry, and `append` in `_MUTATING`.
- `answers.py`: `appended` (adrs/0026): `id` is `<name>#<collection>/<item>`, and `revision`. Plus its CLAUDE.md row entry.
- `tests/test_add_a_step_to_a_process.py`: the two Givens, two Whens and five Thens.

**Decisions** (adrs/0026):
1. **The locator** is `<process>#steps` ("adds a step to a process"). The file holds the step as kb holds an item, with `title` and either `does` or `uses` and `with`, and never an `id`.
2. **"Told the name the new step is known by"**: the answer's `id`, `<process>#steps/<item>`. That is the name a later `write` takes. The Then asserts it ends with the name the last step carries in a whole read.
3. **"The new step is the last step"**: `read <process> --whole`. The last of `steps` has the title and `does` the file gave, and there are three steps.
4. **"Runs 'check the stock' at that point with those settings"**: the whole read's last step has `uses: step/check-the-stock` and the `with` the file gave.
5. **"'check the stock' itself is unchanged" and "another process using it is unaffected"**: the shared step, and a second process the Background records using it, each read `--whole` before the When and after. They are equal, revision included. That is the pattern of `before` in `tests/test_revise_what_the_shop_knows.py`.
6. **The shared step** carries `settings: [shelf]`, as `CHECK_THE_STOCK` in `tests/test_publish_what_the_shop_knows.py` does, and the new use binds `shelf`. Write the dict in this module. Test modules do not import each other.

**Reuse:** `start`, `record` and `knol`; `env`, `shop`, `tmp_path` and `shown`. The `before`-fixture pattern comes from `tests/test_revise_what_the_shop_knows.py`. Each When gives `result`.

- [ ] **Step 1: Red.** `-m slice-40`: `2 failed, 60 deselected`, on the Background.
- [ ] **Step 2: Scenarios 1, 2** in turn, red then green.
- [ ] **Step 3: Green.**
  - `-m slice-40`: `2 passed`;
  - `make test`: `14 failed, 48 passed`;
  - GREEN plus slices 32 to 40: `48 passed`;
  - the shape check: `2 1 1 0`, nothing listed, `cli.py` at most 250;
  - arguments snapshot: only `append` added.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 40 green.`, with:
  - `Evidence:` both answers and the whole process after each;
  - `Open questions:` Review Focus 4, with its reproduction;
  - `Next: slice 42.`

  Set slice 40's Status to `green`.

---

### Task 10: Slice 42, retire what the shop no longer uses

**Slice plan entry:** capability, no unknown. Scenarios, in retire-what-the-shop-no-longer-uses (`@slice-42`, 2):
1. The user retires something nothing points at
2. The user retires something that is still pointed at

**Observable:** a user retires a tag nothing points at, and the shop no longer holds it. Or they retire a tag a decision carries, and are refused, seeing everything that points at it.

**Why each is red today:**
- Both stop at the Background: `StepDefinitionNotFoundError: Given "a shop knowledge base holding a tag "seasonal" that nothing points at"` (run 2026-09-27).
- Underneath that, there is no `delete` command.

**What kb gives, probed on 2026-09-27:**
- `Delete(tag/seasonal)` answers `revision: 2`, and a Read after it is refused: "the store holds nothing by the name 'tag/seasonal'".
- `Delete(tag/pricing)`, while decisions carry it, is refused with one fault per thing pointing at it. Each fault names that artifact and its path, `tags/0`, with rule `on_delete` and the message "'tag/pricing' cannot be removed while '<decision>' points at it at 'tags/0'".

**Where it lands:**
- `arguments.py`: a `delete` subparser, the spec's name for the command ("`shop-knol delete <locator>`"): a locator and `-m`.
- `kb_requests.py`: `delete_request`.
- `cli.py`: a handler, one table entry, and `delete` in `_MUTATING`. kb's refusal goes through `_answered`.
- `answers.py`: `deleted` (adrs/0026): `id`, the locator's name, and `revision`. Plus its CLAUDE.md row entry.
- `tests/test_retire_what_the_shop_no_longer_uses.py`: the two Givens, two Whens and three Thens.

**Decisions** (adrs/0026):
1. **"Retires"** is `delete <tag> -m <why>` under `KB_ACTOR` ("saying who they are and why").
2. **"The shop no longer holds it"**: `shop-knol read tag/seasonal` is refused (exit non-zero), and `list --type tag --ids` holds `tag/pricing` and not `tag/seasonal`.
3. **"Rejected because something in the shop still points at it"**: exit non-zero, nothing on stdout, and stderr saying it cannot be removed while something points at it (kb's words, passed through as the spec says). `read tag/pricing` still succeeds.
4. **"Told everything that points at it"**: the Background tags one decision with `pricing`, and stderr names that decision, one line per pointer.

**Reuse:** `start`, `record` and `knol`; `env`, `shop` and `shown`. The shared Thens in `tests/conftest.py` are "the user is shown that fault in plain words, never a traceback" and "the command reports failure to whatever ran it". Neither is in these scenarios, but they are the model for decision 3's assertions. Each When gives `result`.

- [ ] **Step 1: Red.** `-m slice-42`: `2 failed, 60 deselected`, on the Background.
- [ ] **Step 2: Scenarios 1, 2** in turn, red then green.
- [ ] **Step 3: Green.**
  - `-m slice-42`: `2 passed`;
  - `make test`: `12 failed, 50 passed`;
  - GREEN plus slices 32 to 42: `50 passed`;
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | wc -l`: `12`, and `-m "slice-44 or slice-47 or slice-48 or slice-49 or slice-50"` collects 12;
  - the shape check: `2 1 1 0`, nothing listed, `cli.py` at most 250 (about 220);
  - arguments snapshot: only `delete` added.
- [ ] **Step 4: Checkpoint and commit.** Log `- 2026-09-27 slice 42 green.`, with:
  - `Evidence:` both answers, and stderr verbatim;
  - `Open questions:` whatever the scenarios leave silent, each with a reproduction;
  - `Next: slice 42.1, the fourth architecture review, which runs before the next plan (adrs/0011).`

  Set slice 42's Status to `green`.

---

## After the batch

Slice 42.1, the fourth architecture review, is not a task here. Architecture reviews run before planning, never inside a plan (adrs/0011). It follows the ten slices of this batch, and has two things to weigh:
- how `kb_requests.py` and `answers.py` grew;
- whether slice 42.2 and slice 47's refusals of Init and bootstrap still stand as placed.
