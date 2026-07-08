---
name: po-architect-decomposition-exchange
description: Situational mechanics for the turn-limited PO<->Architect BC-decomposition collaboration. Load this when you are actively running a decomposition exchange with the PO (or, as the PO, with the Architect) and need the round cap, the extension protocol, and the ship-from-here rule. Per PDR-014.
---

# PO ↔ Architect decomposition exchange (turn-limited)

## When to load this skill

Load this skill only while you are *inside* an active BC-decomposition
collaboration — the bounded back-and-forth in which the PO and the Architect
converge on a Domain & Context Map and the set of BCs the product decomposes
into. Outside that exchange these mechanics are not live; the durable posture
("decomposition is bounded and you ship from the current map once the limit is
reached") stays in the role template, but the round-counting mechanics below
do not need to be ambient. This separation is PDR-014: situational guidance is
loaded on demand, not carried as ambient template prose.

## Why the exchange is turn-limited

Decomposition can re-litigate itself forever — every map suggests a slightly
better map. The turn limit exists to force termination: it guarantees the
collaboration converges on a shippable Domain & Context Map instead of
spiralling into indefinite re-decomposition. The limit is a feature, not a
constraint to work around.

## The mechanics

1. **Default round cap: 3 rounds.** The exchange runs a hard cap of **3
   rounds by default**. A "round" is one PO proposal plus the Architect's
   response (or vice versa) — one full back-and-forth turn of the
   collaboration.

2. **One allowed extension.** Beyond the default cap, **one allowed
   extension** is available. Either party may request the extension; the other
   party may accept or refuse it. There is exactly one extension — it is not
   renewable, and a refused extension ends the exchange at the cap.

3. **Ship from the current map when the limit is hit.** If the conversation
   reaches the final round (round 3, or the extension round if one was
   granted) without full convergence, **the current Domain & Context Map is
   what you have, and you ship from there.** You do not hold the exchange open
   for a better map; you take the map as it stands at the limit and proceed to
   scenario-to-BC assignment from it.

## What this skill does not change

This skill carries the *situational mechanics* only. The operative doctrine —
that decomposition is a bounded collaboration and that you ship from the
current map at the limit — remains stated in the lead-architect role template
and continues to hold whether or not this skill is loaded. Loading the skill
adds the round-counting and extension protocol you need to run the exchange;
it does not introduce new decomposition behavior.
