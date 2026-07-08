---
name: bc-review
description: Adversarial review gate for scenario-based BC work; sole emitter of work_done for assign_scenarios and bugfix-with-scenarios dispatches
---

# BC Review

## Overview

The reviewer is dispatched after the implementer's turn on any `assign_scenarios` or `request_bugfix` (with scenarios) message. The reviewer is the **sole role authorized to emit `work_done`** for scenario-based work.

The reviewer's posture is adversarial — not hostile, but genuinely probing. The goal is to catch gaps the implementer missed before the lead sees the output.

## What You Read

Before starting any probe:

1. **The assigned Gherkin scenario(s)** — read from `features/` as committed, including all `@scenario_hash:` tags.
2. **The implementer's work** — `git diff origin/main..HEAD` in the work branch (or the merged commit on `main`).
3. **The step definitions** — `tests/conftest.py` or equivalent.
4. **The implementation** — the relevant `src/` files.

Do not rely on the implementer's summary. Read the artifacts directly.

## BDD Re-Run

Run the assigned scenario(s) yourself against a clean tree:

```bash
git status --porcelain   # must be clean before running
pytest features/ --tags="@scenario_hash:<hash>"   # or your BC's runner
```

If any assigned scenario fails: the work is not done. Do not sign off. This is an implementation gap (see Outcomes).

## Adversarial Probes

### Faithful Realization vs. Literal-Text Shortcut

Check whether the implementation faithfully realizes the behavior named in the scenario, or whether it literally satisfies the step text via a shortcut that would not generalize.

Examples of shortcuts to detect:
- Hardcoded return values matching exactly the scenario's expected output.
- Guard clauses that match only the scenario's specific input, passing nothing else through.
- Assertions in step definitions that match the scenario's exact strings without validating the underlying behavior.

If a shortcut is found: implementation gap.

### Unpinned Adjacent Cases

The scenario pins one path through the behavior. Probe the adjacent paths:
- **Equality boundaries.** If the scenario uses a threshold (e.g., count ≥ 3), test count = 2 and count = 3 explicitly.
- **Reverse cases.** If the scenario tests the happy path, verify the error path is also handled (even if not assigned).
- **Negatives.** If the scenario tests that X happens, verify that X does not happen when the condition is absent.

These are not new scenarios to assign — they are probe tests you run as part of review. If they fail and reveal that the implementation only works for the assigned case, that is an implementation gap.

### Step Definition Failure Modes

Inspect the step definitions for:
- **Overly broad regexes.** A step that matches too broadly may silently pass irrelevant inputs.
- **Silent exception swallowing.** A step that catches exceptions without asserting may hide failures.
- **State leakage between steps.** Shared mutable state in fixtures that is not reset between scenarios.

## Outcomes

Three possible outcomes:

### Sign-off (work_done complete)

All assigned scenarios pass. Adversarial probes reveal no shortcuts or uncovered adjacent cases. Step definitions are sound.

```bash
shop-msg respond work_done \
  --bc <name> \
  --work-id <work_id> \
  --status complete \
  --scenario-hash <hash1> [--scenario-hash <hash2> ...]
```

### Scenario Gap → Clarify to Lead

The reviewer discovers that the assigned scenarios do not fully specify the required behavior — there is a gap in the specification itself that no amount of implementation work can resolve. This is not the implementer's failure; it is a gap in what was assigned.

```bash
shop-msg respond clarify \
  --bc <name> \
  --work-id <work_id> \
  --question "Scenario gap: <description of what the scenario does not specify>"
```

Do not emit `work_done` in this case. The lead must revise the scenario(s) first.

### Implementation Gap → work_done blocked

The scenarios are sufficient but the implementation does not faithfully realize them — shortcuts, failing adjacent cases, or step definition failures.

```bash
shop-msg respond work_done \
  --bc <name> \
  --work-id <work_id> \
  --status blocked \
  --summary "Implementation gap: <specific finding>"
```

Name the specific gap: quote the shortcut, name the failing adjacent case, or describe the step definition flaw. The implementer uses this as the input for a new implementation pass.

## Observable-Artifact Checks (Checks 4–5)

Before running the adversarial probes, the reviewer must run Checks 4 and 5
from the `work-done-gate` skill (invoked via the Skill tool):

**Check 4 (plan artifact):** bd sub-issues exist for the work_id and are
closed, and at least one is an explicit failing-test (RED) sub-issue (title
contains "write the failing test for" or similar). This confirms the
implementer ran TDD planning, not ad-hoc coding.

```bash
bd show <work_id>   # all sub-issues must be closed; ≥1 RED sub-issue required
```

Absent → convert to `work_done --status blocked --summary "no bd plan sub-issues for <work_id>"`.

**Check 5 (test-first artifact):** for each behavior, a `test(red):
<behavior>` commit precedes its `feat(green): <behavior>` commit in the
work-branch history.

```bash
git log --oneline bc/<work_id>   # test(red) must precede feat(green) per behavior
```

Absent or mis-ordered → convert to `work_done --status blocked --summary
"no test-first commit sequence for <behavior>"`.

The `work-done-gate` skill runs Checks 4 and 5 as part of its full gate sweep.
The reviewer invokes `work-done-gate` after completing the adversarial probes
(see FIRST ACTION in the reviewer shim).

## Anti-Rationalization

| Thought | Reality |
|---|---|
| "The scenarios pass — that's enough." | Passing assigned scenarios is necessary but not sufficient. Run the adversarial probes. |
| "The implementer is experienced — trust it." | Trust but verify. Read the diff. |
| "Adjacent cases weren't assigned — not my problem." | Adjacent cases reveal whether the implementation is real. Probing them is the review. |
| "I don't want to slow things down." | A blocked `work_done` now is faster than a production bug later. |
| "The commits look fine from here." | Verify Check 5 via git log — don't assume the test-first sequence is there. |
