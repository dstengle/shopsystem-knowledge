# shop-knowledge batch 18: slices 74 to 76, tested in, an unreadable file, the uses check

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, in slice order, with one change commit and one checkpoint commit per slice, built one scenario at a time under shopsystem-bdd:bdd-red-green.

**This plan carries no code** (adrs/0011).

**Goal:**
- A shop's constraint names the capabilities it is `tested_in` (published "Tested in"), and a constraint tested in a retired capability stops the publish.
- A file publishing may delete but cannot read stops the publish.
- `shop-knol validate` also lists every scenario whose `uses` is not among its capability's `depends_on`, in any shop.

**Spec:**
- `spec/capabilities/publish-a-shops-spec.md`, `check-the-knowledge-base.md` and `use-the-shops-types.md`, read whole.
- `spec/index.md`.
- `spec/decisions.md` from `decision/uses-is-kept-and-checked-for-consistency` on.
- adrs/0064 to 0068.
- Read CLAUDE.md first.

## Global Constraints

The binding constraints of batch 17 hold unchanged:
- Feature files are read-only.
- kb is v0.6.0.
- CLAUDE.md's rules hold, with 250 lines a module. `cli.py` is at 236 lines.
- Given/When/Then never change. A hand-back stops the slice.
- Scratch goes in `.superpowers/batch18/`.
- Commits use the author and trailer of batch 17, as a change commit and then a checkpoint commit with the suite record naming the change commit.
- Never push.

**Scripts:** `/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.10.0/scripts/`

**Review and model:** all three are `Review: batch-end`, `Model: sonnet`.

**Counts:** the suite collected 223 rows at 2d05fb1 and gave `216 passed, 7 failed` in 33 s. By tag: 74: 2, 75: 3, 76: 2.

| after | failed | passed |
|---|---|---|
| 74 | 5 | 218 |
| 75 | 2 | 221 |
| 76 | 0 | 223 |

**Checks:** the four checks of batch 17's plan:
- the failing list: only the slice's rows leave it;
- no module over 250 lines;
- the kb-import grep;
- jsonschema imported by `shape.py` alone.

## Review Focus

Probe by hand and record in the checkpoint; a misbehaviour becomes a Backlog line.
1. A constraint tested in a deprecated capability: published as today, with no refusal (Task 1).
2. Several unreadable files: each named, or the first only. Record which; no line says (Task 2).
3. `validate` on a knowledge base whose kb Check finds nothing and whose `uses` check finds one fault: `sound` is false, the fault is listed, and the exit is 1 (Task 3).

---

### Task 1: Slice 74, a constraint is tested in capabilities

**Review:** batch-end · **Model:** sonnet · **Scripts:** as above.

**Scenario** (tag `slice-74`, 2 rows): the refusal for a constraint tested in a retired capability, in the shop itself or in another shop.

**Why red:** its steps are undefined, and no check exists.

**Where the change lands:**
- `types/shop.yaml`: the constraints part's `pinned_in` becomes `tested_in`, with the same link shape.
- `renderers/spec.py` and `renderers/spec_index.py`: read `tested_in`. The published phrase becomes `Tested in <names>.`
- `renderers/spec_faults.py`: a constraint whose `tested_in` names a retired capability, read whole for its status in any shop, is refused, naming the constraint (by its title) and the capability.
- Tests:
  - `tests/spec_shop.py` and `tests/publish_spec_index.py` use `tested_in` and the new phrase. This is step data; the index scenario's words are unchanged.
- CLAUDE.md: the `spec_faults.py` row names the new check.
- Fold in this backlog line, since the row is being edited: the `spec_faults.py` row should also name the ragged-table check, and the `published.py` row should say a linked cleared directory has nothing deleted (from batch 17's fix-wave re-review).

**Verify:**
- `-m slice-74` → 2 passed.
- The whole suite → `218 passed, 5 failed`.

---

### Task 2: Slice 75, a file publishing cannot read stops the publish

**Review:** batch-end · **Model:** sonnet · **Scripts:** as above.

**Scenario** (tag `slice-75`, 3 rows, one each for `spec/capabilities/`, `features/` and `adrs/`).

**Why red:** its steps are undefined. The behaviour exists today (`published.py`), so expect the rows to go green on steps alone. Show red by making unreadable files count as not published, then revert.

**Where the change lands:**
- The step module for publishing refusals, making a file unreadable with file permissions in the scenario's own temporary directory.
- The Then compares the fault's naming of the file, and that the directory is unchanged.
- No `src/` change is expected. If the fault does not name the file, give `published.py`'s OS-error path a plain-words fault naming it, without passing 250 lines.

**Decisions open, decided:** a test that removes read permission restores it in its own teardown, so the temporary directory can be cleaned.

**Verify:**
- `-m slice-75` → 3 passed.
- The whole suite → `221 passed, 2 failed`.

---

### Task 3: Slice 76, the check finds a scenario using what its capability does not depend on

**Review:** batch-end · **Model:** sonnet · **Scripts:** as above.

**Scenario** (tag `slice-76`, 2 rows: the scenario in the shop, or in the other shop).

**Why red:** `validate` makes kb's Check only, and the steps are undefined.

**Where the change lands:**
- A new module, for example `src/shop_knowledge/consistency.py`, with a module-map row, named beside `coverage.py` and `dependencies.py` in rule 5 and in "Size and shape". It reads every feature through List of kind `feature` and reads each whole, with its capability's `depends_on`. It gives a `kb_pb2.Fault` for each scenario whose `uses` names a capability outside its capability's `depends_on`:
  - `artifact`: the feature;
  - `place`: `scenarios/<item>`;
  - `rule`: `uses-not-depended-on`;
  - message: in plain words, naming the capability used.
- `cli._validate`: after kb's Check has run (a refusal is still refused first, as today), add these faults to the violations. `sound` is false when either kind is found, and the exit refuses all of them together. What is behind its type is still shown beside them.
- `answers.checked` may take the added faults as an argument. It stays shaping only.
- `spec_faults.py`'s publishing check for the same rule should use the same function, so the rule lives in one place.

**Verify:**
- `-m slice-76` → 2 passed.
- The whole suite → `223 passed, 0 failed`.
