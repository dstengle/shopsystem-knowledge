# shop-knowledge batch 19: slices 77 to 83, kb pinned at v0.9.0 (kb.v2) behind two seams

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, in slice order, with one change commit and one checkpoint commit per slice, built under shopsystem-bdd:bdd-red-green.

**This plan carries no code** (adrs/0011).

**Goal:**
- The suite reads green while the portable-knowledge scenarios wait for their slices (77).
- Every kb.v1 form shop-knol spells (a request field naming a kind, the type of types `schema`, an id `schema/<name>`, an answer's `kind` and `schema_version`, a batch's `key`) is spelled in one production module, the seam, and every one a test spells in one test helper (78 to 82), all on kb 0.6.0 with nothing a user sees changed.
- kb is pinned at v0.9.0 (contract kb.v2), and the flip changes only the two seams, the shop's types and the pin (83). Every name a user sees stays as today.

**Spec:**
- `docs/superpowers/specs/2026-10-10-portable-knowledge-design.md` (Identity, S1).
- `spec/index.md` (Order of building, item 4) and the slice plan's log entries of 2026-10-12.
- kb's own contract at v0.9.0: `git -C ../shopsystem-kb show v0.9.0:src/kb/contract/kb.proto`.
- Read CLAUDE.md first.
- Research notes, one per task: `.superpowers/scout/batch19/task-<slice>.md`; earlier probes `.superpowers/scout/kbv2/pin-bump.md` and `seam.md`.

## Global Constraints

- Feature files are read-only. Given/When/Then never change. A hand-back stops the slice.
- kb is v0.6.0 through Task 6; Task 7 pins v0.9.0.
- CLAUDE.md's rules hold, with 250 lines a module. `cli.py` is at 239 lines; `tests/test_make_several_changes_at_once.py` at 232.
- A new module gets its row in CLAUDE.md's module map in the slice that makes it.
- Scratch goes in `.superpowers/batch19/`.
- Commits: a change commit, then a checkpoint commit with the suite record naming the change commit, as in batch 18, each ending with the trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Never push.
- **Batch base:** the commit that adds this plan.

**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.17.0/scripts`

**Decisions of the batch** (each task repeats the ones it needs):
- D1. Until slices 85 to 87, every name shop-knol takes or prints stays as today: `<kind>/<name>` (`decision/start-weekly-price-reviews`, `schema/decision`), and an answer's `type` and `schema_version` print as today.
- D2. The production seam is a new module, `src/shop_knowledge/iris.py`. It owns: a user's name as kb is sent it, and kb's id back as the user's name; every request field that names a kind or the type of types; the fields a Create or a batch create item carries besides title, content and signature; an answer's kind and version back as the user sees them; whether an id names one of the types (today `schema/<name>`, the type of types `schema/schema`). It is the identity on kb 0.6.0. Later (slices 85 and 86) it owns IRIs and the prefixes too.
- D3. At the flip only the seams change: a user's `<kind>/<name>` is `https://missingmass.io/shopsystem/<kind>/missingmass.io/shopsystem/shop-knowledge/<name>`; a kind named in a request is the type's IRI `https://missingmass.io/shopsystem/<kind>`; the shop's types are created at `https://missingmass.io/shopsystem/<type>` with `type` `https://missingmass.io/kb/type@1` (run, task-83 notes); an artifact is created with `type` `<type IRI>@<n>`, its current version; an answer's `type` (a version IRI) prints as the kind (its last segment, the type of types as `schema`) and its `@<n>` as `schema_version`; a create without a name gets the name kb 0.6 minted from its title (lowercased, each run of non-alphanumerics one hyphen), never numbered, a taken name being kb.v2's own refusal; a batch's `@key` resolves to the IRI the seam gives that create (`CreateItem.key` is gone).
- D4. The test seam is a new helper module, `tests/kb_names.py`, imported plainly. It owns every request a test hands kb directly that names a kind, an id or the type of types, every read of a kb message's kind, id, `schema_version` or key, and the fields the dicts steps write for the stand-in spell. It stays independent of `src/` (CLAUDE.md rule 1): it spells D3 itself at the flip.

**Review and model:** Tasks 2 (slice 78) and 7 (slice 83) are `Review: per-task`, `Model: opus`: they touch the published contract. Every other task is `Review: batch-end`, `Model: sonnet`; a batch-end task gets no task review, the batch's branch review covers it.

**Counts:** at 018f17f the suite gave `202 passed, 37 failed` in 34 s (`make test`). By tag: 84: 1, 85: 10, 86: 9, 87: 7, 88: 6, 89: 4, 90: 5, 91: 14, 92: 5; slices 85, 86 and 92 are not collected (no test module binds `name-an-artifact` or `export-the-knowledge-base`), so 37 rows are expected to fail.

| after | result |
|---|---|
| 77 to 82 | `202 passed, 37 xfailed` |
| 83 | `202 passed, 37 xfailed` or fewer xfailed (a scenario going green under the flip, slice 84's one most likely, is credited to 83 and its slice's Status noted) |

**Checks every task runs:** no module over 250 lines; kb imported only as CLAUDE.md rule 1 allows; `jsonschema` imported by `shape.py` alone.

**Execution rules:**

> - **Paths in, short replies out.** The controller dispatches with paths (brief, report, findings, review package, notes) and reads replies, `plan show` and `git log --oneline`. It does not open a diff, a report, a findings file or source: it writes a review package by redirecting `git` output to a file. The one exception is a `BLOCKED` or `NEEDS_CONTEXT` reply, where it reads the part of the report the reply names, to decide or to ask the person.
> - **One line a slice.** The controller writes to the person when a slice goes green and when it takes a decision or needs one, a line each. An agent's notification is acted on, not narrated: every turn re-reads the session.
> - **By step.** A task with Steps is dispatched one step at a time, each to a fresh `bdd-implementer` that is told the step and the task's one report file. One implementer at a time in a worktree. A `PARTIAL` reply is answered with a fresh implementer told it is a continuation, with the same report.
> - **One review per `Review: per-task` task,** after its last step, from the commit before its first. The reviewer is given a findings file to write. A `Review: batch-end` task gets none. A diff over 8 production or 4 test files is reviewed by area, each reviewer given its paths and its own findings file, in parallel.
> - **Fresh fixes.** Findings go to a fresh `bdd-implementer` as a fix round, with the report and the findings file, then to a scoped re-review.
> - **Further rounds only for the severe.** A re-review is dispatched with the triage: fix now only for data left invalid, the system's own fault on input (a crash where a refusal belongs), or a write that lands where a refusal belongs. A finding of one of those kinds gets another fix round and re-review, as many as it takes. Every other finding of a re-review is a backlog line, logged, and the batch closes. No agent is resumed. The branch reviewer is given a findings file too, and the batch's fix wave works from it.
> - **Lanes.** Tasks in different lanes may run at once, each lane in its own git worktree and branch with its own virtualenv, and the dispatch tells each implementer it is in a lane. This replaces subagent-driven-development's rule against parallel implementers, for lanes only. Tasks in one lane run in order; a task with no `Lane:` runs in the main worktree, in order, and not beside a lane. A lane's task is reviewed in its lane, before the merge. A lane's implementer never commits the plan: its reply carries the checkpoint entry. The controller merges the lanes one at a time, runs the suite after each merge, and writes each slice's Status, the checkpoint entry from the reply and the `Suite:` entry itself with `plan`.
> - **Descriptions say what a dispatch is.** Every dispatch's description starts `slice <n>: ` or `slice <n> step <k>: `, then one of `implement`, `fix`, `review`, `re-review`, `research`, `probe`. Work that belongs to no one slice (the branch review, the fix wave, a probe over several slices) starts `batch <name>: `. `measure` attributes each agent's cost by this line.
> - **Measure at the close.** After `plan archive`, the controller runs `python3 <Scripts>/measure batch <the archive file>` and commits the facts file it writes under `docs/superpowers/measurements/` with the archive. It reads nothing from it. The harness removes transcripts after some weeks; the facts are what is kept.
> - **One batch, one session.** When the batch is archived and measured, the controller stops and tells the person the next batch is to be started in a new session that reads its plan. A session that runs a second batch re-reads the first at every turn.

## Review Focus

Probe by hand and record in the checkpoint; a misbehaviour becomes a Backlog line.
1. After the flip, `shop-knol create` of two files with one title: the second is refused in kb's words (a taken IRI), never written over the first and never numbered (Task 7).
2. After the flip, a batch whose link names `@key` of a create in the same batch lands the link on that create's artifact (Task 7; the scenario at `make-several-changes-at-once.feature:45` pins it and must stay green).
3. After the flip, `shop-knol types` and `types <name>` print each type as before, `schema/<name>`, and `validate` still lists an artifact behind its type's version with `schema_version` and `current` as numbers (Task 7).
4. After the flip, `shop-knol init` over a store an operator started under kb 0.6.0: refused in kb's words (a kb.v1 store is an earlier kb's), one line, exit 1, no traceback (Task 7).
5. Between Tasks 2 and 7, a search of `src/` and `tests/` for the kb.v1 forms finds them only in the two seams; the flip's diff outside the seams, `types/` and `pyproject.toml` is empty or listed in its report (Task 7).

---

### Task 1: Slice 77, expected failures for slices not yet built

**Review:** batch-end · **Model:** sonnet · **Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.17.0/scripts` · **Batch base:** as above · **Retires:** none

**Check:** `.venv/bin/python -m pytest -q -n auto` → `202 passed, 37 xfailed`, its summary naming slices 84, 87, 88, 89, 90, 91 as expected to fail; `.venv/bin/python -m pytest --help` lists `--slice`; `make test` passes.

**Why it fails today:** the 37 rows tagged to slices 84 to 92 fail with no plugin to expect them (run, task-77 notes: `37 failed, 202 passed`, no `--slice` in `--help`).

**Where the change lands** (0 production, 2 test):
- `python3 <Scripts>/features plugin tests` writes the plugin, `tests/slice_expectations.py`, which reads each slice's `- Status:` in the slice plan; planned and blocked slices are expected to fail.
- `tests/conftest.py` registers it as the plugin's output says (one star-import line; conftest is at 177 lines).
- CLAUDE.md's Working here gains one line: the slice plugin, `--slice`, and that a scenario of a slice not green is expected to fail.

**Decisions:** none beyond the plugin's own contract. The scout saw it work under xdist and serially, with no unexpected pass (run).

**Tests the decisions break:** none: the scout ran the whole suite with the plugin registered.

**Verify:** the Check above; `-m slice-84` → 1 xfailed.

---

### Task 2: Slice 78, one seam builds kb's requests for the commands

**Review:** per-task · **Model:** opus · **Scripts:** as above · **Batch base:** as above · **Retires:** none

**Check:** `.venv/bin/python -m pytest -q -n auto` → `202 passed, 37 xfailed`; a search of `kb_requests.py`, `bootstrap.py`, `init.py`, `batch.py`, `answers.py` and `cli.py` finds no `kind=`, no `.kind`, no `schema_version`, no `key=`, no `"schema"` and no `schema/` outside `iris.py`.

**Why:** enabling; the suite is green before and after. The forms it moves are listed by line in `.superpowers/scout/batch19/task-78.md`, Part 2 (read).

**Where the change lands** (7 production, 0 test): new `iris.py` with its CLAUDE.md row (D2); `kb_requests.py` (the List of the type of types for init and types, the Create, List, Follow and Search kind fields, the `schema/<name>` locator of `types <name>`); `bootstrap.py` (its Create of each type); `init.py` (reading which types a store holds, the type of types' own id); `batch.py` (a create item's kind and key, a write's id); `answers.py` (an answer's type and schema_version, a stub's and an inbound count's kind, a type's name from its id, a stale row's version); `cli.py` only if wiring needs it (11 lines of room).

**Decisions:**
- D1, D2 and D3 as in Global Constraints. The seam's functions are shaped so that the flip needs no change outside the seam: a Create and a batch create item get every field but title, content and signature from the seam, from the kind and, where there is one, the user's name or key; the seam can tell, for an answer's artifact, stub, inbound count or history entry, the kind and the version a user sees. The scout's notes propose names (`to_kb`, `from_kb`, `kind_of`, `kind_field`, `type_kind`, `create_fields`, `item_key`); the implementer may choose others, and states the final ones in the report for Tasks 3 and 7.
- `init`'s checks of which types a store holds compare names through the seam, never a `schema/` prefix.

**Tests the decisions break:** none: the scout checked the tests asserting printed ids, types and versions (`test_start_a_knowledge_base.py:104,134`, `start_furnished.py:90`, `types_listed_and_read.py:32`, `test_check_the_knowledge_base.py:123-128,156,161`, `types_retiring.py:54`, `spec_shop.py:163`, `test_read_an_artifact.py:104`); D1 keeps every one.

**A guard names its test:** `test_start_a_knowledge_base.py`, `test_use_the_shops_types.py` (types read and listed), `test_make_several_changes_at_once.py` (`@key`, `make-several-changes-at-once.feature:45`), `test_check_the_knowledge_base.py` (behind rows) going red is a stop.

**Verify:** the Check; `-m slice-54 or slice-56` as a quick guard before the whole suite.

---

### Task 3: Slice 79, the readers reach kb through the seam

**Review:** batch-end · **Model:** sonnet · **Scripts:** as above · **Batch base:** as above · **Retires:** none

**Check:** `.venv/bin/python -m pytest -q -n auto` → `202 passed, 37 xfailed`; a search of `src/` finds `kind=`, `.kind`, `"schema"` and `schema/` only in `iris.py`.

**Why:** enabling. The forms, by line, are in `.superpowers/scout/batch19/task-79.md` §2 (read): `coverage.py:17-18,56`, `dependencies.py:17-18,59`, `consistency.py:19,44-45`, `renderers/source.py:24,26-27`, `renderers/shop_capabilities.py:15`, `renderers/spec.py:66`, `renderers/spec_decisions.py:49`.

**Where the change lands** (7 production, 0 test): those seven modules, each calling the seam slice 78 made; `iris.py` gains what they need (a List of a kind's ids by fields, the kind of a read artifact, whether a type is held). The CLAUDE.md rows of `iris.py` and of the seven are corrected where they name a kind.

**Decisions:** D1, D2, D3. `renderers/source.py`'s refusal of an artifact of another type keeps its words (`publish_refused.py:64-66` compares them), with the kind from the seam. `source.slug` splits a `<kind>/<name>` user name; it stays as it is (D1; slice 91 names files from IRIs).

**Tests the decisions break:** none: the scout checked `test_see_what_a_shop_depends_on.py`, `dependencies_steps.py`, `formulated_steps.py`, `test_publish_a_shops_spec.py`, `publish_refused.py` and the stand-in.

**Verify:** the Check.

---

### Task 4: Slice 80, a test seam, first group

**Review:** batch-end · **Model:** sonnet · **Scripts:** as above · **Batch base:** as above · **Retires:** none

**Check:** `.venv/bin/python -m pytest -q -n auto` → `202 passed, 37 xfailed`; a search of `tests/kb_oracle.py`, `tests/record_refused_files.py` and `tests/spec_attempt.py` finds no `kind=`, `schema_version`, `key=` or `schema/` handed to kb or read from a kb message outside `tests/kb_names.py`.

**Where the change lands** (0 production, 4 test): new `tests/kb_names.py` (D4); `kb_oracle.py` (`operator_created`'s Create, line 18-23, 82); `record_refused_files.py:44`; `spec_attempt.py:26`. Lines from `.superpowers/scout/batch19/task-80.md` (read).

**Decisions:** D1, D4; the helper's functions mirror the production seam's roles (a Create's fields from a kind and name, a List or locator by kind, a name for an id) but are written in the tests, never imported from `src/`. CLAUDE.md's Step definitions section names the helper in one line.

**Tests the decisions break:** none: they move, asserting what they asserted.

**Verify:** the Check.

---

### Task 5: Slice 81, the test seam, second group

**Review:** batch-end · **Model:** sonnet · **Scripts:** as above · **Batch base:** as above · **Retires:** none

**Check:** `.venv/bin/python -m pytest -q -n auto` → `202 passed, 37 xfailed`; the same search over `tests/start_refused.py`, `tests/start_not_empty.py`, `tests/test_make_several_changes_at_once.py` and `tests/conftest.py` finds nothing outside `tests/kb_names.py`.

**Where the change lands** (0 production, 4 test): those four (lines in `.superpowers/scout/batch19/task-81.md`): `start_refused.py:138-139` (the List of the type of types the oracle asks, which must stay the same call as shop-knol's own), `start_not_empty.py:44,49` (types created through the oracle), `test_make_several_changes_at_once.py:176` (a CreateItem with kind and key; the module has 18 lines of room), `conftest.py`.

**Decisions:** D1, D4. The oracle's List in `start_refused.py` asks what shop-knol's own init asks, through the helper, so the two stay one call at the flip.

**Tests the decisions break:** none.

**Verify:** the Check.

---

### Task 6: Slice 82, the test seam, third group

**Review:** batch-end · **Model:** sonnet · **Scripts:** as above · **Batch base:** as above · **Retires:** none

**Check:** `.venv/bin/python -m pytest -q -n auto` → `202 passed, 37 xfailed`; a search of `tests/` finds `kind=`, `schema_version` in a kb request or a stand-in dict, `key=`, a `HistoryRequest` locator and a `schema/` id handed to kb only in `tests/kb_names.py`.

**Where the change lands** (0 production, 4 test): `test_read_an_artifact.py`, `test_retire_an_artifact.py`, `test_check_the_knowledge_base.py` (lines in `.superpowers/scout/batch19/task-82.md`), and `session_guard.py`, whose `HistoryRequest` is built with a locator kb.v2 no longer has (run, task-83 notes §4): the guard's call goes through the helper.
- Before writing, search the step modules for dicts written for the stand-in (`driver.answering`) that spell `kind` or `schema_version`; if any module beyond these four needs moving, stop and hand back with the list, for a slice 82.1.

**Decisions:** D1, D4.

**Tests the decisions break:** none.

**Verify:** the Check.

---

### Task 6.1: Slice 82.1, the renderers read mapped artifacts

**Review:** batch-end · **Model:** sonnet · **Scripts:** as above · **Batch base:** as above · **Retires:** none

Cut during execution: slice 79's implementer found renderers reading kb's ids and content raw; the scout's table is `.superpowers/scout/batch19/task-79.1.md` (read).

**Check:** `.venv/bin/python -m pytest -q -n auto` → `202 passed, 37 xfailed`; a search of `renderers/source.py`, `markdown.py`, `skill.py`, `diagram.py` and `agent.py` finds no `.id`, `.content` or `loads(` of a kb answer that has not passed through the seam.

**Where the change lands** (at most 7 production, 0 test): `renderers/source.py` hands every renderer an artifact already mapped through `iris.py` (its id, kind, content and version as the user sees them, D1), and `slug` and `refusal` take mapped values; `markdown.py`, `skill.py`, `diagram.py`, `agent.py` read that; `iris.py`, `limits.py` and `published_from.py` only if needed. CLAUDE.md's `renderers/source.py` row says so.

**Decisions:** D1, D2. The mapped artifact is the one shape the spec family moves to in 82.2; name it so.

**Tests the decisions break:** none: no test spells a kb id or reads an answer's attribute (search, task-79.1 notes §3).

**Verify:** the Check.

---

### Task 6.2: Slice 82.2, the spec renderer reads mapped artifacts

**Review:** batch-end · **Model:** sonnet · **Scripts:** as above · **Batch base:** as above · **Retires:** none

**Check:** `.venv/bin/python -m pytest -q -n auto` → `202 passed, 37 xfailed`; a search of `renderers/spec*.py`, `renderers/gherkin.py`, `renderers/shop_capabilities.py` and `consistency.py` finds no id, content or revision of a kb answer read without the seam, and no id already from kb handed to a request builder that maps it again.

**Where the change lands** (at most 8 production, 0 test): `renderers/spec.py`, `spec_faults.py`, `spec_decisions.py`, `spec_capabilities.py`, `spec_index.py`, `gherkin.py`, `shop_capabilities.py`, `consistency.py`, each taking the mapped artifact 82.1 made. Watch `spec.py:20` and `spec_decisions.py:33`: they pass kb's own id into a request builder that applies `to_kb` again; after this slice every id inside shop-knol is the user's form and goes to kb through `to_kb` once.

**Decisions:** D1, D2. If the budget of 8 is not enough (iris.py too), stop and report.

**Tests the decisions break:** none (search, task-79.1 notes §3).

**Verify:** the Check.

---

### Task 7: Slice 83, kb pinned at v0.9.0

**Review:** per-task · **Model:** opus · **Scripts:** as above · **Batch base:** as above · **Retires:** none

**Check:** `.venv/bin/python -c "import kb.contract.kb_pb2 as m; print(m.DESCRIPTOR.package)"` → `kb.v2`; `.venv/bin/python -m pytest -q -n auto` → `202 passed`, 37 or fewer xfailed, 0 failed; a search of `src/` and `tests/` finds no `kind=` on a request, no `schema_version=`, no `key=` on a create item and no `kb.v1`.

**Why it is red at its start:** with kb 0.9.0 installed every store start dies at bootstrap's Create (`CreateRequest has no "kind" field`), 8 passed, 231 failed (run, pin-bump notes §1). Red is seen by bumping the pin and reinstalling (`make dev`) before the seams change.

**Where the change lands** (2 production, 1 test, plus data): `pyproject.toml`'s pin to `@v0.9.0`; `iris.py` to D3; `src/shop_knowledge/types/*.yaml` rewritten for kb.v2 (a reference `kb:schema/<x>` becomes `kb:https://missingmass.io/shopsystem/<x>@1`, link targets the types' IRIs; probed: all eleven are created in bootstrap order, `type` `https://missingmass.io/kb/type@1`, run, task-83 notes §1); `tests/kb_names.py` to D3; CLAUDE.md where it names kb's version or a `schema/` id; `spec/index.md`'s "kb v0.6.0 is pinned today" line is the spec's, and is left for the person (logged as a QUESTION FOR THE SPEC if the implementer finds it must change).
- If anything else must change for the suite to pass, the implementer stops and reports it: it is a seam the earlier tasks missed, and the controller decides a dotted slice.

**Decisions:**
- D1 and D3, D4. A title goes beside the content, never inside it (kb.v2 refuses it, rule `identity`, run). An answer's `type` IRI maps back to the kind as its last segment; the type of types (`https://missingmass.io/kb/type`) maps back to `schema`; `@<n>` to `schema_version`. A stale row's versions are numbers already (`Stale` keeps them).
- A create without a name gets the slug of its title (D3), never numbered. The step at `tests/test_record_an_artifact.py:179` ("a number added") is bound by no scenario today (search); it is slice 87's to remove.
- A type read back may show `content: "{}"` (run); no scenario reads a type's body through shop-knol other than `types <name>`; if that scenario goes red on it, hand back.

**Tests the decisions break:**
- `tests/types_listed_and_read.py:33` asserts a type's `type` is `schema`: kept, by the mapping above.
- `tests/start_refused.py:139`: the oracle's List must be the call shop-knol makes; kept through the helper (Task 5).
- Every test asserting a `schema/<x>` or `<kind>/<name>` printed name: kept, by D1.
- None other found by the scouts; any other test going red is a stop, reported with its failure.

**Verify:** the Check; then Review Focus 1 to 5 probed by hand and recorded in the checkpoint; then `-m slice-84` to see whether slice 84's scenario went green (noted in the slice plan as credited to 83 if it did).
