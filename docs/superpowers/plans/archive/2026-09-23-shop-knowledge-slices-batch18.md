# shop-knowledge slices

shop-knowledge's living plan. Until kb 0.1 it was the one plan for both
this repository and kb, as both specs' "Order of building" say; on
2026-09-24, with kb tagged `v0.1.0` and pinned here, every slice made only
of kb scenarios moved to kb's own plan,
`shopsystem-kb/docs/superpowers/plans/2026-09-24-kb-slices.md`, with its
number, tags, status, and log entries. The numbers here skip those that
moved; a number is never reused across the two plans, and a slice in the
other plan is named with its repository, as in "kb slice 21". Slices 0 and
1 check or run scenarios in both repositories and stay here; their
Scenarios lines still say which repository each scenario runs in.

From here each repository plans alone. A kb change this repository needs
is a request to bump the pin: the shop-knowledge slice that needs it waits
until kb has released it under a new tag and this repository pins that
tag.

Slice 0 is the enabling slice the skeleton stands on: both checkouts run
their feature suites and this repository imports kb from the checkout
beside it. Slice 1 is the walking skeleton the specs define. Slices 1.1 to
1.28 were the three cuts kb 0.1 waited on, most of them now in kb's plan, each ordered the same way: the
slices that settle one unknown by the size of it, then those with none.
Then the tag. Then slices 2 to 20, which each settle one
unknown, ordered by the size of it. Then the slices with no unknown:
scenarios that share a feature and step definitions bundle into one slice,
and the slices are ordered by value, kb's slice ahead of the shop-knowledge
slice that needs it. An architecture review is an enabling slice cut after
every six implemented slices, counting enabling slices and the refactors a
review cuts. The first review's refactors were placed as dotted slices right
after it; from the second on, each refactor a review calls for is placed by
its risk among the slices not yet begun, like any finding, and precedes a
slice only if that slice needs it.

The order of the sections in this file is the order of the work, and the
numbers read in that order. A slice placed after the plan was cut takes
its place by its unknown among the slices not yet begun, and those slices
are renumbered and their tags rewritten to match, within this repository
only.

## Slice 74: A constraint is tested in capabilities
- Kind: capability
- Scenarios: publish-a-shops-spec / Publishing is refused when a constraint of the shop is tested in a retired capability, in any shop (all rows)
- Observable: a shop's constraints name the capabilities they are tested in, published as 'Tested in', and a constraint tested in a retired capability stops the publish
- Unknown: none
- Needs: pinned_in renamed tested_in in the shop type, the publisher and the test helpers; the published index says 'Tested in' (the index scenario's expected text, step data)
- Status: green

## Slice 75: A file publishing cannot read stops the publish
- Kind: capability
- Scenarios: publish-a-shops-spec / Publishing is refused when, among the files publishing may delete, one cannot be read (all rows)
- Observable: a publish that meets an unreadable file it may delete is refused naming the file, with nothing written or deleted
- Unknown: none
- Needs: none
- Status: green

## Slice 76: The check finds a scenario using what its capability does not depend on
- Kind: capability
- Scenarios: check-the-knowledge-base / The user checks a knowledge base where a scenario uses a capability its capability does not depend on (all rows)
- Observable: shop-knol validate lists, across every shop, each scenario whose uses names a capability its capability does not depend on, as a fault
- Unknown: how validate adds a check of shop-knowledge's own to kb's Check answer while still showing what is behind its type
- Needs: none
- Status: green

## Log
- 2026-10-07 REQUEST kb: a validate-only mode on BatchCreate and BatchReplace, checking a batch as it would land and landing nothing (adrs/0053; spec/capabilities/make-several-changes-at-once.md Not yet). No slice of batch 16 waits on it.
- 2026-10-07 REQUEST shopsystem-bdd: capability-writer and feature-formulator read kb through a read-only shop-knol allowlist (read, list, refs, search, types) and draft shop-knol apply batch files; integrating-a-proposal's and formulating-features' apply steps validate, gate, apply creates then writes, publish with render spec, and commit; the capability format notes the published-from line (adrs/0052, 0053). Moving a shop's real spec into kb waits on it.
- 2026-10-07 QUESTION FOR THE SPEC: publish-a-shops-spec, a decision named by the decisions of two shops: refused (a decision belongs to one shop, naming both shops, nothing written), or allowed (each shop publishes it as its own, each judging its numbers apart)? No principle decides it; for the person. No slice of batch 16 depends on it.
- 2026-10-07 QUESTION FOR THE SPEC: use-the-shops-types, what a capability rests on: the capability type's rests_on targets decisions only, but all 18 of this repository's capabilities rest on other capabilities too (e.g. start-a-knowledge-base rests on capability/find-the-knowledge-base), so the types cannot hold this repository's own spec as written. Widen rests_on to capabilities, or move such links to a field of their own? For the person; it blocks moving a real shop's spec into kb, not batch 16. (batch 16's branch review)
- 2026-10-07 QUESTION FOR THE SPEC: see-what-is-formulated, which capabilities coverage counts: only those in the shop's reading order today, so a capability naming the shop but left out of the order has its lines silently omitted. Count every capability naming the shop, or refuse as publishing does? For the person. (batch 16's branch review)
- 2026-10-07 QUESTION FOR THE SPEC: publish-a-shops-spec, a capability removed from the shop keeps its old page and feature file when publishing over an older spec, and the stale feature file keeps running as a test. Should publishing remove files of artifacts no longer in the shop? Deleting files is the person's call. (Review Focus 3; batch 16's branch review)
- 2026-10-08 QUESTION FOR THE SPEC: publish-a-shops-spec, no scenario pins that a scenario whose uses names a capability of its own shop, among its capability's depends_on, is published; and the index's 'Pinned in' names a retired capability that has no page (keep, drop, or refuse?). For the person. (batch 17's branch review)
- 2026-10-08 Batch batch17 archived to archive/2026-09-23-shop-knowledge-slices-batch17.md; last 2026-10-08 Suite: 216 passed, 0 failed at e01f9b1 in 33 s (batch 17's fix-wave re-review, make test at HEAD)
- 2026-10-08 Suite: 216 passed, 0 failed at e01f9b1 in 33 s (batch 17's fix-wave re-review, make test at HEAD)
- 2026-10-08 Suite: 216 passed, 7 failed at 2d05fb1 in 33 s; failing: batch 18's new scenarios
- 2026-10-08 REQUEST shopsystem-bdd: the capability format defines a depends_on frontmatter key (capabilities a capability builds on, in its own context or another) beside rests_on (decisions only); this repository's capabilities use it (adrs/0067).
- 2026-10-08 slice 74 green. Someone can now: publish a shop whose constraints are tested_in capabilities (Tested in), and be stopped when one is tested in a retired capability of any shop. Surprised by: nothing; the pinned_in to tested_in rename was green on its own before the new steps. Probe: a constraint tested in a deprecated capability publishes as today (Tested in listed). Folded in the ragged-table and linked-directory CLAUDE.md row notes. Open questions: none. Next: slice 75.
- 2026-10-08 Suite: 218 passed, 5 failed at 2779289 in 35 s; failing: slice 75 (3 rows), slice 76 (2 rows)
- 2026-10-08 slice 75 green. Someone can now: be told which file publishing could not read, with the directory untouched. Surprised by: the behaviour did not already name the reason (only the OS's 'Permission denied'), so published.py's OSError path got a plain-words Refused naming the file; the shared 'nothing is written' step had to tell an unreadable file from a changed one. Probe: several unreadable files name the first only (in the order spec/capabilities, features, adrs). Backlog: name every unreadable file, not only the first. Open questions: none. Next: slice 76.
- 2026-10-08 Suite: 221 passed, 2 failed at d1657f5 in 34 s; failing: slice 76 (2 rows)
- 2026-10-08 slice 76 green. Someone can now: run shop-knol validate and be told of every scenario, in any shop, using a capability its capability does not depend on, with sound false and exit 1. Surprised by: nothing; the rule's one function (consistency.undepended) now serves the publishing check too, which gained a place on its fault. Probe: kb's Check clean and one uses fault gives sound false, the fault listed, exit 1. Open questions: none. Next: none.
- 2026-10-08 Suite: 223 passed, 0 failed at 9097d50 in 34 s
- 2026-10-08 batch 18 fix wave green (e6910b0, 0cceeb7). Someone can now: validate a damaged or bare knowledge base and get kb's own answer beside the uses check (no traceback, sound on a bare store as at 018a928), publish a shop whose constraint title holds braces and get one plain refusal, and see one uses fault per scenario and capability.
  Surprised by: kb refuses Remove of a capability a feature points at, so the deleted-capability probe needed a scratch store damaged by hand.
  Open questions: none. Next: the controller's re-review.
- 2026-10-08 Suite: 223 passed, 0 failed at 0cceeb7 in 33 s
- 2026-10-08 QUESTION FOR THE SPEC: check-the-knowledge-base's Implementation says the uses fault carries rule uses-not-depended-on, but shop-knol never prints a fault's rule, so no user sees it: drop it from the line, or print rules? For the person. (batch 18's branch review)
- 2026-10-08 Settled by batch 18, so these Backlog lines no longer stand: an unreadable file refuses the publish (adrs/0066, slice 75); the index's 'Pinned in' names a retired capability (slice 74 refuses it); the CLAUDE.md module-map rows (folded into slice 74).
- 2026-10-08 Suite: 223 passed, 0 failed at fd3eb62 in 35 s (batch 18's fix-wave re-review, make test at HEAD)
- 2026-10-08 Batch 18 branch review: with fixes; fix wave (no .format over user text; the uses check never takes kb's answer away or crashes; module map; one step per Then; one fault per scenario and capability) re-reviewed, all addressed
