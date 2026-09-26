# shop-knowledge batch 2: slices 1.30, 1.31, 1.32, 4, 15, 16, 17 and 18

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, in slice order. Tasks 1 to 3 are enabling refactors, verified by their slice's Check line. Tasks 4 to 8 are capability slices: inside each, follow `shopsystem-bdd:bdd-red-green` scenario by scenario; its stop conditions, hand-back and checkpoint apply, and they override any step here that conflicts with them.

**Goal:** The three refactors the first architecture review cut bring shop-knowledge's code into the shape its `CLAUDE.md` sets: the steps every feature shares are defined once, reading the user's file is one function, and turning a read answer into what is shown is one function. Every refusal then reaches the one printer the one way. Over that shape, a new knowledge base arrives with all seven of the shop's types on one base. A user applies a batch of changes as one change, reviews the history of one thing with who, when, what and why, and publishes a process as a skill with its reused steps written out in full. A skill that runs past the limits the harness publishes is refused, and nothing is written.

**Architecture:** shop-knowledge (`/home/vscode/shopsystem-knowledge`) is the Python package `shop_knowledge`. Its `shop-knol` command (`cli.py`) calls kb through kb's in-process client (`kb.client.connect`) with the contract's messages (`kb.contract.kb_pb2`), and reads and prints YAML 1.2 through `kb.content`. The shop's types are YAML files under `src/shop_knowledge/types/`, created as schema artifacts by `bootstrap.py` when `shop-knol init` starts a knowledge base. This batch first reshapes `cli.py`:
- `main` parses, calls the command's handler, and catches `Refused`, the one exception every refusal travels as, printing it through the one printer, `_refuse` (Task 2);
- `_document(source)` reads a file the user gave, raising `Refused` where kb cannot read it (Task 2);
- `_answered(response)` gives back a kb answer or raises the refusal it carries, and every handler calls kb through it (Task 3);
- `_glance(response)` shapes a read answer into what is shown (Task 3).

Then it adds, each command a handler of a few lines over those three helpers:
- the five missing types and the base all seven build on (Task 4);
- `batch.py` and `shop-knol apply` (Task 5);
- `shop-knol journal --artifact`, and a test-only clock that sets the day kb stamps its history with (Task 6);
- `renderers/`, whose `skill` renderer gives back a `Rendered` (files, or faults) that `shop-knol render` refuses through `_answered` like any kb answer, and writes only when nothing was refused (Task 7);
- `renderers/limits.py`, which checks a skill against the harness's published limits before anything is written (Task 8).

kb is **not** a checkout here. It is `shopsystem-kb` v0.2.0, installed from its git tag into this checkout's `.venv` by `make dev`, and it is never edited from this repository.

**Provenance:** Every code block in this plan was assembled in a scratch clone of this repository (`/tmp/skb2/shop`) on 2026-09-26, run with this checkout's `.venv/bin/python` and `PYTHONPATH=/tmp/skb2/shop/src`. Each task was applied in order and run. The red and green results, the suite counts, the list of failing tests and the Review Focus reproductions below are what those runs gave. The plan was then replayed from its own text in a fresh clone (`/tmp/skb2-replay`, with `.venv` linked to this checkout's), in the foreground. Every check, red and suite count came out as stated, and every file under `src/` and `tests/`, and `CLAUDE.md`, came out byte-identical to the scratch run's. This checkout was not touched.

**Tech Stack:** Python 3.11, setuptools (src layout), kb v0.2.0 (protobuf contract, in-process client, JSON Schema Draft 2020-12 types with kb's `ref`, `parts`, `sections`, `summary` and `title` keywords, `allOf` composition and `kb:schema/<type>#/...` shared shapes), pytest 8 + pytest-bdd 8, argparse.

**Spec:** `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md` (The CLI, Bootstrap types, Renderers). `CLAUDE.md` in this repository, the rules the code is held to. kb's schema language is in `/home/vscode/shopsystem-kb/docs/superpowers/specs/2026-09-23-kb-design.md` (Artifact model, Schema language), read-only. Slice plan: `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, slices 1.30, 1.31, 1.32, 4, 15, 16, 17, 18. Feature files: `features/`. Each capability slice's scenarios carry `@slice-<n>`, so a slice is selected with `.venv/bin/python -m pytest -q -m slice-<n>`.

## Global Constraints

- Feature files are read-only. Only `slicing-into-increments` edits a tag line, and only `formulating-features` edits a Given, When or Then. Any other diff under `features/` is a stop condition.
- Code only what a scenario asserts (bdd-red-green). Where the scenarios are silent the code is silent, and the silence goes into the checkpoint entry as an open question. A refactor task changes where code lives and how it is split, never what shop-knol prints, refuses or exits with.
- kb is v0.2.0 from its tag, in `.venv`, and is never edited here. "shop-knowledge never touches kb's files or git. It calls the contract through the in-process client." A kb change a slice needs is not coded: it is logged in the slice plan as a request to bump the pin, and the slice stops.
- `CLAUDE.md`'s rules are implemented once, and every command uses that one implementation rather than a check of its own: a file the user gives is read only by `cli._document`; a kb answer is refused only by `cli._answered`; a refusal is printed only by `main`, through `_refuse`, from a `Refused`. From Task 3 on, a handler holds no `if response.faults`, no `try`, and no call to `_refuse`.
- "Every mutating command requires an actor and `-m`." "The actor comes from `KB_ACTOR` as `role` or `role:execution-id`."
- "Every file shop-knol reads or writes, on `create`, `write`, `append`, `apply`, and in its own output, is YAML 1.2, read and written the way kb reads content." "Output is YAML by default."
- "shop-knol never shows a traceback." "Errors are printed as returned by kb, with artifact, path, and message, and exit non-zero."
- Bootstrap types: "Schema artifacts for: `decision`, `feature`, `work-item`, `role`, `process`, `step`, `tag`. Plus whatever data-type schemas the process and feature schemas share through `$ref`." "All seven build on a `shop-artifact` base schema through kb's composition mechanism, so the fields every shop artifact carries, such as owner, status, and tags, are declared once." "`process` declares a `steps` part collection whose items either define a step inline or carry `uses: <ref to step>` and `with: <bindings>`." "`role` separates the harness contract fields from the corpus identity fields into two named field groups." "`tag` is a title and description; a `tags` reference field on other types targets it."
- Renderers: "Client code, invoked only by `shop-knol render`. Each reads the resolved whole artifact, the stubs of its references, and its schema through the contract, and writes files to the target directory." "`skill` for `process`: `SKILL.md` in Anthropic's frontmatter-plus-body shape with resolved steps as the body." "`skill` and `agent` validate their output against the limits the harness publishes and fail rather than emit something it would reject."
- `shop-knol apply --from <batch>` maps to Apply; `shop-knol journal [--artifact] [--actor] [--execution] [--since]` maps to Journal; `shop-knol render <renderer> <id> --to <dir>` is client-side rendering. This batch adds only the options its scenarios use: `journal --artifact`; `--actor`, `--execution` and `--since` are slice 36's.
- Work on `main` in this checkout. `make test` runs the suite in `.venv`; while scenarios are red its last line is make's own `Error 1`, so read pytest's summary line above it.
- Commits: `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`, the message ending with the Co-Authored-By line of the model that made the commit, e.g. `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
- pytest-bdd prints `PytestRemovedIn10Warning`s, two for each `target_fixture` step. That is the baseline, not a fault.
- Baseline before Task 1: `55 failed, 7 passed`. After each task, pytest's summary is: Tasks 1, 2 and 3 `55 failed, 7 passed`, with the same 55 failing test ids; Task 4 `54 failed, 8 passed`; Task 5 `53 failed, 9 passed`; Task 6 `52 failed, 10 passed`; Task 7 `51 failed, 11 passed`; Task 8 `50 failed, 12 passed`. The slices already green (`-m "slice-1 or slice-1.17 or slice-1.24 or slice-1.27 or slice-1.28"` → `7 passed`) stay green after every task.
- **The shape check**, run at the end of Task 3 and of every task after it, is the one command that says the rules above still hold:

  ```bash
  cd /home/vscode/shopsystem-knowledge && grep -c "_refuse(" src/shop_knowledge/cli.py; grep -c "if response.faults:" src/shop_knowledge/cli.py; grep -c read_text src/shop_knowledge/cli.py; find src -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'
  ```

  Expected: `2` (the printer's definition and `main`'s one call), `1` (`_answered`), `1` (`_document`), and nothing more: no module over 250 lines.

## What changed from batch 1

Batch 1 (`2026-09-26-shop-knowledge-batch1-implementation.md`) planned slices 4, 15, 16, 17 and 18 as its Tasks 2 to 6 over the code as it stood before the first review. Its Task 1, slice 1.29, ran, and the review cut slices 1.30 to 1.32, so those five tasks never ran. They are re-planned here as Tasks 4 to 8, over the shape Tasks 1 to 3 leave. Every behaviour they give a user is the same, and every decision and probe of batch 1 still holds (listed below). What changed is where code sits and how the steps are named:

1. **One refusal path instead of an `if` per handler.** Batch 1's `_apply`, `_journal` and `_render` each checked `faults` and called `_refuse`, and its `_document` gave back a `(content, faults)` pair that `create` and `apply` each checked. Here `_document` raises `Refused`, every kb call goes through `_answered`, and `main` alone prints. A renderer gives back a `Rendered` (`files`, `faults`), so `_render` refuses it through the same `_answered` as a kb answer.
2. **`_document` is slice 1.31's, not slice 15's.** Batch 1's Task 3 introduced it; here Task 2 does, and Task 5 only calls it.
3. **Handlers are named on their parsers.** `main`'s dict of handlers, which each of batch 1's tasks edited, is gone: each subparser carries `set_defaults(handler=...)`, so a task adds a command in one place.
4. **Every When that runs shop-knol gives `result`.** Batch 1 named them `started`, `applied`, `reviewed` and `published` (a dict of result, target and before). Slice 1.30 defines the shared Thens once in `tests/conftest.py` over `result`, so every When here gives `result`, as slice 47's refusal scenario, which reuses slice 4's When, will need. The publish steps' directory and before-snapshot become the fixtures `target` and `before`, and the When asks for `before` so it is taken before the command runs.
5. **Shaping sits apart from calling.** `_journal`'s entry shaping is `_change(entry)`, as `_read`'s is `_glance`; `_render`'s writing is `_write(files, directory)`; the skill renderer's heading and limit check are `_skill(process, written)`.
6. **The history entry's message is `kb_pb2.Entry`.** Batch 1 left `_journal` untyped. The prototype's first try annotated it `kb_pb2.JournalEntry`, which does not exist in kb v0.2.0; the message is `Entry`.
7. **Unused `RESTOCK` constant dropped** from the publish steps, and the comprehension in slice 15's Then no longer reuses the name `result`.

Nothing else moved: the type files, `batch.py`, the clock, `renderers/skill.py`'s body and branch wording, `renderers/limits.py`, and every step's assertion are batch 1's, byte for byte where this plan shows the same text. No request to bump the pin.

## Decisions this plan makes (the spec left them open or silent)

1. **One exception carries every refusal (Tasks 2 and 3).** `CLAUDE.md` rule 4 says every refusal is printed by the one printer. The review found that true only by each handler calling it. Here refusing is raising `cli.Refused(faults)`, and `main` is the only caller of `_refuse`. Only `Refused` is caught: any other exception still raises as before, since which tracebacks become refusals is behaviour that slices 22, 26 and 47 own (the review's defect list).
2. **Validate's answer stays whole.** kb's `ValidateResponse` carries `faults` and `violations`, and slice 1.28 prints both, faults first. `_validate` raises `Refused` over both rather than going through `_answered`, which would drop the violations when both are present.
3. **Init's answer is still ignored.** The review found `_init` drops Init's faults and `bootstrap.load` drops every Create answer. Refusing them changes what `init` exits with, which is slice 47's, so no task here routes them through `_answered`.
4. **The shop's types (slice 4), from batch 1.** `shop-artifact` declares `owner`, `status` and `tags`, none required, so every decision and work item the earlier scenarios record still fits. `tags` moves from `decision` to the base. A `step` artifact has a `does` text and the names of its `settings`, and declares the one shared shape, `binding` (`name`, `value`), in its `$defs`: a process's `with` refers to it as `kb:schema/step#/$defs/binding`. A process's step item is either inline (`does`) or a reuse (`uses`, a link to a step, with `with` bindings), exactly one of the two (`oneOf`). A step item's `branches` are `{when, go_to}`, where `go_to` is the name kb gave another step of the same process: a plain string kb does not check, since a process cannot link into its own parts before kb has named it. A role's two named groups are `harness` (`name`, `description`, `tools`, `model`) and `shop` (`responsible_for`, `answers_to`). A feature has a `story` and a `scenarios` part collection of `{title, pins}`. The types are created in the order each needs the ones before it: `shop-artifact`, `tag`, `decision`, `work-item`, `feature`, `role`, `step`, `process`. Probed again in scratch over the new shape: a step item with neither or both of `does` and `uses`, a binding without its value, and a `uses` naming no step are each refused, naming the place (Task 4, Step 5).
5. **A batch file (slice 15), from batch 1.** One YAML 1.2 mapping, `changes:`, a list in the order the changes are made. Each change is `create: <kind>` or `write: <name>`, with its `content`; a create's title is the content's `title`, as on `shop-knol create`. The set's one actor and one message come from `KB_ACTOR` and `-m`, as for every other mutating command. `apply` prints the set's name and each change's name and version. Only create and write, the two the scenario makes, are read; append and delete wait for a scenario. The file is read by `_document`, as `create`'s is.
6. **The day in a scenario (slice 16), from batch 1.** kb stamps its history from `kb.journal.now()`, a module function kb documents as settable from outside, and the contract carries no clock. shop-knol runs as a process of its own, so the steps put `tests/clock/` on that process's `PYTHONPATH` with `TEST_NOW` set, and Python's `sitecustomize` hook there points `kb.journal.now` at that moment, a second later at each stamp. Nothing in `src/` knows about it and kb is untouched. The review's Background needs an agent acting for a named piece of work, so `KB_ACTOR`'s `role:execution` form (a spec line) is read here; slice 28's scenario that pins it may then pass on its steps alone.
7. **What `journal` shows, from batch 1.** `changes:`, oldest first, each with `at`, `actor` (`role`, `execution`), `op`, `artifact`, `revision` and `message`.
8. **What a renderer reads (slice 17's unknown), from batch 1.** kb v0.2.0's whole read with a depth fills in links in an artifact's own fields, but "a link inside one of its items stays a name" (`kb/read.py`), and stubs come only with a summary read. So the resolved whole read is not enough to write a reused step out in full. The `skill` renderer reads the process whole, then each step it reuses whole, all through the contract. No kb change is needed, so no request to bump the pin. Renderers give back a `Rendered` and write nothing. `shop-knol render` writes the files under `--to` only when the renderer refused nothing.
9. **The skill's shape, from batch 1.** `<dir>/<name>/SKILL.md`, where `<name>` is the process's name without its kind (the harness keeps each skill in a directory of its name). The heading block is `name` (that name) and `description` (the process's title), written as YAML 1.2. The body is `# <title>`, then `## <n>. <step title>` for each step. An inline step's `does` follows. A reused step says `This is the shared step <title>, where <setting> is <value>.` and then its `does` in full. Each branch is `- If <when>, go to step <n> (<title>).`
10. **The limits the harness publishes (slice 18's unknown), from batch 1.** Anthropic's Agent Skills documentation (platform.claude.com, Agent Skills overview and Skill authoring best practices, read 2026-09-26) publishes: `name` at most 64 characters, only lowercase letters, numbers and hyphens, no XML tags, not "anthropic" or "claude"; `description` non-empty, at most 1024 characters, no XML tags; and "Keep SKILL.md body under 500 lines". Only the last is one a process's steps can run past, and it is the one the scenario asserts, so it is the one checked: a body of 500 lines or more is refused with rule `harness-limit` at `steps`. The name and description limits have no scenario and are Review Focus 3. The best-practices page gives 500 lines "for optimal performance"; the spec's "fail rather than emit" treats it as a limit, which Task 8's checkpoint notes as a question for the spec.

## Review Focus

writing-plans asks that each line here get a test in the owning task. In this project tests are scenarios, and the feature files are the human gate, so no unit tests are added. Instead each line goes into the owning task's checkpoint entry as a `QUESTION FOR THE SPEC`, with the reproduction given here. Batch 1 found these five; each was reproduced again in scratch after all eight tasks here, over the new shape, with the output shown.

1. **A batch file of the wrong shape** (`changes:` holding `- delete: tag/pricing`, or a file with no `changes:`): `KeyError: 'content'` and `KeyError: 'changes'` tracebacks, against "shop-knol never shows a traceback". A person would expect the file refused in plain words naming the place. `Refused` would carry it, but which faults to raise is behaviour no scenario pins. Task 5 logs it.
2. **Publishing something that is not a process as a skill** (`shop-knol render skill tag/pricing --to out`): `pricing/SKILL.md` with a heading and no steps is written and the command exits 0. A person would expect a refusal saying a skill is published from a process. Task 7 logs it.
3. **A skill whose heading breaks the published limits** (a process titled "Ask Claude first"): `ask-claude-first/SKILL.md` is written and the command exits 0, though "claude" is a reserved word in a skill's name; a title over 1024 characters would pass the same way. Task 8 logs it.
4. **`render --to` a path that is a file, and `journal` with `KB_ROOT` unset**: `NotADirectoryError: [Errno 20] Not a directory: 'afile/ask-claude-first'` and `KeyError: 'KB_ROOT'` tracebacks. Slice 22 owns finding the knowledge base; the first has no slice. Task 7 logs the first, Task 6 the second.
5. **A branch that goes to no step** (`go_to: nowhere`): kb stores it, and the skill says `- If always, go to nowhere.` A person would expect the process refused when recorded, or the renderer to refuse. The schema language cannot say it (decision 4), so it is client-side or nowhere. Task 4 logs it for the type, Task 7 for the renderer.

---

### Task 1: Slice 1.30, the steps every feature shares are defined once

**Slice plan entry:** Slice 1.30, enabling. Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same 55 failing scenarios as before the slice (55 failed, 7 passed), and `grep -rnE "never a traceback|reports failure to whatever ran it" tests/*.py | grep -v conftest.py` prints nothing.

**Files:**
- Modify: `tests/conftest.py`, `tests/driver.py`
- Modify: `tests/test_check_the_shops_knowledge_is_sound.py`, `tests/test_read_back_what_the_shop_knows.py`, `tests/test_record_a_decision.py`
- Modify: `CLAUDE.md` (Step definitions), the slice plan (status, checkpoint)

**Interfaces:**
- Consumes: nothing new.
- Produces: in `tests/conftest.py`, `Then the user is shown that fault in plain words, never a traceback` and `Then the command reports failure to whatever ran it`, both reading the fixture `result`, the `subprocess.CompletedProcess` of the shop-knol command a When ran. Every When in Tasks 4 to 8 that runs shop-knol gives `result`. `driver.refused_plainly` and `driver.reported_failure` are removed; their assertions now live in those two steps.

- [ ] **Step 1: Record the failing tests, and see the check fail**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -rf 2>&1 | grep ^FAILED | sort > /tmp/failed-before.txt; wc -l < /tmp/failed-before.txt; grep -rnE "never a traceback|reports failure to whatever ran it" tests/*.py | grep -v conftest.py
```

Expected: `55`, then six lines, two in each of `test_check_the_shops_knowledge_is_sound.py`, `test_read_back_what_the_shop_knows.py` and `test_record_a_decision.py`. `/tmp/failed-before.txt` is compared against after each of Tasks 1 to 3.

- [ ] **Step 2: The shared steps, once**

Replace the whole of `tests/conftest.py` with:

```python
"""Suite wiring, and the fixtures and steps more than one feature shares. The rest live beside their scenarios."""
import os
import re
from pathlib import Path

import pytest
from pytest_bdd import given, then

from driver import start


def pytest_configure(config):
    """Register every @slice-<n> tag in the feature files as a marker, so -m slice-<n> selects a slice."""
    tags = set()
    for feature in Path(config.rootpath, "features").glob("*.feature"):
        tags.update(re.findall(r"@(slice-\d+(?:\.\d+)?)", feature.read_text()))
    for tag in sorted(tags):
        config.addinivalue_line("markers", f"{tag}: scenario of that slice in the plan")


@pytest.fixture
def shop(tmp_path):
    """The directory the shop's knowledge base is started in, there before it starts; the store is its kb/ subdirectory."""
    shop = tmp_path / "shop"
    shop.mkdir()
    return shop


@pytest.fixture
def env(shop):
    return {**os.environ, "KB_ROOT": str(shop), "KB_ACTOR": "shopkeeper"}


@given("a shop knowledge base holding the shop's types")
def _shop_knowledge_base(env, shop):
    start(env, shop)


@then("the user is shown that fault in plain words, never a traceback")
def _shown_in_plain_words(result):
    """Something said on stderr, no traceback anywhere, nothing on stdout."""
    assert result.stderr.strip(), "nothing was said"
    assert "Traceback" not in result.stderr + result.stdout, result.stderr
    assert result.stdout == ""


@then("the command reports failure to whatever ran it")
def _reports_failure(result):
    assert result.returncode != 0, result.stdout
```

Replace the whole of `tests/driver.py` with (the two assertion helpers are gone; their bodies are the steps above):

```python
"""Drive shop-knol the way a user does: a subprocess per command, YAML in files and on stdout."""
import subprocess
import sys

from kb.content import dumps, loads


def knol(env, *args):
    return subprocess.run(
        [sys.executable, "-m", "shop_knowledge", *args],
        env=env, capture_output=True, text=True,
    )


def start(env, shop):
    result = knol(env, "init", str(shop))
    assert result.returncode == 0, result.stderr


def record(env, tmp_path, type_name, content, message):
    """Write content to a file, record it, and return the id the user is shown."""
    path = tmp_path / f"{content['title']}.yaml"
    path.write_text(dumps(content))
    result = knol(env, "create", type_name, "--from", str(path), "-m", message)
    assert result.returncode == 0, result.stderr
    return loads(result.stdout)["id"]
```

- [ ] **Step 3: Each feature's When gives `result`, and its own copies of the shared steps go**

Replace the whole of `tests/test_check_the_shops_knowledge_is_sound.py` with (the When's `checked` is now `result`):

```python
from kb import canonical
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("check-the-shops-knowledge-is-sound.feature")

WEEKLY = "decision/price-reviews-happen-weekly"
MONTHLY = "decision/prices-are-reviewed-monthly"
SECTIONS = [
    {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
    {"title": "Rationale", "body": "Costs move weekly.\n"},
]


@given(
    "a shop knowledge base where someone edited a decision's file by hand and left it in a shape the shop cannot read"
)
def _shop_with_a_file_mangled_by_hand(env, shop, tmp_path):
    """Two decisions edited by hand: one left unreadable, one left readable but without the body of its purpose."""
    start(env, shop)
    record(env, tmp_path, "decision", {"title": "Price reviews happen weekly", "sections": SECTIONS}, "Record weekly")
    record(env, tmp_path, "decision", {"title": "Prices are reviewed monthly", "sections": SECTIONS}, "Record monthly")
    (shop / "kb" / f"{WEEKLY}.yaml").write_text("title: [a bracket opened by hand and never closed\n")
    monthly = shop / "kb" / f"{MONTHLY}.yaml"
    held = canonical.load(monthly.read_text())
    del held["sections"][0]["body"]
    monthly.write_text(canonical.dump(held))


@when("the user checks the shop's knowledge", target_fixture="result")
def _check(env):
    return knol(env, "validate")


@then("that file is listed as a fault, naming the file")
def _unreadable_listed(result):
    assert result.stderr.splitlines()[0].startswith(f"{WEEKLY}: the stored file {WEEKLY}.yaml cannot be read: ")


@then("everything else the shop knows is checked and listed alongside it")
def _the_rest_listed(result):
    assert result.stderr.splitlines()[1:] == [f"{MONTHLY} at sections/0: 'body' is a required property"]
```

Replace the whole of `tests/test_read_back_what_the_shop_knows.py` with (its When already gave `result`):

```python
import pytest
from kb.content import loads
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("read-back-what-the-shop-knows.feature")

OLDER = "decision/prices-are-reviewed-monthly"
DECISION = "decision/price-reviews-happen-weekly"


@given(
    'a shop knowledge base holding a decision with a purpose and a rationale, tagged "pricing", '
    "superseding an older decision, and pointed at by two work items",
    target_fixture="decision_id",
)
def _shop_with_a_linked_decision(env, shop, tmp_path):
    start(env, shop)
    record(env, tmp_path, "tag", {"title": "pricing", "description": "How the shop sets prices.\n"}, "Add the pricing tag")
    record(env, tmp_path, "decision", {
        "title": "Prices are reviewed monthly",
        "sections": [
            {"title": "Purpose", "body": "Keep prices current.\n"},
            {"title": "Rationale", "body": "Monthly was enough once.\n"},
        ],
    }, "Record the monthly review")
    decision_id = record(env, tmp_path, "decision", {
        "title": "Price reviews happen weekly",
        "supersedes": OLDER,
        "tags": ["tag/pricing"],
        "sections": [
            {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
            {"title": "Rationale", "body": "Costs move weekly.\n"},
        ],
    }, "Move price reviews to weekly")
    record(env, tmp_path, "work-item", {"title": "Move the review to Mondays", "decisions": [DECISION]}, "Plan the move")
    record(env, tmp_path, "work-item", {"title": "Tell the pricing team", "decisions": [DECISION]}, "Plan the telling")
    return decision_id


@when("the user reads the decision", target_fixture="result")
def _read_the_decision(env, decision_id):
    return knol(env, "read", decision_id)


@pytest.fixture
def shown(result):
    """What the user is shown, for the steps that expect the read to succeed."""
    assert result.returncode == 0, result.stderr
    return loads(result.stdout)


@then("the user sees its name, its title and the few fields the shop shows for a decision")
def _name_title_and_fields(shown):
    assert shown["id"] == DECISION
    assert shown["title"] == "Price reviews happen weekly"
    assert shown["supersedes"] == OLDER
    assert shown["tags"] == ["tag/pricing"]


@then("the user sees a stub of each thing it points at")
def _stubs(shown):
    stubs = {(stub["field"], stub["id"], stub["type"], stub["title"]) for stub in shown["references"]}
    assert stubs == {
        ("supersedes", OLDER, "decision", "Prices are reviewed monthly"),
        ("tags", "tag/pricing", "tag", "pricing"),
    }


@then("the user sees how many things point back at it, and of what kind")
def _inbound(shown):
    assert shown["inbound"] == [{"type": "work-item", "field": "decisions", "count": 2}]


@given("someone edited the decision's file by hand and left it in a shape the shop cannot read")
def _decision_file_mangled_by_hand(shop):
    (shop / "kb" / f"{DECISION}.yaml").write_text("title: [a bracket opened by hand and never closed\n")


@then("the command is rejected because that file cannot be read, naming the file")
def _rejected_as_unreadable(result):
    assert result.stderr.startswith(f"{DECISION}: the stored file {DECISION}.yaml cannot be read: ")
```

Replace the whole of `tests/test_record_a_decision.py` with (the When's `recorded` is now `result`; the two Thens that read the decision back call their own read `read`, so they do not hide `result`):

```python
from kb.content import dumps, loads
from pytest_bdd import given, parsers, scenarios, then, when

from driver import knol, record

scenarios("record-a-decision.feature")

OLDER = {
    "title": "Prices are reviewed monthly",
    "sections": [
        {"title": "Purpose", "body": "Keep prices current.\n"},
        {"title": "Rationale", "body": "Monthly was enough once.\n"},
    ],
}
WEEKLY = {
    "title": "Price reviews happen weekly",
    "supersedes": "decision/prices-are-reviewed-monthly",
    "sections": [
        {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
        {"title": "Rationale", "body": "Costs move weekly, so a monthly review lags them.\n"},
    ],
}


@given(
    "a decision in a file, with a title, a purpose, a rationale and the decision it supersedes",
    target_fixture="decision_file",
)
def _decision_in_a_file(env, tmp_path):
    record(env, tmp_path, "decision", OLDER, "Record the monthly review")
    path = tmp_path / "weekly.yaml"
    path.write_text(dumps(WEEKLY))
    return path


@when("the user records that file as a decision, saying who they are and why", target_fixture="result")
def _record_it(env, decision_file):
    return knol(env, "create", "decision", "--from", str(decision_file), "-m", "Move price reviews to weekly")


@then("the user is shown the name the decision was given, which the user did not choose")
def _shown_the_name(result, decision_file):
    assert result.returncode == 0, result.stderr
    assert loads(result.stdout)["id"] == "decision/price-reviews-happen-weekly"
    assert "id" not in loads(decision_file.read_text())


@then("the shop holds the decision under that name and reads it back by it", target_fixture="read_back")
def _reads_back_by_name(env, result):
    name = loads(result.stdout)["id"]
    read = knol(env, "read", name)
    assert read.returncode == 0, read.stderr
    shown = loads(read.stdout)
    assert shown["id"] == name
    assert shown["title"] == "Price reviews happen weekly"
    return shown


@then("the decision is at its first version")
def _first_version(read_back):
    assert read_back["revision"] == 1


@given(parsers.parse('a decision in a file whose title is written "{title}"'), target_fixture="decision_file")
def _decision_in_a_file_titled(tmp_path, title):
    """The title is written bare, as a person types it, so YAML is free to read it as something else."""
    path = tmp_path / "titled.yaml"
    path.write_text(
        f"title: {title}\n"
        "sections:\n"
        "  - title: Purpose\n    body: Keep prices in step with costs.\n"
        "  - title: Rationale\n    body: Costs move weekly.\n"
    )
    return path


def _title_read_back(env, result, decision_file):
    """The title as the shop reads it back under the name the decision was given, and the title as written."""
    assert result.returncode == 0, result.stderr
    read = knol(env, "read", loads(result.stdout)["id"])
    assert read.returncode == 0, read.stderr
    written = decision_file.read_text().splitlines()[0].removeprefix("title: ")
    return loads(read.stdout)["title"], written


@then("the shop reads the title back as the text that was written, not as a date")
def _title_is_text_not_a_date(env, result, decision_file):
    shown, written = _title_read_back(env, result, decision_file)
    assert shown == written == "2026-09-24"


@then("the shop reads the title back as the text that was written, not as a yes or a no")
def _title_is_text_not_a_bool(env, result, decision_file):
    shown, written = _title_read_back(env, result, decision_file)
    assert shown == written == "yes"


@then("the name the decision was given is made from that text")
def _name_from_that_text(result, decision_file):
    written = decision_file.read_text().splitlines()[0].removeprefix("title: ")
    assert loads(result.stdout)["id"] == f"decision/{written}"


@given("a decision in a file that names the same entry twice in the same place", target_fixture="decision_file")
def _decision_in_a_file_naming_an_entry_twice(tmp_path):
    path = tmp_path / "twice.yaml"
    path.write_text(
        "title: Price reviews happen weekly\n"
        "sections:\n"
        "  - title: Purpose\n"
        "    body: Keep prices in step with costs.\n"
        "    body: Keep prices low.\n"
        "  - title: Rationale\n"
        "    body: Costs move weekly.\n"
    )
    return path


@then("the decision is rejected because an entry is named once and only once, naming the place in the file")
def _rejected_for_an_entry_named_twice(result, decision_file):
    assert result.stderr.splitlines() == [
        f"{decision_file} at sections/0/body: an entry is named once and only once; 'body' is named again at line 5",
    ]
```

In `CLAUDE.md`'s "Step definitions" section, after the line pair

```markdown
- Fixtures and steps shared by more than one feature live in `tests/conftest.py`; the rest sit beside the scenarios
  they serve.
```

insert:

```markdown
- A When that runs shop-knol gives what it ran as the fixture `result`, so the shared Thens that say how a command
  ended, such as "the command reports failure to whatever ran it", read it under one name in every feature.
```

- [ ] **Step 4: Run the check**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -rf 2>&1 | grep ^FAILED | sort | diff - /tmp/failed-before.txt && echo "same 55"; make test 2>&1 | grep -E "^[0-9]+ failed"; grep -rnE "never a traceback|reports failure to whatever ran it" tests/*.py | grep -v conftest.py
```

Expected: `same 55`, then `55 failed, 7 passed`, then nothing.

- [ ] **Step 5: Checkpoint and commit**

Set slice 1.30's `- Status: planned` to `- Status: green`, and append to the very end of the slice plan's `## Log` (verify with `tail -3`), every placeholder filled with the real output:

```markdown
- 2026-09-26 slice 1.30 green. The shared refusal steps, "the user is shown that fault in plain words, never a traceback" and "the command reports failure to whatever ran it", are defined once in `tests/conftest.py` over the fixture `result`, which every When that runs shop-knol now gives. Check: <Step 4's output, complete>.
  Surprised by: <anything, or "nothing">.
  Next: slice 1.31.
```

```bash
cd /home/vscode/shopsystem-knowledge && git add CLAUDE.md tests docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -q -m "Slice 1.30: the steps every feature shares are defined once

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>" && git status --short
```

Expected: nothing printed by `git status --short`.

---

### Task 2: Slice 1.31, reading the user's file is one function of its own

**Slice plan entry:** Slice 1.31, enabling. Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same 55 failing scenarios as before (55 failed, 7 passed), and `.venv/bin/python -c "import inspect,shop_knowledge.cli as c; s=inspect.getsource(c._create); assert 'try' not in s and 'read_text' not in s"` succeeds, and `grep -c read_text src/shop_knowledge/cli.py` prints 1.

**Files:**
- Modify: `src/shop_knowledge/cli.py`
- Modify: `CLAUDE.md` (Size and shape), the slice plan (status, checkpoint)

**Interfaces:**
- Consumes: nothing new.
- Produces: `cli.Refused(faults)`, an exception whose `faults` is a list of `kb_pb2.Fault`; `main` catches it and prints it through `_refuse`, exit 1. `cli._document(source: str) -> dict`, the user's file read the way kb reads content, raising `Refused` with the place where kb cannot read it. `cli._parser() -> argparse.ArgumentParser`, where each subparser names its handler with `set_defaults(handler=...)`. Tasks 5 to 7 add commands in `_parser` the same way, and Task 5's `apply` reads its file with `_document`.

- [ ] **Step 1: See the check fail**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -c "import inspect,shop_knowledge.cli as c; s=inspect.getsource(c._create); assert 'try' not in s and 'read_text' not in s" 2>&1 | tail -1
```

Expected: `AssertionError`. `_create` reads the file and catches `NotCanonical` itself.

- [ ] **Step 2: One reader, and one catch for every refusal**

Replace the whole of `src/shop_knowledge/cli.py` with:

```python
"""shop-knol: the shop's command line over kb. KB_ROOT finds the repository, KB_ACTOR says who is acting.

Every file it reads and everything it prints is YAML 1.2, read and written by kb's own reading and writing of content.
A refusal, kb's or its own, is printed in plain words on stderr, one fault a line, with a non-zero exit; never a traceback.
"""
import argparse
import os
import sys
from pathlib import Path

from kb import canonical, client as kb_client
from kb.content import dumps, loads, text
from kb.contract import kb_pb2

from shop_knowledge import bootstrap


class Refused(Exception):
    """A refusal on its way to the one printer: the faults to print, one line each."""

    def __init__(self, faults):
        super().__init__(faults)
        self.faults = list(faults)


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    try:
        return args.handler(args)
    except Refused as refusal:
        return _refuse(refusal.faults)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shop-knol")
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="start a shop knowledge base at <root>/kb/ with the shop's types")
    init.add_argument("root")
    init.set_defaults(handler=_init)

    create = commands.add_parser("create", help="record an artifact from a YAML file; prints the id kb chose")
    create.add_argument("type")
    create.add_argument("--from", dest="source", required=True, metavar="FILE")
    create.add_argument("-m", dest="message", required=True, help="why")
    create.set_defaults(handler=_create)

    read = commands.add_parser("read", help="read an artifact at a glance")
    read.add_argument("locator")
    read.set_defaults(handler=_read)

    validate = commands.add_parser(
        "validate", help="check everything the shop knows; lists every fault, exits non-zero if any",
    )
    validate.set_defaults(handler=_validate)
    return parser


def _actor() -> kb_pb2.Actor:
    return kb_pb2.Actor(role=os.environ["KB_ACTOR"])


def _client():
    return kb_client.connect(Path(os.environ["KB_ROOT"]))


def _show(document: dict) -> None:
    print(dumps(document), end="")


def _plain(fault: kb_pb2.Fault) -> str:
    """One fault as a line a person reads: where, then what is wrong."""
    where = f"{fault.artifact} at {fault.path}" if fault.path else fault.artifact
    return f"{where}: {fault.message}"


def _refuse(faults) -> int:
    for fault in faults:
        print(_plain(fault), file=sys.stderr)
    return 1


def _init(args) -> int:
    root = Path(args.root)
    client = kb_client.connect(root)
    client.Init(kb_pb2.InitRequest(root=str(root), actor=_actor()))
    bootstrap.load(client, _actor())
    return 0


def _document(source: str) -> dict:
    """A file the user gave, read the way kb reads content, or refused with the place kb could not read it at."""
    try:
        return loads(Path(source).read_text())
    except canonical.NotCanonical as fault:
        raise Refused([kb_pb2.Fault(artifact=source, path=fault.path, rule="content", message=str(fault))])


def _create(args) -> int:
    content = _document(args.source)
    title = text(content.pop("title", None))
    response = _client().Create(kb_pb2.CreateRequest(
        type=args.type, title=title, content=dumps(content), actor=_actor(), message=args.message,
    ))
    if response.faults:
        return _refuse(response.faults)
    _show({"id": response.id, "revision": response.revision})
    return 0


def _read(args) -> int:
    response = _client().Read(kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=args.locator)))
    if response.faults:
        return _refuse(response.faults)
    _show({
        "id": response.id,
        "type": response.type,
        "schema_version": response.schema_version,
        "revision": response.revision,
        "title": response.title,
        **loads(response.content),
        "references": [
            {"field": stub.field, "id": stub.id, "type": stub.type, "title": stub.title, **loads(stub.fields)}
            for stub in response.references
        ],
        "parts": [{"collection": stub.collection, "id": stub.id, "title": stub.title} for stub in response.parts],
        "inbound": [{"type": count.type, "field": count.field, "count": count.count} for count in response.inbound],
    })
    return 0


def _validate(args) -> int:
    response = _client().Validate(kb_pb2.ValidateRequest())
    return _refuse([*response.faults, *response.violations]) if response.faults or response.violations else 0
```

What moved: `main` parses with `_parser()`, calls the handler the subparser names, and catches `Refused`, printing it with `_refuse`, the one printer; `_document` holds the one `try` and the one `read_text`, raising `Refused` with the same fault `_create` printed before. `_create`'s kb answer and `_validate`'s still go through `_refuse` directly; Task 3 moves them.

In `CLAUDE.md`'s "Size and shape" section, replace the line

```markdown
- A file a user gives is read in one place, and a kb answer's faults are refused in one way.
```

with:

```markdown
- A file a user gives is read in one place, `cli._document`, and a kb answer's faults are refused in one way.
```

- [ ] **Step 3: Run the check**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -rf 2>&1 | grep ^FAILED | sort | diff - /tmp/failed-before.txt && echo "same 55"; make test 2>&1 | grep -E "^[0-9]+ failed"; .venv/bin/python -c "import inspect,shop_knowledge.cli as c; s=inspect.getsource(c._create); assert 'try' not in s and 'read_text' not in s" && echo "create reads no file"; grep -c read_text src/shop_knowledge/cli.py
```

Expected: `same 55`, `55 failed, 7 passed`, `create reads no file`, `1`. Slice 1.24's scenario, the file naming an entry twice, is among the 7 passing: the refusal still prints the same line with exit 1.

- [ ] **Step 4: Checkpoint and commit**

Set slice 1.31's status to green and append to the very end of the log (verify with `tail -3`):

```markdown
- 2026-09-26 slice 1.31 green. A file the user gives is read only by `cli._document`, which raises `cli.Refused` where kb cannot read it; `main` catches `Refused` and prints it through `_refuse`, the one printer, and each subparser names its handler. Check: <Step 3's output, complete>.
  Surprised by: <anything, or "nothing">.
  Next: slice 1.32.
```

```bash
cd /home/vscode/shopsystem-knowledge && git add CLAUDE.md src/shop_knowledge docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -q -m "Slice 1.31: reading the user's file is one function of its own

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>" && git status --short
```

---

### Task 3: Slice 1.32, turning a read answer into what is shown is one function of its own

**Slice plan entry:** Slice 1.32, enabling. Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same 55 failing scenarios as before (55 failed, 7 passed), and `.venv/bin/python -c "import inspect,shop_knowledge.cli as c; s=inspect.getsource(c._read); assert ' for ' not in s and len(s.splitlines())<=6"` succeeds.

**Files:**
- Modify: `src/shop_knowledge/cli.py`
- Modify: `CLAUDE.md` (rule 4, Size and shape), the slice plan (status, checkpoint)

**Interfaces:**
- Consumes: `cli.Refused`, `main`'s catch (Task 2).
- Produces: `cli._answered(response)`, which gives back any kb answer with no `faults` and raises `Refused(response.faults)` otherwise; every handler after this calls kb through it. `cli._glance(response: kb_pb2.ReadResponse) -> dict`, what `read` shows, which slices 22 and 32 extend.

- [ ] **Step 1: See the check fail**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -c "import inspect,shop_knowledge.cli as c; s=inspect.getsource(c._read); assert ' for ' not in s and len(s.splitlines())<=6" 2>&1 | tail -1
```

Expected: `AssertionError`.

- [ ] **Step 2: One way to refuse a kb answer, and the read's shaping apart**

In `src/shop_knowledge/cli.py`, replace:

```python
def _refuse(faults) -> int:
    for fault in faults:
        print(_plain(fault), file=sys.stderr)
    return 1
```

with:

```python
def _refuse(faults) -> int:
    for fault in faults:
        print(_plain(fault), file=sys.stderr)
    return 1


def _answered(response):
    """kb's answer, or the refusal it carries: every kb answer's faults are refused this one way."""
    if response.faults:
        raise Refused(response.faults)
    return response
```

Replace:

```python
    response = _client().Create(kb_pb2.CreateRequest(
        type=args.type, title=title, content=dumps(content), actor=_actor(), message=args.message,
    ))
    if response.faults:
        return _refuse(response.faults)
```

with:

```python
    response = _answered(_client().Create(kb_pb2.CreateRequest(
        type=args.type, title=title, content=dumps(content), actor=_actor(), message=args.message,
    )))
```

Replace everything from `def _read(args) -> int:` to the end of the file with:

```python
def _read(args) -> int:
    response = _answered(_client().Read(kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=args.locator))))
    _show(_glance(response))
    return 0


def _glance(response: kb_pb2.ReadResponse) -> dict:
    """A summary read as the user is shown it: identity, the fields the type shows, stubs, parts and inbound counts."""
    return {
        "id": response.id,
        "type": response.type,
        "schema_version": response.schema_version,
        "revision": response.revision,
        "title": response.title,
        **loads(response.content),
        "references": [
            {"field": stub.field, "id": stub.id, "type": stub.type, "title": stub.title, **loads(stub.fields)}
            for stub in response.references
        ],
        "parts": [{"collection": stub.collection, "id": stub.id, "title": stub.title} for stub in response.parts],
        "inbound": [{"type": count.type, "field": count.field, "count": count.count} for count in response.inbound],
    }


def _validate(args) -> int:
    """kb's check answers with the store's faults and violations alike; any of either is a refusal."""
    response = _client().Validate(kb_pb2.ValidateRequest())
    if response.faults or response.violations:
        raise Refused([*response.faults, *response.violations])
    return 0
```

`_validate` raises `Refused` over its faults and its violations together rather than going through `_answered` (decision 2), so the check's listing is printed exactly as before.

In `CLAUDE.md`, rule 4, replace the line

```markdown
   `cli.py`, one line each, with exit 1. shop-knol never shows a traceback.
```

with:

```markdown
   `cli.py`, one line each, with exit 1. shop-knol never shows a traceback. Code that refuses raises `cli.Refused`
   with its faults and `main` alone prints them, so no handler prints a refusal of its own.
```

and in "Size and shape", replace the line

```markdown
- A file a user gives is read in one place, `cli._document`, and a kb answer's faults are refused in one way.
```

with:

```markdown
- A file a user gives is read in one place, `cli._document`, and a kb answer's faults are refused in one way,
  `cli._answered`.
```

- [ ] **Step 3: Run the check, and the shape check**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -rf 2>&1 | grep ^FAILED | sort | diff - /tmp/failed-before.txt && echo "same 55"; make test 2>&1 | grep -E "^[0-9]+ failed"; .venv/bin/python -c "import inspect,shop_knowledge.cli as c; s=inspect.getsource(c._read); assert ' for ' not in s and len(s.splitlines())<=6" && echo "read calls, refuses or shows"
```

Expected: `same 55`, `55 failed, 7 passed`, `read calls, refuses or shows`. Then run the shape check from Global Constraints. Expected: `2`, `1`, `1`, and nothing more.

- [ ] **Step 4: Checkpoint and commit**

Set slice 1.32's status to green and append to the very end of the log (verify with `tail -3`):

```markdown
- 2026-09-26 slice 1.32 green. Every kb answer is refused through `cli._answered`, which raises `Refused`, so `main` is the only caller of `_refuse`; `_read` calls, refuses or shows, and `_glance` shapes the answer. `_validate` raises its faults and violations together, as it printed them before. Check: <Step 3's output, complete, and the shape check's>.
  Surprised by: <anything, or "nothing">.
  Open questions: none. The review's rule-4 breaks that change behaviour (Init's answer and bootstrap's Create answers dropped, the `KB_ACTOR` and `KB_ROOT` tracebacks) stay with slices 22, 26 and 47.
  Next: slice 4.
```

```bash
cd /home/vscode/shopsystem-knowledge && git add CLAUDE.md src/shop_knowledge docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -q -m "Slice 1.32: turning a read answer into what is shown is one function of its own

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>" && git status --short
```

---

### Task 4: Slice 4, the shop's seven types

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
- Produces: the types `shop-artifact`, `tag`, `decision`, `work-item`, `feature`, `role`, `step`, `process`, in the shapes of decision 4, which Tasks 5 to 8 record into. The steps `Given an empty directory for the shop's knowledge` and `When the user starts a shop knowledge base in that directory, saying who they are` (gives `result`), which slice 47 reuses beside the shared `Then the command reports failure to whatever ran it`.

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


@when("the user starts a shop knowledge base in that directory, saying who they are", target_fixture="result")
def _start_saying_who(env, shop):
    return knol(env, "init", str(shop))


@then("the shop can hold decisions, features, work items, roles, processes, steps and tags")
def _holds_the_seven(env, tmp_path, result):
    assert result.returncode == 0, result.stderr
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

Replace the whole of `src/shop_knowledge/types/tag.yaml` with (the base added; `summary: []` gone, since the base's `summary` is the tag's):

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

Replace the whole of `src/shop_knowledge/types/decision.yaml` with (the base added; `tags` moved to the base):

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

Replace the whole of `src/shop_knowledge/types/work-item.yaml` with (the base added):

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

- [ ] **Step 4: Run it green, the suite, and the shape check**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-4 2>&1 | tail -1 && .venv/bin/python -m pytest -q -m "slice-1 or slice-1.17 or slice-1.24 or slice-1.27 or slice-1.28" 2>&1 | tail -1 && make test 2>&1 | grep -E "^[0-9]+ failed"
```

Expected: `1 passed, 61 deselected`, then `7 passed, 55 deselected`, then `54 failed, 8 passed` (warning counts and timings follow on the first two lines). Then run the shape check from Global Constraints: `2`, `1`, `1`, nothing more.

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

### Task 5: Slice 15, make several changes at once from the command line

**Slice plan entry:** Slice 15, capability. Unknown: what shape does a batch take in a file, given each change carries its own content and the set carries one actor and one message? Scenario:

1. make-several-changes-at-once / The user makes several changes at once

**Files:**
- Create: `src/shop_knowledge/batch.py`
- Modify: `src/shop_knowledge/cli.py`
- Modify: `tests/test_make_several_changes_at_once.py`
- Modify: `CLAUDE.md` (module map row), the slice plan (checkpoint)

**Interfaces:**
- Consumes: the `work-item` and `decision` types (Task 4); `cli._document`, `cli._answered`, `_parser`'s `set_defaults(handler=...)` (Tasks 2 and 3); `driver.knol`, `driver.record`, `driver.start(env, shop)`.
- Produces: `shop_knowledge.batch.operations(document: dict) -> list[kb_pb2.Operation]`; `shop-knol apply --from FILE -m MESSAGE`, printing `batch:` and `results:` (`id`, `revision`). The Background step and `When the user applies the batch, saying who they are and why` (gives `result`), which slice 48 reuses. Task 6 uses `apply` to make a revision.

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


@when("the user applies the batch, saying who they are and why", target_fixture="result")
def _apply(env, batch_file):
    return knol(env, "apply", "--from", str(batch_file), "-m", "Review prices weekly, starting with dairy")


@then("both changes are in the shop")
def _both_in_the_shop(env, result):
    assert result.returncode == 0, result.stderr
    assert [change["id"] for change in loads(result.stdout)["results"]] == [WEEKLY, WORK_ITEM]
    decision = knol(env, "read", WEEKLY)
    assert decision.returncode == 0, decision.stderr
    work_item = loads(knol(env, "read", WORK_ITEM).stdout)
    assert [(stub["field"], stub["id"]) for stub in work_item["references"]] == [("decisions", WEEKLY)]


@then("the shop's history shows them as one change")
def _one_change(shop, result):
    batch = loads(result.stdout)["batch"]
    history = kb_client.connect(shop).Journal(kb_pb2.JournalRequest(batch=batch))
    assert [(entry.op, entry.artifact) for entry in history.entries] == [("create", WEEKLY), ("write", WORK_ITEM)]
    assert {entry.message for entry in history.entries} == {"Review prices weekly, starting with dairy"}
```

The history is read through kb's in-process client because no shop-knol command shows it until Task 6; `CLAUDE.md` allows that for what no command yet shows.

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-15 2>&1 | grep -E "^E  |passed|failed" | head -3
```

Expected: `E       AssertionError: usage: shop-knol [-h] {init,create,read,validate} ...`, then `E         shop-knol: error: argument command: invalid choice: 'apply' (choose from 'init', 'create', 'read', 'validate')`.

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

In `_parser`, replace:

```python
    validate.set_defaults(handler=_validate)
    return parser
```

with:

```python
    validate.set_defaults(handler=_validate)

    apply = commands.add_parser("apply", help="make every change in a batch file as one change; prints the set's name")
    apply.add_argument("--from", dest="source", required=True, metavar="FILE")
    apply.add_argument("-m", dest="message", required=True, help="why")
    apply.set_defaults(handler=_apply)
    return parser
```

Append at the end of the file:

```python


def _apply(args) -> int:
    operations = batch.operations(_document(args.source))
    response = _answered(_client().Apply(kb_pb2.ApplyRequest(
        operations=operations, actor=_actor(), message=args.message,
    )))
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

- [ ] **Step 4: Run it green, the suite, and the shape check**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m "slice-15 or slice-1.24" 2>&1 | tail -1 && make test 2>&1 | grep -E "^[0-9]+ failed"
```

Expected: `2 passed, 60 deselected` (slice 1.24's refusal of a file naming an entry twice still goes through the one reader), then `53 failed, 9 passed`. Then the shape check: `2`, `1`, `1`, nothing more.

- [ ] **Step 5: Checkpoint and commit**

Set slice 15's status to green and append to the very end of the log (verify with `tail -3`):

```markdown
- 2026-09-26 slice 15 green. A user can now: apply a batch file that records a decision and points a work item at it, as one change in the history under one role and one message.
  Assumption "a batch is a file of changes, each with its own content, and the set's actor and message come from the command line like any other change": <held or failed>. Evidence: <the `apply` output from a run of the scenario's batch, and the Journal entries under its batch name>.
  Surprised by: <anything, or "nothing">.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 1): a batch file of the wrong shape (`changes:` holding `- delete: tag/pricing`, or no `changes:`) gives `KeyError: 'content'` / `KeyError: 'changes'` tracebacks. What is it told?
  Next: slice 16.
```

```bash
cd /home/vscode/shopsystem-knowledge && git add CLAUDE.md src/shop_knowledge tests docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -q -m "Slice 15: make several changes at once from a batch file

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>" && git status --short
```

---

### Task 6: Slice 16, review the changes to one thing

**Slice plan entry:** Slice 16, capability. Unknown: how does the command line let step definitions set the day, so a change made two days ago and one made today appear as such? Scenario:

1. review-who-changed-what / The user reviews the changes to one thing

**Files:**
- Create: `tests/clock/sitecustomize.py`
- Modify: `tests/driver.py`, `tests/test_review_who_changed_what.py`
- Modify: `src/shop_knowledge/cli.py`
- Modify: `CLAUDE.md` (Step definitions), the slice plan (checkpoint)

**Interfaces:**
- Consumes: `shop-knol apply` (Task 5), the `decision` type (Task 4), `cli._answered` (Task 3).
- Produces: `driver.at(env, moment: str) -> dict`, the environment in which shop-knol's history is stamped from `moment` (ISO, UTC); `shop-knol journal [--artifact NAME]`, printing `changes:` as in decision 7; `cli._change(entry: kb_pb2.Entry) -> dict`; `cli._actor()` reading `role:execution`. The Background steps `Given today is {day}` (gives `today`) and the recorded-then-revised Given, and the constants `WEEKLY` and `PIECE_OF_WORK`, which slice 36 reuses.

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

Replace the whole of `tests/driver.py` with (`os` and `Path` imported, and `at` added at the end):

```python
"""Drive shop-knol the way a user does: a subprocess per command, YAML in files and on stdout."""
import os
import subprocess
import sys
from pathlib import Path

from kb.content import dumps, loads


def knol(env, *args):
    return subprocess.run(
        [sys.executable, "-m", "shop_knowledge", *args],
        env=env, capture_output=True, text=True,
    )


def start(env, shop):
    result = knol(env, "init", str(shop))
    assert result.returncode == 0, result.stderr


def record(env, tmp_path, type_name, content, message):
    """Write content to a file, record it, and return the id the user is shown."""
    path = tmp_path / f"{content['title']}.yaml"
    path.write_text(dumps(content))
    result = knol(env, "create", type_name, "--from", str(path), "-m", message)
    assert result.returncode == 0, result.stderr
    return loads(result.stdout)["id"]


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


@when("the user reviews the changes to that decision", target_fixture="result")
def _review_the_decision(env):
    return knol(env, "journal", "--artifact", WEEKLY)


@then("the user sees both changes, each with who made it, when, what it did and why")
def _both_changes(result, today):
    assert result.returncode == 0, result.stderr
    assert [
        (change["actor"], change["at"][:10], change["op"], change["message"])
        for change in loads(result.stdout)["changes"]
    ] == [
        ({"role": "shopkeeper", "execution": ""}, "2026-09-21", "create", "Record weekly reviews"),
        ({"role": "agent", "execution": PIECE_OF_WORK}, today, "write", "Accept weekly reviews"),
    ]
```

Each command is given its own moment, so no two processes stamp the same second and no two history entries share a name.

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-16 2>&1 | grep -E "^E  |passed|failed" | head -3
```

Expected: `E       AssertionError: usage: shop-knol [-h] {init,create,read,validate,apply} ...`, then `E         shop-knol: error: argument command: invalid choice: 'journal' (choose from 'init', 'create', 'read', 'validate', 'apply')`. The Background already runs: kb takes `agent:reprice-dairy` as a role until Step 3 splits it.

- [ ] **Step 3: The command, and the piece of work in `KB_ACTOR`**

In `src/shop_knowledge/cli.py`:

In `_parser`, replace:

```python
    apply.set_defaults(handler=_apply)
    return parser
```

with:

```python
    apply.set_defaults(handler=_apply)

    journal = commands.add_parser("journal", help="review who changed what: every change, oldest first")
    journal.add_argument("--artifact", default="", help="only the changes to this one")
    journal.set_defaults(handler=_journal)
    return parser
```

Replace `_actor`:

```python
def _actor() -> kb_pb2.Actor:
    return kb_pb2.Actor(role=os.environ["KB_ACTOR"])
```

with:

```python
def _actor() -> kb_pb2.Actor:
    """KB_ACTOR is the role, or the role and the piece of work it acts for as role:execution."""
    role, _, execution = os.environ["KB_ACTOR"].partition(":")
    return kb_pb2.Actor(role=role, execution=execution)
```

Append at the end of the file:

```python


def _journal(args) -> int:
    response = _answered(_client().Journal(kb_pb2.JournalRequest(artifact=args.artifact)))
    _show({"changes": [_change(entry) for entry in response.entries]})
    return 0


def _change(entry: kb_pb2.Entry) -> dict:
    """One entry of the history as the user is shown it: when, who and for what piece of work, what it did, and why."""
    return {
        "at": entry.at,
        "actor": {"role": entry.actor.role, "execution": entry.actor.execution},
        "op": entry.op,
        "artifact": entry.artifact,
        "revision": entry.revision,
        "message": entry.message,
    }
```

The history entry's message type is `kb_pb2.Entry`; there is no `JournalEntry` in kb v0.2.0.

In `CLAUDE.md`'s "Step definitions" section, after the `result` line Task 1 added, insert:

```markdown
- `tests/clock/` is put on shop-knol's `PYTHONPATH`, with `TEST_NOW` set, only through `driver.at`, when a scenario
  says what day it is. Nothing under `src/` knows the day is set.
```

- [ ] **Step 4: Run it green, the suite, and the shape check**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m "slice-16 or slice-15" 2>&1 | tail -1 && make test 2>&1 | grep -E "^[0-9]+ failed"
```

Expected: `2 passed, 60 deselected`, then `52 failed, 10 passed`. Then the shape check: `2`, `1`, `1`, nothing more.

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

### Task 7: Slice 17, publish a process as a skill

**Slice plan entry:** Slice 17, capability. Unknown: is a resolved whole read, with the stubs of its references and its type, enough for a renderer to write a reused step out in full? Scenario:

1. publish-what-the-shop-knows / The user publishes a process as a skill

**Files:**
- Create: `src/shop_knowledge/renderers/__init__.py`, `src/shop_knowledge/renderers/rendered.py`, `src/shop_knowledge/renderers/skill.py`
- Modify: `src/shop_knowledge/cli.py`
- Modify: `tests/test_publish_what_the_shop_knows.py`
- Modify: `CLAUDE.md` (module map row), the slice plan (checkpoint)

**Interfaces:**
- Consumes: the `process`, `step` and `role` types (Task 4); `cli._answered` (Task 3).
- Produces: `shop_knowledge.renderers.rendered.Rendered(files: dict[str, str], faults: list[kb_pb2.Fault])`, a `NamedTuple`, and `rendered.refused(faults) -> Rendered`; `shop_knowledge.renderers.RENDERERS: dict[str, Callable[[client, str], Rendered]]`; `renderers.skill.render(client, name) -> Rendered` and `renderers.skill.body(title, steps, shared) -> str`; `shop-knol render <renderer> <name> --to DIR`, printing `written:`; `cli._write(files, directory)`. The Background (gives `process_name`), the fixtures `target` (the empty directory published into) and `before` (the knowledge base's files, taken when the When runs), and `When the user publishes the process as a skill into a directory` (gives `result`), which Task 8 and slices 19, 20 and 50 reuse.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-17 2>&1 | grep -E "StepDefinitionNotFound|passed|failed" | head -3
```

Expected: `1 failed`, with `StepDefinitionNotFoundError` for the Background's Given.

- [ ] **Step 2: The steps**

Replace the whole of `tests/test_publish_what_the_shop_knows.py` with:

```python
import re

import pytest
from kb.content import loads
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("publish-what-the-shop-knows.feature")

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


@pytest.fixture
def target(tmp_path):
    """The directory the user publishes into, there and empty before they do."""
    target = tmp_path / "published"
    target.mkdir()
    return target


@pytest.fixture
def before(shop):
    """Every file of the shop's knowledge base, byte for byte, as it was when first asked for."""
    return _everything_under(shop / "kb")


@when("the user publishes the process as a skill into a directory", target_fixture="result")
def _publish_as_a_skill(env, process_name, target, before):
    """Asks for `before` so the knowledge base is taken as it was before the command runs."""
    return knol(env, "render", "skill", process_name, "--to", str(target))


def _heading_block_and_body(text):
    match = re.fullmatch(r"---\n(.*?)---\n\n(.*)", text, re.DOTALL)
    assert match, text
    return loads(match.group(1)), match.group(2)


@then(
    "that directory holds a skill whose heading block is the process's identity and whose body is its steps, "
    "with the reused step written out in full"
)
def _a_skill(result, target):
    assert result.returncode == 0, result.stderr
    heading, body = _heading_block_and_body((target / "restock-a-shelf" / "SKILL.md").read_text())
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
def _unchanged(shop, before):
    assert _everything_under(shop / "kb") == before
```

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-17 2>&1 | grep -E "^E  |passed|failed" | head -3
```

Expected: `E       AssertionError: usage: shop-knol [-h] {init,create,read,validate,apply,journal} ...`, then `E         shop-knol: error: argument command: invalid choice: 'render' (choose from 'init', 'create', 'read', 'validate', 'apply', 'journal')`.

- [ ] **Step 3: The renderer and the command**

Create `src/shop_knowledge/renderers/__init__.py`:

```python
"""Renderers: client code that reads an artifact through the contract and gives back the files to publish, by path
under the directory asked for. A renderer writes nothing and changes nothing; the command line writes what it gives."""
from shop_knowledge.renderers import skill

RENDERERS = {"skill": skill.render}
```

Create `src/shop_knowledge/renderers/rendered.py`:

```python
"""What every renderer gives back: the files to write, by path under the directory asked for, or the faults that stop
it. It carries its faults the way kb's answers do, so the command line refuses both the one way it refuses anything."""
from typing import NamedTuple

from kb.contract import kb_pb2


class Rendered(NamedTuple):
    files: dict[str, str]
    faults: list[kb_pb2.Fault]


def refused(faults) -> Rendered:
    return Rendered({}, list(faults))
```

Create `src/shop_knowledge/renderers/skill.py`:

```python
"""The skill renderer: a process as SKILL.md in the harness's heading-block-plus-body shape. The heading block is the
process's identity; the body is its steps in order, each reused step written out in full with its own settings, and
each branch saying which step it goes to."""
from kb.content import dumps, loads
from kb.contract import kb_pb2

from shop_knowledge.renderers.rendered import Rendered, refused


def render(client, name: str) -> Rendered:
    """The skill's files by path, or the faults of the reads that could not be made."""
    process = _whole(client, name)
    if process.faults:
        return refused(process.faults)
    steps = loads(process.content).get("steps", [])
    shared = {used: _whole(client, used) for used in dict.fromkeys(step["uses"] for step in steps if "uses" in step)}
    faults = [fault for response in shared.values() for fault in response.faults]
    if faults:
        return refused(faults)
    return _skill(process, body(process.title, steps, shared))


def _skill(process: kb_pb2.ReadResponse, written: str) -> Rendered:
    """SKILL.md in a directory of the skill's name, the process's name without its kind."""
    slug = process.id.split("/", 1)[1]
    heading = dumps({"name": slug, "description": process.title})
    return Rendered({f"{slug}/SKILL.md": f"---\n{heading}---\n\n{written}"}, [])


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

In `_parser`, replace:

```python
    journal.set_defaults(handler=_journal)
    return parser
```

with:

```python
    journal.set_defaults(handler=_journal)

    render = commands.add_parser("render", help="publish an artifact into a directory; the shop is only read")
    render.add_argument("renderer", choices=sorted(RENDERERS))
    render.add_argument("locator")
    render.add_argument("--to", required=True, metavar="DIR")
    render.set_defaults(handler=_render)
    return parser
```

Append at the end of the file:

```python


def _render(args) -> int:
    rendered = _answered(RENDERERS[args.renderer](_client(), args.locator))
    _write(rendered.files, Path(args.to))
    _show({"written": sorted(rendered.files)})
    return 0


def _write(files: dict[str, str], directory: Path) -> None:
    """The files a renderer gave back, each written at its path under the directory asked for."""
    for relative, content in files.items():
        path = directory / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
```

`_render` refuses the renderer's faults through `_answered`, before `_write` runs, so nothing is written when anything was refused.

In `CLAUDE.md`'s module map, add this row after `batch.py`'s:

```markdown
| `renderers/` | one module per renderer, each reading an artifact through the contract and giving back a `Rendered` (`rendered.py`): `{path: text}`, or faults; `RENDERERS` names them for `shop-knol render` | writing files, kb writes |
```

- [ ] **Step 4: Run it green, the suite, and the shape check**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-17 2>&1 | tail -1 && make test 2>&1 | grep -E "^[0-9]+ failed"
```

Expected: `1 passed, 61 deselected`, then `51 failed, 11 passed`. Then the shape check: `2`, `1`, `1`, nothing more.

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

### Task 8: Slice 18, a skill the harness would reject is not published

**Slice plan entry:** Slice 18, capability. Unknown: which limits does the harness publish for a skill, and can the renderer check its output against them before writing anything? Scenario:

1. publish-what-the-shop-knows / A skill the harness would reject is not published

**Files:**
- Create: `src/shop_knowledge/renderers/limits.py`
- Modify: `src/shop_knowledge/renderers/skill.py`
- Modify: `tests/test_publish_what_the_shop_knows.py`
- Modify: `CLAUDE.md` (module map row), the slice plan (checkpoint)

**Interfaces:**
- Consumes: the publish Background, `target`, `before` and When (Task 7); `renderers.skill._skill`, `renderers.rendered.refused`.
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
def _rejected_for_the_limits(result):
    assert result.stderr.splitlines() == [
        "process/count-every-shelf at steps: a skill's body is under 500 lines, the limit the harness publishes; "
        "this one is 801",
    ]
    assert result.returncode != 0


@then("nothing is written to the directory")
def _nothing_written(target):
    assert list(target.iterdir()) == []
```

The Given's `target_fixture="process_name"` takes the place of the Background's process for this scenario.

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-18 2>&1 | grep -E "^E  |passed|failed" | head -3
```

Expected: `E       assert [] == ['process/cou...s one is 801']`: the skill is written and nothing is said.

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

In `src/shop_knowledge/renderers/skill.py`, replace the line `from shop_knowledge.renderers.rendered import Rendered, refused` with:

```python
from shop_knowledge.renderers import limits
from shop_knowledge.renderers.rendered import Rendered, refused
```

and replace the head of `_skill`:

```python
def _skill(process: kb_pb2.ReadResponse, written: str) -> Rendered:
    """SKILL.md in a directory of the skill's name, the process's name without its kind."""
    slug = process.id.split("/", 1)[1]
```

with:

```python
def _skill(process: kb_pb2.ReadResponse, written: str) -> Rendered:
    """SKILL.md in a directory of the skill's name, the process's name without its kind, or refused if the harness would
    reject it."""
    faults = limits.skill(process.id, written)
    if faults:
        return refused(faults)
    slug = process.id.split("/", 1)[1]
```

In `CLAUDE.md`'s module map, add this row after `renderers/`'s:

```markdown
| `renderers/limits.py` | the limits the harness publishes, each checked against a renderer's output before anything is written, with where it was published | rendering, files |
```

- [ ] **Step 3: Run it green, the suite, and the shape check**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m "slice-18 or slice-17" 2>&1 | tail -1 && make test 2>&1 | grep -E "^[0-9]+ failed"
```

Expected: `2 passed, 60 deselected`, then `50 failed, 12 passed`. Then the shape check: `2`, `1`, `1`, nothing more.

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

After Task 8: `make test` gives `50 failed, 12 passed`, every failure tagged 19 or later, and `cli.py` is under 250 lines. Next in the slice plan is slice 19, then slice 19.1, the second architecture review.
