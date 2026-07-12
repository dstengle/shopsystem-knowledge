---
type: adr
id: adr-0032
title: Sign every digest entry
status: proposed
description: A proposal to attach a cryptographic signature to each digest entry.
derives-from: [adr-0031]
---

# adr-0032: Sign every digest entry

A signature would let a consumer verify a digest entry's provenance.

## Decision

Attach a cryptographic signature to every L1 digest entry.

## Consequences

Consumers can verify provenance, at the cost of a signing step.
