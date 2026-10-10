# Requests to kb: portable knowledge

Requests from shop-knowledge to kb, 2026-10-10, for a kb session to integrate into kb's spec. Each asks for a
change to one of kb's capabilities, or a new one, and names the decision behind it. The decisions were the
person's, made in a shop-knowledge brainstorming session about migrating markdown specs into kb and not losing a
shop's knowledge with its server; they are recorded in shopsystem-kb/adrs/0022-0030 (uncommitted, for the kb
session to keep) and shopsystem-knowledge/adrs/0070-0075. How each is worded as Behaviour, and everything not
settled below, is the kb session's.

## Why

shop-knowledge will move every shop's markdown spec into kb, render and export it after every change, and must
not lose it if the server goes. Three things in kb stand in the way today:

- An artifact's id is minted from its title and means something in one store only, so a link survives a move
  only into a fresh store, where every name is kept. A product's contexts link to each other and to the
  product's lead shop, so they cannot be moved one at a time.
- Import goes only into a freshly started store, and a link must land on something already held.
- Export is the operator's, writes to the store's machine, and drops history; there is no backup.

## Release grouping

- **K1, Backup and restore**: request 1. Operator only, no contract change. Wanted first: it covers losing the
  server before anything else lands.
- **K2, Portable identity**: requests 2-8. Breaking: contract `kb.v2`.
- **K3, Export and import between stores**: requests 9-10. Adds to `kb.v2`; one release with K2, so clients break
  once.

## The requests

### 1. operate-a-store: back up and restore a store whole (adrs/0028)

The operator backs up a running store whole, its history and journal included, without stopping writers, and
restores a backup as a store in an empty place, or for a fresh server. Promotes "Backups and managing volumes
beyond `kb export`" from Not yet. Export stays the readable, portable copy (request 9); backup is how a lost
server is recovered with nothing lost.

### 2. name-artifacts-and-items: the client chooses an artifact's id, an IRI under its type (adrs/0022, 0023)

An artifact's id is an https IRI: its type's IRI, a `/`, and a path of plain names the client chooses. kb checks
the grammar, that the id sits under its type's IRI, and that it is unique, and never mints one. Parts are still
named by kb, from title or position, and are written as the artifact's IRI with a fragment (`…#behaviour-3`).
An id is fixed for life. Supersedes adrs/0002 for artifacts; the "client never chooses a name" lines go.

shop-knowledge's convention, for illustration only (kb sees a path): below the type, the owner's domain, product,
bounded context and name, e.g. `https://missingmass.io/shopsystem/capability/missingmass.io/ecommercesite/catalog/browse-the-catalog`.

### 3. define-a-type: a type has an IRI, and each version an IRI of its own (adrs/0027)

A type has a stable IRI, any https IRI its client chooses, which its artifacts' ids sit under. Each version has
its own IRI, the type's with `@` and the version (`…/capability@2`), and is fixed once made; a change to a type is
a new version. Several versions of a type are held while artifacts conform to them. A link's targets name the
type, any version. Moving content between versions stays Not yet. The type that describes types gets an IRI under
a domain kb owns, which replaces the published id `schema/schema`.

### 4. change-the-store and hand-over-content: an artifact names the version it conforms to (adrs/0027)

A create says the id and the type version, by its IRI, in place of `schema_version`; a write may name a later
version of the same type and is checked against it, the artifact keeping its id. What travels beside the content
is the IRI, the version's IRI, revision and title.

### 5. check-a-change: a link may land on a placeholder (adrs/0024)

A link to an IRI the store does not hold, under a type it holds, is accepted, and lands on a placeholder: typed by
its place under its type and checked against the link's targets. An IRI under a type the store does not hold is
refused as today. Creating an artifact at that IRI fills the placeholder. The rule is the same over the contract,
in a set and in import. A placeholder is not stored: it is an IRI linked to and not held.

### 6. read-an-artifact and query-the-store: placeholders are seen and listed (adrs/0024)

A read marks a link whose target is not held, distinctly from one that lands. A query lists every placeholder
with what links to it. Listing and following select by the path below the type, across types, beside today's
selection by kind.

### 7. check-the-store: placeholders reported, never failed (adrs/0025)

The check answer and `kb validate` list every placeholder with what links to it, apart from violations and from
artifacts behind their type, and a store holding placeholders and nothing else checks clean. "Behind its type"
becomes: conforms to a version of its type that a later version has followed.

### 8. make-several-changes-in-one-go, keep-the-history, snapshot-what-work-read, name-what-is-asked-for: IRIs throughout (adrs/0022, 0023)

Every name a call carries or answers is an IRI. In a set, new artifacts can name each other by the IRIs their
creates carry; whether `@key` stays is the kb session's (shop-knowledge's batches would no longer need it).

### 9. export-and-import-a-store (and the contract): export is a call, streamed, with its position (adrs/0029, 0030)

A client exports through the contract: a stream of canonical files, one to a message, the store at one moment,
whole or selected by the path below each type and by type, the answer saying the journal position it reflects.
The same against a store in process or a server; a read, never refused as busy. Export of what changed since a
position is to be added later as an optional field, and stays Not yet. The layout follows the IRI's path. The
operator's `kb export` remains.

### 10. export-and-import-a-store: import into any store (adrs/0026)

Import goes into any store, not only a fresh one. An artifact the store already holds at the same IRI, with the
same content and type version, is passed over; one that differs refuses the whole import, naming each IRI, and
nothing lands. A link to an IRI neither the directory nor the store holds lands on a placeholder (request 5),
which replaces the chain of files skipped for linking to a broken one. History still does not travel with an
export (request 1 keeps it).

## Still outstanding

- 2026-10-07: a validate-only mode on BatchCreate and BatchReplace, checking a set as it would land and landing
  nothing (shop-knowledge adrs/0053). shop-knol's migration (adrs/0070) checks its drafted batches with it before
  the gate.

## For the kb session to settle

- The IRI grammar: scheme, segments, length, case, and how a fragment is written.
- Which domain kb owns for its own type.
- Whether a type version no artifact conforms to can be removed, and whether `@key` stays in a set.
- What shop-knowledge waits for: K1, then K2 and K3 as one release; shop-knowledge's S1 (onto kb v2), S2 (render
  and export after every change) and S3 (`shop-knol migrate`) follow, each on a pin bump.
