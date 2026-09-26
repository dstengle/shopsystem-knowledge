# shop-knowledge batch 1: slices 1.29, 4, 15, 16, 17 and 18

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, in slice order. Inside a capability task, follow `shopsystem-bdd:bdd-red-green` scenario by scenario; its stop conditions, hand-back and checkpoint apply, and they override any step here that conflicts with them.

**Goal:** shop-knowledge gets the conventions its code is held to and a first review against them. Then a new knowledge base arrives with all seven of the shop's types on one base. A user applies a batch of changes as one change, reviews the history of one thing with who, when, what and why, and publishes a process as a skill with its reused steps written out in full. A skill that runs past the limits the harness publishes is refused, and nothing is written.

**Architecture:** shop-knowledge (`/home/vscode/shopsystem-knowledge`) is the Python package `shop_knowledge`. Its `shop-knol` command (`cli.py`) calls kb through kb's in-process client (`kb.client.connect`) with the contract's messages (`kb.contract.kb_pb2`), and reads and prints YAML 1.2 through `kb.content`. The shop's types are YAML files under `src/shop_knowledge/types/`, created as schema artifacts by `bootstrap.py` when `shop-knol init` starts a knowledge base. This batch adds:
- the five missing types and the base all seven build on (Task 2);
- `batch.py`, which reads a batch file into the operations of one Apply, and `shop-knol apply` (Task 3);
- `shop-knol journal --artifact`, and a test-only clock that sets the day kb stamps its history with (Task 4);
- `renderers/`, whose `skill` renderer reads a process through the contract and gives back the files to write, and `shop-knol render` (Task 5);
- `renderers/limits.py`, which checks a skill against the harness's published limits before anything is written (Task 6).

kb is **not** a checkout here. It is `shopsystem-kb` v0.2.0, installed from its git tag into this checkout's `.venv` by `make dev`, and it is never edited from this repository.

**Provenance:** Every code block in this plan was assembled in a scratch clone of this repository (`/tmp/skb1/shop`) on 2026-09-26, run with this checkout's `.venv/bin/python` and `PYTHONPATH=/tmp/skb1/shop/src`. Each task was applied in order and run. The red and green results, the suite counts and the Review Focus reproductions below are what those runs gave. The plan was then replayed from its own text in a fresh clone (`/tmp/skb1-replay`, with `.venv` linked to this checkout's), in the foreground: every red and every suite count was as stated, Task 2's probe printed exactly its expected text, and every file under `src/` and `tests/` came out byte-identical to the scratch run's. Task 1's review was stood in for by a log line saying no refactor, since an Opus review cannot be replayed. This checkout was not touched.

**Tech Stack:** Python 3.11, setuptools (src layout), kb v0.2.0 (protobuf contract, in-process client, JSON Schema Draft 2020-12 types with kb's `ref`, `parts`, `sections`, `summary` and `title` keywords, `allOf` composition and `kb:schema/<type>#/...` shared shapes), pytest 8 + pytest-bdd 8, argparse.

**Spec:** `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md` (The CLI, Bootstrap types, Renderers). kb's schema language is in `/home/vscode/shopsystem-kb/docs/superpowers/specs/2026-09-23-kb-design.md` (Artifact model, Schema language), read-only. Slice plan: `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, slices 1.29, 4, 15, 16, 17, 18. Feature files: `features/`. Each capability slice's scenarios carry `@slice-<n>`, so `make test` style runs select a slice with `.venv/bin/python -m pytest -q -m slice-<n>`.

## Global Constraints

- Feature files are read-only. Only `slicing-into-increments` edits a tag line, and only `formulating-features` edits a Given, When or Then. Any other diff under `features/` is a stop condition.
- Code only what a scenario asserts (bdd-red-green). Where the scenarios are silent the code is silent, and the silence goes into the checkpoint entry as an open question. The decisions this plan makes are listed below, each tied to the spec line or scenario that asks for it.
- kb is v0.2.0 from its tag, in `.venv`, and is never edited here. "shop-knowledge never touches kb's files or git. It calls the contract through the in-process client." A kb change a slice needs is not coded: it is logged in the slice plan as a request to bump the pin, and the slice stops.
- "Every mutating command requires an actor and `-m`." "The actor comes from `KB_ACTOR` as `role` or `role:execution-id`."
- "Every file shop-knol reads or writes, on `create`, `write`, `append`, `apply`, and in its own output, is YAML 1.2, read and written the way kb reads content." "Output is YAML by default."
- "shop-knol never shows a traceback." "Errors are printed as returned by kb, with artifact, path, and message, and exit non-zero."
- Bootstrap types: "Schema artifacts for: `decision`, `feature`, `work-item`, `role`, `process`, `step`, `tag`. Plus whatever data-type schemas the process and feature schemas share through `$ref`." "All seven build on a `shop-artifact` base schema through kb's composition mechanism, so the fields every shop artifact carries, such as owner, status, and tags, are declared once." "`process` declares a `steps` part collection whose items either define a step inline or carry `uses: <ref to step>` and `with: <bindings>`." "`role` separates the harness contract fields from the corpus identity fields into two named field groups." "`tag` is a title and description; a `tags` reference field on other types targets it."
- Renderers: "Client code, invoked only by `shop-knol render`. Each reads the resolved whole artifact, the stubs of its references, and its schema through the contract, and writes files to the target directory." "`skill` for `process`: `SKILL.md` in Anthropic's frontmatter-plus-body shape with resolved steps as the body." "`skill` and `agent` validate their output against the limits the harness publishes and fail rather than emit something it would reject."
- `shop-knol apply --from <batch>` maps to Apply; `shop-knol journal [--artifact] [--actor] [--execution] [--since]` maps to Journal; `shop-knol render <renderer> <id> --to <dir>` is client-side rendering. This batch adds only the options its scenarios use: `journal --artifact`; `--actor`, `--execution` and `--since` are slice 36's.
- Work on `main` in this checkout. `make test` runs the suite in `.venv`; while scenarios are red its last line is make's own `Error 1`, so read pytest's summary line above it.
- Commits: `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`, the message ending with the Co-Authored-By line of the model that made the commit, e.g. `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
- pytest-bdd prints `PytestRemovedIn10Warning`s, two for each `target_fixture` step. That is the baseline, not a fault.
- Baseline before Task 1: `55 failed, 7 passed`. After each task, pytest's summary is: Task 1 `55 failed, 7 passed`; Task 2 `54 failed, 8 passed`; Task 3 `53 failed, 9 passed`; Task 4 `52 failed, 10 passed`; Task 5 `51 failed, 11 passed`; Task 6 `50 failed, 12 passed`. The slices already green (`-m "slice-1 or slice-1.17 or slice-1.24 or slice-1.27 or slice-1.28"` → `7 passed`) stay green after every task.

## Decisions this plan makes (the spec left them open or silent)

1. **The conventions the review holds the code to.** This repository has no `CLAUDE.md`. Task 1 writes one in the shape of kb's: a module map (what each module owns and never holds), the rules that make whole classes of defect unreachable here (kb only through its contract, YAML 1.2 through `kb.content`, one refusal printer, types only as data, renderers that only read), size limits (no module over 250 lines), and how the step definitions drive shop-knol. Each later task that adds a module adds its row, as kb's slices do.
2. **The first review's gate.** The review is an Opus subagent at execution time; what it finds cannot be planned. If it calls for any refactor, the refactors are cut as slices 1.30 onward (enabling, each with a check), the batch **stops after Task 1**, and Tasks 2 to 6 are re-planned over the new shape. If it calls for none, Tasks 2 to 6 run as written. Defects the review finds that a planned slice already owns (the unset `KB_ACTOR` traceback, slice 26; `init` ignoring Init's answer, slice 47; `KB_ROOT` required, slice 22) are named in its log entry, not cut as refactors.
3. **The shop's types (slice 4).** `shop-artifact` declares `owner`, `status` and `tags`, none required, so every decision and work item the earlier scenarios record still fits. `tags` moves from `decision` to the base. A `step` artifact has a `does` text and the names of its `settings`, and declares the one shared shape, `binding` (`name`, `value`), in its `$defs`: a process's `with` refers to it as `kb:schema/step#/$defs/binding`. A process's step item is either inline (`does`) or a reuse (`uses`, a link to a step, with `with` bindings), exactly one of the two (`oneOf`). A step item's `branches` are `{when, go_to}`, where `go_to` is the name kb gave another step of the same process: a plain string kb does not check, since a process cannot link into its own parts before kb has named it. A role's two named groups are `harness` (`name`, `description`, `tools`, `model`) and `shop` (`responsible_for`, `answers_to`). A feature has a `story` and a `scenarios` part collection of `{title, pins}`. The types are created in the order each needs the ones before it: `shop-artifact`, `tag`, `decision`, `work-item`, `feature`, `role`, `step`, `process`. Probed in scratch: a step item with neither or both of `does` and `uses`, a binding without its value, and a `uses` naming no step are each refused, naming the place.
4. **A batch file (slice 15).** One YAML 1.2 mapping, `changes:`, a list in the order the changes are made. Each change is `create: <kind>` or `write: <name>`, with its `content`; a create's title is the content's `title`, as on `shop-knol create`. The set's one actor and one message come from `KB_ACTOR` and `-m`, as for every other mutating command. `apply` prints the set's name and each change's name and version. Only create and write, the two the scenario makes, are read; append and delete wait for a scenario. The file is read by the same helper as `create`'s (`_document`), which replaces `create`'s own reading rather than sitting beside it.
5. **The day in a scenario (slice 16).** kb stamps its history from `kb.journal.now()`, a module function kb documents as settable from outside, and the contract carries no clock. shop-knol runs as a process of its own, so the steps put `tests/clock/` on that process's `PYTHONPATH` with `TEST_NOW` set, and Python's `sitecustomize` hook there points `kb.journal.now` at that moment, a second later at each stamp. Nothing in `src/` knows about it and kb is untouched. The review's Background needs an agent acting for a named piece of work, so `KB_ACTOR`'s `role:execution` form (a spec line) is read here; slice 28's scenario that pins it may then pass on its steps alone.
6. **What `journal` shows.** `changes:`, oldest first, each with `at`, `actor` (`role`, `execution`), `op`, `artifact`, `revision` and `message`.
7. **What a renderer reads (slice 17's unknown).** kb v0.2.0's whole read with a depth fills in links in an artifact's own fields, but "a link inside one of its items stays a name" (`kb/read.py`), and stubs come only with a summary read. So the resolved whole read is not enough to write a reused step out in full. The `skill` renderer reads the process whole, then each step it reuses whole, all through the contract. No kb change is needed, so no request to bump the pin. Renderers give back `{path: text}` and faults; they write nothing. `shop-knol render` writes the files under `--to` only when the renderer refused nothing.
8. **The skill's shape.** `<dir>/<name>/SKILL.md`, where `<name>` is the process's name without its kind (the harness keeps each skill in a directory of its name). The heading block is `name` (that name) and `description` (the process's title), written as YAML 1.2. The body is `# <title>`, then `## <n>. <step title>` for each step. An inline step's `does` follows. A reused step says `This is the shared step <title>, where <setting> is <value>.` and then its `does` in full. Each branch is `- If <when>, go to step <n> (<title>).`
9. **The limits the harness publishes (slice 18's unknown).** Anthropic's Agent Skills documentation (platform.claude.com, Agent Skills overview and Skill authoring best practices, read 2026-09-26) publishes: `name` at most 64 characters, only lowercase letters, numbers and hyphens, no XML tags, not "anthropic" or "claude"; `description` non-empty, at most 1024 characters, no XML tags; and "Keep SKILL.md body under 500 lines". Only the last is one a process's steps can run past, and it is the one the scenario asserts, so it is the one checked: a body of 500 lines or more is refused with rule `harness-limit` at `steps`. The name and description limits have no scenario and are Review Focus 3. The best-practices page gives 500 lines "for optimal performance"; the spec's "fail rather than emit" treats it as a limit, which Task 6's checkpoint notes as a question for the spec.

## Review Focus

writing-plans asks that each line here get a test in the owning task. In this project tests are scenarios, and the feature files are the human gate, so no unit tests are added. Instead each line goes into the owning task's checkpoint entry as a `QUESTION FOR THE SPEC`, with the reproduction given here. Each was reproduced in scratch after all six tasks.

1. **A batch file of the wrong shape** (`changes:` holding `- delete: tag/x`, or a file with no `changes:`): `KeyError: 'content'` and `KeyError: 'changes'` tracebacks, against "shop-knol never shows a traceback". A person would expect the file refused in plain words naming the place. Task 3 logs it.
2. **Publishing something that is not a process as a skill** (`shop-knol render skill tag/pricing --to out`): a SKILL.md with a heading and no steps is written and the command succeeds. A person would expect a refusal saying a skill is published from a process. Task 5 logs it.
3. **A skill whose heading breaks the published limits** (a process titled "Ask Claude first"): `ask-claude-first/SKILL.md` is written though "claude" is a reserved word in a skill's name; a title over 1024 characters would pass the same way. Task 6 logs it.
4. **`render --to` a path that is a file, and `journal` with `KB_ROOT` unset**: `NotADirectoryError` and `KeyError: 'KB_ROOT'` tracebacks. Slice 22 owns finding the knowledge base; the first has no slice. Task 5 logs the first, Task 4 the second.
5. **A branch that goes to no step** (`go_to: nowhere`): kb stores it, and the skill says "go to nowhere." A person would expect the process refused when recorded, or the renderer to refuse. The schema language cannot say it (decision 3), so it is client-side or nowhere. Task 5 logs it.

---

### Task 1: Slice 1.29, the first architecture review

**Slice plan entry:** Slice 1.29, enabling. Check: this repository's `CLAUDE.md` states the module map, the rules and the size limits its code keeps; an Opus review of the code and the step definitions against it, after slices 0, 1, 1.17, 1.24, 1.27 and 1.28, is in the slice plan's log, and every refactor it calls for is a slice of its own right after this one with a check.

**Files:**
- Create: `CLAUDE.md`
- Modify: `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md` (status, log entry, any refactor slices)

**Interfaces:**
- Consumes: nothing.
- Produces: `CLAUDE.md`, whose module map Tasks 3, 4, 5 and 6 each extend by one row.

- [ ] **Step 1: The check fails before the slice**

```bash
cd /home/vscode/shopsystem-knowledge && ls CLAUDE.md; grep -c "architecture review of shop-knowledge" docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md
```

Expected: `ls: cannot access 'CLAUDE.md': No such file or directory`, then `0`.

- [ ] **Step 2: Write `CLAUDE.md`**

Create `/home/vscode/shopsystem-knowledge/CLAUDE.md`:

````markdown
# shop-knowledge: how this code is shaped

Read before changing anything under `src/shop_knowledge/` or `tests/`. These are rules, not preferences; a change
that breaks one is refactored into place first, then made.

shop-knowledge is a client of kb. It owns the shop's types, the seed content, the renderers and the `shop-knol`
command line; kb owns storage, checking and history. kb is pinned in `pyproject.toml` and installed from its tag.

## Module map

| module | owns | never holds |
|---|---|---|
| `cli.py` | `shop-knol`: its arguments, one handler per command making the kb calls that command maps to, the actor and the client from the environment, and printing: answers as YAML on stdout, refusals as plain words on stderr | the shop's types, rendering, reading a batch |
| `bootstrap.py` | loading the shop's types through Create when a knowledge base starts | the types themselves |
| `types/*.yaml` | the shop's types, one file each, as schema artifacts in kb's schema language | code |
| `__main__.py` | `python -m shop_knowledge` | anything else |

A new concern gets a new module and a row here. Nothing is added "beside" existing code in a module that does not
own it.

## Rules that make whole classes of defect unreachable

1. **kb only through its contract.** Code under `src/` calls kb through `kb.client.connect` with
   `kb.contract.kb_pb2` messages. From the rest of kb it imports only `kb.content`, content as YAML 1.2 text, and
   `kb.canonical`, for `NotCanonical` alone, the exception `kb.content` raises. It never reads or writes a file inside a
   knowledge base and never runs git.
2. **kb is pinned, never edited here.** A change shop-knowledge needs from kb is logged in the slice plan as a
   request to bump the pin, and the slice that needs it waits for the release.
3. **YAML 1.2, the way kb reads it.** Every file a user gives and everything printed goes through `kb.content`.
   No other YAML library is imported.
4. **One way to refuse.** Every refusal, kb's or shop-knol's own, is a `Fault` printed by the one printer in
   `cli.py`, one line each, with exit 1. shop-knol never shows a traceback.
5. **Types are data.** The shop's types reach kb only as schema artifacts created at `init`. No code outside a
   renderer for that type, and the step definitions, knows a type's fields.
6. **Renderers only read.** A renderer reads through the contract and gives back the files to write, or faults.
   It writes nothing; the command writes the files, and only when the renderer refused nothing.

## Size and shape

- No module over 250 lines. When a change would cross the limit, split first.
- A function does one thing at one level of abstraction; if it needs a comment to separate its phases, it is two
  functions.
- A file a user gives is read in one place, and a kb answer's faults are refused in one way.

## Step definitions

- Step definitions drive shop-knol the way a user does, a subprocess per command, through `tests/driver.py`.
- They may use kb's in-process client, or read and hand-edit a knowledge base's files, only to set up or observe
  what no shop-knol command yet does; the step says so where it does.
- Fixtures and steps shared by more than one feature live in `tests/conftest.py`; the rest sit beside the scenarios
  they serve.

## Working here

- `make dev` once; `make test` runs the suite in this checkout's `.venv`. While scenarios are red its last line is
  make's own error; pytest's summary line above it is the answer.
- Behaviour comes from `features/`; code is written red-green against a scenario, one at a time, and never adds
  behaviour no scenario asks for.
- A refactor is an enabling slice: its check is the suite giving the same answer and the structural target met.

````

- [ ] **Step 3: Commit it**

```bash
cd /home/vscode/shopsystem-knowledge && git add CLAUDE.md && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -q -m "CLAUDE.md: how shop-knowledge's code is shaped

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>" && git log --oneline -1
```

- [ ] **Step 4: Run the review**

Dispatch one subagent with `model: opus`, in the foreground, with this prompt verbatim:

```text
You are reviewing the shape of the code in /home/vscode/shopsystem-knowledge against that repository's CLAUDE.md. Read CLAUDE.md first, then every file under src/shop_knowledge/ and tests/. Do not edit anything. kb is a pinned dependency installed in .venv; do not review kb.

Answer in four parts:
1. For each rule and each size-and-shape line in CLAUDE.md: kept or broken, with file:line evidence for every break.
2. For each module map row: does the module own what the row says and hold nothing the row says it never holds? file:line for every mismatch.
3. The refactors the breaks call for. Each one is a separate item with: a one-line name in the form "<what> <is/lives> <where>", the rule or row it restores, the files it touches, and a measurable check: `.venv/bin/python -m pytest -q` still gives "55 failed, 7 passed" with the same failing test ids, plus a structural target a command can verify (a grep that prints nothing, a line count under a number, an import that succeeds). Propose no behaviour change: a refactor changes where code lives or how it is split, never what shop-knol prints or refuses.
4. Defects you notice that are not shape (a traceback, a silently ignored answer). List them with a reproduction; they are not refactors. Say which of these the slice plan (docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md) already assigns to a slice: slice 22 owns finding the knowledge base (KB_ROOT), slice 26 owns refusing a change by nobody (KB_ACTOR unset), slice 47 owns init's refusals.

If nothing is broken, say so plainly in part 3: "No refactor is called for."
```

- [ ] **Step 5: Log the review and cut what it calls for**

Append to the very end of the slice plan's `## Log` (verify with `tail -3`) one entry, in the form below, filled from the review's answer (every placeholder is the real content, never this template's words):

```markdown
- 2026-09-26 First architecture review of shop-knowledge (slice 1.29), by an Opus subagent against `CLAUDE.md` (commit <hash from Step 3>), after slices 0, 1, 1.17, 1.24, 1.27 and 1.28. Kept: <rules and rows kept>. Broken: <each break, file:line>. Refactors: <"none" or each as "slice 1.<n>: <name>">. Defects that are not shape: <each with its reproduction and the slice that owns it, or "QUESTION FOR THE SPEC" if none does>.
```

For each refactor, invoke `shopsystem-bdd:slicing-into-increments` to cut it as an enabling slice numbered 1.30, 1.31, … placed right after slice 1.29 and before slice 4, with the review's check as its Check line, `Unknown: none`, `Status: planned`. Then set slice 1.29's `- Status: planned` to `- Status: green`.

- [ ] **Step 6: Commit, and take the gate**

```bash
cd /home/vscode/shopsystem-knowledge && git add docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -q -m "Slice 1.29: first architecture review

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>" && grep -c "architecture review of shop-knowledge" docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md
```

Expected: `1`. **Gate:** if Step 5 cut any refactor slice, stop here. Append `- 2026-09-26 Batch 1 stops after slice 1.29: the review cut slices 1.30 to 1.<n>. Next: writing-plans over those refactors, then Tasks 2 to 6 of 2026-09-26-shop-knowledge-batch1-implementation.md re-planned over the new shape.` to the log, commit, and report back. Otherwise go on to Task 2.

---

### Task 2: Slice 4, the shop's seven types

**Slice plan entry:** Slice 4, capability. Unknown: can the process type, whose steps are each either written in place or a reuse of a shared step with bindings, and which carry branches, be said in kb's schema language? Scenario:

1. start-a-shop-knowledge-base / The user starts a knowledge base and the shop's types are ready

**Files:**
- Create: `src/shop_knowledge/types/shop-artifact.yaml`, `feature.yaml`, `role.yaml`, `step.yaml`, `process.yaml`
- Modify: `src/shop_knowledge/types/tag.yaml`, `decision.yaml`, `work-item.yaml`
- Modify: `src/shop_knowledge/bootstrap.py:7`
- Modify: `tests/test_start_a_shop_knowledge_base.py`
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `driver.knol(env, *args)`, `driver.record(env, tmp_path, type_name, content, message) -> id`; fixtures `env`, `shop`, `tmp_path` (`conftest.py`).
- Produces: the types `shop-artifact`, `tag`, `decision`, `work-item`, `feature`, `role`, `step`, `process`, in the shapes of decision 3, which Tasks 3 to 6 record into. The steps `Given an empty directory for the shop's knowledge` and `When the user starts a shop knowledge base in that directory, saying who they are` (gives `started`), which slice 47 reuses.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-4 2>&1 | grep -E "StepDefinitionNotFound|passed|failed" | head -3
```

Expected: `1 failed`, with `StepDefinitionNotFoundError` for `Given "an empty directory for the shop's knowledge"`.

- [ ] **Step 2: The steps**

Replace the whole of `tests/test_start_a_shop_knowledge_base.py` with:

```python
from pytest_bdd import given, scenarios, then, when

from driver import knol, record

scenarios("start-a-shop-knowledge-base.feature")

THE_SHOPS_TYPES = {"shop-artifact", "decision", "feature", "work-item", "role", "process", "step", "tag"}


@given("an empty directory for the shop's knowledge")
def _an_empty_directory(shop):
    assert not any(shop.iterdir())


@when("the user starts a shop knowledge base in that directory, saying who they are", target_fixture="started")
def _start_saying_who(env, shop):
    return knol(env, "init", str(shop))


@then("the shop can hold decisions, features, work items, roles, processes, steps and tags")
def _holds_the_seven(env, tmp_path, started):
    assert started.returncode == 0, started.stderr
    record(env, tmp_path, "tag", {"title": "Pricing", "description": "How the shop sets its prices.\n"}, "Tag pricing")
    record(env, tmp_path, "decision", {
        "title": "Price reviews happen weekly",
        "tags": ["tag/pricing"],
        "sections": [
            {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
            {"title": "Rationale", "body": "Costs move weekly.\n"},
        ],
    }, "Record weekly reviews")
    record(env, tmp_path, "work-item", {
        "title": "Reprice the dairy shelf", "decisions": ["decision/price-reviews-happen-weekly"],
    }, "Open the repricing")
    record(env, tmp_path, "feature", {
        "title": "Restock the shelves",
        "story": "So that nothing runs out, the shopkeeper restocks the shelves.\n",
        "scenarios": [{"title": "A short shelf is restocked", "pins": "A shelf below its level is filled.\n"}],
    }, "Describe restocking")
    record(env, tmp_path, "role", {
        "title": "Stock keeper",
        "harness": {"name": "stock-keeper", "description": "Keeps the shelves stocked.", "tools": ["Read"]},
        "shop": {"responsible_for": "What is on the shelves", "answers_to": "role/shopkeeper"},
        "sections": [{"title": "How it works", "body": "Counts, then orders.\n"}],
    }, "Describe the stock keeper")
    record(env, tmp_path, "step", {
        "title": "Check the stock", "does": "Count what is on the shelf.\n", "settings": ["shelf"],
    }, "Share the stock check")
    record(env, tmp_path, "process", {
        "title": "Restock a shelf",
        "steps": [
            {"title": "Check it", "uses": "step/check-the-stock", "with": [{"name": "shelf", "value": "dairy"}]},
            {
                "title": "Decide",
                "does": "Decide whether the shelf is short.\n",
                "branches": [{"when": "the shelf is short", "go_to": "order-more"}, {"when": "it is not", "go_to": "stop"}],
            },
            {"title": "Order more", "does": "Order enough to fill the shelf.\n"},
            {"title": "Stop", "does": "Leave the shelf as it is.\n"},
        ],
    }, "Describe restocking a shelf")


@then("the user defines nothing of their own before recording the first one")
def _defines_nothing(shop):
    held = {path.stem for path in (shop / "kb" / "schema").glob("*.yaml")}
    assert held == THE_SHOPS_TYPES | {"schema"}
```

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-4 2>&1 | grep -E "^E  |passed|failed" | head -3
```

Expected: `E       AssertionError: : a kind must name a type the store holds; the store holds no type called 'feature'` and `1 failed`. The tag, decision and work item record; the feature is the first kind the store holds no type for.

- [ ] **Step 3: The types**

Create `src/shop_knowledge/types/shop-artifact.yaml`:

```yaml
title: Shop artifact
version: 1
schema:
  type: object
  properties:
    owner:
      type: string
    status:
      type: string
    tags:
      type: array
      items:
        type: string
      ref:
        targets: [tag]
        cardinality: many
        parts: false
        on_delete: refuse
  summary: [tags]
```

In `src/shop_knowledge/types/tag.yaml`, `decision.yaml` and `work-item.yaml`, insert these two lines right after the line `schema:`:

```yaml
  allOf:
    - $ref: kb:schema/shop-artifact
```

In `tag.yaml`, delete the last line, `  summary: []`. In `decision.yaml`, delete the `tags:` property (the nine lines from `    tags:` to its `        on_delete: refuse`), and change the last line `  summary: [supersedes, tags]` to `  summary: [supersedes]`. The three files then read:

```yaml
title: Tag
version: 1
schema:
  allOf:
    - $ref: kb:schema/shop-artifact
  type: object
  properties:
    title:
      type: string
    description:
      type: string
  required: [title, description]
```

```yaml
title: Decision
version: 1
schema:
  allOf:
    - $ref: kb:schema/shop-artifact
  type: object
  properties:
    title:
      type: string
    supersedes:
      type: string
      ref:
        targets: [decision]
        cardinality: one
        parts: false
        on_delete: refuse
  required: [title]
  sections:
    - title: Purpose
    - title: Rationale
  summary: [supersedes]
```

```yaml
title: Work item
version: 1
schema:
  allOf:
    - $ref: kb:schema/shop-artifact
  type: object
  properties:
    title:
      type: string
    decisions:
      type: array
      items:
        type: string
      ref:
        targets: [decision]
        cardinality: many
        parts: false
        on_delete: refuse
  required: [title]
  summary: [decisions]
```

Create `src/shop_knowledge/types/feature.yaml`:

```yaml
title: Feature
version: 1
schema:
  allOf:
    - $ref: kb:schema/shop-artifact
  type: object
  properties:
    title:
      type: string
    story:
      type: string
  required: [title, story]
  parts:
    scenarios:
      items:
        type: object
        properties:
          title:
            type: string
          pins:
            type: string
        required: [title, pins]
```

Create `src/shop_knowledge/types/role.yaml`:

```yaml
title: Role
version: 1
schema:
  allOf:
    - $ref: kb:schema/shop-artifact
  type: object
  properties:
    title:
      type: string
    harness:
      type: object
      properties:
        name:
          type: string
        description:
          type: string
        tools:
          type: array
          items:
            type: string
        model:
          type: string
      required: [name, description]
      additionalProperties: false
    shop:
      type: object
      properties:
        responsible_for:
          type: string
        answers_to:
          type: string
      required: [responsible_for]
      additionalProperties: false
  required: [title, harness, shop]
```

Create `src/shop_knowledge/types/step.yaml`:

```yaml
title: Step
version: 1
schema:
  allOf:
    - $ref: kb:schema/shop-artifact
  type: object
  properties:
    title:
      type: string
    does:
      type: string
    settings:
      type: array
      items:
        type: string
  required: [title, does]
  $defs:
    binding:
      type: object
      properties:
        name:
          type: string
        value:
          type: string
      required: [name, value]
      additionalProperties: false
```

Create `src/shop_knowledge/types/process.yaml`:

```yaml
title: Process
version: 1
schema:
  allOf:
    - $ref: kb:schema/shop-artifact
  type: object
  properties:
    title:
      type: string
  required: [title]
  parts:
    steps:
      items:
        type: object
        properties:
          title:
            type: string
          does:
            type: string
          uses:
            type: string
            ref:
              targets: [step]
              cardinality: one
              parts: false
              on_delete: refuse
          with:
            type: array
            items:
              $ref: kb:schema/step#/$defs/binding
          branches:
            type: array
            items:
              type: object
              properties:
                when:
                  type: string
                go_to:
                  type: string
              required: [when, go_to]
              additionalProperties: false
        required: [title]
        oneOf:
          - required: [does]
          - required: [uses]
```

In `src/shop_knowledge/bootstrap.py`, replace the line `TYPES = ("tag", "decision", "work-item")` with:

```python
TYPES = ("shop-artifact", "tag", "decision", "work-item", "feature", "role", "step", "process")
```

Each type is created after every type it refers to by `$ref`.

- [ ] **Step 4: Run it green, and the suite**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-4 2>&1 | tail -1 && .venv/bin/python -m pytest -q -m "slice-1 or slice-1.17 or slice-1.24 or slice-1.27 or slice-1.28" 2>&1 | tail -1 && make test 2>&1 | grep -E "^[0-9]+ failed"
```

Expected: `1 passed, 61 deselected`, then `7 passed, 55 deselected`, then `54 failed, 8 passed`.

- [ ] **Step 5: Probe what the process type refuses**

```bash
rm -rf /tmp/probe4 && mkdir /tmp/probe4 && cd /tmp/probe4 && export KB_ACTOR=shopkeeper KB_ROOT=/tmp/probe4 && PY=/home/vscode/shopsystem-knowledge/.venv/bin/python && $PY -m shop_knowledge init /tmp/probe4 && printf 'title: Check the stock\ndoes: Count.\n' > s.yaml && $PY -m shop_knowledge create step --from s.yaml -m s >/dev/null && printf 'title: P\nsteps:\n  - title: Neither\n  - title: Both\n    does: x\n    uses: step/check-the-stock\n  - title: Gone\n    uses: step/nothing\n  - title: Bad with\n    uses: step/check-the-stock\n    with:\n      - name: shelf\n' > p.yaml && $PY -m shop_knowledge create process --from p.yaml -m p; echo "exit $?"
```

Expected, the four refusals and `exit 1`:

```text
process/p at steps/0: {'title': 'Neither'} is not valid under any of the given schemas
process/p at steps/1: {'title': 'Both', 'does': 'x', 'uses': 'step/check-the-stock'} is valid under each of {'required': ['uses']}, {'required': ['does']}
process/p at steps/3/with/0: 'value' is a required property
process/p at steps/2/uses: a link must land on a node of a kind the type allows; 'step/nothing' does not
exit 1
```

This is the evidence for the checkpoint's assumption line.

- [ ] **Step 6: Checkpoint and commit**

Set slice 4's `- Status: planned` to `- Status: green`, and append to the very end of the log (verify with `tail -3`):

```markdown
- 2026-09-26 slice 4 green. A user can now: start a knowledge base that holds decisions, features, work items, roles, processes, steps and tags on one base, defining nothing first.
  Assumption "the process type, steps inline or reused with bindings and carrying branches, can be said in kb's schema language": <held or failed>. Evidence: <Step 5's output, complete>.
  Surprised by: <anything, or "nothing">.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 5): a branch's go_to names a step of the same process as a plain string kb does not check; `go_to: nowhere` is stored. Refuse it client-side, or leave it?
  Next: slice 15.
```

```bash
cd /home/vscode/shopsystem-knowledge && git add src/shop_knowledge tests docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -q -m "Slice 4: the shop's seven types on one base

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>" && git status --short
```

Expected: nothing printed by `git status --short`.

---

### Task 3: Slice 15, make several changes at once from the command line

**Slice plan entry:** Slice 15, capability. Unknown: what shape does a batch take in a file, given each change carries its own content and the set carries one actor and one message? Scenario:

1. make-several-changes-at-once / The user makes several changes at once

**Files:**
- Create: `src/shop_knowledge/batch.py`
- Modify: `src/shop_knowledge/cli.py`
- Modify: `tests/test_make_several_changes_at_once.py`
- Modify: `CLAUDE.md` (module map row), the slice plan (checkpoint)

**Interfaces:**
- Consumes: the `work-item` and `decision` types (Task 2); `driver.knol`, `driver.record`, `driver.start(env, shop)`.
- Produces: `shop_knowledge.batch.operations(document: dict) -> list[kb_pb2.Operation]`; `shop-knol apply --from FILE -m MESSAGE`, printing `batch:` and `results:` (`id`, `revision`); `cli._document(source: str) -> tuple[dict, list[kb_pb2.Fault]]`, used by `create` and `apply`. The Background step and `When the user applies the batch, saying who they are and why` (gives `applied`), which slice 48 reuses. Task 4 uses `apply` to make a revision.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-15 2>&1 | grep -E "StepDefinitionNotFound|passed|failed" | head -3
```

Expected: `1 failed`, with `StepDefinitionNotFoundError` for `Given "a shop knowledge base holding the shop's types and a work item"`.

- [ ] **Step 2: The steps**

Replace the whole of `tests/test_make_several_changes_at_once.py` with:

```python
from kb import client as kb_client
from kb.content import dumps, loads
from kb.contract import kb_pb2
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("make-several-changes-at-once.feature")

WORK_ITEM = "work-item/reprice-the-dairy-shelf"
WEEKLY = "decision/price-reviews-happen-weekly"
SECTIONS = [
    {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
    {"title": "Rationale", "body": "Costs move weekly.\n"},
]


@given("a shop knowledge base holding the shop's types and a work item")
def _shop_with_a_work_item(env, shop, tmp_path):
    start(env, shop)
    record(env, tmp_path, "work-item", {"title": "Reprice the dairy shelf"}, "Open the repricing")


@given("a batch that records a decision and points the work item at it", target_fixture="batch_file")
def _a_batch_recording_and_pointing(tmp_path):
    path = tmp_path / "batch.yaml"
    path.write_text(dumps({"changes": [
        {"create": "decision", "content": {"title": "Price reviews happen weekly", "sections": SECTIONS}},
        {"write": WORK_ITEM, "content": {"decisions": [WEEKLY]}},
    ]}))
    return path


@when("the user applies the batch, saying who they are and why", target_fixture="applied")
def _apply(env, batch_file):
    return knol(env, "apply", "--from", str(batch_file), "-m", "Review prices weekly, starting with dairy")


@then("both changes are in the shop")
def _both_in_the_shop(env, applied):
    assert applied.returncode == 0, applied.stderr
    assert [result["id"] for result in loads(applied.stdout)["results"]] == [WEEKLY, WORK_ITEM]
    decision = knol(env, "read", WEEKLY)
    assert decision.returncode == 0, decision.stderr
    work_item = loads(knol(env, "read", WORK_ITEM).stdout)
    assert [(stub["field"], stub["id"]) for stub in work_item["references"]] == [("decisions", WEEKLY)]


@then("the shop's history shows them as one change")
def _one_change(shop, applied):
    batch = loads(applied.stdout)["batch"]
    history = kb_client.connect(shop).Journal(kb_pb2.JournalRequest(batch=batch))
    assert [(entry.op, entry.artifact) for entry in history.entries] == [("create", WEEKLY), ("write", WORK_ITEM)]
    assert {entry.message for entry in history.entries} == {"Review prices weekly, starting with dairy"}
```

The history is read through kb's in-process client because no shop-knol command shows it until Task 4; `CLAUDE.md` allows that for what no command yet shows.

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-15 2>&1 | grep -E "^E  |passed|failed" | head -3
```

Expected: `E       AssertionError: usage: shop-knol [-h] {init,create,read,validate} ...`, then `shop-knol: error: argument command: invalid choice: 'apply' …`, and `1 failed`.

- [ ] **Step 3: The batch file and the command**

Create `src/shop_knowledge/batch.py`:

```python
"""A batch file: several changes that land as one set. Each change is a create of a kind or a write to a name, with
its own content; the set as a whole carries one actor and one message, given on the command line like any other."""
from kb.content import dumps, text
from kb.contract import kb_pb2


def operations(document: dict) -> list[kb_pb2.Operation]:
    """The batch's changes, in the order written, as the operations of one Apply."""
    return [_operation(change) for change in document["changes"]]


def _operation(change: dict) -> kb_pb2.Operation:
    content = dict(change["content"])
    if "create" in change:
        title = text(content.pop("title", None))
        return kb_pb2.Operation(create=kb_pb2.Creation(type=change["create"], title=title, content=dumps(content)))
    return kb_pb2.Operation(write=kb_pb2.Replacement(locator=kb_pb2.Locator(id=change["write"]), content=dumps(content)))
```

In `src/shop_knowledge/cli.py`:

Replace `from shop_knowledge import bootstrap` with `from shop_knowledge import batch, bootstrap`.

After the line `    commands.add_parser("validate", help="check everything the shop knows; lists every fault, exits non-zero if any")`, insert:

```python

    apply = commands.add_parser("apply", help="make every change in a batch file as one change; prints the set's name")
    apply.add_argument("--from", dest="source", required=True, metavar="FILE")
    apply.add_argument("-m", dest="message", required=True, help="why")
```

Replace the line `    return {"init": _init, "create": _create, "read": _read, "validate": _validate}[args.command](args)` with:

```python
    handlers = {
        "init": _init, "create": _create, "read": _read, "validate": _validate,
        "apply": _apply,
    }
    return handlers[args.command](args)
```

Replace the head of `_create`, from `def _create(args) -> int:` through its `return _refuse([kb_pb2.Fault(artifact=args.source, …)])` line, with the helper and a new head, so the file is read in one place:

```python
def _document(source: str) -> tuple[dict, list[kb_pb2.Fault]]:
    """A file the user gave, read the way kb reads content; or, if it cannot be read so, the fault saying where."""
    try:
        return loads(Path(source).read_text()), []
    except canonical.NotCanonical as fault:
        return {}, [kb_pb2.Fault(artifact=source, path=fault.path, rule="content", message=str(fault))]


def _create(args) -> int:
    content, faults = _document(args.source)
    if faults:
        return _refuse(faults)
```

(The rest of `_create`, from `    title = text(content.pop("title", None))`, is unchanged.) Append at the end of the file:

```python


def _apply(args) -> int:
    document, faults = _document(args.source)
    if faults:
        return _refuse(faults)
    response = _client().Apply(kb_pb2.ApplyRequest(
        operations=batch.operations(document), actor=_actor(), message=args.message,
    ))
    if response.faults:
        return _refuse(response.faults)
    _show({
        "batch": response.batch,
        "results": [{"id": result.id, "revision": result.revision} for result in response.results],
    })
    return 0
```

In `CLAUDE.md`'s module map, add this row after `cli.py`'s:

```markdown
| `batch.py` | a batch file read into the operations of one Apply, in the order written | reading files, kb calls |
```

- [ ] **Step 4: Run it green, and the suite**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m "slice-15 or slice-1.24" 2>&1 | tail -1 && make test 2>&1 | grep -E "^[0-9]+ failed"
```

Expected: `2 passed, 60 deselected` (slice 1.24's refusal of a file naming an entry twice still goes through the one reader), then `53 failed, 9 passed`.

- [ ] **Step 5: Checkpoint and commit**

Set slice 15's status to green and append to the very end of the log (verify with `tail -3`):

```markdown
- 2026-09-26 slice 15 green. A user can now: apply a batch file that records a decision and points a work item at it, as one change in the history under one role and one message.
  Assumption "a batch is a file of changes, each with its own content, and the set's actor and message come from the command line like any other change": <held or failed>. Evidence: <the `apply` output from a run of the scenario's batch, and the Journal entries under its batch name>.
  Surprised by: <anything, or "nothing">.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 1): a batch file of the wrong shape (`changes:` holding `- delete: tag/x`, or no `changes:`) gives `KeyError: 'content'` / `KeyError: 'changes'` tracebacks. What is it told?
  Next: slice 16.
```

```bash
cd /home/vscode/shopsystem-knowledge && git add CLAUDE.md src/shop_knowledge tests docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -q -m "Slice 15: make several changes at once from a batch file

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>" && git status --short
```

---

### Task 4: Slice 16, review the changes to one thing

**Slice plan entry:** Slice 16, capability. Unknown: how does the command line let step definitions set the day, so a change made two days ago and one made today appear as such? Scenario:

1. review-who-changed-what / The user reviews the changes to one thing

**Files:**
- Create: `tests/clock/sitecustomize.py`
- Modify: `tests/driver.py`, `tests/test_review_who_changed_what.py`
- Modify: `src/shop_knowledge/cli.py`
- Modify: `CLAUDE.md` (tests section), the slice plan (checkpoint)

**Interfaces:**
- Consumes: `shop-knol apply` (Task 3), the `decision` type (Task 2).
- Produces: `driver.at(env, moment: str) -> dict`, the environment in which shop-knol's history is stamped from `moment` (ISO, UTC); `shop-knol journal [--artifact NAME]`, printing `changes:` as in decision 6; `cli._actor()` reading `role:execution`. The Background steps `Given today is {day}` (gives `today`) and the recorded-then-revised Given, and the constants `WEEKLY` and `PIECE_OF_WORK`, which slice 36 reuses.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-16 2>&1 | grep -E "StepDefinitionNotFound|passed|failed" | head -3
```

Expected: `1 failed`, with `StepDefinitionNotFoundError` for `Given "today is 2026-09-23"`.

- [ ] **Step 2: The clock and the steps**

Create `tests/clock/sitecustomize.py`:

```python
"""Loaded by every Python process started with this directory on PYTHONPATH, as the steps start shop-knol when a
scenario says what day it is. With TEST_NOW set, kb stamps its history from that moment, a second later at each
stamp, instead of from the machine's clock. kb's journal clock is a module function for this purpose."""
import os

if os.environ.get("TEST_NOW"):
    from datetime import datetime, timedelta, timezone

    import kb.journal

    _moments = iter(
        datetime.fromisoformat(os.environ["TEST_NOW"]).replace(tzinfo=timezone.utc) + timedelta(seconds=tick)
        for tick in range(10_000)
    )
    kb.journal.now = lambda: next(_moments)
```

In `tests/driver.py`, replace the lines `import subprocess` and `import sys` with:

```python
import os
import subprocess
import sys
from pathlib import Path
```

and append at the end of the file:

```python


CLOCK = Path(__file__).parent / "clock"


def at(env, moment):
    """The environment shop-knol runs in when the history is to say it ran at `moment` (ISO, UTC)."""
    path = os.pathsep.join(filter(None, [str(CLOCK), env.get("PYTHONPATH")]))
    return {**env, "PYTHONPATH": path, "TEST_NOW": moment}
```

Replace the whole of `tests/test_review_who_changed_what.py` with:

```python
from kb.content import dumps, loads
from pytest_bdd import given, parsers, scenarios, then, when

from driver import at, knol, record

scenarios("review-who-changed-what.feature")

WEEKLY = "decision/price-reviews-happen-weekly"
PIECE_OF_WORK = "reprice-dairy"
SECTIONS = [
    {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
    {"title": "Rationale", "body": "Costs move weekly.\n"},
]


@given(parsers.parse("today is {day}"), target_fixture="today")
def _today(day):
    return day


@given(
    "a shop knowledge base where the shopkeeper recorded a decision on 2026-09-21 and an agent revised it today "
    "as part of a named piece of work"
)
def _recorded_then_revised(env, shop, tmp_path, today):
    started = knol(at(env, "2026-09-21T09:00:00"), "init", str(shop))
    assert started.returncode == 0, started.stderr
    record(at(env, "2026-09-21T10:00:00"), tmp_path, "decision",
           {"title": "Price reviews happen weekly", "sections": SECTIONS}, "Record weekly reviews")
    revision = tmp_path / "revision.yaml"
    revision.write_text(dumps({"changes": [{"write": WEEKLY, "content": {
        "status": "accepted", "sections": SECTIONS,
    }}]}))
    agent = {**at(env, f"{today}T10:00:00"), "KB_ACTOR": f"agent:{PIECE_OF_WORK}"}
    revised = knol(agent, "apply", "--from", str(revision), "-m", "Accept weekly reviews")
    assert revised.returncode == 0, revised.stderr


@when("the user reviews the changes to that decision", target_fixture="reviewed")
def _review_the_decision(env):
    return knol(env, "journal", "--artifact", WEEKLY)


@then("the user sees both changes, each with who made it, when, what it did and why")
def _both_changes(reviewed, today):
    assert reviewed.returncode == 0, reviewed.stderr
    assert [
        (change["actor"], change["at"][:10], change["op"], change["message"])
        for change in loads(reviewed.stdout)["changes"]
    ] == [
        ({"role": "shopkeeper", "execution": ""}, "2026-09-21", "create", "Record weekly reviews"),
        ({"role": "agent", "execution": PIECE_OF_WORK}, today, "write", "Accept weekly reviews"),
    ]
```

Each command is given its own moment, so no two processes stamp the same second and no two history entries share a name.

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-16 2>&1 | grep -E "^E  |passed|failed" | head -3
```

Expected: `E       AssertionError: usage: shop-knol [-h] {init,create,read,validate,apply} ...`, then `shop-knol: error: argument command: invalid choice: 'journal' …`, and `1 failed`. The Background already runs: kb takes `agent:reprice-dairy` as a role until Step 3 splits it.

- [ ] **Step 3: The command, and the piece of work in `KB_ACTOR`**

In `src/shop_knowledge/cli.py`:

Before the line `    apply = commands.add_parser("apply", …)`, insert:

```python
    journal = commands.add_parser("journal", help="review who changed what: every change, oldest first")
    journal.add_argument("--artifact", default="", help="only the changes to this one")

```

In `handlers`, replace `        "apply": _apply,` with `        "apply": _apply, "journal": _journal,`.

Replace `_actor`:

```python
def _actor() -> kb_pb2.Actor:
    """KB_ACTOR is the role, or the role and the piece of work it acts for as role:execution."""
    role, _, execution = os.environ["KB_ACTOR"].partition(":")
    return kb_pb2.Actor(role=role, execution=execution)
```

Append at the end of the file:

```python


def _journal(args) -> int:
    response = _client().Journal(kb_pb2.JournalRequest(artifact=args.artifact))
    if response.faults:
        return _refuse(response.faults)
    _show({"changes": [
        {
            "at": entry.at,
            "actor": {"role": entry.actor.role, "execution": entry.actor.execution},
            "op": entry.op,
            "artifact": entry.artifact,
            "revision": entry.revision,
            "message": entry.message,
        }
        for entry in response.entries
    ]})
    return 0
```

In `CLAUDE.md`'s "Step definitions" section, add this line at its end:

```markdown
- `tests/clock/` is put on shop-knol's `PYTHONPATH`, with `TEST_NOW` set, only through `driver.at`, when a scenario
  says what day it is. Nothing under `src/` knows the day is set.
```

- [ ] **Step 4: Run it green, and the suite**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m "slice-16 or slice-15" 2>&1 | tail -1 && make test 2>&1 | grep -E "^[0-9]+ failed"
```

Expected: `2 passed, 60 deselected`, then `52 failed, 10 passed`.

- [ ] **Step 5: Checkpoint and commit**

Set slice 16's status to green and append to the very end of the log (verify with `tail -3`):

```markdown
- 2026-09-26 slice 16 green. A user can now: review every change to one decision, oldest first, each with who made it and for which piece of work, when, what it did and why.
  Assumption "step definitions can set the day kb stamps without kb taking a clock on its contract": <held or failed>. Evidence: <the `journal --artifact` output of the scenario's store, showing 2026-09-21 and 2026-09-23>.
  Surprised by: <anything, or "nothing">.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 4): `shop-knol journal` with `KB_ROOT` unset gives `KeyError: 'KB_ROOT'`; slice 22 owns finding the knowledge base.
  Next: slice 17.
```

```bash
cd /home/vscode/shopsystem-knowledge && git add CLAUDE.md src/shop_knowledge tests docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -q -m "Slice 16: review the changes to one thing

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>" && git status --short
```

---

### Task 5: Slice 17, publish a process as a skill

**Slice plan entry:** Slice 17, capability. Unknown: is a resolved whole read, with the stubs of its references and its type, enough for a renderer to write a reused step out in full? Scenario:

1. publish-what-the-shop-knows / The user publishes a process as a skill

**Files:**
- Create: `src/shop_knowledge/renderers/__init__.py`, `src/shop_knowledge/renderers/skill.py`
- Modify: `src/shop_knowledge/cli.py`
- Modify: `tests/test_publish_what_the_shop_knows.py`
- Modify: `CLAUDE.md` (module map row), the slice plan (checkpoint)

**Interfaces:**
- Consumes: the `process`, `step` and `role` types (Task 2).
- Produces: `shop_knowledge.renderers.RENDERERS: dict[str, Callable[[client, str], tuple[dict[str, str], list[kb_pb2.Fault]]]]`; `renderers.skill.render(client, name)` and `renderers.skill.body(title, steps, shared) -> str`; `shop-knol render <renderer> <name> --to DIR`, printing `written:`. The Background (gives `process_name`), `When the user publishes the process as a skill into a directory` (gives `published`: `result`, `target`, `before`), which Task 6 and slices 19, 20 and 50 reuse.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-17 2>&1 | grep -E "StepDefinitionNotFound|passed|failed" | head -3
```

Expected: `1 failed`, with `StepDefinitionNotFoundError` for the Background's Given.

- [ ] **Step 2: The steps**

Replace the whole of `tests/test_publish_what_the_shop_knows.py` with:

```python
import re

from kb.content import loads
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("publish-what-the-shop-knows.feature")

RESTOCK = "process/restock-a-shelf"
CHECK_THE_STOCK = {"title": "Check the stock", "does": "Count what is on the shelf, front and back.\n", "settings": ["shelf"]}
ROLE = {
    "title": "Stock keeper",
    "harness": {"name": "stock-keeper", "description": "Keeps the shelves stocked.", "tools": ["Read"]},
    "shop": {"responsible_for": "What is on the shelves"},
    "sections": [{"title": "How it works", "body": "Counts, then orders.\n"}],
}


@given(
    "a shop knowledge base holding a process whose steps include a branch and a reused shared step, and a role",
    target_fixture="process_name",
)
def _shop_with_a_process_and_a_role(env, shop, tmp_path):
    start(env, shop)
    record(env, tmp_path, "step", CHECK_THE_STOCK, "Share the stock check")
    record(env, tmp_path, "role", ROLE, "Describe the stock keeper")
    return record(env, tmp_path, "process", {
        "title": "Restock a shelf",
        "steps": [
            {"title": "Check it", "uses": "step/check-the-stock", "with": [{"name": "shelf", "value": "dairy"}]},
            {
                "title": "Decide",
                "does": "Decide whether the shelf is short.\n",
                "branches": [{"when": "the shelf is short", "go_to": "order-more"}, {"when": "it is not", "go_to": "stop"}],
            },
            {"title": "Order more", "does": "Order enough to fill the shelf.\n"},
            {"title": "Stop", "does": "Leave the shelf as it is.\n"},
        ],
    }, "Describe restocking a shelf")


def _everything_under(directory):
    return {path.relative_to(directory): path.read_bytes() for path in sorted(directory.rglob("*")) if path.is_file()}


@when("the user publishes the process as a skill into a directory", target_fixture="published")
def _publish_as_a_skill(env, shop, tmp_path, process_name):
    target = tmp_path / "published"
    target.mkdir()
    before = _everything_under(shop / "kb")
    result = knol(env, "render", "skill", process_name, "--to", str(target))
    return {"result": result, "target": target, "before": before}


def _heading_block_and_body(text):
    match = re.fullmatch(r"---\n(.*?)---\n\n(.*)", text, re.DOTALL)
    assert match, text
    return loads(match.group(1)), match.group(2)


@then(
    "that directory holds a skill whose heading block is the process's identity and whose body is its steps, "
    "with the reused step written out in full"
)
def _a_skill(published):
    result = published["result"]
    assert result.returncode == 0, result.stderr
    heading, body = _heading_block_and_body((published["target"] / "restock-a-shelf" / "SKILL.md").read_text())
    assert heading == {"name": "restock-a-shelf", "description": "Restock a shelf"}
    assert body.splitlines() == [
        "# Restock a shelf", "",
        "## 1. Check it", "",
        "This is the shared step Check the stock, where shelf is dairy.", "",
        "Count what is on the shelf, front and back.", "",
        "## 2. Decide", "",
        "Decide whether the shelf is short.", "",
        "- If the shelf is short, go to step 3 (Order more).",
        "- If it is not, go to step 4 (Stop).", "",
        "## 3. Order more", "",
        "Order enough to fill the shelf.", "",
        "## 4. Stop", "",
        "Leave the shelf as it is.",
    ]


@then("the shop's knowledge base is unchanged")
def _unchanged(shop, published):
    assert _everything_under(shop / "kb") == published["before"]
```

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-17 2>&1 | grep -E "^E  |passed|failed" | head -3
```

Expected: `E       AssertionError: usage: shop-knol [-h] {init,create,read,validate,journal,apply} ...`, then `invalid choice: 'render'`, and `1 failed`.

- [ ] **Step 3: The renderer and the command**

Create `src/shop_knowledge/renderers/__init__.py`:

```python
"""Renderers: client code that reads an artifact through the contract and gives back the files to publish, by path
under the directory asked for. A renderer writes nothing and changes nothing; the command line writes what it gives."""
from shop_knowledge.renderers import skill

RENDERERS = {"skill": skill.render}
```

Create `src/shop_knowledge/renderers/skill.py`:

```python
"""The skill renderer: a process as SKILL.md in the harness's heading-block-plus-body shape. The heading block is the
process's identity; the body is its steps in order, each reused step written out in full with its own settings, and
each branch saying which step it goes to."""
from kb.content import dumps, loads
from kb.contract import kb_pb2


def render(client, name: str) -> tuple[dict[str, str], list[kb_pb2.Fault]]:
    """The skill's files by path, or the faults of the reads that could not be made."""
    process = _whole(client, name)
    if process.faults:
        return {}, list(process.faults)
    steps = loads(process.content).get("steps", [])
    shared = {}
    for used in dict.fromkeys(step["uses"] for step in steps if "uses" in step):
        response = _whole(client, used)
        if response.faults:
            return {}, list(response.faults)
        shared[used] = response
    slug = process.id.split("/", 1)[1]
    heading = dumps({"name": slug, "description": process.title})
    return {f"{slug}/SKILL.md": f"---\n{heading}---\n\n{body(process.title, steps, shared)}"}, []


def body(title: str, steps: list[dict], shared: dict) -> str:
    """The process as instructions: a heading, then each step under a numbered heading of its own."""
    numbers = {step["id"]: number for number, step in enumerate(steps, 1)}
    titles = {step["id"]: step["title"] for step in steps}
    lines = [f"# {title}", ""]
    for step in steps:
        lines += [f"## {numbers[step['id']]}. {step['title']}", ""]
        if "uses" in step:
            lines += _reused(step, shared[step["uses"]])
        else:
            lines += [step["does"].rstrip(), ""]
        branches = step.get("branches", [])
        lines += [f"- If {branch['when']}, go to {_step(branch['go_to'], numbers, titles)}." for branch in branches]
        lines += [""] if branches else []
    return "\n".join(lines)


def _step(name: str, numbers: dict, titles: dict) -> str:
    """Where a branch goes: the step by its number and title, or the name as written if no step of the process has it."""
    return f"step {numbers[name]} ({titles[name]})" if name in numbers else name


def _reused(step: dict, used: kb_pb2.ReadResponse) -> list[str]:
    """A shared step written out in full where it is used, with the settings this use gives it."""
    settings = ", ".join(f"{binding['name']} is {binding['value']}" for binding in step.get("with", []))
    said = f"This is the shared step {used.title}" + (f", where {settings}." if settings else ".")
    return [said, "", loads(used.content)["does"].rstrip(), ""]


def _whole(client, name: str) -> kb_pb2.ReadResponse:
    return client.Read(kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=name), level=kb_pb2.ReadRequest.WHOLE))
```

In `src/shop_knowledge/cli.py`:

After `from shop_knowledge import batch, bootstrap`, add the line `from shop_knowledge.renderers import RENDERERS`.

Before the line `    apply = commands.add_parser("apply", …)`, insert:

```python
    render = commands.add_parser("render", help="publish an artifact into a directory; the shop is only read")
    render.add_argument("renderer", choices=sorted(RENDERERS))
    render.add_argument("locator")
    render.add_argument("--to", required=True, metavar="DIR")

```

In `handlers`, replace `        "apply": _apply, "journal": _journal,` with `        "apply": _apply, "journal": _journal, "render": _render,`.

Append at the end of the file:

```python


def _render(args) -> int:
    files, faults = RENDERERS[args.renderer](_client(), args.locator)
    if faults:
        return _refuse(faults)
    for relative, content in files.items():
        path = Path(args.to) / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    _show({"written": sorted(files)})
    return 0
```

In `CLAUDE.md`'s module map, add this row after `batch.py`'s:

```markdown
| `renderers/` | one module per renderer, each reading an artifact through the contract and giving back `{path: text}` or faults; `RENDERERS` names them for `shop-knol render` | writing files, kb writes |
```

- [ ] **Step 4: Run it green, and the suite**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-17 2>&1 | tail -1 && make test 2>&1 | grep -E "^[0-9]+ failed"
```

Expected: `1 passed, 61 deselected`, then `51 failed, 11 passed`.

- [ ] **Step 5: Checkpoint and commit**

Set slice 17's status to green and append to the very end of the log (verify with `tail -3`):

```markdown
- 2026-09-26 slice 17 green. A user can now: publish a process into a directory as a skill whose heading block is its identity and whose body is its steps, the reused step written out in full with its settings, leaving the shop's knowledge unchanged.
  Assumption "a resolved whole read, with the stubs of its references and its type, is enough for a renderer to write a reused step out in full": failed, and no kb change was needed. kb v0.2.0 fills in only links in an artifact's own fields ("a link inside one of its items stays a name", kb/read.py), and stubs come only with a summary read. The renderer reads the process whole, then each reused step whole. Evidence: <the SKILL.md the scenario publishes, complete>.
  Surprised by: <anything, or "nothing">.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 2): `shop-knol render skill tag/pricing` writes a SKILL.md with no steps and succeeds. Refuse anything that is not a process?
  - QUESTION FOR THE SPEC (Review Focus 4): `render --to` a path that is a file gives a `NotADirectoryError` traceback.
  - QUESTION FOR THE SPEC (Review Focus 5): a branch whose go_to names no step is published as "go to nowhere."
  - The spec says a renderer reads "the resolved whole artifact, the stubs of its references, and its schema"; the skill renderer needs a whole read of each step it reuses as well. If the spec should keep that sentence, the request is for kb to fill in links inside items on a resolved read, a bump of the pin.
  Next: slice 18.
```

```bash
cd /home/vscode/shopsystem-knowledge && git add CLAUDE.md src/shop_knowledge tests docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -q -m "Slice 17: publish a process as a skill

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>" && git status --short
```

---

### Task 6: Slice 18, a skill the harness would reject is not published

**Slice plan entry:** Slice 18, capability. Unknown: which limits does the harness publish for a skill, and can the renderer check its output against them before writing anything? Scenario:

1. publish-what-the-shop-knows / A skill the harness would reject is not published

**Files:**
- Create: `src/shop_knowledge/renderers/limits.py`
- Modify: `src/shop_knowledge/renderers/skill.py`
- Modify: `tests/test_publish_what_the_shop_knows.py`
- Modify: `CLAUDE.md` (module map row), the slice plan (checkpoint)

**Interfaces:**
- Consumes: the publish Background and When (Task 5), `renderers.skill.body`.
- Produces: `shop_knowledge.renderers.limits.skill(artifact: str, body: str) -> list[kb_pb2.Fault]`, rule `harness-limit`, which slice 50's agent renderer extends with the heading limits when a scenario asks for them.

- [ ] **Step 1: The steps, and run it red**

Append to `tests/test_publish_what_the_shop_knows.py`:

```python


@given("a process whose steps run past the limits the harness publishes", target_fixture="process_name")
def _a_process_past_the_limits(env, tmp_path):
    """Two hundred steps written out at four lines each is past the five hundred lines a skill's body may run to."""
    steps = [{"title": f"Count shelf {number}", "does": f"Count what is on shelf {number}.\n"} for number in range(1, 201)]
    return record(env, tmp_path, "process", {"title": "Count every shelf", "steps": steps}, "Describe the stocktake")


@then("the skill is rejected because it goes beyond the limits the harness publishes")
def _rejected_for_the_limits(published):
    assert published["result"].stderr.splitlines() == [
        "process/count-every-shelf at steps: a skill's body is under 500 lines, the limit the harness publishes; "
        "this one is 801",
    ]
    assert published["result"].returncode != 0


@then("nothing is written to the directory")
def _nothing_written(published):
    assert list(published["target"].iterdir()) == []
```

The Given's `target_fixture="process_name"` takes the place of the Background's process for this scenario.

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-18 2>&1 | grep -E "^E  |passed|failed" | head -3
```

Expected: `E       assert [] == ['process/cou...s one is 801']` and `1 failed`: the skill is written and nothing is said.

- [ ] **Step 2: The limit, checked before anything is written**

Create `src/shop_knowledge/renderers/limits.py`:

```python
"""The limits the harness publishes for what it loads, checked before anything is written. Anthropic's Agent Skills
documentation (platform.claude.com/docs/en/agents-and-tools/agent-skills, best practices) publishes that a SKILL.md
body is under 500 lines. It also publishes limits on a skill's name and description; no scenario asks for those yet."""
from kb.contract import kb_pb2

BODY_LINES = 500


def skill(artifact: str, body: str) -> list[kb_pb2.Fault]:
    """Every way a skill goes beyond what the harness accepts, each a fault on the artifact it was published from."""
    lines = len(body.splitlines())
    if lines < BODY_LINES:
        return []
    return [kb_pb2.Fault(
        artifact=artifact, path="steps", rule="harness-limit",
        message=f"a skill's body is under {BODY_LINES} lines, the limit the harness publishes; this one is {lines}",
    )]
```

In `src/shop_knowledge/renderers/skill.py`, after `from kb.contract import kb_pb2` add a blank line and `from shop_knowledge.renderers import limits`. Then replace the last three lines of `render`:

```python
    slug = process.id.split("/", 1)[1]
    heading = dumps({"name": slug, "description": process.title})
    return {f"{slug}/SKILL.md": f"---\n{heading}---\n\n{body(process.title, steps, shared)}"}, []
```

with:

```python
    slug = process.id.split("/", 1)[1]
    written = body(process.title, steps, shared)
    faults = limits.skill(process.id, written)
    if faults:
        return {}, faults
    heading = dumps({"name": slug, "description": process.title})
    return {f"{slug}/SKILL.md": f"---\n{heading}---\n\n{written}"}, []
```

In `CLAUDE.md`'s module map, add this row after `renderers/`'s:

```markdown
| `renderers/limits.py` | the limits the harness publishes, each checked against a renderer's output before anything is written, with where it was published | rendering, files |
```

- [ ] **Step 3: Run it green, and the suite**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m "slice-18 or slice-17" 2>&1 | tail -1 && make test 2>&1 | grep -E "^[0-9]+ failed"
```

Expected: `2 passed, 60 deselected`, then `50 failed, 12 passed`.

- [ ] **Step 4: Checkpoint and commit**

Set slice 18's status to green and append to the very end of the log (verify with `tail -3`):

```markdown
- 2026-09-26 slice 18 green. A user can now: publish a process whose steps run past the 500 lines the harness publishes for a skill's body, and be refused for that reason with nothing written.
  Assumption "the harness publishes limits a renderer can check before writing": held. Anthropic's Agent Skills documentation publishes name (64 characters; lowercase letters, numbers, hyphens; no XML tags; not "anthropic" or "claude"), description (non-empty, 1024 characters, no XML tags), and "Keep SKILL.md body under 500 lines". Evidence: <the scenario's stderr and the empty directory listing>.
  Surprised by: <anything, or "nothing">.
  Open questions:
  - QUESTION FOR THE SPEC: the 500 lines is published "for optimal performance", not as a rejection; the spec's "fail rather than emit" treats it as a limit.
  - QUESTION FOR THE SPEC (Review Focus 3): the name and description limits have no scenario, so a process titled "Ask Claude first" publishes `ask-claude-first/SKILL.md`.
  Next: slice 19.
```

```bash
cd /home/vscode/shopsystem-knowledge && git add CLAUDE.md src/shop_knowledge tests docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -q -m "Slice 18: a skill past the harness's limits is not published

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>" && git status --short
```

After Task 6: `make test` gives `50 failed, 12 passed`, every failure tagged 19 or later. Next in the slice plan is slice 19, then slice 19.1, the second architecture review.
