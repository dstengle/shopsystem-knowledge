---
id: ADR-0021
title: Adopt a read-through cache for the projection index
status: accepted
description: The projection index is served through a read-through cache to avoid regenerating it on every read.
---

# ADR-0021: Adopt a read-through cache for the projection index

Serving the projection index by regenerating it on every read was wasteful for
hot lookups.

## Decision

Serve the projection index through a read-through cache so a repeated lookup is
answered from the cache rather than regenerating the index.

## Consequences

Hot lookups become cheap, and the cache becomes a component whose staleness has
to be reasoned about.
