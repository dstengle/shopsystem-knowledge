---
type: pdr
id: pdr-0007
title: Distribute full source documents to every BC
status: rejected
description: A rejected proposal to push whole source documents across the distribution boundary.
decision-makers: [architect, product-owner]
derives-from: [adr-0020]
---

# pdr-0007: Distribute full source documents to every BC

## Context

Some consumers asked for the whole source document rather than a projection.

## Options considered

Distribute L2 full documents, or distribute only L0 and L1 projections.

## Decision

Rejected: L2 full documents are not distributed across the boundary; only L0
and L1 projections cross.

## Consequences

Consumers receive projections, never full source documents.
