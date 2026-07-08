---
id: ADR-3101
title: Retry a failed request three times with exponential backoff
status: accepted
description: A failed request is retried three times with exponential backoff before an error surfaces to the caller.
---

# ADR-3101: Retry a failed request three times with exponential backoff

Transient failures were surfacing as hard errors to callers.

## Decision

Retry a failed request three times with exponential backoff before surfacing an
error to the caller.

## Consequences

Transient failures are absorbed and callers see fewer spurious errors.
