# shop-knowledge batch 10: slices 50.10 to 50.12

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, in slice order. The capability tasks (1 and 2) are built under shopsystem-bdd:bdd-red-green, one scenario at a time. Its stop conditions, hand-back and checkpoint apply, and they override any step here that conflicts with them.

**Goal:** The three slices cut on 2026-09-27 (commit a9803d9) from the batch 9 reviews, in plan order:
- shop-knol refuses, never tracebacks, when the working directory no longer exists (50.10);
- markdown spells a yes, a no and an empty value in words (50.11, adrs/0043);
- the batch 9 review's minor findings are tidied (50.12, enabling).

**Architecture:** shop-knowledge is the Python package `shop_knowledge`, and its `shop-knol` command is a client of kb v0.2.1. Its scenarios are driven by pytest-bdd 8.1 step definitions under `tests/`: one `test_<feature>.py` per feature file, sibling modules a test module star-imports (adrs/0035), the shared steps and fixtures in `tests/conftest.py`, and the one way of driving shop-knol in `tests/driver.py`. Across the batch the code changes in three places:
- the `init` argument's default (`src/shop_knowledge/arguments.py`);
- the markdown renderer's inline layout (`src/shop_knowledge/renderers/markdown.py`);
- the harness limits' faults (`src/shop_knowledge/renderers/limits.py`), in the tidy only.

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

**Spec:** `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md`: the CLI section's "shop-knol never shows a traceback" and its `shop-knol init [<root>]` row, and the Renderers section's `markdown` bullet, amended in 57a1305. Read CLAUDE.md alongside it, and in the slice plan slices 50.10 to 50.12, the 2026-09-27 batch 9 final review entry and the re-slice entries after it. The decisions this plan rests on are adrs/0032, 0035, 0037, 0038, 0041, 0042 and 0043.

## Global Constraints

- Feature files are read-only, tag lines included. The tags `@slice-50.10` and `@slice-50.11` are already written. Any diff under `features/` is a stop condition.
- kb is v0.2.1 in `.venv` and is never edited here (CLAUDE.md, rule 2).
- Every rule in CLAUDE.md holds at the end of every task. No module under `src/` or `tests/` goes past 250 lines (adrs/0034).
- Work on `main` in this checkout (adrs/0009). Run every command from the checkout's root. While scenarios are red, `make test`'s last line is make's own error, so read pytest's summary above it.
- Scratch files and probes go under `.superpowers/batch10/`, which `.git/info/exclude` covers (it excludes `.superpowers/`). Never under `/tmp`.
- Commits: `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`. The message ends with the Co-Authored-By line of the model that made the commit. Each task makes one commit, holding the slice's change and its checkpoint. When the batch is done, push: `git push origin main` (adrs/0036).
- pytest-bdd prints `PytestRemovedIn10Warning`s, two for each `target_fixture` step. That is the baseline, not a fault.
- **Counts.** The suite collects 72 scenarios (`.venv/bin/python -m pytest --collect-only -q | grep -c ::`, run 2026-09-27). What the tags select:
  - `-m slice-50.10` selects 2: one in the start feature, one in the read-back feature;
  - `-m slice-50.11` selects 4, the four rows of the yes/no/empty outline;
  - `-m slice-50.6` selects 2, the markdown layout outline, which runs under the Then Task 2 widens;
  - `-m "slice-4 or slice-47 or slice-50.8"` selects 7, the start scenarios that guard `init`'s default.

  The test modules collect as follows: `tests/test_publish_what_the_shop_knows.py` 12, `tests/test_start_a_shop_knowledge_base.py` 10, `tests/test_read_back_what_the_shop_knows.py` 13.

  | after | failed | passed |
  |---|---|---|
  | before Task 1 (run 2026-09-27) | 6 | 66 |
  | 50.10 | 4 | 68 |
  | 50.11 | 0 | 72 |
  | 50.12 | 0 | 72 |

  Every one of the six fails today on `StepDefinitionNotFoundError`, none on an assertion. pytest-bdd names only a scenario's first missing step, so a Then may be missing too: the start and read-back scenarios' Then, "the user is shown the refusal in plain words, never a traceback", is not defined, and neither is the outline's "that directory holds a page of the <thing>". Each scenario is seen red on its own assertion only once its steps exist, and the checkpoint says so.
- **The size check**, run at the start and end of every task: `find src tests -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'`. Today it lists nothing. The modules this batch touches: `tests/test_start_a_shop_knowledge_base.py` 210, `tests/test_publish_what_the_shop_knows.py` 198, `tests/test_read_back_what_the_shop_knows.py` 194, `tests/publish_as_markdown.py` 110, `tests/read_back_from_elsewhere.py` 88, `tests/conftest.py` 63, `tests/driver.py` 47, `src/shop_knowledge/cli.py` 233, `src/shop_knowledge/arguments.py` 115, `renderers/markdown.py` 81, `renderers/limits.py` 37.

## Review Focus

writing-plans asks for a test in the owning task for each line here. In this project tests are scenarios, and feature files are the human gate, so no test is added. Each line goes into the owning task's checkpoint instead: a failure mode as a thing checked, or a behaviour as a `QUESTION FOR THE SPEC` with its reproduction.

1. **Every other command from a removed working directory** (owner: Task 1). The scenarios cover `init` and `read`, standing for every command that finds a knowledge base. After Task 1, from a directory under `.superpowers/batch10/` removed out from under the shell, run `init elsewhere`, `list --type decision`, `create decision --from x.yaml -m m`, `render markdown decision/x --to out` and `validate`, each with `KB_ACTOR=a`. Each writes exactly one line to stderr, no `Traceback`, and exits 1. Log each line.
2. **`KB_ROOT` naming a store while the working directory is removed** (owner: Task 1, the formulator's question 2). Run `read` from a removed directory with `KB_ROOT` naming a store that exists. Log whether it reads through `KB_ROOT` or refuses. Either is a QUESTION FOR THE SPEC: the spec says the store is found "upward from the working directory ... or through `KB_ROOT`", and says nothing of a working directory that is gone.
3. **`init <absolute path>` from a removed working directory** (owner: Task 1, the formulator's question 4). Run `KB_ACTOR=a shop-knol init <absolute path to an empty directory>` from a removed directory. Log whether it starts `kb/` there or refuses. The spec's init row gives the argument to "start a knowledge base somewhere else on purpose", which reads as working. A refusal is a QUESTION FOR THE SPEC with this reproduction.
4. **Text that reads like a yes, a no or nothing** (owner: Task 2). adrs/0043 is about values that are a yes, a no or empty, not about text. After Task 2, in a throwaway store, publish as markdown a role holding `motto: "yes"`, `flag: "True"` and `none: "null"`, all quoted in the file so each is text. Each is shown as written, with no word swapped in. Today `"yes"` already shows as `yes`, so on the page a yes and the text `yes` look the same by adrs/0043's choice. The code tells them apart by what kind of value each is, never by spelling. Log what the page shows. A text `True` on a page is text the user wrote, not a program's spelling, and no scenario holds one.
5. **A yes, a no or nothing where a block cannot sit** (owner: Task 2). adrs/0043 says an empty value is "nothing between the separators where it sits inline". After Task 2, publish a process one of whose steps holds a field that is a mapping with a yes and a null inside it; a table cell lays that mapping out inline. Also try a shared-step use binding a setting to a null value, and a role whose `harness` group holds a boolean field. The binding's schema may require text, and the role's schema closes the harness group (`additionalProperties: false`), so kb may refuse either; log any refusal as kb's, not a defect. Check that the inline mapping shows `yes`/`no` and nothing, with no trailing space on any line, `- **field**:` lines included. Log what each shows.

---

### Task 1: Slice 50.10, shop-knol refuses, never tracebacks, when the working directory no longer exists

**Slice plan entry:** capability.
- Scenarios:
  - start-a-shop-knowledge-base / Starting a knowledge base from a directory that has been removed ends in a plain refusal;
  - read-back-what-the-shop-knows / Reading from a directory that has been removed ends in a plain refusal.
- Observable: a user whose shell sits in a directory that has since been removed is refused in one plain line, not shown a traceback, whether they start a knowledge base or read from one.
- Unknown: whether shop-knol can meet a working directory that no longer exists with its own refusal before it has taken any argument, with the working directory still `init`'s default and that default still declared once (adrs/0032, 0037).

**Why it is red today.**
- Both scenarios fail on `StepDefinitionNotFoundError`: the Givens "the user is working in a directory that has since been removed" (start) and "the user is working in a directory that has since been removed, and nothing names a knowledge base" (read-back) are not defined. Neither is their shared Then, "the user is shown the refusal in plain words, never a traceback".
- Once the steps exist, each is red on its Then. The root cause was reproduced on 2026-09-27 for `init`, `init elsewhere`, `read decision/x` and `list --type decision`: each ends in `FileNotFoundError: [Errno 2] No such file or directory`, a full traceback, raised from `Path.cwd()`. `arguments.py` declares `init`'s `root` with a default that is the working directory, evaluated when `command_parser()` builds the parser. That happens for every command, before `cli._run`'s guard that turns an `OSError` into a fault. `cli._parsed` catches only `ArgumentRefused`.
- Before slice 50.8 (commit 049bb00), `read` from a removed directory gave one line, `No such file or directory`, exit 1. So this is a regression, not behaviour never held.

**Spike, already run (its result, not its code).** A child process can be left running from a removed working directory: `subprocess`'s pre-exec hook runs in the child after the child has entered `cwd`, so removing the directory there leaves `python -m shop_knowledge` started in a directory that no longer exists. Python starts, and the traceback is shop-knol's own. Any other way that gives the same state will do.

**Where the change lands (CLAUDE.md's module map).**
- The fix is in `arguments.py`. It owns every command's arguments, and `root`'s meaning is declared there once (adrs/0032). The default must stop being evaluated when the parser is built. The working directory stays the default, and `init -h` still says so. Whether the parser then gives a relative path or leaves the default to be resolved later is the implementer's choice. Either way, the working directory is read only where `cli._run`'s guard already turns an operating system's refusal into a fault. No new catch is added beside it (rule 4: one way to refuse). If the working directory must be read outside that guard, stop and hand back.
- `kb_requests.init_request` sends `root` to kb as text. It must still send what kb resolves as the working directory. The seven start scenarios under `-m "slice-4 or slice-47 or slice-50.8"` guard that.
- The Givens:
  - The start feature's Given goes in `tests/test_start_a_shop_knowledge_base.py`, which gives the directory the user works in through the `start_in` fixture.
  - The read-back Given goes in `tests/read_back_from_elsewhere.py`, the sibling module holding the steps about where the knowledge base is found, which give `workdir`. Its docstring counts "the five scenarios that give `workdir`". It becomes six, and the docstring says so.
- How shop-knol is run from a directory removed once its process is in it is said once, in `tests/driver.py`, the one way the steps drive shop-knol (CLAUDE.md, Step definitions). The existing Whens are reused by their text and unchanged in what they say: "the user starts a shop knowledge base there without naming a directory, saying who they are" (`_start_saying_who`, through `start_in`) and "the user reads the decision" (`_read_the_decision`, through `workdir`). If a When's body must change to carry the removal, it changes for every scenario it serves, and every scenario that uses it stays green.
- The shared Then, "the user is shown the refusal in plain words, never a traceback", is used by two features, so it goes in `tests/conftest.py`. It says what the existing Then "the user is shown that fault in plain words, never a traceback" (`_shown_in_plain_words`) says. Define it once, with both texts on the one body, so no assertion is written twice. It also holds the one-line part of rule 4: the refusal is exactly one line on stderr. If adding that to the shared body turns an existing scenario red, the new text gets a body of its own that reuses the shared one, and the checkpoint logs why.
- The read-back Given says "nothing names a knowledge base", so, like `_working_elsewhere_naming_nothing`, it removes `KB_ROOT` from `env`. It depends on `decision_id`, as that Given does, so the Background has run first.

**Decisions the spec leaves open.**
- What the refusal says. The scenarios ask only for a refusal in plain words. The spec lists no refusal for a working directory that is gone. The line is whatever `cli._run`'s guard makes of the operating system's refusal. The Then asserts no wording, and the checkpoint logs the line each command gave. It stays the formulator's question 1, a QUESTION FOR THE SPEC.

**Reuse:** `knol`, `start` (driver); `env`, `shop`, the shared Then "the command reports failure to whatever ran it" (conftest); `start_in`, `_start_saying_who` (start feature); `workdir`, `decision_id`, `_read_the_decision` (read-back feature).

- [ ] **Step 1:** Run the size check. Run `.venv/bin/python -m pytest -q -m slice-50.10` and confirm `2 failed`, each on `StepDefinitionNotFoundError`.
- [ ] **Step 2:** Under bdd-red-green, take the start scenario first. Write its steps, run `.venv/bin/python -m pytest -q -m slice-50.10 tests/test_start_a_shop_knowledge_base.py`, and see it red on its Then, the traceback, before any change under `src/`. Log the red run's assertion.
- [ ] **Step 3:** Make it green with the change in `arguments.py`. Confirm `.venv/bin/python -m shop_knowledge init -h` still shows `root` as optional, with the working directory as its default. Run `-m "slice-4 or slice-47 or slice-50.8"` and get `7 passed`.
- [ ] **Step 4:** Take the read-back scenario. Write its Given, then run it. Log whether it goes green at once, since the Step 3 change fixed its cause. If so, credit its green to Step 3, and log the red observed when Step 2's run first showed the traceback for every command. Otherwise see it red on its own assertion, then make it green.
- [ ] **Step 5:** Run the Review Focus probes 1, 2 and 3 under `.superpowers/batch10/`. Log each command's stderr line and exit code, and the two QUESTION FOR THE SPEC outcomes.
- [ ] **Step 6:** `.venv/bin/python -m pytest -q` gives `68 passed, 4 failed`, the four failing being `-m slice-50.11`'s. `.venv/bin/python -m pytest --collect-only -q | grep -c ::` gives 72. Run the size check. `git diff --stat -- features` is empty.
- [ ] **Step 7:** Checkpoint in the slice plan's log, and set slice 50.10's Status to green. The checkpoint holds:
  - the red runs seen, each with its assertion;
  - what `init` and `read` print from a removed directory;
  - the probes' outcomes;
  - the suite's line.

  Commit.

### Task 2: Slice 50.11, markdown spells a yes, a no and an empty value in words

**Slice plan entry:** capability.
- Scenarios: publish-what-the-shop-knows / Markdown never shows a yes, a no or an empty value the way a program prints it, all four rows:
  - a role's yes and no;
  - a role's empty value;
  - a process step's yes and no;
  - a process step's empty value.
- Observable: a user publishing a role or a process as markdown finds a yes as `yes`, a no as `no` and an empty value as nothing, in the field list and in a table cell alike. The page never shows `True`, `False`, `None`, `true`, `false` or `null` (adrs/0043).
- Unknown: whether a value the user wrote as a yes, a no or an empty value still reaches the page as one after kb has checked and stored it, and is told apart there from text that reads `yes`.

**Why it is red today.**
- All four rows fail on `StepDefinitionNotFoundError`. The first missing step is each row's Given:
  - "the role holds a field that is a yes and a field that is a no";
  - "the role holds a field with no value";
  - "the process holds steps that each say more than one thing, one of them a yes and a no";
  - "the process holds steps that each say more than one thing, one of them with no value".

  The Then "that directory holds a page of the <thing>" is not defined either.
- Once the steps exist, each row is red on the page. A probe on 2026-09-27 in a throwaway store showed kb accepting and keeping each kind of value:
  - a role with `on_call: true`, `retired: false` and `answers_to_nobody: null` is shown as `- **on_call**: True`, `- **retired**: False` and `- **answers_to_nobody**: None`;
  - a process step with `optional: true`, `skippable: false` shows cells `True` and `False`;
  - a step with `note: null` shows the cell `None`.

  The cause is `markdown._inline`'s last line: a plain value's text is what Python's `str()` makes of it.
- The same probe showed the text `motto: "yes"` as `yes`. So text survives as text, and the yes/no values reach the renderer as a yes and a no, not as text. The unknown is to be confirmed, not assumed, in the red run.

**Where the change lands (CLAUDE.md's module map).**
- `renderers/markdown.py`, `_inline`: a yes, a no and nothing get their own spelling ahead of the plain-value fallback. The branch is on what kind of value it is, never on a field's name (rule 5) and never on its spelling. The text `True` stays `True`.
- Every place a value is laid out passes through `_inline`: the field list, a table cell, and a mapping or list laid out inline. So the rule is implemented once there.
- The field list's line for a field holding nothing is `- **field**:`, with no trailing space (adrs/0043's example). `_items` writes a field's name, `: ` and its inline value. The implementer makes that line end at the colon when the value lays out as nothing, without a second spelling of "nothing" beside `_inline`'s.
- Update `_inline`'s docstring, and the module docstring if it no longer says what the module does, to name adrs/0043.
- The steps go in `tests/publish_as_markdown.py`, the markdown steps' own module (adrs/0035). It is 110 lines, so there is room.
  - The two role Givens change the Background role through `shop-knol write`, as `_role_holds_more_than_one_tag` does: the `role_content` fixture's content without its title, plus the new fields. The role's top level is open in its schema, so a field of the user's own naming is kept.
  - The two process Givens change the Background process through `shop-knol write`. They start from its whole read (`whole`, through the driver), with the extra field on one step. A process step's items are open in the schema too. If writing back the whole read's step ids is refused, the Given writes the steps as the Background's Given first gave them, and the checkpoint says which.
  - Name the fields in the user's words, the way the review's reproduction did.
- The Then "that directory holds a page of the <thing>" pins the exact page for each row, line by line, as `_steps_as_a_table` and `_tags_as_a_bullet_list` do. That way adrs/0043's spelling is held by the suite, not only its absence. The Then text is the same for the two rows of one thing, so the page each row expects must come from its Given: a fixture the Given gives is one way. How is the implementer's.
- The existing Then "nothing on the page is a programming language's representation of a value" (`_no_repr_on_the_page`) also looks for the spellings adrs/0043 rules out: `True`, `False`, `None`, `true`, `false`, `null` as a value. This was the batch 9 final review's minor 7. It looks for them as a whole value on the page, not as a substring of prose. The Background role's section says "Counts, then orders." and a later scenario's text may hold any word. Slice 50.6's two rows run under the widened Then and stay green: `-m slice-50.6` gives `2 passed`.

**Decisions the spec leaves open.** None about spelling: adrs/0043 and the amended Renderers bullet settle a yes, a no and nothing. Two cases are left open and are not decided here:
- whether a field holding nothing should be left off the page (adrs/0043 keeps it, as `- **field**:`);
- how an empty list is shown (carried from 50.6).

**Reuse:**
- `knol`, `record`, `whole` (driver);
- `process_name`, `role_content`, `target` (publish feature);
- the When "the user publishes the <thing> as markdown into a directory" (`_publish_as_markdown`);
- the Then "nothing on the page is a programming language's representation of a value".

- [ ] **Step 1:** Run the size check. Run `.venv/bin/python -m pytest -q -m slice-50.11` and confirm `4 failed`, each on `StepDefinitionNotFoundError`.
- [ ] **Step 2:** Under bdd-red-green, one row at a time, the role's yes and no first. Write its Given and the Then, run it, and see it red on the page's `True`/`False`, before any change under `src/`. Log the red assertion. Make it green in `_inline`.
- [ ] **Step 3:** The role's empty value. See it red on `None`, and on the trailing space if the first cut leaves one. Make it green.
- [ ] **Step 4:** The two process rows in turn, each seen red on its own cell before any change it needs. If a row is green as soon as its steps exist, credit it to the step whose change made it so, and log that.
- [ ] **Step 5:** Widen `_no_repr_on_the_page`. Show that it catches the defect: a throwaway revert of `_inline`'s new branch turns the rows red on that Then too. Restore it, and log the run. Then `-m slice-50.6` gives `2 passed` and `-m slice-50.11` gives `4 passed`.
- [ ] **Step 6:** Run the Review Focus probes 4 and 5 under `.superpowers/batch10/`, and log what each page shows.
- [ ] **Step 7:** `.venv/bin/python -m pytest -q` gives `72 passed`. Run the size check. `git diff --stat -- features src/shop_knowledge/types` is empty. `grep -n "sections" src/shop_knowledge/renderers/markdown.py` shows the one name the renderer knows (adrs/0015) and no field name besides.
- [ ] **Step 8:** Checkpoint in the slice plan's log, and set slice 50.11's Status to green. The checkpoint holds:
  - the red runs seen;
  - how the unknown was answered;
  - the probes' outcomes;
  - the suite's line.

  Commit.

### Task 3: Slice 50.12, the batch 9 review's minor findings are tidied

**Slice plan entry:** enabling, no unknown. Check:
- `.venv/bin/python -m pytest -q` gives `72 passed`, the same as after slice 50.11;
- `grep -rn "Task [0-9]" src tests --include="*.py"` gives nothing;
- `grep -c "role/stock-keeper" tests/publish_as_markdown.py` gives 0;
- `grep -c "Fault(" src/shop_knowledge/renderers/limits.py` gives 1;
- in the publish feature's test module, every fixture is defined before the first step;
- a reader finds each docstring naming everything its code holds and does: the markdown renderer's table test and field layout, and the publish feature's markdown steps module;
- the size check lists nothing;
- `git diff --stat -- features src/shop_knowledge/types` is empty.

Observable: a reader finds:
- the markdown steps publishing whichever role a Given names;
- every fixture of the publish feature in one place;
- the harness limits' faults built one way;
- no docstring pointing at a task of a batch plan;
- the docstrings the review found short or awkward saying what their code does.

**Why the check fails today** (each run or read on 2026-09-27, before Tasks 1 and 2):
1. `tests/publish_as_markdown.py`'s module docstring says it holds "the When ... and the Thens". It also holds the Givens "the process holds steps that each say more than one thing" and "the role holds more than one tag", and after Task 2 four more. This is the review's "a sibling module's docstring undercounting what it holds".
2. `tests/test_publish_what_the_shop_knows.py` defines `role_name` at line 155, among the agent steps, while its other fixtures (`role_content`, `target`, `before`) sit together at lines 49 to 66. This is the review's "a fixture defined out of its usual place".
3. `_publish_as_markdown` names `"role/stock-keeper"` itself rather than taking `role_name`, and so does `_role_holds_more_than_one_tag`'s write. After Task 2, so may the new role Givens. `grep -c "role/stock-keeper" tests/publish_as_markdown.py` gives 2 today.
4. `role_content`'s docstring ends "(Task 1, decision 2)", pointing at batch 9's plan. The decision it stands for is adrs/0035's: a sibling module reaches the test module's content only through a fixture, never by importing it. `grep -rn "Task [0-9]" src tests --include="*.py"` finds that one line today.
5. `renderers/limits.py` builds `kb_pb2.Fault(... rule="harness-limit" ...)` three times, once in `skill` and twice in `agent`, the same way each time. `grep -c "Fault(" src/shop_knowledge/renderers/limits.py` gives 3.
6. `markdown._is_table`'s docstring ("... and not, say, a part collection's own kind of emptiness: an empty list stays in the field list") reads awkwardly (the batch 9 final review).
7. `markdown._items`'s docstring says a list field's items are "plain values", but its list branch lays out any item inline (the 50.9 review's "not called for", taken up here).

**Where the change lands.** Only in the files named above. No behaviour changes:
- every faults line the agent and skill scenarios assert stays byte for byte (`-m "slice-18 or slice-50.7"` gives `2 passed`);
- every page stays as it was.

Details for some of the items:
- For item 3, the markdown When takes `role_name`, as `_publish_as_an_agent` does, and so does every markdown Given that writes over the Background role.
- For item 5, one private function in `limits.py` builds a harness-limit fault from the artifact, the path and the message. `skill` and `agent` call it. The docstring keeps each limit's source.
- For items 6 and 7, the docstring says what the function decides, in the plain words the module's other docstrings use.

The tidy adds nothing that no finding asks for.

**Reuse:** nothing new. This task only moves and rewords.

- [ ] **Step 1:** Run the size check, `.venv/bin/python -m pytest -q` (`72 passed`) and each grep in the check, and log the before-values.
- [ ] **Step 2:** Items 2 and 3, then run `-m "slice-20 or slice-50 or slice-50.6 or slice-50.7 or slice-50.11"` and get `9 passed`.
- [ ] **Step 3:** Items 1 and 4, the test docstrings.
- [ ] **Step 4:** Item 5, then run `-m "slice-18 or slice-50.7"` and get `2 passed`.
- [ ] **Step 5:** Items 6 and 7.
- [ ] **Step 6:** Run every command in the check, and get the values it gives. `.venv/bin/python -m pytest -q` gives `72 passed`.
- [ ] **Step 7:** Checkpoint in the slice plan's log (each check's before and after), and set slice 50.12's Status to green. Commit.

## After the batch

- [ ] Final whole-branch review over this batch's commits, on the most capable model, against the plan, CLAUDE.md and the ADRs above. The reviewer runs the suite and the checks themselves.
- [ ] Log its findings and rulings in the slice plan, as batch 9's final review did. Push: `git push origin main` (adrs/0036).
