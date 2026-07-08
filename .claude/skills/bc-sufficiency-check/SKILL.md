---
name: bc-sufficiency-check
description: Determines whether an inbound lead message is sufficient to act on, or whether a clarify response is required before dispatch
---

# BC Sufficiency Check

## Overview

Before any dispatch, the router runs this check. Its job is a binary verdict: **proceed** or **clarify**. The check is per-message-type; each type has its own criteria.

The check has two failure modes to guard against:

- **Under-asking** — rationalizing "I can figure it out" or "asking would be theatre" when a genuine gap exists. These are hallmarks of an insufficient message. Ask.
- **Over-asking** — rationalizing "better safe than sorry" or "clarify just in case" when the message actually passes every criterion. If the check passes, proceed. Unnecessary clarification wastes lead cycles and is its own failure mode.

## Per-Type Sufficiency Criteria

### `request_maintenance`

Proceed if ALL of:

1. **Acceptance criteria present.** The message contains at least one explicit acceptance criterion — not just a description of a problem.
2. **Criteria are measurable.** Each criterion names a concrete, observable outcome (pass/fail, value, count, error message). Vague criteria like "should be better" or "more robust" fail this gate.
3. **Criteria define the OUTCOME, not just constraints.** A constraint ("must not break existing tests") is not an acceptance criterion; an outcome ("the widget count endpoint returns 200 within 500ms") is.
4. **Description specifies what "the thing" is.** The description names: what is being maintained, its inputs (if any), and its expected outputs/effects. Unnamed or ambiguous subjects fail this gate.

### `assign_scenarios`

Proceed if ALL of:

1. **Well-formed Gherkin.** Each scenario uses Given/When/Then structure. Scenarios missing any leg are malformed.
2. **Steps are concrete enough to test.** Each step describes an observable action or assertion. Vague steps like "and the system behaves correctly" fail this gate.
3. **`@scenario_hash:` tag present on each scenario.** The hash is the lead's commitment; without it the BC cannot satisfy ADR-010 (work_done scenario_hashes must be a subset of pinned hashes). Missing tag → clarify.
4. **"Fits existing capability" probe.** Check whether the BC is already implementing this behavior in unpinned form (search `features/` and `src/`). If yes, the message may be assigning a scenario to pin something already present — that is valid and should proceed. Flag as a mechanism observation, not a clarify.

### `request_bugfix`

Two sub-cases:

**With non-empty scenarios:** Apply the full `assign_scenarios` check to each scenario. If any scenario fails, clarify before dispatch.

**With empty scenarios (no Gherkin attached):**
1. **Concrete description.** The description must name the behavior under change specifically — what currently happens versus what should happen.
2. **Subject identified.** The bug report names the component, endpoint, function, or interaction that is misbehaving. "Something is broken somewhere" fails this gate.

## Decision Table

| Check | Passes | Fails |
|---|---|---|
| Acceptance criteria present | proceed | clarify: name which criterion is missing |
| Criteria measurable | proceed | clarify: name the vague criterion |
| `@scenario_hash:` tag present | proceed | clarify: name the missing tag and which scenario |
| Well-formed Gherkin Given/When/Then | proceed | clarify: name the malformed step |
| Concrete step descriptions | proceed | clarify: quote the vague step |
| Bug description is concrete | proceed | clarify: ask for current-vs-expected behavior |

## Anti-Rationalization

**Under-asking guards** — these thoughts mean you MUST clarify:
- "I can infer what they mean from context." → Inference is not specification. Ask.
- "Asking would be theatre — it's obvious." → If it's obvious, write it in the clarify as the proposed interpretation and ask the lead to confirm. That is not theatre.
- "The acceptance criteria are implied by the scenario steps." → Implied criteria cannot be verified. Ask for explicit ones.

**Over-asking guards** — these thoughts mean you MUST proceed:
- "Better safe than sorry — I'll clarify just in case." → If the check passes, proceed. Unnecessary clarification is a failure mode.
- "I want to make sure I understand the full intent." → Intent beyond the criteria is implementation detail. Proceed and emit a mechanism observation if needed.
- "I'd like confirmation before touching anything." → You have the specification. Proceed.

## Clarify Format

When the check fails, emit exactly one `clarify` response naming:
1. The specific criterion that failed.
2. What the message contains versus what is required.
3. (Optional) A proposed interpretation for the lead to confirm, if that would accelerate resolution.

Do not bundle multiple clarifications into a single message — name the blocking gap and stop.
