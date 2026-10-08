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

## Slice 68: A decision links to its shop
- Kind: capability
- Scenarios: read-an-artifact / every scenario (its Background now records the decision of a shop); follow-the-links / The user sees what a decision points at; follow-the-links / The user follows the links two steps out; use-the-shops-types / The user reads a product, a shop, a capability, a decision or a feature at a glance (all rows)
- Observable: a decision names the shop it belongs to and shows it at a glance, and following a decision's links reaches its shop and that shop's product
- Unknown: whether every step that records a decision can give it a shop without changing what any other scenario observes
- Needs: the decision-fields helper gives every recorded decision a shop of its own scenario (step data only); the ledger and records find a shop's decisions through the links pointing at it
- Status: green

## Slice 69: Capabilities link to their shop in order
- Kind: capability
- Scenarios: publish-a-shops-spec / every scenario standing on its changed Background that holds today: the index, a file for each active or deprecated capability, the ledger of the shop's own decisions, a feature file for each formulated capability, a record for each decision, the index in order, a capability's file named from its title (all rows), a decision's record named (all rows), the published-from line (all rows), every ledger entry, and the five refusals that stay (two capabilities on one file name, two decisions on one file name, two decisions on one number, two features on one capability, a ragged table); use-the-shops-types / The user records a capability that depends on capabilities of its own shop and of other shops; The user records a capability whose status is not active, deprecated or retired; The user records a capability whose order is not one or more whole numbers joined by dots (all rows)
- Observable: a shop's capabilities are the capabilities linking to it, published and counted in their dotted order, each carrying a status and the capabilities it depends on
- Unknown: how publishing and coverage find a shop's capabilities through the links pointing at it and sort dotted orders part by part
- Needs: shop.reading_order and shop.decisions leave the types; coverage reads capabilities the same way publishing does
- Status: green

## Slice 70: Publishing deletes the files it no longer writes
- Kind: capability
- Scenarios: publish-a-shops-spec / The user publishes a shop's spec into a directory holding files published earlier, and those this publish does not write are deleted (all rows); The user publishes a shop's spec into a directory holding a file with no published-from line, at a name it does not write (all rows)
- Observable: republishing a shop removes the files of artifacts it no longer publishes, and of renamed ones, and leaves every file it did not publish
- Unknown: where deleting published files lives, given that a renderer only reads and the command writes
- Needs: none
- Status: green

## Slice 71: See what a shop depends on
- Kind: capability
- Scenarios: see-what-a-shop-depends-on / every scenario; follow-the-links / The user follows the links into a capability
- Observable: the user asks shop-knol dependencies for a shop and is shown its published capabilities depending on deprecated or retired capabilities in any shop, with the scenarios that use them; following links into a capability shows who depends on it
- Unknown: how to find, through the contract, the status and shop of each capability a shop's capabilities depend on, and the scenarios of theirs that use it
- Needs: none
- Status: green

## Slice 72: Deprecated and retired capabilities
- Kind: capability
- Scenarios: publish-a-shops-spec / The user publishes a shop's spec holding a deprecated capability; The user publishes a shop's spec holding a retired capability; Publishing is refused when an active or deprecated capability of the shop depends on a retired capability (all rows); use-the-shops-types / The user sets a capability's status to retired while other capabilities or scenarios depend on it, in any shop (all rows); see-what-is-formulated / Where a capability linking to the shop is retired, the user asks what is formulated and is shown none of its lines
- Observable: a deprecated capability is published and marked, a retired one is kept but not published or counted, and a capability depending on a retired one stops its shop's publish
- Unknown: none
- Needs: none
- Status: green

## Slice 73: Publishing refuses a capability's inconsistent links
- Kind: capability
- Scenarios: publish-a-shops-spec / Publishing is refused when two of the shop's capabilities carry one order; Publishing is refused when a capability of the shop rests on a decision of another shop; Publishing is refused when a scenario's uses names a capability its capability does not depend on
- Observable: a shop whose capabilities share an order, rest on another shop's decision, or whose scenarios use what their capability does not depend on is refused with nothing written or deleted
- Unknown: none
- Needs: none
- Status: green

## Log
- 2026-10-07 REQUEST kb: a validate-only mode on BatchCreate and BatchReplace, checking a batch as it would land and landing nothing (adrs/0053; spec/capabilities/make-several-changes-at-once.md Not yet). No slice of batch 16 waits on it.
- 2026-10-07 REQUEST shopsystem-bdd: capability-writer and feature-formulator read kb through a read-only shop-knol allowlist (read, list, refs, search, types) and draft shop-knol apply batch files; integrating-a-proposal's and formulating-features' apply steps validate, gate, apply creates then writes, publish with render spec, and commit; the capability format notes the published-from line (adrs/0052, 0053). Moving a shop's real spec into kb waits on it.
- 2026-10-07 QUESTION FOR THE SPEC: publish-a-shops-spec, a decision named by the decisions of two shops: refused (a decision belongs to one shop, naming both shops, nothing written), or allowed (each shop publishes it as its own, each judging its numbers apart)? No principle decides it; for the person. No slice of batch 16 depends on it.
- 2026-10-07 QUESTION FOR THE SPEC: use-the-shops-types, what a capability rests on: the capability type's rests_on targets decisions only, but all 18 of this repository's capabilities rest on other capabilities too (e.g. start-a-knowledge-base rests on capability/find-the-knowledge-base), so the types cannot hold this repository's own spec as written. Widen rests_on to capabilities, or move such links to a field of their own? For the person; it blocks moving a real shop's spec into kb, not batch 16. (batch 16's branch review)
- 2026-10-07 QUESTION FOR THE SPEC: see-what-is-formulated, which capabilities coverage counts: only those in the shop's reading order today, so a capability naming the shop but left out of the order has its lines silently omitted. Count every capability naming the shop, or refuse as publishing does? For the person. (batch 16's branch review)
- 2026-10-07 QUESTION FOR THE SPEC: publish-a-shops-spec, a capability removed from the shop keeps its old page and feature file when publishing over an older spec, and the stale feature file keeps running as a test. Should publishing remove files of artifacts no longer in the shop? Deleting files is the person's call. (Review Focus 3; batch 16's branch review)
- 2026-10-08 Batch batch16 archived to archive/2026-09-23-shop-knowledge-slices-batch16.md; last 2026-10-08 Suite: 190 passed, 0 failed at e7d73ea in 22.4 s (batch 16's fix-wave re-review, make test at HEAD)
- 2026-10-08 Suite: 190 passed, 0 failed at e7d73ea in 22.4 s (batch 16's fix-wave re-review, make test at HEAD)
- 2026-10-08 Suite: 148 passed, 64 failed at 57bf44c in 15 s; failing: the new and changed scenarios of batch 17 (read-an-artifact and publish-a-shops-spec through their changed Backgrounds), see-what-a-shop-depends-on not yet collected
- 2026-10-08 slice 68 green. Someone can now: record a decision linked to its one shop, and see that shop at a glance and among what it points at (and, two steps out, the shop's product).
  Surprised by: making the link required reached every step recording a decision (tests/decision_fields.shop_of records a product and a shop first); the no-shop check (spec_faults._unowned) and its unbound steps went with shop.decisions, since a decision's shop is now required.
  Open questions: none. Next: slice 69.
- 2026-10-08 Suite: 158 passed, 54 failed at 390424a in 17 s; failing: publish-a-shops-spec through its changed Background (43), the slice 69-73 rows of use-the-shops-types (9), follow-the-links into a capability, see-what-is-formulated's retired capability
- 2026-10-08 slice 69 green. Someone can now: link a capability to its shop with a dotted order, a status and the capabilities it depends on, and publish and cover a shop's capabilities found through those links in their order. Surprised by: the depends_on row passed once the step existed, since kb keeps an undeclared field, so its Then reads the field as a link at a glance; the ledger and index scenarios add to the Background's two decisions and two capabilities (orders 5 and 6), so their Thens read the relative order. Open questions: none. Next: slice 70.
- 2026-10-08 Suite: 191 passed, 21 failed at 5218efb in 27 s; failing: publish-a-shops-spec slice 70-73 rows (deletion, deprecated and retired pages, refusals), the slice 71 retired rows of use-the-shops-types, follow-the-links into a capability, see-what-is-formulated's retired capability
- 2026-10-08 HAND-BACK slice 70, scenario "The user publishes a shop's spec into a directory holding files published earlier, and those this publish does not write are deleted" (rows spec/capabilities and features): going green needs work no scenario in the slice describes; the stale artifact of both rows is a capability linking to the shop whose status is retired (and the feature formulating it), and the spec publisher still publishes retired capabilities, which slice 72 changes.
  Evidence: AssertionError: ('`spec/capabilities/old-cache.md`', 'written:\n ... - features/old-cache.feature ... - spec/capabilities/old-cache.md ...'), and the same for `features/old-cache.feature`: the publish itself writes both stale files, so they are written over, not deleted. Deletion is implemented (published.py) and the adrs row is green.
  Green in this slice: the adrs row of that outline. Red: its spec/capabilities and features rows; "The user publishes a shop's spec into a directory holding a file with no published-from line, at a name it does not write" (all three rows) not started. Suggest slice 72 (retired capabilities left out of publishing) before slice 70's two rows, or slice 70 resumed once it is green.
- 2026-10-08 Suite: 192 passed, 20 failed at 88c38dc in 30 s; failing: publish-a-shops-spec slice 70 rows (deletion's spec/capabilities and features rows, the three no-published-from-line rows) and slice 72-73 rows (deprecated and retired pages, refusals), the slice 71 retired rows of use-the-shops-types, follow-the-links into a capability, see-what-is-formulated's retired capability
- 2026-10-08 Re-slice (hand-back of slice 70): the deletion outline ('...and those this publish does not write are deleted', 3 rows) moves to slice 72, since two of its rows take a retired capability as the stale artifact and only slice 72 stops publishing retired capabilities; slice 70 keeps the outline for a file with no published-from line (3 rows). The deletion code landed in 88c38dc stays. Ruling under the person's delegation.
- 2026-10-08 slice 70 green. Someone can now: publish a shop's spec into its repository without losing a file written by hand directly in spec/capabilities/, features/ or adrs/ at a name nothing is published under; publishing deletes only files carrying the published-from line where the publisher puts it, and only the spec renderer deletes (published.py, with its module-map row, landed in the hand-back commit 88c38dc).
  Surprised by: the deletion outline needed slice 72's retired filtering (handed back, re-sliced into slice 72); its adrs row is already green. The three rows here passed as soon as their steps existed, since no code deletes a file without the line; a mutation making every file count as published turned all three red on their Then. Review Focus probes (.superpowers/batch17/probe_deletion.py): a well-formed line naming another shop's artifact is deleted; a malformed line, a line not first or after the frontmatter, a non-UTF-8 file, a subdirectory under features/, a symlink, and files outside the three directories (notes/old.md, spec/old.md) are left; publishing through the markdown renderer deletes nothing.
  Open questions: an unreadable file (OSError) in the three directories refuses the publish before anything is written, which no scenario covers. Next: slice 71.
- 2026-10-08 Suite: 195 passed, 17 failed at 296212f in 29 s; failing: publish-a-shops-spec slice 72-73 rows (deletion's spec/capabilities and features rows, deprecated and retired pages, refusals), the slice 72 retired rows of use-the-shops-types, follow-the-links into a capability, see-what-is-formulated's retired capability
- 2026-10-08 slice 71 green. Someone can now: run shop-knol dependencies <shop> and see which of its capabilities lean on deprecated or retired ones, with the scenarios using them; and follow the links into a capability to see who depends on it. Surprised by: follow-the-links' into-a-capability row passed on its new steps alone, no code; an empty list prints as an empty value; the shared shop-is-absent and answered Thens moved to conftest. Open questions: none. Next: slice 72.
- 2026-10-08 Suite: 200 passed, 16 failed at 3602d0c in 33 s; failing: publish-a-shops-spec slice 72-73 rows, the slice 72 retired rows of use-the-shops-types, see-what-is-formulated's retired capability
- 2026-10-08 slice 72 green. Someone can now: deprecate or retire a capability and see publishing and coverage honour it, the publish refused where a published capability depends on a retired one. Surprised by: the use-the-shops-types retiring scenario needed steps only, kb accepts the status change, so it went green on its step definitions alone; the formulated retired scenario went green with the same shop_capabilities filter as the retired publish (red seen by briefly disabling it). Open questions: none. Next: slice 73.
- 2026-10-08 Suite: 213 passed, 3 failed at d7bf510 in 34 s; failing: publish-a-shops-spec slice 73 rows (two capabilities one order, a scenario's uses not depended on, a capability resting on another shop's decision)
- 2026-10-08 slice 73 green. Someone can now: publish a shop's spec and have it refused for two capabilities at one order (3 and 3.0 are one), a capability resting on another shop's decision, or a scenario using what its capability does not depend on. Surprised by: position() needed trailing zeros dropped for 3 and 3.0 to be one order; two Givens already existed in publish_spec_decisions (reused); shared refusal helpers moved to tests/publish_refusals.py. Open questions: none. Next: none (batch 17's last slice).
- 2026-10-08 Suite: 216 passed, 0 failed at c2849ba in 34 s
- 2026-10-08 Suite: 216 passed, 0 failed at 7961fc4 in 35 s (batch 17's branch review, make test)
- 2026-10-08 QUESTION FOR THE SPEC: publish-a-shops-spec, no scenario pins that a scenario whose uses names a capability of its own shop, among its capability's depends_on, is published; and the index's 'Pinned in' names a retired capability that has no page (keep, drop, or refuse?). For the person. (batch 17's branch review)
- 2026-10-08 Fix wave for batch 17's branch review green: publishing deletes only files inside the directory asked for (a linked adrs/, features/ or spec/ deletes nothing); a scenario may use its own shop's capability (uses-its-own-shop refusal and its steps removed); module-map rows brought up to date; dependencies.PUBLISHED and unreachable steps removed; dependency scenario Then keyed by pair. Open: writing through a linked directory stays a backlog line.
- 2026-10-08 Suite: 216 passed, 0 failed at 52ca71d in 35 s
- 2026-10-08 Suite: 216 passed, 0 failed at e01f9b1 in 33 s (batch 17's fix-wave re-review, make test at HEAD)
- 2026-10-08 Batch 17 branch review: with fixes; fix wave (deletion stays inside --to, own-shop uses no longer refused, module-map rows, dead code and unreached steps, dependency steps keyed by pair) re-reviewed, all addressed
