---
type: adr
id: adr-0040
title: Distribute only L0 and L1 projections across the boundary
status: accepted
description: Across the distribution boundary only L0 cards and the L1 digest cross, never L2 full documents.
derives-from: [current-state-0003]
---

# adr-0040: Distribute only L0 and L1 projections across the boundary

Consuming BCs need the decision and its card, not the whole source document.

## Decision

Pour only the L0 card and the L1 decision digest across the distribution
boundary; never deliver an L2 full document to a consuming BC.

## Consequences

A consuming BC receives projections it can act on without ever holding a full
source document.
