---
id: ADR-0013
title: Keep generation free of ambient state
status: accepted
description: Generation reads only the source corpus and embeds no timestamp, hostname, or absolute path.
---

# ADR-0013: Keep generation free of ambient state

Embedding the wall-clock time, the build host, or an absolute checkout path
would make otherwise-identical regenerations differ byte-for-byte.

## Decision Outcome

Generate every projection and index entry from the source corpus alone, so the
output carries no timestamp, no hostname, and no absolute filesystem path.

## Consequences

Two regenerations of the same corpus on different hosts at different times are
byte-for-byte identical.
