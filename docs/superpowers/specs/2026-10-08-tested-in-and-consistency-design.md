# Tested in, consistency checks, and this repository's dependencies

Date: 2026-10-08. Status: approved in conversation. Decisions: adrs/0064 to 0067.

A proposal against `spec/`.

## A constraint is tested in capabilities

- A shop's constraint names the capabilities whose scenarios show its promise holds through `tested_in`, which
  replaces `pinned_in`. The published index writes it `Tested in <names>.`, replacing `Pinned in <names>.`
- This repository's own `spec/index.md` writes "Tested in" where it writes "Pinned in" today, and its Constraints
  carried preamble and its decision ledger keep their words except where they name the term.
- Publishing a shop's spec is refused when a constraint's `tested_in` names a retired capability, naming the
  constraint and the capability, with nothing written or deleted.

## Consistency checks

- `shop-knol validate` (check-the-knowledge-base) also reports, as faults, every scenario whose `uses` names a
  capability not among its capability's `depends_on`, across the whole knowledge base, whichever shop it is in. A
  check that finds faults refuses with them and still shows what is behind its type, as today.
- Checking a shop's declared dependencies against what its code actually calls is not yet. Promoted when a shop's
  code is found to call a capability it does not declare.

## A file publishing cannot read

- When publishing a shop's spec finds, among the files it may delete, one it cannot read, the publish is refused,
  naming the file, and nothing is written or deleted. (This is what it does today; the line makes it contract.)

## This repository's capabilities declare depends_on

- Every capability of this repository's `spec/` that lists a capability under `rests_on` lists it under a
  `depends_on` frontmatter key instead, after `rests_on`; `rests_on` keeps decisions only. Nine capabilities do
  today.
- Request to shopsystem-bdd: the capability format defines `depends_on` (capabilities a capability builds on, in its
  own context or another) beside `rests_on` (decisions).

## Not in this proposal

- Dropping `uses` (kept, adrs/0064).
