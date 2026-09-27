# shop-knowledge batch 11: slices 50.13 to 50.15

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, in slice order. Every task is a capability slice built under shopsystem-bdd:bdd-red-green, one scenario at a time. Its stop conditions, hand-back and checkpoint apply, and they override any step here that conflicts with them.

**Goal:** The three riskiest slices cut on 2026-09-27 (commit 6a1d535) from the spec as amended in bdbd580, in plan order:
- a check that finds faults still shows what is behind its type (50.13, adrs/0046);
- markdown stays well-formed whatever a value holds, and an empty list is shown as nothing (50.14, adrs/0043 and 0045);
- a renderer refuses an artifact of a type it does not render (50.15).

After them the seventh architecture review (50.16) falls due. It runs before the next plan (adrs/0010, 0011), so slices 50.17 to 50.22 are not in this batch.

**Architecture:** shop-knowledge is the Python package `shop_knowledge`, and its `shop-knol` command is a client of kb v0.2.1. Its scenarios are driven by pytest-bdd 8.1 step definitions under `tests/`:
- one `test_<feature>.py` per feature file;
- sibling modules a test module star-imports (adrs/0035);
- the shared steps and fixtures in `tests/conftest.py`;
- the one way of driving shop-knol in `tests/driver.py`.

Across the batch the code changes in three places:
- the check's handler and its answer (`cli._validate`, `answers.checked`);
- the markdown renderer (`renderers/markdown.py`);
- the three renderers that take one type each (`renderers/agent.py`, `skill.py`, `diagram.py`, with what they share in `renderers/source.py`).

**This plan carries no code** (adrs/0011). The implementer writes every change in the execution session. What each task gives instead:
- the slice and its scenarios;
- the observable and the unknown it settles;
- why each scenario is red today, found by running it in this checkout;
- where the change lands by CLAUDE.md's module map, and the rule it implements once;
- the decisions the spec leaves open, each resting on a passage;
- what existing steps and fixtures to reuse, by name;
- the commands, with counts from the tags;
- the checkpoint to log.

**Tech Stack:** Python 3.11, pytest 8 + pytest-bdd 8.1, kb v0.2.1 (`kb.content` for YAML, `kb.contract.kb_pb2` for faults and answers).

**Spec:** `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md` as amended in bdbd580. The passages this batch implements:
- the command table's validate row: "Validate; a check that finds faults refuses with them and still shows what is behind its type";
- the Renderers section's opening: "A renderer given an artifact of a type it does not render refuses it, naming the type";
- the `markdown` bullet: "an empty value, an empty list among them, is shown as nothing: the field's name and its colon, or an empty table cell. Whatever a value holds, the page stays well-formed markdown: a table row keeps one cell per column, and no line ends in a space."

Read CLAUDE.md alongside it, and in the slice plan slices 50.13 to 50.15 and the 2026-09-27 log entries from "Spec amended in bdbd580" on. The decisions this plan rests on are adrs/0023, 0029, 0035, 0038, 0041, 0043, 0044, 0045 and 0046.

## Global Constraints

- Feature files are read-only, tag lines included. The tags `@slice-50.13`, `@slice-50.14` and `@slice-50.15` are already written. Any diff under `features/` is a stop condition.
- kb is v0.2.1 in `.venv` and is never edited here (CLAUDE.md, rule 2).
- Every rule in CLAUDE.md holds at the end of every task. No module under `src/` or `tests/` goes past 250 lines (adrs/0034).
- Work on `main` in this checkout (adrs/0009). Run every command from the checkout's root. While scenarios are red, `make test`'s last line is make's own error, so read pytest's summary above it.
- Scratch files and probes go under `.superpowers/batch11/`, which `.git/info/exclude` covers. Never under `/tmp`.
- Commits: `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`. The message ends with the Co-Authored-By line of the model that made the commit. Each task makes one commit, holding the slice's change and its checkpoint. When the batch is done, push: `git push origin main` (adrs/0036).
- pytest-bdd prints `PytestRemovedIn10Warning`s, two for each `target_fixture` step. That is the baseline, not a fault.
- **Counts.** The suite collects 87 scenarios (`.venv/bin/python -m pytest --collect-only -q | grep -c ::`, run 2026-09-27). What the tags select:
  - `-m slice-50.13` selects 1;
  - `-m slice-50.14` selects 10: the four rows of the well-formed outline, and all six rows of the yes/no/empty outline, whose first four slice 50.11 made green;
  - `-m slice-50.15` selects 3;
  - `-m "slice-44 or slice-42.2"` selects 3, the check's earlier scenarios, which the shared Then Task 1 changes must keep green;
  - `-m "slice-20 or slice-50.6"` selects 3, the markdown pages Task 2 must keep byte for byte;
  - `-m "slice-17 or slice-18 or slice-19 or slice-50 or slice-50.7"` selects 5, the renderers' existing scenarios, which Task 3 must keep green.

  The test modules collect as follows: `tests/test_check_the_shops_knowledge_is_sound.py` 5, `tests/test_publish_what_the_shop_knows.py` 22.

  | after | failed | passed |
  |---|---|---|
  | before Task 1 (run 2026-09-27) | 17 | 70 |
  | 50.13 | 16 | 71 |
  | 50.14 | 10 | 77 |
  | 50.15 | 7 | 80 |

  The seven left red after the batch are slices 50.17 to 50.22's. Every scenario of this batch fails today on `StepDefinitionNotFoundError`, none on an assertion. Each is seen red on its own assertion only once its steps exist, and the checkpoint says so.
- **The size check**, run at the start and end of every task: `find src tests -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'`. Today it lists nothing. The modules this batch touches:

  | module | lines | note |
  |---|---|---|
  | `tests/publish_as_markdown.py` | 210 | too full for Task 2's steps |
  | `tests/test_publish_what_the_shop_knows.py` | 199 | |
  | `tests/test_check_the_shops_knowledge_is_sound.py` | 109 | |
  | `tests/conftest.py` | 72 | |
  | `src/shop_knowledge/cli.py` | 233 | |
  | `src/shop_knowledge/answers.py` | 143 | |
  | `renderers/markdown.py` | 94 | |
  | `renderers/source.py` | 14 | |
  | `renderers/agent.py`, `skill.py`, `diagram.py` | each under 70 | |

## Review Focus

writing-plans asks for a test in the owning task for each line here. In this project tests are scenarios, and feature files are the human gate, so no test is added. Each line goes into the owning task's checkpoint instead. A failure mode is logged as a thing checked. A behaviour is settled, under adrs/0044, by the principle it cites, or logged as a `QUESTION FOR THE SPEC` with its reproduction only when no principle answers it.

1. **A check whose faults include an unreadable file, beside something behind its type** (owner: Task 1). Slice 1.28's hand-mangled file and a decision behind its type together: after Task 1, the unreadable file's fault line and the `behind` list both appear, and stdout is still one YAML document that `--json` gives as the same structure, if `validate` takes `--json`. Log what it shows.
2. **`sound` on a check with faults and nothing behind** (owner: Task 1). After Task 1, a check with a fault and no stale artifact shows `sound: false` and an empty `behind` list on stdout, with the fault on stderr. Slice 44's two-fault scenario still passes, since its Thens read only stderr.
3. **A `|` in the field list, and in a nested mapping laid out inline in a cell** (owner: Task 2). The scenarios put the character in a table cell. After Task 2, publish a role whose top-level text field holds `a | b`. The field list is not a table, so the text shows as written, unescaped. Also publish a process step holding a mapping whose value holds `a | b`: inside the cell it is escaped like any cell text. Log both.
4. **Text holding a backslash before a `|`** (owner: Task 2). A step's `does` of `a \| b` in a table cell. After Task 2, the cell still has one cell's worth of text, and the page shows the user's backslash. Log how it is escaped. The spec's "a table row keeps one cell per column" is the principle. If no layout keeps both the text and the columns, that is a QUESTION FOR THE SPEC with this reproduction.
5. **The markdown renderer given any type, and a renderer given something that does not exist** (owner: Task 3). After Task 3, `render markdown tag/pricing` still publishes, since markdown is "for any type", as does `render markdown schema/decision`. `render agent role/nobody` is still refused on kb's read fault, not the type check: the read's faults come first. Log each.

---

### Task 1: Slice 50.13, a check that finds faults still shows what is behind its type

**Slice plan entry:** capability.
- Scenario: check-the-shops-knowledge-is-sound / The user is told what is behind its type even when the check finds faults.
- Observable: a user whose check finds faults sees them, one line each, and in the same run sees which artifacts are behind their type. The command still reports failure (adrs/0046).
- Unknown: whether a refusal can carry the check's answer on stdout while its faults still reach the user only through the one printer, one line each, exit 1.

**Why it is red today.**
- The scenario fails on `StepDefinitionNotFoundError`: its Given "a shop knowledge base where a decision is missing something its type requires and another decision was last checked against an older version of the decision type" is not defined. So is its first Then, "the fault is listed, naming the artifact and the place in it at fault".
- Once the steps exist, it is red on stdout. `cli._validate` passes kb's answer through `_answered` with its violations, which raises `Refused` before `answers.checked` is reached, so nothing is shown on stdout (adrs/0029).
- `answers.checked` also answers `sound: True` whatever it is given. Its docstring says it is only for "a check that found no fault".

**Where the change lands (CLAUDE.md's module map).**
- `answers.checked` shapes the check's answer, so `sound` comes from whether the check found faults or violations. The document is otherwise unchanged: `behind` under kb's own field names (adrs/0029). Its docstring says it answers every check.
- `cli._validate` shows the answer on stdout and refuses with the faults.
  - Rule 4 holds: the faults still reach stderr only through `Refused` and `main`'s one printer, one line each, exit 1. No handler prints a refusal of its own. Showing the answer is not printing a refusal.
  - The faults are still refused through `_answered`, the one way a kb answer's faults are (CLAUDE.md, Size and shape).
  - Whether the handler shows first and refuses after, or `Refused` carries the document for `main` to show, is the implementer's choice. The choice must not add a second printer or a second way to refuse, and the checkpoint says which was taken and why.
- The Given goes in `tests/test_check_the_shops_knowledge_is_sound.py`, beside the check's other Givens. Only one decision may be behind its type, because the Then "the other decision is listed as behind its type" names one. So the order matters:
  1. record the decision that will be behind;
  2. bring the decision type to version 2, as `_shop_with_a_decision_behind_its_type` does, through `shop-knol write`;
  3. record the decision that will be at fault, so it is checked against version 2;
  4. edit its file by hand to remove something its type requires, as `_shop_with_two_faults` does, saying so as CLAUDE.md's Step definitions ask.

  The Given gives the names the Thens need, through a fixture or `target_fixture`, not a second constant.
- The shared Then "it is not listed as a fault" (`_not_a_fault`) asserts today that stderr is empty and the exit is 0. Neither can hold beside the new scenario's faults. Its body changes so that it holds for both scenarios: the artifact behind its type appears on no fault line. The old scenario, with no faults at all, must keep its exit-0 assertion. Either say that only when stderr is empty, or move the exit to where its scenario already holds it. Whichever is chosen, `-m "slice-44 or slice-42.2"` stays green, and the checkpoint shows the old scenario's red when its exit is wrong (a throwaway change).
- The Then "the other decision is listed as behind its type" reads `shown`, the document on stdout, as `_listed_as_behind` does. If the shared `shown` fixture cannot read stdout on a failed command, say why in the checkpoint and read stdout directly.

**Decisions the spec leaves open:** none. adrs/0046 settles `sound: false` with the `behind` list on stdout beside the faults.

**Reuse:**
- `knol`, `record`, `start`, `whole` (driver);
- `WEEKLY`, `MONTHLY`, `SECTIONS`, `_check` (the When "the user checks the shop's knowledge");
- the shared Then "the command reports failure to whatever ran it";
- the setup shapes of `_shop_with_two_faults` and `_shop_with_a_decision_behind_its_type`, reused by calling or by a helper, never copied.

- [ ] **Step 1:** Run the size check. Run `.venv/bin/python -m pytest -q -m slice-50.13` and confirm `1 failed` on `StepDefinitionNotFoundError`. `-m "slice-44 or slice-42.2"` gives `3 passed`.
- [ ] **Step 2:** Under bdd-red-green, write the Given and the Thens, run the scenario, and see it red on stdout before any change under `src/`. Log the red assertion.
- [ ] **Step 3:** Make it green in `answers.checked` and `cli._validate`. `-m "slice-44 or slice-42.2"` stays green.
- [ ] **Step 4:** Run the Review Focus probes 1 and 2 under `.superpowers/batch11/`, and log what each shows.
- [ ] **Step 5:** `.venv/bin/python -m pytest -q` gives `71 passed, 16 failed`, the sixteen being slices 50.14, 50.15 and 50.17 to 50.22's. Run the size check. `git diff --stat -- features` is empty.
- [ ] **Step 6:** Checkpoint in the slice plan's log, and set slice 50.13's Status to green. The checkpoint holds:
  - the red runs;
  - the way chosen to show and refuse, and why;
  - the probes' outcomes;
  - the suite's line.

  Commit.

### Task 2: Slice 50.14, markdown stays well-formed whatever a value holds, an empty list shown as nothing

**Slice plan entry:** capability.
- Scenarios:
  - publish-what-the-shop-knows / Markdown stays well-formed whatever a value holds, all four rows: a cell holding the character that separates cells; text over more than one line; an empty value among a list's items; text ending in a space;
  - publish-what-the-shop-knows / Markdown never shows a yes, a no or an empty value the way a program prints it, all six rows. Its first four are green from slice 50.11; its two new rows are a role's empty list and a process step's empty list.
- Observable: a user publishing as markdown finds every table row with one cell per column, no line ending in a space, and every value shown. An empty list is shown as its field's name and colon, or as an empty cell (adrs/0043, 0045).
- Unknown: whether any text a value holds can be shown in a cell or a line as written, the character that separates cells among it, without the page's layout breaking.

**Why it is red today.**
- All six red rows fail on `StepDefinitionNotFoundError`. The first missing step is each row's Given:
  - "the process holds steps that each say more than one thing, one of them holding the character that separates table cells";
  - "... one of them holding text over more than one line";
  - "the role holds a list of plain values with an empty value among its items";
  - "the role holds a field whose text ends in a space";
  - "the role holds a field holding an empty list";
  - "the process holds steps that each say more than one thing, one of them an empty list".

  The well-formed outline's three Thens are not defined either:
  - "that directory holds a page where every table row has one cell for each column";
  - "no line on the page ends in a space";
  - "every value the <thing> holds is shown on the page".
- Once the steps exist, the rows are red on the page. A probe on 2026-09-27 showed each of these:
  - a step whose `does` is `Count a | b.` renders the row `| count | Count | Count a | b. |`, four cells under three columns;
  - a role holding `answers: ["a", null]` renders the bullet `  - ` (it ends in a space);
  - a role holding `empty: []` renders `- **empty**`, with no colon.

  A field whose text ends in a space renders its line ending in that space. `_inline` drops only the text's line breaks.
- Text over more than one line is already joined by a space in a cell (adrs/0041). That row may go green as soon as its steps exist. If so, credit it to adrs/0041's layout (slice 50.6) in the log.

**Where the change lands (CLAUDE.md's module map).**
- `renderers/markdown.py` alone, and the layout is still decided by a value's kind and shape, never a field's name (rule 5):
  - a cell's text escapes the character that separates cells;
  - a list item and a field line end where their text ends, with no trailing space;
  - an empty list in the field list is laid out as an empty value, by the same `_after_the_colon` that holds adrs/0043's one spelling of nothing;
  - an empty list in a cell is already an empty cell.
- Update the docstrings the change makes wrong, naming adrs/0045.
- Escaping belongs to a cell, not to every inline value: the field list is not a table, and a `|` there is shown as written (Review Focus 3). Where the escape is applied is the implementer's choice. It happens once, where a cell's text is made.
- The steps:
  - `tests/publish_as_markdown.py` is 210 lines, so the well-formed outline's steps go in a new sibling module beside it. Name it for its concern, not `test_*`. Only the publish feature's test module star-imports it (adrs/0035, CLAUDE.md Step definitions).
  - The two new empty-list Givens sit with the outline's other Givens in `tests/publish_as_markdown.py`, if it stays under 250 lines. Otherwise they go to the new module too.
  - Helpers both modules need (`_write_over`, `_role_page`, `_process_page`, `_step_holding` and the like) are imported from where they are, never copied. If that coupling reads badly, move them once to the one module both import, and say so.
- The well-formed Givens follow the yes/no/empty outline's pattern: each changes the Background role or process through `shop-knol write`, and gives its expected page as `page`, so a Then can check the whole page when it needs to.
  - The Then "every value the <thing> holds is shown on the page" checks that each value the Given wrote appears on the page, laid out as adrs/0041 and this slice say. The whole-page comparison against `page` is one way to do that.
  - The Thens "every table row has one cell for each column" and "no line on the page ends in a space" check the property itself, over the whole page:
    - count a row's cells as a markdown reader does, where an escaped separator is not a boundary;
    - check every line for a trailing space.

    Neither compares against a stored page. That way they catch a defect the expected page was written around.

**Decisions the spec leaves open.**
- How the separator is escaped: `\|`, GitHub-flavoured markdown's escape for a pipe in a table cell. It is markdown's own spelling, so no behaviour of its own (the batch 9 plan's Review Focus 1 said the same). A backslash the user wrote before a `|` is Review Focus 4's.
- A trailing space in text is not shown. The user approved this reading on 2026-09-27 ("the trailing space is not shown"), and the slice plan's log says so.
- An empty value among a list's items is a bullet with nothing after its dash, `  -`, since nothing is shown as nothing (adrs/0043) and the line may not end in a space.

**Reuse:**
- `knol`, `record`, `whole` (driver);
- `process_name`, `role_content`, `role_name`, `target` (publish feature);
- the When "the user publishes the <thing> as markdown into a directory" (`_publish_as_markdown`);
- the Thens `_a_page_of` and `_no_repr_on_the_page`;
- the helpers `_write_over`, `_role_page`, `_process_page`, `_step_holding`.

- [ ] **Step 1:** Run the size check, `.venv/bin/python -m pytest -q -m slice-50.14` (`6 failed, 4 passed`), and `-m "slice-20 or slice-50.6"` (`3 passed`).
- [ ] **Step 2:** Under bdd-red-green, one row at a time, the separator row first.
  - Write its Given and the three Thens, and see it red on the column count before any change under `src/`. Log the red assertion.
  - Make it green in `markdown.py`.
- [ ] **Step 3:** Take each other red row in turn:
  - the text over several lines;
  - the empty item among a list's items;
  - the text ending in a space;
  - the role's empty list;
  - the process step's empty list.

  Each is seen red on its own assertion before the change it needs. A row green as soon as its steps exist is credited to the change or slice that made it so, and logged.
- [ ] **Step 4:** `-m slice-50.14` gives `10 passed`. `-m "slice-20 or slice-50.6"` gives `3 passed`, the pages unchanged byte for byte.
- [ ] **Step 5:** Run the Review Focus probes 3 and 4 under `.superpowers/batch11/`, and log what each shows.
- [ ] **Step 6:** `.venv/bin/python -m pytest -q` gives `77 passed, 10 failed`. Run the size check. `grep -n "sections" src/shop_knowledge/renderers/markdown.py` shows the one name the renderer knows (adrs/0015) and no field name besides. `git diff --stat -- features src/shop_knowledge/types` is empty.
- [ ] **Step 7:** Checkpoint in the slice plan's log, and set slice 50.14's Status to green. The checkpoint holds:
  - the red runs;
  - the escape chosen and where it is applied;
  - the probes' outcomes;
  - the suite's line.

  Commit.

### Task 3: Slice 50.15, a renderer refuses an artifact of a type it does not render

**Slice plan entry:** capability.
- Scenario: publish-what-the-shop-knows / Publishing something as a kind of file it cannot become is refused, all three rows:
  - a process as an agent;
  - a role as a skill;
  - a role as a diagram.
- Observable: a user publishing something as a kind of file it cannot become is refused. They are told the artifact's type and the type that kind is made from, and find nothing written.
- Unknown: whether a renderer can tell what type an artifact is from what it reads through the contract before it lays anything out.

**Why it is red today.**
- All three rows fail on `StepDefinitionNotFoundError`. Each row's When is not defined: "the user publishes the process as agent into a directory", "the user publishes the role as skill into a directory", "the user publishes the role as diagram into a directory". The outline gives the kind without an article, so these are not the existing Whens' texts ("as an agent", "as a skill", "as a diagram"). The Then "the <kind> is rejected because it is not made from a <thing>, naming the type <thing>" is not defined either.
- Once the steps exist, each row is red on its exit.
  - A probe on 2026-09-27 published `tag/pricing` as each of the three: each exited 0 and wrote a file (`.claude/agents/pricing.md`, `pricing/SKILL.md`, `pricing.mmd`).
  - None of the three renderers checks what type it was given.
- kb's read answer carries the artifact's type (`kb_pb2.ReadResponse.type`), so the check needs no field of the content.

**Where the change lands (CLAUDE.md's module map).**
- `renderers/`. Each of `agent`, `skill` and `diagram` renders one type, which it names. Naming the type a renderer is for is that renderer's own knowledge (rule 5). The check itself is said once, not three times:
  - either as a function of `renderers/source.py`, which owns "reading the artifact a renderer publishes";
  - or beside it, if the module map's row would then say less than the module does. In that case update the row.
- The check comes after the read's own faults are refused, so a name that does not exist is still refused on kb's fault (Review Focus 5). It comes before anything is laid out or written: a refused `Rendered`, which `cli._render` refuses through `_answered` as it does the harness limits' faults (rule 6: nothing is written when a renderer refuses).
  - The fault is on the artifact published from, and says in plain words the artifact's type and the type the kind is made from. The user approved that reading on 2026-09-27, and the slice plan's log says so. For example: an agent is made from a role, and `process/restock-a-shelf` is a process.
  - Its `rule` names what it is, the way the harness limits' faults use `harness-limit`. The name is the implementer's choice.
- The skill renderer also reads the shared steps a process uses. The type check applies to the artifact published, not to those.
- `markdown` renders any type and takes no check.
- The steps go in `tests/test_publish_what_the_shop_knows.py`, which holds the other renderers' steps. It is 199 lines. If the outline's When and Then take it past 250, they go to a sibling module named for the concern, as Task 2's do.
  - The When takes the thing and the kind from the outline, parsed, and publishes the Background's process by `process_name` or its role by `role_name`, with the renderer named by the kind.
  - The Then asserts:
    - the command's one stderr line names the artifact and says both types, in the words the renderer uses;
    - exit non-zero, held by the shared Then "the command reports failure to whatever ran it";
    - nothing written, held by the Then "nothing is written to the directory".

    If "nothing is written to the directory" is not defined yet, it is defined here, and it checks the `target` directory is empty.

**Decisions the spec leaves open.**
- The fault's wording, beyond its two types. The Then asserts the line's whole text, so the wording is pinned by the suite once written. It follows the harness limits' faults: what the kind takes, then what this one is.

**Reuse:**
- `knol` (driver);
- `process_name`, `role_name`, `target` (publish feature);
- the shared Then "the command reports failure to whatever ran it";
- the existing renderer steps' shape (`_publish_as_an_agent`).

- [ ] **Step 1:** Run the size check. Run `.venv/bin/python -m pytest -q -m slice-50.15` and confirm `3 failed` on `StepDefinitionNotFoundError`. `-m "slice-17 or slice-18 or slice-19 or slice-50 or slice-50.7"` gives `5 passed`.
- [ ] **Step 2:** Under bdd-red-green, the process-as-agent row first.
  - Write the When and the Thens, and see it red on its exit (0) before any change under `src/`. Log the red assertion.
  - Make it green with the check and the agent renderer's use of it.
- [ ] **Step 3:** The role-as-skill row, then the role-as-diagram row. Each is seen red before its renderer takes the check, then green.
- [ ] **Step 4:** The renderers' existing scenarios stay green: `5 passed`.
- [ ] **Step 5:** Run the Review Focus probe 5 under `.superpowers/batch11/`, and log what each command shows.
- [ ] **Step 6:** `.venv/bin/python -m pytest -q` gives `80 passed, 7 failed`, the seven being slices 50.17 to 50.22's. Run the size check. `git diff --stat -- features src/shop_knowledge/types` is empty.
- [ ] **Step 7:** Checkpoint in the slice plan's log, and set slice 50.15's Status to green. The checkpoint holds:
  - the red runs;
  - where the check lives;
  - the fault's wording;
  - the probes' outcomes;
  - the suite's line.

  Commit.

## After the batch

- [ ] Final whole-branch review over this batch's commits, on the most capable model, against the plan, CLAUDE.md and the ADRs above. The reviewer runs the suite and the checks themselves.
- [ ] Log its findings and rulings in the slice plan. Push: `git push origin main` (adrs/0036).
- [ ] Then slice 50.16, the seventh architecture review, runs before slices 50.17 to 50.21 are planned (adrs/0010, 0011). Slice 50.22 waits for kb's release.
