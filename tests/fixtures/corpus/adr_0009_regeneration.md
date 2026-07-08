---
id: ADR-0009
title: Regenerate projections rather than hand-edit
status: accepted
description: Projections are treated as build output regenerated from source, never edited in place.
---

# ADR-0009: Regenerate projections rather than hand-edit

Hand-editing a generated tier reintroduces the drift the single-source rule was
adopted to eliminate.

## Decision

Treat every projection tier as build output that is regenerated from the source
corpus, and never edit a generated tier in place.

## Consequences

A generated tier can always be reproduced from source, so a check mode can flag
any tier that has drifted from what the source would generate.
