---
id: ADR-4001
title: Change the default pagination page size
status: accepted
description: The default pagination page size is changed from fifty to one hundred items per response.
---

# ADR-4001: Change the default pagination page size

The fifty-item default pagination response left mobile-first clients making too
many round trips for a single screen of data.

## Decision

Change the default pagination page size from fifty to one hundred items per
response.

## Consequences

Callers receive larger pages and paginate less often for the same dataset.
