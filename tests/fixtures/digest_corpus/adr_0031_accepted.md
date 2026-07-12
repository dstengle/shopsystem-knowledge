---
type: adr
id: adr-0031
title: Adopt the L1 decision digest
status: accepted
description: The knowledge context publishes accepted decisions as a self-contained L1 digest.
derives-from: [adr-0028]
supersedes: [adr-0028]
superseded-by: []
---

# adr-0031: Adopt the L1 decision digest

The prior arrangement forced a reader to open the full source document to learn
what a decision superseded.

## Decision

Generate an L1 decision digest whose every entry is self-contained: it carries
the decision's own id, its status, its supersede edges, and the verbatim L1
decision extract, so a reader of one entry needs no other entry or source.

## Consequences

A reader can determine a decision, its status, and what it supersedes from a
single digest entry.
