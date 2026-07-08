---
name: work-done-gate
description: Pre-emission gate that must pass before any work_done --status complete is sent; converts to --status blocked with named evidence on any failure
---

# Work-Done Gate

## Overview

Before any `work_done --status complete` emission, run this gate. Three checks must all pass. Any single failure converts the emission to `work_done --status blocked` with named evidence — no exceptions, no partial passes.

This gate is the enforcement point for ADR-010 and the integration contract. It is not optional.

## The Three Pre-Emit Checks

### Check 1: Clean Working Tree (deliverable-scope)

```bash
git status --porcelain -uall
```

Check 1 is **deliverable-scoped**. The **deliverable directories** are `features/`, `src/`, and `tests/` — where a dispatch's work product lands. Check 1 inspects only whether a **deliverable** path is dirty; churn confined to **non-deliverable** paths never blocks an emit. This is a single coherent model — there is no separate parallel carve-out mechanism.

**Pass:** no entry names a modified, staged, untracked, or deleted path under any deliverable directory (`features/`, `src/`, `tests/`). The tree MAY carry dirty **non-deliverable** paths and still pass. Non-deliverable paths are:
- **Harness / configuration** paths — e.g. `.claude/settings.json`, `.claude/canonical/bc-primer.md`.
- **Ambient carve-outs** (named process artifacts) — `.beads/issues.jsonl`, `.specstory` (and anything under it), `.claude/scheduled_tasks.lock`. These are a **subset** of the non-deliverable paths: exactly the list the executable `bc-emit work-done` wrapper discounts (`_CARVE_OUTS`), so a tree whose only changes are these is clean under both the prose and the wrapper.

**Fail:** any entry naming a path under a deliverable directory (`features/`, `src/`, `tests/`).

> **Why deliverable-scope (one model that subsumes the carve-out list):** deliverable-scope generalizes — and subsumes — the ambient carve-out exemption. The carve-outs are non-deliverable paths, so they are already clean under deliverable-scope; do not implement a second carve-out check beside it. In particular, **Check 4** below closes the work_id plan bead, writing the non-deliverable `.beads/issues.jsonl` — which therefore never blocks, dissolving the Check-1/Check-4 deadlock. The wrapper's `_CARVE_OUTS` enforcement is a (narrower) instance of this same rule.

Evidence on failure: show the `git status --porcelain -uall` output restricted to the dirty **deliverable** paths. Name each one verbatim. Block with message:
```
blocked: dirty deliverable path(s) at emission time. Paths: <dirty paths under features/ src/ tests/ from git status --porcelain -uall>
```

A dirty deliverable path at `work_done` time means uncommitted work product. The BC must commit or discard those changes before emitting. Changes confined to non-deliverable harness/config or ambient carve-out paths do not block.

### Check 2: work_id Commit Reachable from `origin/main`

```bash
git fetch origin
git log origin/main -E --grep="\b<work_id>\b" --oneline
```

**Pass:** the search finds the work_id as a WHOLE TOKEN in at least one commit on `origin/main`.

**Fail:** no match.

Evidence on failure: show the current `origin/main` HEAD SHA and the work_id searched for. Block with message:
```
blocked: work_id <work_id> not reachable from origin/main (HEAD: <sha>). Run integrating-to-main.
```

**Why `git fetch origin` first:** the local ref `origin/main` may be stale. Fetching before the check ensures the gate sees the actual remote state. Skipping the fetch is a false pass.

The attribution mechanism: the work_id must appear as a WHOLE TOKEN (exact / word-boundary match — bounded by start/end-of-line or non-identifier characters) in the commit subject or body, NOT as a loose substring. A work_id that is a strict PREFIX of another commit's work_id (e.g. `lead-8v` as a prefix of `lead-8vwf`) therefore does NOT match — loose substring matching false-positive-attributes the wrong commit's lineage. Tags and `git notes` naming exactly the work_id are also acceptable, but the word-boundary `git log -E --grep="\b<work_id>\b"` form is the canonical check (it is the same canonical attribution form the executable `bc-emit work-done` wrapper applies in both its commit-mode and tag-mode reachability checks).

**Idempotent no-op branch (flat maintenance only).** When the dispatch vehicle is **flat maintenance** whose intended end-state **already holds** in the BC repository — a verifiably-correct convergence that requires no change and so produces no new commit naming the work_id — Check 2 passes via this **idempotent-no-op branch** even though `git fetch origin` followed by `git log origin/main -E --grep="\b<work_id>\b"` finds no commit: none was needed. This branch applies ONLY when **both** (a) the vehicle is flat maintenance and (b) the intended end-state already holds with **zero delta**. When a delta IS needed (the end-state does not already hold), the idempotent-no-op branch does NOT apply and Check 2 still requires a work_id commit reachable from `origin/main`, failing to `--status blocked` when none exists. A scenario-bearing or non-flat-maintenance dispatch never takes this branch.

### Check 3: Scenario Hash Integrity (ADR-010)

ADR-010 rule: `work_done.scenario_hashes` must be a **subset** of the `@scenario_hash:` tags actually pinned in the BC's `features/`.

Three sub-steps:

**3a. Recompute hashes.**
```bash
scenarios hash features/<scenario_file>.feature
```
Recompute the canonical hash for each scenario you intend to include in `work_done`. Do not trust hashes from memory or prior conversation turns.

**3b. Confirm presence via git grep.**
```bash
git grep "@scenario_hash:<hash>" features/
```
Each hash you intend to report must appear in the committed `features/` tree. If a hash is not present in `features/`, it was never pinned — you cannot claim it.

**3c. Enforce subset rule.**
The set of hashes you pass (one repeatable `--scenario-hash <hash>` flag per hash) must be a strict subset of the hashes found in `features/`. You may report fewer than all pinned hashes (partial delivery is valid); you must not report a hash not in `features/`.

**Pass:** all three sub-steps pass for every hash in the intended `work_done` payload.

**Fail:** any hash not found via `git grep`, or any hash whose recomputed value does not match.

Evidence on failure: name the mismatched or missing hash, the path searched, and the `origin/main` short SHA. Block with message:
```
blocked: scenario_hash <hash> not found in features/ (searched: features/; origin/main: <sha>). Scenario may not be pinned.
```

### Check 4: BD Plan Sub-Issues Present, Closed, and Durable

Verify that bd sub-issues exist for the work_id and that **every** sub-issue
reachable under the work_id umbrella bead is closed. At least one sub-issue
must be an explicit failing-test (RED) sub-issue (title contains "write the
failing test for" or similar RED nomenclature).

```bash
bd children <umbrella> --json   # enumerate EVERY sub-issue: status + title
bd dolt push                    # durability: closures reachable on the remote
```

**Enumerate EVERY reachable sub-issue, not the self-reported set.** The
precondition is evaluated by independently enumerating every sub-issue
reachable under the work_id umbrella bead from the BC's own bd registry — NOT
only the set the implementer reports or itself closed. An **orphaned OPEN
sub-issue** left behind by an abandoned earlier decomposition that the
implementer never created or closed therefore **still blocks** the emit. The
prior "at least one RED exists and all sub-issues the implementer closed are
closed" check alone does NOT pass the gate; an OPEN sub-issue the implementer
did not create still blocks it (scenario 0b48508e40fdde18).

**Durability — the decomposition-and-closure state must be reachable from the
pushed tracker remote.** bd is dolt-backed and `.beads/issues.jsonl` is a
carved-out **non-idempotent ambient artifact** under Check 1 (its working-tree
bytes cannot be made clean by a commit), so a clean working tree cannot by
itself establish that the sub-issue creations and closures are durable. The
durability precondition is satisfied by the decomposition-and-closure state
being reachable from the **pushed tracker remote** — the configured bd-dolt
remote — verified by a successful `bd dolt push` (the same unpushable-tracker
signal the session-start work-tracker health step uses). A non-durable
decomposition is named **specifically** as a bd-decomposition-durability
failure, NOT as a generic dirty-working-tree cause (scenario 7bcfc89161c0b2ee).

**Pass:** at least one RED sub-issue exists, every sub-issue reachable under
the work_id umbrella bead is closed, and the decomposition-and-closure state is
reachable from the pushed tracker remote.

**Fail:** no sub-issues exist for the work_id; any sub-issue reachable under
the umbrella (including an orphan the implementer never closed) is OPEN; no RED
(failing-test) sub-issue is present; or the decomposition-and-closure state is
not reachable from the pushed tracker remote.

Evidence on failure: list the open sub-issues by bd id (including orphans) and
note the missing RED sub-issue, or name the bd-decomposition-durability
precondition and the work_id. Block with message:
```
blocked: no bd plan sub-issues for <work_id>
```
or:
```
blocked: bd sub-issue(s) not closed for <work_id>: <list, incl. orphaned OPEN ids>
```
or:
```
blocked: bd decomposition+closures for <work_id> not reachable from the pushed tracker remote (configured bd-dolt remote)
```

> The executable `bc-emit work-done` wrapper enforces this check when invoked
> with `--plan-umbrella <umbrella>`: it runs `bd children <umbrella>` to
> enumerate every reachable sub-issue (catching orphans) and a `bd dolt push`
> reachability probe for durability — both against the BC's own bd registry.

### Check 5: Test-First Artifact in Work-Branch History

For each behavior, verify that a `test(red): <behavior>` commit precedes its
`feat(green): <behavior>` commit in the work-branch history:

```bash
git log --oneline bc/<work_id>   # inspect commit sequence
```

For each behavior, locate the `test(red)` commit and the `feat(green)` commit.
The `test(red)` commit must appear **earlier** in the log (i.e., was authored
before the `feat(green)` commit).

**Genuine red (not merely red-before-green).** Commit *order* alone is not
sufficient: the newly-added tests introduced by a `test(red)` commit must
**demonstrably FAIL** when run against the tree **at that `test(red)`
commit**. Check out (or worktree) the `test(red)` commit and run exactly the
tests that commit added; they must fail there. A `test(red)` commit whose
newly-added tests already PASS at the red commit is a **tautological red** —
the order holds but the test never demonstrated the absence of the behavior,
so it provides no test-first evidence.

```bash
git checkout <test(red)-sha> --   # or a throwaway worktree
# run ONLY the tests that commit newly added; they MUST fail here
```

**Pass:** for every behavior with a `feat(green)` commit, a `test(red)` commit
for the same behavior appears before it in the branch history, AND that
`test(red)` commit's newly-added tests demonstrably fail at the `test(red)`
commit.

**Fail:** any `feat(green)` commit has no corresponding `test(red)` commit; or
the `test(red)` commit appears after `feat(green)`; or the `test(red)`
commit's newly-added tests PASS at the red commit (a tautological red) even
though the red-before-green order holds.

Evidence on failure: name the behavior, the `feat(green)` commit SHA, and
either the missing/mis-ordered `test(red)` commit or — for a tautological
red — the `test(red)` commit whose newly-added tests passed at that commit.
Block with message:
```
blocked: no test-first commit sequence for <behavior>
```
or, for a tautological red:
```
blocked: tautological red for <behavior>: test(red) <sha> newly-added tests pass at the red commit
```

## Gate Summary Table

| Check | Command | Pass condition | Fail → blocked evidence |
|---|---|---|---|
| Clean working tree (deliverable-scope) | `git status --porcelain -uall` | no dirty path under deliverable dirs `features/`/`src/`/`tests/` (non-deliverable harness/config + ambient carve-outs `.beads/issues.jsonl`, `.specstory`, `.claude/scheduled_tasks.lock` don't block) | dirty deliverable paths list |
| work_id reachable | `git fetch origin && git log origin/main -E --grep="\b<work_id>\b" --oneline` | whole-token match, OR idempotent no-op for flat maintenance whose end-state already holds (no delta) | work_id + origin/main HEAD SHA |
| Scenario hash subset | `scenarios hash` + `git grep` | all hashes in features/ | mismatched hash + path + SHA |
| BD plan sub-issues | `bd show <work_id>` | sub-issue(s) exist, all closed, ≥1 RED | "no bd plan sub-issues for <work_id>" |
| Test-first artifact (genuine red) | `git log --oneline bc/<work_id>` + run red tests at the red commit | test(red) precedes feat(green) AND the red commit's newly-added tests fail at the red commit | "no test-first commit sequence" / "tautological red" for `<behavior>` |

## On Pass — Emit the Sign-Off via the `bc-emit work-done` Wrapper

When all checks pass, emit the routine `work_done --status complete` sign-off
through the **`bc-emit work-done`** wrapper — that is the concrete command for
the routine sign-off emit, NOT the bare `shop-msg respond work_done`
primitive. The wrapper re-runs these same preconditions (clean working tree,
work_id reachable from `origin/main`, and the block-only scenario-hash match —
including the orphan/stale/missing refusal) at emission time, so a
bare-primitive sign-off that skips the gate cannot slip a stale or orphaned
hash through:

```bash
bc-emit work-done \
  --bc <name> \
  --work-id <work_id> \
  --scenario-hash <h1> [--scenario-hash <h2> ...] \
  --summary "<probes considered + dismissed>"
```

The bare `shop-msg respond work_done --force` path is the forced-recovery
escape valve ONLY — never the routine sign-off emit. If `bc-emit work-done`
refuses, fix the named underlying state and retry rather than reaching for
`--force`.

## Failure Converts Complete to Blocked

When any check fails, do not emit `work_done --status complete`. Emit:

```bash
shop-msg respond work_done \
  --bc <name> \
  --work-id <work_id> \
  --status blocked \
  --summary "<named evidence from the failing check>"
```

Named evidence means: specific paths, the work_id value, the `origin/main` short SHA, and the specific check that failed. Vague evidence ("something went wrong") is not acceptable.

## After Resolving a Block

Fix the underlying cause (clean tree → commit or discard; unreachable commit → run `integrating-to-main`; hash mismatch → pin or correct the scenario), then re-run the full gate from Check 1. Do not skip checks that previously passed — run all three again.
