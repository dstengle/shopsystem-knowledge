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

## Slice 77: Expected failures for slices not yet built
- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> 202 passed, 0 failed, 37 expected
- Observable: The suite reads green while the portable-knowledge scenarios wait for their slices
- Unknown: none
- Needs: the scenarios of slices 84-92 tagged
- Lands: 0 production, 2 test
- Status: green

## Slice 78: One seam builds kb's requests for the commands
- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> 202 passed, 0 failed, 37 expected; a search over the command, batch, init, bootstrap and answer modules finds no request field naming a kind, no schema_version and no schema/ id outside the seam
- Observable: Every command reaches kb's kind, id and type fields through one module, so moving to kb.v2 changes that module
- Unknown: whether the commands' requests and answers can name kinds and ids through one module without a change a user sees
- Needs: none
- Lands: 7 production, 0 test
- Status: green

## Slice 79: The readers reach kb through the seam
- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> 202 passed, 0 failed, 37 expected; a search over src/ finds a List by kind, a read of an answer's kind and a schema/ id only in the seam
- Observable: coverage, dependencies, the consistency check and the renderers find artifacts by kind through the seam
- Unknown: none
- Needs: none
- Lands: 7 production, 0 test
- Status: green

## Slice 80: A test seam for what tests hand kb, first group
- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> 202 passed, 0 failed, 37 expected; a search shows the oracle, the refused-files steps and the spec attempt build no kb request naming a kind or id directly
- Observable: Tests that ask kb directly do so through one helper
- Unknown: whether one helper can stand for every request a test hands kb
- Needs: none
- Lands: 0 production, 4 test
- Status: green

## Slice 81: The test seam, second group
- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> 202 passed, 0 failed, 37 expected; a search shows the start steps, the batch steps and conftest build no kb request naming a kind or id directly
- Observable: Start and batch steps ask kb through the test seam
- Unknown: none
- Needs: none
- Lands: 0 production, 4 test
- Status: green

## Slice 82: The test seam, third group
- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> 202 passed, 0 failed, 37 expected; a search over tests/ finds kind, schema_version, key and schema/ ids handed to kb only in the test seam
- Observable: No test outside the seam spells a kb.v1 form
- Unknown: none
- Needs: none
- Lands: 0 production, 4 test
- Status: green

## Slice 82.1: The renderers read mapped artifacts
- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -n auto` -> 202 passed, 0 failed, 37 expected; a search of renderers/source.py, markdown.py, skill.py, diagram.py and agent.py finds no id, content or loads of a kb answer outside the seam
- Observable: Every page renderer reads an artifact as the user names it, through one reader
- Unknown: whether one mapped artifact can stand for kb's answer in every renderer
- Needs: none
- Lands: 7 production, 0 test
- Status: green

## Slice 82.2: The spec renderer reads mapped artifacts
- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -n auto` -> 202 passed, 0 failed, 37 expected; a search of renderers/spec*.py, gherkin.py, shop_capabilities.py and consistency.py finds no id, content or revision of a kb answer read outside the seam
- Observable: The spec renderer and the consistency check read artifacts as the user names them
- Unknown: none
- Needs: none
- Lands: 8 production, 0 test
- Status: green

## Slice 83: kb pinned at v0.9.0
- Kind: enabling
- Check: `.venv/bin/python -c "import kb.contract.kb_pb2 as m; print(m.DESCRIPTOR.package)"` -> kb.v2; `.venv/bin/python -m pytest -q` -> 202 passed, 0 failed, 37 expected (fewer expected where a scenario goes green, credited here); a search over src/ and tests/ finds no kb.v1 field
- Observable: shop-knol works against kb.v2 with every name the user sees unchanged
- Unknown: whether everything the suite passes on kb.v1 passes on kb.v2 through the two seams alone
- Needs: the shop's types written as kb.v2 type artifacts
- Lands: 3 production, 2 test
- Status: green

## Log
- 2026-10-07 REQUEST kb: a validate-only mode on BatchCreate and BatchReplace, checking a batch as it would land and landing nothing (adrs/0053; spec/capabilities/make-several-changes-at-once.md Not yet). No slice of batch 16 waits on it.
- 2026-10-07 REQUEST shopsystem-bdd: capability-writer and feature-formulator read kb through a read-only shop-knol allowlist (read, list, refs, search, types) and draft shop-knol apply batch files; integrating-a-proposal's and formulating-features' apply steps validate, gate, apply creates then writes, publish with render spec, and commit; the capability format notes the published-from line (adrs/0052, 0053). Moving a shop's real spec into kb waits on it.
- 2026-10-07 QUESTION FOR THE SPEC: publish-a-shops-spec, a decision named by the decisions of two shops: refused (a decision belongs to one shop, naming both shops, nothing written), or allowed (each shop publishes it as its own, each judging its numbers apart)? No principle decides it; for the person. No slice of batch 16 depends on it.
- 2026-10-07 QUESTION FOR THE SPEC: use-the-shops-types, what a capability rests on: the capability type's rests_on targets decisions only, but all 18 of this repository's capabilities rest on other capabilities too (e.g. start-a-knowledge-base rests on capability/find-the-knowledge-base), so the types cannot hold this repository's own spec as written. Widen rests_on to capabilities, or move such links to a field of their own? For the person; it blocks moving a real shop's spec into kb, not batch 16. (batch 16's branch review)
- 2026-10-07 QUESTION FOR THE SPEC: see-what-is-formulated, which capabilities coverage counts: only those in the shop's reading order today, so a capability naming the shop but left out of the order has its lines silently omitted. Count every capability naming the shop, or refuse as publishing does? For the person. (batch 16's branch review)
- 2026-10-07 QUESTION FOR THE SPEC: publish-a-shops-spec, a capability removed from the shop keeps its old page and feature file when publishing over an older spec, and the stale feature file keeps running as a test. Should publishing remove files of artifacts no longer in the shop? Deleting files is the person's call. (Review Focus 3; batch 16's branch review)
- 2026-10-08 QUESTION FOR THE SPEC: publish-a-shops-spec, no scenario pins that a scenario whose uses names a capability of its own shop, among its capability's depends_on, is published; and the index's 'Pinned in' names a retired capability that has no page (keep, drop, or refuse?). For the person. (batch 17's branch review)
- 2026-10-08 REQUEST shopsystem-bdd: the capability format defines a depends_on frontmatter key (capabilities a capability builds on, in its own context or another) beside rests_on (decisions only); this repository's capabilities use it (adrs/0067).
- 2026-10-08 QUESTION FOR THE SPEC: check-the-knowledge-base's Implementation says the uses fault carries rule uses-not-depended-on, but shop-knol never prints a fault's rule, so no user sees it: drop it from the line, or print rules? For the person. (batch 18's branch review)
- 2026-10-08 Batch batch18 archived to archive/2026-09-23-shop-knowledge-slices-batch18.md; last 2026-10-08 Suite: 223 passed, 0 failed at fd3eb62 in 35 s (batch 18's fix-wave re-review, make test at HEAD)
- 2026-10-08 Suite: 223 passed, 0 failed at fd3eb62 in 35 s (batch 18's fix-wave re-review, make test at HEAD)
- 2026-10-09 Answered: the uses question above, by the person: shop-knol prints every fault's rule, artifact at place: rule: message (adrs/0069), at 7f3b571
- 2026-10-09 Suite: 223 passed, 0 failed at 7f3b571 in 33 s
- 2026-10-10 REQUEST kb: portable knowledge, ten changes to kb's capabilities (backup and restore; ids as IRIs under their type, chosen by the client; type versions as IRIs; placeholders, reported and never failed by kb; export over the contract, streamed, with its position; import into any store), in docs/superpowers/specs/2026-10-10-requests-to-kb-portable-knowledge.md (kb adrs/0022-0030; adrs/0070-0075). For a kb session. Migrating a markdown spec into kb (adrs/0070) and exporting after every change (adrs/0071, 0075) wait on it.
- 2026-10-10 Formulated: portable knowledge (docs/superpowers/specs/2026-10-10-portable-knowledge-design.md), spec at 0120676, 9a29999, c5a55fc, 4c4598c, features at the next commit; questions after the person's own answers settled under their delegation (adrs/0083). Suite: 202 passed, 37 failed, every failure a new, changed or rewritten scenario. Slicing waits for kb.v2 (REQUEST kb, 2026-10-10): nothing here can go green before the pin bump.
- 2026-10-10 For slicing: the existing When steps that record or apply without naming (record-an-artifact, make-several-changes-at-once) are kept as approved; their step definitions supply a name, as they supply a role and a message.
- 2026-10-12 Probe: tools -> coverage 7.16.2, pytest-cov 7.1.0, jedi 0.20.0, ast-grep 0.50.0, ruff 0.17.0, vulture 2.16, import-linter 2.15, hypothesis 6.169.0
- 2026-10-12 Suite: 202 passed, 37 failed at f0c4eb1 in 34 s; failing: the portable-knowledge scenarios formulated 2026-10-10 (no --slice option yet)
- 2026-10-12 Probe: git ls-remote --tags shopsystem-kb -> v0.9.0 (2026-10-11), contract kb.v2, portable knowledge; the REQUEST kb of 2026-10-10 released
- 2026-10-12 Probe: suite in a scratch copy with kb 0.9.0 installed -> 8 passed, 231 failed; ~224 die at bootstrap's CreateRequest(kind=...) (field removed in kb.v2); none of the 37 goes green (.superpowers/scout/kbv2/pin-bump.md)
- 2026-10-12 Probe: searches for kb.v1 forms (kind=, .kind, schema_version, key, schema/ ids, CreateItem, ListRequest) -> 13 production, 25 test: over the budget; the bump is cut as expand, migrate, contract (one kb installed, so the seams expand on kb 0.6.0 and one slice flips them)
- 2026-10-12 Probe: kb 0.6.0 mints a name from a title by lowercasing and hyphenating runs of non-alphanumerics, numbering a taken one -2, -3 (run, .superpowers/scout/kbv2/seam.md); no scenario at HEAD asserts a numbered name (the -2 scenario was rewritten as a refusal)
- 2026-10-12 Probe: searches for the kb.v1 forms by module (seam.md) -> production: 6 commands-and-answers modules plus the seam, and 7 reading modules; tests: 10 modules hand kb a request or read its fields, plus the test seam; the stand-in spells no v1 field
- 2026-10-12 Sweep: kb mints the ids (reversed: the client names every artifact at an IRI, kb.v2) -> 13 production places, 13 test places; owned by slices 78-83 (seams and flip, names kept as today meanwhile, shop-knol minting the slug kb minted) and 87-88 (the user names what they create); 0 questions, 0 deferred
- 2026-10-12 slice 77 green. Someone can now: run the suite and read 37 expected failures of slices 84, 87-91 instead of 37 failures, with --slice <n> for the slice being built. Surprised by: slices 85, 86 and 92 have no test module, so their 24 scenarios are not collected and not expected. Open questions: none. Next: slice 78.
- 2026-10-12 Suite: 202 passed, 0 failed, 37 expected at faad1c9 in 31 s
- 2026-10-12 slice 78 green. Someone can now: find every kind, id, type-of-types and version field the commands send kb or read back in one module, src/shop_knowledge/iris.py (the identity on kb.v1), so the flip to kb.v2 changes that module for the commands, init, bootstrap, batch and answers.
  Surprised by: the check's search forbids the field names themselves (kind=, key=, schema_version), so the seam hands back request fields as dicts (of_kind, of_types, create_fields, item_fields) and the printed version as a dict (versioned); ids, not only kinds, were routed through to_kb/from_kb (D2), including journal --artifact, snapshot names and history entries.
  Open questions: at the flip, the seam must map an empty kind or name (refs/search --type, journal --artifact) to empty; links inside content (a whole read's links, a batch's @key in content) still carry the user's names, which kb.v2 may want as IRIs, and no module owns rewriting them. Next: slice 79.
- 2026-10-12 Suite: 202 passed, 0 failed, 37 expected at 333671b in 32 s
- 2026-10-12 slice 78 fix round 1: content sent and shown, a printed fault's artifact and a Create's or batch item's type version (through the client it is handed) now go through iris.py, the identity on kb.v1; kb's refusal messages printed verbatim (rulings in the batch's progress.md). Open question: the round-trip invariant (from_kb(to_kb(n)) == n, to_kb('') == '', of_kind('') every kind) has no test module that fits; for the branch review.
- 2026-10-12 Suite: 202 passed, 0 failed, 37 expected at b9a30ac in 33 s
- 2026-10-12 slice 79 green. Someone can now: change kb's pin by changing iris.py alone for the readers' Lists, kinds and content. Surprised by: nothing. Open questions: renderers outside the seven (spec_faults, diagram, skill, markdown, agent, spec_capabilities) read ids and content raw. Next: slice 80.
- 2026-10-12 Suite: 202 passed, 0 failed, 37 expected at 9bdcac1 in 33 s
- 2026-10-12 slice 80 green. Someone can now: change what kb_oracle, record_refused_files and spec_attempt hand kb or read from its messages by changing tests/kb_names.py alone. Surprised by: nothing. Open questions: none. Next: slice 81.
- 2026-10-12 Suite: 202 passed, 0 failed, 37 expected at 3ce6003 in 32 s
- 2026-10-12 Probe: searches for ids and content read from kb answers outside iris.py (.superpowers/scout/batch19/task-79.1.md) -> 12 production modules (source and four page renderers; the spec family and consistency), 0 test; cut as slices 82.1 and 82.2 before the flip
- 2026-10-12 slice 81 green. Someone can now: change the pin with start, batch and conftest requests going through tests/kb_names.py. Surprised by: start_not_empty.py was already done by slice 80. Open questions: none. Next: slice 82.
- 2026-10-12 Suite: 202 passed, 0 failed, 37 expected at 7d6be27 in 32 s
- 2026-10-12 slice 82 green. Someone can now: move the pin by changing tests/kb_names.py alone on the test side. Surprised by: session_guard's HistoryRequest has no fields in the code, so the helper only wraps it; test_make_several_changes_at_once.py's HistoryRequest(batch=) is not a locator and stays. Open questions: none. Next: slice 83.
- 2026-10-12 Suite: 202 passed, 0 failed, 37 expected at 14305f1 in 32 s
- 2026-10-12 slice 82.1 green. Someone can now: change kb's pin with the page renderers (markdown, skill, diagram, agent) reading only source.Mapped, built through iris.py. Surprised by: nothing; limits' fault artifact is sent back through iris.to_kb since cli's printer maps it. Open questions: none. Next: slice 82.2 (spec family takes source.Mapped via source.mapped(artifact)).
- 2026-10-12 Suite: 202 passed, 0 failed, 37 expected at 7597f6b in 31 s
- 2026-10-12 slice 82.2 green. Someone can now: change iris.py alone and the spec renderer, its faults and the consistency check follow, ids going to kb through to_kb once. Surprised by: coverage.py and dependencies.py read shop_capabilities.of, so it keeps a raw-artifact twin beside mapped_of; they move in a later slice. Open questions: none. Next: slice 83.
- 2026-10-12 Suite: 202 passed, 0 failed, 37 expected at 0136ffa in 32 s
- 2026-10-12 HAND-BACK slice 83, scenario "Two creates carrying the same key leave the shop untouched" | test tests/test_make_several_changes_at_once.py::test_two_creates_carrying_the_same_key_leave_the_shop_untouched: an existing test can only stay green by being rewritten, and the task does not list it under Tests the decisions break. kb.v2 has no batch key (CreateItem.key reserved), so no kb refusal names a key; D3 says only that a @key resolves to the IRI the seam gives that create, and nothing what a key two creates carry is. With no link written to the shared key, the batch lands. Evidence: tests/test_make_several_changes_at_once.py:163 assert faults and any(fault.rule == LINK and key in printed(fault) for fault in faults) fails: kb's answer to the same BatchCreate, asked after shop-knol's, is two faults rule 'identity', 'an IRI names one artifact; the store already holds one at ...', since shop-knol's apply had landed both creates. Decision needed: who refuses a key two creates carry under kb.v2 (shop-knol in its own words, which the Then's kb-words oracle does not allow), and what the Then becomes. Green in this slice: 201 of 202 (the rest of the suite under kb 0.9.0). Red: that scenario.
- 2026-10-12 Re-planned the hand-back of slice 83 (planner row, no scenario line changes): Tests the decisions break gains make-several-changes-at-once / Two creates carrying the same key leave the shop untouched: with kb.v2's keys gone (D3) shop-knol refuses a key two creates carry before asking kb, naming the key, nothing landing; its Then step compares with shop-knol's own line, not kb's answer
- 2026-10-12 QUESTION FOR THE SPEC: spec/index.md says kb v0.6.0 is pinned today; it is v0.9.0 now
- 2026-10-12 slice 83 green. Someone can now: run shop-knol against kb v0.9.0 (contract kb.v2), every name still read and printed as <kind>/<name>, the shop's types created at https://missingmass.io/shopsystem/<type> and its artifacts at their D3 IRIs. Review Focus: 1, a second create of one title refused in kb's words (tag/pricing: identity: an IRI names one artifact; the store already holds one at '<IRI>'), exit 1, not numbered; 2, a batch's @t link lands on the tag the keyed create made (read shows tags: [tag/produce] and its reference); 3, types lists names and types decision shows id schema/decision, type schema, schema_version 1, and validate after writing a type to version 2 lists behind: artifact, schema_version 1, current 2; 4, init over a store kb 0.6.0 started: through KB_ROOT, kb's 'unreadable: the store at <root> was made by an earlier version of kb' one line exit 1; named as a directory or from inside it, kb.init's 'a store is never started over another' one line exit 1, no traceback either way; 5, the v1 forms are gone, every remaining kind/schema_version/schema/ hit is a kb.v2 field or a printed D1 name, and the diff outside the seams, types/ and pyproject.toml is CLAUDE.md, batch.py and three test modules, listed in the report. Slice 84 not credited (still xfailed). Surprised by: kb.v2 has no batch key, so a key two creates carry went unrefused until the ruling put the refusal in batch.py; three Thens read kb's ids raw past the test seam; a stale create at @1 is accepted, so the seam reads the type's version. Open questions: none. Next: slice 84.
- 2026-10-12 Suite: 202 passed, 0 failed, 37 expected at aaac283 in 35 s
- 2026-10-12 QUESTION FOR THE SPEC: list-what-the-shop-holds has no scenario listing by a field that holds a link ('The user lists the shops whose product is a given product'); batch 19's fix wave pins it with a plain test, tests/test_list_what_the_shop_holds.py::test_listing_by_a_link_field_shows_the_artifacts_linking_there, until one is formulated
- 2026-10-12 QUESTION FOR THE SPEC: types <name> now shows a type's body in kb.v2's grammar: targets: [schema/shop] (was [shop]) and $ref: kb:https://missingmass.io/shopsystem/shop-artifact@1 (was kb:schema/shop-artifact); schema/x strings in content are not translated. Repro: shop-knol types capability in a fresh store. Slice 85 owns how a type is shown (batch 19 branch review M7)
- 2026-10-12 batch 19 fix wave green. Someone can now: list one type by a field holding a link, --where <field>=<kind>/<name>, and see the artifacts linking there (kb.v2 is sent the IRI). Fixed besides: the review's M1, M2, M3, M4 (but cli.py, backlog), M5, M8; the backlog lines of 2026-10-12 on list --where and on the unreachable shared-key branch are done. Surprised by: no scenario lists by a link field, so the fix is pinned by a plain test beside the feature's steps; ruff's I001 fix on cli.py would take it over 250 lines. Open questions: the two spec questions above. Next: slice 84.
- 2026-10-12 Suite: 203 passed, 0 failed, 37 expected at 028dbbd in 34 s
