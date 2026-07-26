---
type: current-state
id: current-state-0003
title: Knowledge distribution current state
status: current
description: The versioned record of how the knowledge context distributes decisions to BCs.
incorporates: [adr-0040]
derived-by: [adr-0040]
---

# current-state-0003: Knowledge distribution current state

## Current decisions

The record of how the knowledge context distributes settled decisions to the
bounded contexts that consume them. It incorporates the distribution decision
adr-0040.

## Stewardship

This is a versioned append-only instance (a numbered series, ADR-069 D7): a new
numbered current-state is issued as decisions land rather than revising a single
document in place, and it does not itself decide projection tiers.
