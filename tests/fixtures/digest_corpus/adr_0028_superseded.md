---
type: adr
id: adr-0028
title: Publish decisions inline in the source document
status: superseded
description: Decisions were read directly from each source document rather than a digest.
derives-from: [adr-0020]
superseded-by: [adr-0031]
---

# adr-0028: Publish decisions inline in the source document

Readers opened each full source document to learn a decision and what it
superseded.

## Decision

Read every decision directly from its source document, with no separate digest
tier.

## Consequences

A reader must open the full source to learn a decision's supersede edges.
