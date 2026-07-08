---
id: ADR-0022
title: Invalidate the projection cache on source change
status: accepted
description: A change to the source corpus invalidates the affected projection cache entries.
---

# ADR-0022: Invalidate the projection cache on source change

A read-through cache over the projection index can serve a stale entry after the
source corpus changes.

## Decision

Invalidate the projection cache entries affected by a source change, so the next
lookup repopulates the cache from the regenerated index.

## Consequences

The cache never serves an entry that the current source would not regenerate.
