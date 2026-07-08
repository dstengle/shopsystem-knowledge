---
id: ADR-3002
title: Reduce the default pagination page size
status: accepted
description: The default pagination page size is reduced from fifty to twenty items per response.
---

# ADR-3002: Reduce the default pagination page size

The fifty-item default pagination response was too heavy for mobile clients.

## Decision

Change the default pagination page size from fifty to twenty items per response.

## Consequences

Mobile clients pay for smaller responses and paginate more often.
