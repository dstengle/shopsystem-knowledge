# shop-knowledge batch 17: slices 68 to 73, shop links held once, capability dependencies and lifecycle

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, in slice order, with one change commit and one checkpoint commit per slice. Every task is a capability slice, built one scenario at a time under shopsystem-bdd:bdd-red-green.

**This plan carries no code** (adrs/0011).

**Goal:** each fact is held once, and the rest is inferred:
- a decision links to its shop, and a shop's decisions are the ones linking to it;
- a capability links to its shop and carries its dotted `order`, and `reading_order` goes.

A capability declares `depends_on` and has a lifecycle: `active`, `deprecated`, `retired`. Publishing:
- marks deprecated capabilities;
- leaves out retired ones;
- deletes the files it no longer writes;
- refuses inconsistent links.

`shop-knol dependencies <shop>` shows what a shop depends on that is deprecated or retired. Every approved scenario is green.

**Architecture:**
- Types stay data.
- Everything that today reads `shop.reading_order` or `shop.decisions` reads the links pointing at the shop instead: List filtered on the link field, or Follow inward. This covers the `spec` renderer modules and `coverage.py`.
- Deleting stale files is the command's work, not the renderer's (rule 6). It lives in a module of its own.
- `dependencies` is a new command whose reading lives in a module of its own, as `coverage` does (adrs/0057).

**Tech stack:** Python 3.11, pytest-bdd (<9), kb v0.6.0 through `kb.client.connect`, `kb.content`, `kb.contract.kb_pb2`.

**Spec:**
- Read whole: `spec/capabilities/` `use-the-shops-types.md`, `publish-a-shops-spec.md`, `see-what-is-formulated.md`, `see-what-a-shop-depends-on.md`, `follow-the-links.md` and `read-an-artifact.md`.
- `spec/index.md`.
- `spec/decisions.md` from `decision/a-decision-links-to-its-shop` on.
- The note `docs/superpowers/specs/2026-10-08-shop-links-and-capability-lifecycle-design.md`, for context only.
- adrs/0057 to 0063.
- Read CLAUDE.md first.

## Global Constraints

**Change control**
- Feature files are read-only, tag lines included.
- kb is v0.6.0 and never edited here. A change needed from kb is a `REQUEST kb:` line, and the slice stops.
- Every CLAUDE.md rule holds, the 250-line limit included. A new concern gets a new module and a module-map row in the same commit. `src/shop_knowledge/cli.py` is at 239 lines: a slice that would push it past 250 moves the concern it adds into a module of its own first.
- An existing scenario's Given, When and Then never change. Step data may change.
- A slice that cannot go green without changing what a scenario says hands back (`HAND-BACK`) and stops.

**Where to work**
- Work on `main` from the checkout's root. Scratch goes under `.superpowers/batch17/` only.
- Never export `GIT_*` variables.

**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Review and model:** `Review: per-task` with `Model: opus` for the published contract, data integrity, deleting files or what `init` furnishes. Otherwise `Review: batch-end` with `Model: sonnet`.

**Commits:**
- Use `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`, the message ending `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- One change commit per slice, then a checkpoint commit: the slice plan's log line, the suite record naming the change commit, and Status green.
- Never push.

**Counts:** the suite collected 212 rows at 57bf44c and gave `148 passed, 64 failed` in 15 s. see-what-a-shop-depends-on (4 rows) is collected once Task 4 binds it. Rows by tag: 68: 15 (the 5 glance rows pass today and must stay green); 69: 33; 70: 6; 71: 5; 72: 11; 73: 3.

| after | collected | failed | passed |
|---|---|---|---|
| 68 | 212 | 54 | 158 |
| 69 | 212 | 21 | 191 |
| 70 | 212 | 15 | 197 |
| 71 | 216 | 14 | 202 |
| 72 | 216 | 3 | 213 |
| 73 | 216 | 0 | 216 |

**Checks at each slice's end:**
- The failing list (`.venv/bin/python -m pytest -q -n auto -rf | grep ^FAILED | sort`): only the slice's rows leave it, and none join it.
- `wc -l src/shop_knowledge/*.py src/shop_knowledge/renderers/*.py tests/*.py tests/*/*.py | awk '$1 > 250 && $2 != "total"'` is empty.
- This is empty: `grep -rnE "^\s*(from kb[ .]|import kb\b)" src tests | grep -vE "kb\.client|kb\.content|kb\.contract|import kb$|from kb import (init|NotStarted)|kb\.testing"`.
- `jsonschema` is imported by `shape.py` alone.

## Review Focus

Probe each by hand once its slice is green, in `.superpowers/batch17/`, and record it in the checkpoint. A misbehaviour becomes a Backlog line with its reproduction. No scenario is written for any of them.
1. **Orders `3` and `3.0`, or `3` and `3.1`:** which sorts first, and whether `3` and `3.0` count as one order (Task 2; settled in Task 6's refusal by comparing the parts as numbers).
2. **A directory where a file's published-from line has been edited by hand** to name an artifact of another shop, or is malformed. Expected: it is deleted only if it carries a well-formed published-from line, and nothing outside the three directories is ever touched (Task 3).
3. **`dependencies` named a non-shop**, or a shop with no capabilities: one plain refusal, or an empty answer, never a traceback (Task 4).
4. **A capability depending on itself, or on a capability twice:** publishing and `dependencies` neither loop nor show it twice (Tasks 4 and 5).
5. **Retiring a capability that has a feature:** its feature is not published and its feature file is deleted on the next publish. The feature artifact itself stays in kb (Task 5, together with Task 3's deletion).

---

### Task 1: Slice 68, a decision links to its shop

**Review:** per-task
**Model:** opus
**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (tag `slice-68`, 15 rows):
- read-an-artifact, every scenario (its Background changed);
- follow-the-links: "The user sees what a decision points at" and "The user follows the links two steps out";
- use-the-shops-types: the glance outline (5 rows, green today).

**Why red:**
- read-an-artifact's Background now records "a decision of the shop "knowledge"", which no step defines.
- follow-the-links' Thens now expect the shop, and two steps out the product too, which the decision type has no link for.

**Where the change lands**
- `types/decision.yaml`: a required `shop` link (`ref`, one, to `shop`, `parts: false`), added to `summary` after `statement`, `date` and `supersedes`, as use-the-shops-types' table orders the glance fields.
- `types/shop.yaml`: `decisions` goes.
- `renderers/spec_decisions.py`: a shop's own decisions are found by List of kind `decision` filtered by `shop`. Task 1 of batch 16 probed that List filters on a link field. Any reading of `shop.decisions` goes.
- The other-shop part of the ledger (`_others`) goes, by the changed ledger line. A decision that `rests_on` names from another shop is now Task 6's refusal. Until then it is simply not listed.

**Needs (step data):**
- Every recorded decision gets a shop. Extend `tests/decision_fields.py` (the one home of a decision's required fields) so a scenario recording a decision first has a product and a shop in its own knowledge base, without new Givens.
- Keep search, check and refusal observables unchanged. A changed observable is a hand-back.
- tests/spec_shop.py: decisions link to the shop instead of being named by it.

**Decisions open, decided**
- A decision's shop is its own scenario's shop. Where a scenario records several decisions, they share one shop unless the scenario says otherwise.
- follow-the-links' two-steps Then compares a set of ids and routes, never an order (CLAUDE.md).

**Verify:**
- `-m slice-68` → 15 passed.
- The whole suite → `158 passed, 54 failed`.

---

### Task 2: Slice 69, capabilities link to their shop in order

**Review:** batch-end
**Model:** sonnet
**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (tag `slice-69`, 33 rows):
- publish-a-shops-spec: every scenario standing on its changed Background that the slice plan lists for 69;
- use-the-shops-types: `depends_on` recorded, a status not active, deprecated or retired refused, an order not dotted refused (3 rows).

**Why red:**
- publish-a-shops-spec's Background now gives capabilities that link to the shop, each with an order of its own, and decisions that link to the shop. No step defines it.
- The capability type has no `order`, `status` restriction or `depends_on`.

**Where the change lands**
- `types/capability.yaml`:
  - `order` (required): a string with the pattern of one or more whole numbers joined by dots, written so a trailing line break is refused as in batch 16.
  - `status` (required) restricted to `active`, `deprecated` or `retired`. The base's free `status` stays for the other types.
  - `depends_on` (optional): many links to `capability`.
- `types/shop.yaml`: `reading_order` goes.
- `renderers/spec.py` and the page modules, and `coverage.py`:
  - a shop's capabilities are found by List of kind `capability` filtered by `shop`;
  - in this slice every one is published, whatever its status; Task 5 adds the status rules;
  - they are sorted by `order`, its parts compared as whole numbers.
  - The sort lives in one place, a function in `renderers/names.py` or a module of its own, and both readers use it.
- The capability page's frontmatter shows `depends_on` after `rests_on`, where the capability has it.
- `spec_faults.py`: the reading-order checks go (their lines were removed).
- `tests/spec_shop.py`: builds capabilities with `shop`, `order`, `status: active`, and no reading order.

**Decisions open, decided**
- The index's Composition counts 1, 2, 3 (integration answer, round 2).

**Verify:**
- `-m slice-69` → 33 passed.
- The whole suite → `191 passed, 21 failed`.

---

### Task 3: Slice 70, publishing deletes the files it no longer writes

**Review:** per-task
**Model:** opus
**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (tag `slice-70`, 6 rows, two outlines over `spec/capabilities/`, `features/` and `adrs/`).

**Why red:** nothing deletes, and the steps are undefined.

**Where the change lands**
- A new module, for example `src/shop_knowledge/published.py`, with a module-map row. It owns the files a publish leaves in the directory, and gives back what to delete:
  - the files directly under `spec/capabilities/`, `features/` and `adrs/` of the directory asked for;
  - only those carrying a well-formed published-from line;
  - only those not among the files this render writes.
- It recognises the line with the same format `renderers/published_from.py` writes. Reuse its knowledge: one module owns the line's wording, and the other asks it whether a line is one.
- `cli._render` deletes those files only when the renderer refused nothing (rule 6, adrs/0053's "nothing written or deleted"), after writing.
- Keep `cli.py` under 250 lines, by moving `_write` beside the deletion if needed.

**Decisions open, decided**
- Only regular files directly in the three directories are considered. Subdirectories, and files elsewhere in the directory, are never touched.
- A file that cannot be read as UTF-8 text is not a published file, and it is left.
- A refused publish deletes nothing. The five existing refusals already pin that with a stale `adrs/0099-old-rule.md`.

**Verify:**
- `-m slice-70` → 6 passed.
- The whole suite → `197 passed, 15 failed`.

---

### Task 4: Slice 71, see what a shop depends on

**Review:** batch-end
**Model:** sonnet
**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (tag `slice-71`, 5 rows): see-what-a-shop-depends-on (4), and follow-the-links' "The user follows the links into a capability".

**Why red:** no test module binds see-what-a-shop-depends-on, there is no `dependencies` command, and follow-the-links' new steps are undefined.

**Where the change lands**
- `arguments.py`: a `dependencies` command taking one shop name, which may not be given empty.
- `cli.py`: its handler, kept under 250 lines.
- A new module, `src/shop_knowledge/dependencies.py`, with a module-map row and named beside `coverage.py` in rule 5 and in "Size and shape" (adrs/0057's reasoning applies; no new ADR is needed). It reads:
  - the shop, refusing as coverage does;
  - its capabilities, found as Task 2 finds them, active or deprecated;
  - for each `depends_on`, the target's status and its shop;
  - the scenarios of the depending capability's feature whose `uses` name the target.
- It answers a list with one entry per pair of a depending capability and a deprecated or retired dependency. Each entry gives the capability, the dependency, the dependency's shop and status, and the scenarios. An empty list is an empty value.
- follow-the-links "into a capability" uses today's `refs --inbound`. No new code is expected; the steps build a capability with dependents in two shops.

**Decisions open, decided**
- One entry per (capability, dependency) pair (the formulator's open case; spec silent; the plain answer).
- A capability named twice in `depends_on`, or depending on itself, is shown once per distinct dependency.

**Verify:**
- `-m slice-71` → 5 passed.
- The whole suite → `202 passed, 14 failed`.

---

### Task 5: Slice 72, deprecated and retired capabilities

**Review:** batch-end
**Model:** sonnet
**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (tag `slice-72`, 11 rows):
- publish-a-shops-spec: a deprecated capability; a retired capability; the refusal for a published capability depending on a retired one (all rows);
- use-the-shops-types: retiring a capability others depend on (all rows);
- see-what-is-formulated: a retired capability's lines.

**Why red:** publishing and coverage ignore status, and the steps are undefined.

**Where the change lands**
- The capability-finding function from Task 2 takes only `active` and `deprecated` capabilities, for publishing and coverage alike.
- Capability pages: `status: deprecated` in the frontmatter only when deprecated. The index's Composition line ends ` (deprecated)`.
- A retired capability's feature is not published. Task 3's deletion then removes its earlier files.
- `spec_faults.py`: a published capability whose `depends_on` names a retired capability, in any shop, read whole for its status, is refused naming both.
- Retiring needs no code: kb accepts the status change. The scenario pins that nothing refuses it.

**Verify:**
- `-m slice-72` → 11 passed.
- The whole suite → `213 passed, 3 failed`.

---

### Task 6: Slice 73, publishing refuses a capability's inconsistent links

**Review:** batch-end
**Model:** sonnet
**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Scenarios** (tag `slice-73`, 3 rows): two capabilities with one order; a capability resting on another shop's decision; a scenario's `uses` not among its capability's `depends_on`.

**Why red:** the checks do not exist, and the steps are undefined.

**Where the change lands:** `spec_faults.py`, beside the existing checks, each a plain-words fault naming what is at fault:
- orders compared part by part as whole numbers, so `3` and `3.0` are one order;
- a `rests_on` decision whose `shop` is not this shop;
- a scenario's `uses` not in its capability's `depends_on`.

If `spec_faults.py` would pass 250 lines, split it by concern first, with a module-map row.

**Verify:**
- `-m slice-73` → 3 passed.
- The whole suite → `216 passed, 0 failed`.
