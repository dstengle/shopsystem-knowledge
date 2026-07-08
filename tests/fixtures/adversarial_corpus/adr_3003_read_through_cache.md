---
id: ADR-3003
title: Serve the projection index through a read-through cache
status: accepted
description: The projection index is served through a read-through cache answered from memory.
---

# ADR-3003: Serve the projection index through a read-through cache

Regenerating the projection index on every read was wasteful for hot lookups.

## Decision

Serve the projection index through a read-through cache answered from memory on
a repeated lookup.

## Consequences

Hot lookups become cheap and the cache staleness has to be reasoned about.
