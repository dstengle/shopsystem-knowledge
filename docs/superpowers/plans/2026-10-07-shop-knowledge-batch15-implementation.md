# shop-knowledge batch 15: slices 52.1 to 55.2, on kb v0.6.0

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, in slice order, with one commit per slice. Tasks 1 and 2 are enabling slices checked by their checks. Tasks 3 to 5 are capability slices, built one scenario at a time under shopsystem-bdd:bdd-red-green.

**This plan carries no code** (adrs/0011).

**Goal:** every approved scenario is green, with shop-knowledge on kb v0.6.0 and its three server scenarios reaching a server only through kb's served-store double (adrs/0050). The work, in order:
- 52.1 makes the suite answer in under a minute by running it in parallel;
- 52.2 pins kb v0.6.0 and lets rule 1 admit what the server scenarios need from kb;
- 53 reads the shop's knowledge through a server;
- 55.1's server row refuses to furnish a served store that already holds the shop's types;
- 55.2 furnishes a served empty store.

**Spec:** `spec/`: `index.md` (Constraints carried: lines 14, 73 and 75 on servers and isolation), and the capabilities `find-the-knowledge-base` and `start-a-knowledge-base`; `spec/decisions.md` from line 406 (init furnishes what kb finds) and 461 (what "already holds the shop's knowledge" covers). kb's side: shopsystem-kb at tag v0.6.0, its README's "Serving a store" and "Serving a store for tests" sections and `src/kb/testing.py`. Read CLAUDE.md, and adrs/0047, 0048, 0049 and 0050.

## Global Constraints

**Change control**
- Feature files are read-only, tag lines included.
- kb is v0.5.0 until Task 2 pins v0.6.0, and is never edited here. A change needed from kb is logged as a KB REQUEST and the slice stops.
- Every rule in CLAUDE.md holds. Task 2 rewords rule 1 so tests may use `kb.testing.served` and src may ask a client `where()` (`kb.client.Where`); nothing else of kb is added.
- No test starts `kb serve` or writes `kb/server.yaml` (adrs/0050); every server is kb's double, `kb.testing.served`, which writes and removes the connection itself.
- shop-knol's commands, flags and answer keys do not change.

**Where to work**
- Work on `main`, and run every command from the checkout's root.
- Scratch goes under `.superpowers/batch15/` (add `.superpowers/` to `.gitignore` if it is not there). Never create a file outside this repository's `.superpowers/` or a test's own temporary directory, and never export `GIT_*` variables. `/home/vscode` is shared with the kb checkout.

**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/` (`plan` for the slice plan's status and log, `features` for counts).

**Review and model**
- Each task's `Review:` and `Model:` lines say how the controller dispatches it. `Review: per-task` with `Model: opus` for a task that touches the published contract, concurrency, data integrity or a stored knowledge base; `Review: batch-end` with `Model: sonnet` for the rest. A batch-end task gets no task review: the batch's branch review covers it.

**Commits**
- Commit with `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`, the message ending with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- One commit per slice, each holding its checkpoint in the slice plan's Log and its Status set to green.
- The implementer never pushes.

**Counts**
- The suite collects 132 scenarios (Examples rows counted) and gives `129 passed, 3 failed` at 414cf0f, in 124 s. The three: slice 53's one, slice 55.1's server row, slice 55.2's one, each red on an undefined server Given.
- The tags select 53: 1; 55.1: 3 (two green today, the server row red); 55.2: 1.

| after | failed | passed |
|---|---|---|
| 52.1 | 3 | 129 |
| 52.2 | 3 | 129 |
| 53 | 2 | 130 |
| 55.1 | 1 | 131 |
| 55.2 | 0 | 132 |

**Checks**
- The failing list, compared at a slice's start and end with `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort`: only the slice's own scenarios may leave it.
- `wc -l src/shop_knowledge/*.py src/shop_knowledge/renderers/*.py tests/*.py tests/*/*.py | awk '$1 > 250 && $2 != "total"'` lists nothing at each slice's end.
- From Task 2 on, `grep -rn "^from kb\|^import kb" src tests | grep -v "kb.client\|kb.content\|kb.contract\|^.*import kb$\|from kb import \(init\|NotStarted\)\|kb.testing"` lists nothing, and `grep -rln "kb.testing" src tests` lists only the one test module that serves a store.
- `grep -rn -E "kb serve|server\.yaml" src tests` lists nothing at any slice's end.

## Review Focus

Inputs no scenario covers that are most likely to bite. For each, the owning task probes it by hand once the slice is green, in a scratch directory under `.superpowers/batch15/`, records what happened in its checkpoint, and logs a misbehaviour as a Backlog line with its reproduction. It writes no scenario for it (CLAUDE.md: no behaviour no scenario asks for).
1. Any shop-knol command where kb finds a connection to a server that is not running (the double's address after its block ended, the connection rewritten by hand in scratch): one plain line in kb's words (`unreachable`), exit 1, never a traceback (Task 3).
2. A shop-knol change (`create`) with `KB_ROOT` naming the store itself while it is served: one plain line in kb's words (`served`), exit 1, nothing changed (Task 3).
3. `init` with nothing named where kb finds a connection to a server hosting a store holding types other than the shop's: refused as not empty, and what it names as the knowledge base (today `_refuse_unless_furnished` names nothing where nothing is named) (Task 4).
4. `init` where the connection kb finds cannot be read (a `kb/server.yaml` of garbage, written by hand in scratch, never by a test): one plain line (`connection`), exit 1, nothing started in the working directory (Task 5).
5. The suite run twice at once from the same checkout in parallel mode: no scenario reaches another's directory, and the session guard still refuses when a store is reachable from the checkout (Task 1).

---

### Task 1: Slice 52.1, the suite runs in parallel and answers in under a minute

Review: per-task. Model: opus. (It touches the suite's isolation, which guards the developer's own knowledge bases.)

Scripts: `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Check:** `make test` -> `129 passed, 3 failed`, the same three, with pytest's own summary line under 60 s; `make dev` in a fresh virtualenv installs what the parallel run needs. The failing list is the same before and after.

**Why now:** the suite takes 124 s serially (`make test` is `pytest -q`), each step starting shop-knol as a subprocess; the machine has 32 cores. CLAUDE.md requires a subprocess per command but says nothing that keeps the run serial. Every later task pays for each run.

**Where it lands:**
- `pyproject.toml`: the parallel runner (pytest-xdist) among the `dev` extras.
- `Makefile`'s `test` target, or pytest's options in `pyproject.toml`, so `make test` runs in parallel. Keep `-m slice-<n>` and a single test id usable as today.
- `tests/`: only what parallel running proves needs changing. Things to look at, not to change unless a run shows they must: `driver._default_cwd` and `driver._runs` are module state, which is per worker process; `conftest.pytest_configure` registers markers in every worker; `session_guard._starting_directories` reads pytest's base temp, which differs per worker; the guard's own call to kb runs once per process. The guard must still refuse in every worker and in the controller as it does today.
- CLAUDE.md's "Working here": `make test` runs in parallel; say how to run it serially when a run's output must be read in order.

**Decisions already made:**
- Each scenario stays in its own temporary directory under the allowlisted environment (CLAUDE.md, Step definitions). Parallel running changes nothing about what a scenario may reach.

**Steps:**
- [ ] Record the failing list and the time.
- [ ] Make the change; meet the check.
- [ ] Probe Review Focus 5.
- [ ] Checkpoint: `plan status 52.1 green`, `plan log` with the Suite line (`N passed, M failed at <hash> in <s> s`) and what parallel running needed. Commit.

### Task 2: Slice 52.2, shop-knowledge pins kb v0.6.0, and its rules admit kb's served-store double

Review: per-task. Model: opus. (It moves the pinned published contract.)

Scripts: `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Check:** `grep -n "shopsystem-kb" pyproject.toml` -> the `v0.6.0` tag; after `make dev`, `.venv/bin/pip show shopsystem-kb` -> `Version: 0.6.0` and `.venv/bin/python -c "import kb.testing; kb.testing.served"` exits 0; CLAUDE.md's rule 1 names `kb.testing.served` as what tests may use for a served store and `client.where()` (`kb.client.Where`) as what src may ask a client; `make test` -> `129 passed, 3 failed`, the same three.

**Why now:** the three server scenarios need the double, and slice 55.1's server row needs `where()`; both ship in v0.6.0 only. Probed 2026-10-07: the suite on v0.6.0 gives the same answer.

**Where it lands:**
- `pyproject.toml`: the pin.
- CLAUDE.md rule 1: add `kb.testing.served` (tests only, one module) and the client's `where()` to what is used of kb, and drop nothing. In the Step definitions section, the sentence on servers says the double is `kb.testing.served`, used through one fixture. Keep the wording clear of the Global Constraints' grep (`kb serve`, `server.yaml`).
- Nothing under `src/` or `tests/` changes.

**Decisions already made:**
- kb v0.6.0 adds to contract v1 and changes nothing in it (kb's `spec/decisions.md`, its last entry); kb also now searches upward from a root given to `connect`. If any answer differs on v0.6.0, stop and hand back with the scenario.

**Steps:**
- [ ] Record the failing list.
- [ ] Make the change; meet the check.
- [ ] Checkpoint: `plan status 52.2 green`, `plan log`. Commit.

### Task 3: Slice 53, shop-knol answers through a kb server exactly as through the store

Review: per-task. Model: opus. (It reaches the store over the network through the published contract.)

Scripts: `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (`@slice-53`, 1): find-the-knowledge-base / Reading where the knowledge base found is a connection to a server hosting the store.

**Why red today:** its Givens "the shop's knowledge base is hosted by a server" and "the user is working in a folder deep inside a directory holding a connection to that server", and its Then "the user sees the decision, just as they would from the store itself", are undefined (slice 59.1 removed the steps that started `kb serve`).

**Where it lands:**
- `src/`: nothing is expected to change (adrs/0049: shop-knol does nothing different between the two). If anything must, stop and hand back.
- The served store: a pytest fixture over `kb.testing.served(store_root, connection_dir)`, in the form kb's README gives, that yields the address and ends the block at teardown. It is shared: slices 55.1 and 55.2 use it from the start feature. Put it, and the Givens it serves, where CLAUDE.md says steps and fixtures shared by more than one feature go (`tests/conftest.py`, or a module beside it that conftest alone star-imports when conftest would pass 250 lines; adrs/0048). It is the one module that imports `kb.testing`. Because the double serves a store and a step names the connection directory, the fixture needs a store root and a connection directory chosen by the Given that asks for it; a fixture that yields a function, or an indirect fixture, both fit. The store is the one the Background started (`shop`, with `decision_id` recorded before serving: while a store is served, a change asked of it directly is refused with `served`).
- The connection directory is a directory of the test's own (`tmp_path`), never `shop`, and the user works in a folder deep inside it, with KB_ROOT removed from `env`, as `_working_deep_inside_the_shop` in `tests/read_back_from_elsewhere.py` does for a store.
- The Then: the decision as shown through the server equals the decision as read from the store itself. The read straight from the store is a read (reads of a served store are not refused), with KB_ROOT naming `shop`. Put the find feature's own Then in `tests/read_back_from_elsewhere.py`.
- Reuse: the Background's steps and `decision_id`; the When "the user reads the decision" (`_read_the_decision`, `tests/test_read_an_artifact.py`) with `workdir`; `shown` from conftest.

**Decisions already made:**
- Tests reach a server only through kb's double (adrs/0050); the double writes and removes the connection, and no step writes it.
- Every run stays inside the test's own temporary directory (`driver._isolated`); the double's server binds 127.0.0.1 only.

**Steps:**
- [ ] Record the failing list; run `-m slice-53` and see it red on its undefined Given.
- [ ] Red-green the scenario.
- [ ] Run `-m slice-53` -> `1 passed`.
- [ ] Probe Review Focus 1 and 2.
- [ ] Checkpoint: `plan status 53 green`, `plan log`. Commit.

### Task 4: Slice 55.1's server row, init never furnishes a served store twice

Review: per-task. Model: opus. (It decides whether init writes to a stored knowledge base.)

Scripts: `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (`@slice-55.1`, 3; two green today): start-a-knowledge-base / Starting where the knowledge base to furnish already holds the shop's types is refused, its row `through a server`.

**Why red today:** its Given "the user is working where kb finds a connection to a server hosting a store holding the shop's types" is undefined. Once it exists the row stays red in `src/`: with nothing named, `init._found` lists the served store, sees the shop's types, finds KB_ROOT unset, and goes on to start a store in the working directory with `kb.init`; the user sees kb's refusal, or worse a second store, where the outline says "rejected because it already holds the shop's knowledge" and "nothing changes".

**Where it lands:**
- The Given, in `tests/start_not_empty.py`, beside `_kb_root_names_a_furnished_one`: a store started and furnished with the shop's types (`driver.start` in a directory of its own), then served through Task 3's fixture, the connection put in the directory the user works in, KB_ROOT removed from `env`. It fills `journal_before` through `_noted`, with `named` set to the decision below.
- `src/shop_knowledge/init.py` (`_found`): a knowledge base kb reaches through a server, holding the shop's types, is refused as already holding the shop's knowledge, raised as `Refused`, before anything is started. Telling one reached through a server is the client's `where()` (`address` non-empty), the one thing of kb's `Where` src reads (Task 2's rule 1). The module's docstring and CLAUDE.md's `init.py` row name the server case among the already-holds refusals.
- The Thens exist: `_rejected_already_holds` and `_nothing_changes`. `_nothing_changes` reads the journal straight from the store while it is served (a read, not refused) and checks no store was started where the user works.

**Decisions already made:**
- A server-found knowledge base holding the shop's types is refused as already holding the shop's knowledge (`spec/decisions.md` line 461; start-a-knowledge-base Behaviour line 47).
- The refusal names it by the server's address as `where()` gives it (`host:port`): a ruling under the person's delegation, logged 2026-10-07 in the slice plan for the person to confirm; the outline's Then says nothing of naming.
- With nothing named and a store found in place (upward), nothing changes from today: the inside and already-holds-a-knowledge-base refusals stay kb.init's (decision 461's second sentence).

**Steps:**
- [ ] Record the failing list; run `-m slice-55.1` and see the server row red on its undefined Given.
- [ ] Red-green the row.
- [ ] Run `-m slice-55.1` -> `3 passed`.
- [ ] Probe Review Focus 3.
- [ ] Checkpoint: `plan status 55.1 green`, `plan log`. Commit.

### Task 5: Slice 55.2, init furnishes a served empty store

Review: batch-end. Model: sonnet.

Scripts: `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (`@slice-55.2`, 1): start-a-knowledge-base / With no directory named, an empty store kb reaches through a server is furnished with the shop's types.

**Why red today:** its Given "the user is working where kb finds a connection to a server hosting a store kb's operator started empty" is undefined. Once it exists, init's List and Creates go wherever kb's client finds, so `src/` is expected not to change; only a run will say.

**Where it lands:**
- The Given, in `tests/start_furnished.py`: a store started empty through `_operator_started` (so `operated["root"]` is the served store), served through Task 3's fixture with the connection in the directory the user works in, KB_ROOT removed from `env`; it gives `start_in`.
- Reuse: the When `_start_where_found`; the Then `_holds_the_types_alone`, which lists and reads the journal straight from the operator's store with KB_ROOT naming it (reads, not refused while served). The Creates bootstrap makes go through the server and are stamped by the server's clock.
- If `src/` must change, it is `init.py`, and the hand-back rule applies only if a Given, When or Then would have to differ.

**Decisions already made:**
- A server-found empty knowledge base is furnished as one found in place (start-a-knowledge-base Behaviour line 41; `spec/decisions.md` line 406).

**Steps:**
- [ ] Record the failing list; run `-m slice-55.2` and see it red on its undefined Given.
- [ ] Red-green the scenario.
- [ ] Run `-m slice-55.2` -> `1 passed`.
- [ ] Probe Review Focus 4.
- [ ] Checkpoint: `plan status 55.2 green`, `plan log`. Commit.
