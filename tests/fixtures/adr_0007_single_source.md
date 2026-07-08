---
id: ADR-0007
title: Adopt single-source projection generation
status: accepted
description: All projection tiers are generated deterministically from one source document.
---

# ADR-0007: Adopt single-source projection generation

The knowledge context previously maintained projection tiers by hand, which
allowed the tiers to drift apart.

## Decision

Generate the L0 card, the L1 extract, and the L2 projection, together with the
machine and human index entries, from a single source Markdown document whose
frontmatter is the only machine truth.

## Consequences

Regeneration is deterministic and idempotent, and no tier can introduce a fact
that is absent from the source.
