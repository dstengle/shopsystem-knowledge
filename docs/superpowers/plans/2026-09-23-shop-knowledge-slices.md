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
- Status: planned

## Slice 80: A test seam for what tests hand kb, first group
- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> 202 passed, 0 failed, 37 expected; a search shows the oracle, the refused-files steps and the spec attempt build no kb request naming a kind or id directly
- Observable: Tests that ask kb directly do so through one helper
- Unknown: whether one helper can stand for every request a test hands kb
- Needs: none
- Lands: 0 production, 4 test
- Status: planned

## Slice 81: The test seam, second group
- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> 202 passed, 0 failed, 37 expected; a search shows the start steps, the batch steps and conftest build no kb request naming a kind or id directly
- Observable: Start and batch steps ask kb through the test seam
- Unknown: none
- Needs: none
- Lands: 0 production, 4 test
- Status: planned

## Slice 82: The test seam, third group
- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> 202 passed, 0 failed, 37 expected; a search over tests/ finds kind, schema_version, key and schema/ ids handed to kb only in the test seam
- Observable: No test outside the seam spells a kb.v1 form
- Unknown: none
- Needs: none
- Lands: 0 production, 4 test
- Status: planned

## Slice 83: kb pinned at v0.9.0
- Kind: enabling
- Check: `.venv/bin/python -c "import kb.contract.kb_pb2 as m; print(m.DESCRIPTOR.package)"` -> kb.v2; `.venv/bin/python -m pytest -q` -> 202 passed, 0 failed, 37 expected (fewer expected where a scenario goes green, credited here); a search over src/ and tests/ finds no kb.v1 field
- Observable: shop-knol works against kb.v2 with every name the user sees unchanged
- Unknown: whether everything the suite passes on kb.v1 passes on kb.v2 through the two seams alone
- Needs: the shop's types written as kb.v2 type artifacts
- Lands: 3 production, 2 test
- Status: planned

## Slice 84: The shop's types at their IRIs
- Kind: capability
- Scenarios: start-a-knowledge-base / The user starts a knowledge base and each of the shop's types is held at its own IRI, its current version at that version's IRI
- Observable: init furnishes each of the shop's types at https://missingmass.io/shopsystem/<type>, its version at <type>@<n>
- Unknown: how bootstrap names a type and its version IRI where kb.v2 asks the client to
- Needs: none
- Status: planned

## Slice 85: Names shown short
- Kind: capability
- Scenarios: name-an-artifact / Whenever shop-knol shows the user the name of an artifact, it is shown short, in a JSON answer as in a YAML one; name-an-artifact / Whenever shop-knol shows the user the name of a shop or a product, it is shown short, in a JSON answer as in a YAML one; name-an-artifact / Whenever shop-knol shows the user a type beside an artifact, it is shown by its name and the version that artifact names, in a JSON answer as in a YAML one; name-an-artifact / Whenever shop-knol shows the user a type on its own, it is shown by its name and its current version, in a JSON answer as in a YAML one
- Observable: Every answer shows IRIs shortened by the shop's prefixes
- Unknown: whether one module can shorten every IRI every answer prints
- Needs: none
- Status: planned

## Slice 86: Names taken short, full or in a context
- Kind: capability
- Scenarios: name-an-artifact / The user names an artifact by its short IRI, whatever context it is in; name-an-artifact / The user names an artifact by its full IRI, whatever context it is in; name-an-artifact / Where SHOP_CONTEXT names a context, the user names an artifact by its name alone; name-an-artifact / Where SHOP_CONTEXT names a context, the user names an artifact by its type and its name; name-an-artifact / Where SHOP_CONTEXT names a context, a name alone carried by artifacts of more than one type in it is refused; name-an-artifact / A name that is neither a short nor a full IRI, while SHOP_CONTEXT is not set, is refused; name-an-artifact / A name that is neither a short nor a full IRI, while SHOP_CONTEXT is set empty, is refused
- Observable: A user names an artifact short, full, or by name within SHOP_CONTEXT
- Unknown: how a bare name is resolved against SHOP_CONTEXT when more than one type may carry it
- Needs: none
- Status: planned

## Slice 87: The user names what they record
- Kind: capability
- Scenarios: record-an-artifact / The user records a file as a decision under a name of their choosing; record-an-artifact / The user records an artifact naming some of its parts; record-an-artifact / An artifact recorded without a name is refused; record-an-artifact / An artifact recorded under a name the shop already holds is refused; record-an-artifact / The user records a file whose title is written as a date; record-an-artifact / The user records a file whose title is written as a yes; use-the-shops-types / The user records an artifact holding parts without naming them
- Observable: create takes the artifact's name and its parts' names, and no longer mints one from a title
- Unknown: how a part named by the user and a part left unnamed reach kb.v2's create
- Needs: none
- Status: planned

## Slice 88: A batch names what it creates
- Kind: capability
- Scenarios: make-several-changes-at-once / The user applies a batch of creates, saying who they are and why; make-several-changes-at-once / The user applies a batch of creates naming some of their parts; make-several-changes-at-once / The user applies a batch of creates in which a link names the IRI one of its creates carries; make-several-changes-at-once / A create in a batch carrying no name leaves the shop untouched; make-several-changes-at-once / A create in a batch carrying a name the shop already holds leaves the shop untouched; make-several-changes-at-once / Two creates in a batch carrying one name leave the shop untouched
- Observable: apply carries each create's name, and links in a batch name IRIs
- Unknown: whether a batch's names are refused whole before kb is asked or by kb's own refusal
- Needs: none
- Status: planned

## Slice 89: The types' second versions
- Kind: capability
- Scenarios: use-the-shops-types / The user records a capability with an "Implementation, may change" section; use-the-shops-types / The user records a shop with a "Mechanisms every command shares" section; publish-a-shops-spec / The user publishes a shop's spec and a capability's page holds its "Implementation, may change" section; publish-a-shops-spec / The user publishes the spec of a shop holding a "Mechanisms every command shares" section
- Observable: A capability holds an Implementation section and a shop a mechanisms section, each published
- Unknown: how a type's second version is furnished beside its first
- Needs: none
- Status: planned

## Slice 90: Placeholders marked and checked
- Kind: capability
- Scenarios: read-an-artifact / The user reads a decision holding a link to something the knowledge base does not hold; read-an-artifact / The user reads the whole decision holding a link to something the knowledge base does not hold; read-an-artifact / The user reads a decision with the things it points at filled in, and one of its links lands on something the knowledge base does not hold; follow-the-links / The user follows the links out of a decision holding a link to something the knowledge base does not hold; check-the-knowledge-base / The user checks a knowledge base where an artifact links to an artifact the knowledge base does not hold
- Observable: read and refs mark a link to nothing held; validate fails on it
- Unknown: how kb's placeholders become a mark in a read and a fault in a check
- Needs: none
- Status: planned

## Slice 91: Published files named from IRIs
- Kind: capability
- Scenarios: publish-a-shops-spec / The user publishes a shop's spec and a capability's file is named from the name in its IRI; publish-a-shops-spec / The user publishes a shop's spec and a decision's record is named from its number and the name in its IRI; publish-a-shops-spec / The user publishes a shop's spec into a directory holding files published earlier, and those this publish does not write are deleted; publish-a-shops-spec / Publishing is refused when two of the shop's capabilities would be published under one file name; publish-a-shops-spec / Publishing is refused when two of the shop's decisions would be published under one file name; publish-a-shops-spec / Publishing is refused when an artifact the shop's spec would publish carries a link to an artifact the knowledge base does not hold
- Observable: render spec names every page from the name in its artifact's IRI and refuses a link to nothing held
- Unknown: whether names from IRIs replace names from titles everywhere the spec renderer names a file
- Needs: none
- Status: planned

## Slice 92: Export the knowledge base
- Kind: capability
- Scenarios: export-the-knowledge-base / The user exports the knowledge base into an empty directory; export-the-knowledge-base / The user exports one context into an empty directory; export-the-knowledge-base / The user exports the whole knowledge base and is shown its position; export-the-knowledge-base / The user exports one context and is shown the knowledge base's position, not the context's last change; export-the-knowledge-base / Exporting into a directory that is not empty is refused
- Observable: shop-knol export writes kb's streamed export, whole or by context, into an empty directory
- Unknown: how kb's streamed export is written to files and its position shown
- Needs: none
- Status: planned

## Satisfied by existing behaviour

- none

## Backlog

- 2026-09-28 `read <id> --section ""` answers the summary and `journal --artifact ""` the whole history, where "a name given empty names no place" would refuse them; these arguments default to `""`, so telling "given empty" apart needs another default. No capability line names them yet (from batch 13's review, routed to formulation).
- 2026-09-28 A relative `--from` or `--to` named from a removed working directory is refused in the operating system's words (`d.yaml: No such file or directory`), where the directory being gone is the cause. No line names it (from batch 13's review).
- 2026-10-05 A knowledge base whose furnishing stopped at a refused Create cannot be finished by `init`: it keeps the shop's types created before the refusal, and a second `init` refuses it as not empty, naming them. Reproduction: an operator-started store named by KB_ROOT, `init` run with the stand-in (`driver.answering`) answering the Create titled `Decision` with a refusal, then `init` again without it: exit 1, `<KB_ROOT>: it is not empty: it holds the types decision, shop-artifact, tag` (decision is there because the stand-in asks the real kb first). No capability line says what a half-furnished knowledge base is (slice 55's Review Focus 2 probe, routed to formulation).
- 2026-10-05 A create in a batch given `key: ""` lands as a create carrying no key: the batch shape takes it as a string and contract v1's `CreateItem.key` cannot tell empty from absent, so kb is never asked. Reproduction: `shop-knol apply` of a batch holding one decision create with `key: ""`: exit 0, the decision created. A link written `@` alone is refused in kb's words (`work-item/start-weekly-price-reviews at decisions/0: a link must land on a node of a kind the type allows; '@' does not`, exit 1). No line says whether an empty key is a key (slice 56's Review Focus 4 probe, routed to formulation).
- 2026-10-05 `types shop-artifact` and `types schema` are shown whole, as kb holds them, exit 0: the command passes kb's read through and names no one of the seven as the only ones readable. Review Focus 5 asked for one line; only `nonesuch` (and a path such as `a/b`) is refused in one line, in kb's words. Reproduction: `shop-knol types schema` in a started knowledge base.
- 2026-10-06 init over a store kb cannot read hides the damage behind kb.init's reason: garbage in the store's database, then `shop-knol init` from a directory below it prints "stores do not nest" where `list` prints that the database cannot be read (start's finding does not tell a damaged store from a found one). From batch 14's branch review.
- 2026-10-06 A removed working directory with KB_ROOT naming an empty store: `shop-knol init` says the directory is gone, where find-the-knowledge-base answers from KB_ROOT. Also a question for the spec (from batch 14's branch review).
- 2026-10-06 A store found upward that holds other types is refused "it is not empty: …" with nothing naming the knowledge base: how init names one found upward is for formulation (from batch 14's branch review).
- 2026-10-06 The stand-in's `from_kb` would turn a refusal answer into a result (`tests/stand_in/sitecustomize.py`); no step writes that combination (from Task 2's review).
- 2026-10-06 KB_ROOT naming the knowledge base the user works inside is refused "it already holds the shop's knowledge" (a ruling under the person's delegation), where the "inside" line could also apply: for the person to confirm, with an Examples row (from Task 5.1's review).
- 2026-10-07 init with nothing named, where kb finds a connection to a server hosting a store holding types other than the shop's, is refused as not empty but names no knowledge base: stderr is 'it is not empty: it holds the types recipe, supplier' (the Fault's artifact empty), while the already-holds refusal of a served store names its address. Reproduction: .superpowers/batch15/probe55-1/scripts/probe.py <empty scratch dir> (kb.init a store, the operator creates schema Recipe and Supplier, kb.testing.served(store, office), shop-knol init from office with KB_ROOT unset). Whether it should name the address as already-holds does is for the person; the not-empty outline has no server row.
- 2026-10-07 init over a damaged connection to a server hides the damage behind kb.init's reason: a garbage kb/server.yaml in the working directory, then `shop-knol init` prints 'a store goes in a place of its own, and <dir> already holds something in that place' where `list --type schema --ids` prints that the connection cannot be read or names no address. Same class as the damaged-store entry. (slice 55.2's Review Focus 4 probe)
- 2026-10-07 If the session guard refuses in the xdist workers only, each worker shows a "node down" traceback and the run exits 5 instead of one line and exit 4 (session_guard.py pytest_sessionstart). Reproduction: a scratch plugin pointing only the workers' guard at a store, then `make test` (slice 52.1's log). From batch 15's review.
- 2026-10-07 The served-store fixture's serve() does not forward kb.testing.served's clock, so a scenario that sets the day (driver.at) and writes through a server would be stamped with the machine's day. No scenario does today. From batch 15's review.
- 2026-10-07 tests/start_not_empty.py's _noted does not check the exit code of the journal read it records, so a failed before-read makes "nothing changes" compare empty with empty for the KB_ROOT and named-directory rows. From batch 15's review.
- 2026-10-07 init._reached_at compares where().root with the named root even when where() found nothing (root "" resolves to the process's working directory); harmless today since the List is refused and kb.init's refusal re-raised, but the intent is obscure: return False when where() carries faults. Reproduction: `shop-knol init <dir>` with a garbage connection in <dir>, naming `.` versus another path. From batch 15's fix-wave re-review.
- 2026-10-07 Probe stores from earlier batches sit inside the checkout under .superpowers/ (batch4 to batch14, r5): a shop-knol run started inside one finds it, and the suite's guard looks upward only. Clean them up, or keep probes in the test temp dir. From batch 15's fix-wave re-review.
- 2026-10-07 A feature file publishes unparseable where a docstring line holds three double quotes, where a table cell holds a pipe, or where one step has both a table and a docstring (renderers/gherkin.py writes them verbatim). Reproduce: gherkin.feature_file with a step docstring 'a\n"""\nb' or table cell 'a|b', parse with pytest_bdd.parser.FeatureParser: TokenError / inconsistent cell count.
- 2026-10-07 A capability listed twice in a shop's reading order: publishing refuses it as sharing a file with itself (capability/restock: would share the file spec/capabilities/restock.md with capability/restock) and coverage lists each line twice. Repro: reading_order [c, c], then render spec and coverage. (from batch 16's branch review)
- 2026-10-07 A decision named by two shops: the ledger's source silently takes the first shop Follow returns (renderers/spec_decisions.py). Repro: shops Aisles and Bays both name decision/shared-one, a capability of Shelves rests on it: source shop/aisles. Waits on the logged question. (from batch 16's branch review)
- 2026-10-07 A carriage return, U+2028 or U+0085 passes the one-line pattern of a gist, statement or part title. Repro: create product with gist "a\rb", "a\u2028b" or "a\x85b": kept, exit 0. (from batch 16's branch review)
- 2026-10-07 A decision date of 2026-13-99 is accepted: the pattern checks digits, not a real day. Repro: create decision with that date: exit 0. (from batch 16's branch review)
- 2026-10-07 Gherkin is laid out verbatim: a label without @ is dropped by the parser; a description line starting with Given parses as a step; one starting with # vanishes as a comment; a step text holding a line break adds a step. Repro: gherkin.feature_file with each input, parsed by pytest-bdd's FeatureParser. Extends the earlier docstring/pipe backlog line. (from batch 16's branch review)
- 2026-10-08 tests/publish_spec_index.py:34 and tests/publish_spec_capabilities.py:37 take the expected page name from kb's minted id, while the publisher names pages with names.from_title: the Thens pass only while kb's slug rule agrees. Build them with names.from_title over spec_shop's titles, as publish_spec_from.py does; tests/publish_spec_decisions.py:12 hand-copies the naming rule the same way. (from batch 16's fix-wave re-review)
- 2026-10-08 An unreadable file (permission denied) directly in spec/capabilities/, features/ or adrs/ refuses the whole publish of a shop's spec, where the plan's reading would leave it. Repro: chmod 000 <dir>/adrs/locked.md, then shop-knol render spec <shop> --to <dir>: 'Permission denied', nothing written. Leave or refuse is for the spec. (from batch 17's Task 3 review)
- 2026-10-08 The published index names a retired capability a constraint is pinned in (`Pinned in restock-the-shelves and count-the-stock`) though that capability is no longer published, so the link points at no page. Repro: build a shop, retire a capability a constraint pins, `shop-knol render spec <shop> --to d`, read d/spec/index.md. (from batch 17's slice 72 probe)
- 2026-10-08 Deleting stops at the first stale file it cannot remove, after the new files are written. Repro: a stale published file in <dir>/adrs, chmod 555 <dir>/adrs, render spec: new files written, stale one kept, 'Permission denied', exit 1. (from batch 17's branch review)
- 2026-10-08 Writes through a symlinked adrs/, features/ or spec/ land outside --to, for every renderer (predates batch 17). Repro: repo/adrs -> ../victim, render spec: the new ADR is written into victim/. (from batch 17's branch review)
- 2026-10-08 If finding a shop's capabilities ever returned nothing for a shop with published pages, publishing would delete them all as stale; a guard is optional. (from batch 17's branch review)
- 2026-10-08 A capability may depend on itself and publishes without complaint; no line says. Repro: depends_on [<itself>], render spec. (from batch 17's branch review)
- 2026-10-08 CLAUDE.md module map: the spec_faults.py row omits the ragged-table check, and the published.py row does not say a linked cleared directory has nothing deleted. (from batch 17's fix-wave re-review)
- 2026-10-08 Several unreadable files in one publish: only the first is named. Repro: chmod 000 on two stale published files in features/ and adrs/, render spec: one line, exit 1. (from batch 18's branch review)
- 2026-10-08 Slice 75's rows fail when the suite runs as root (chmod 000 does not stop root reading). Repro: -m slice-75 as root. Skip with a reason, or make the file unreadable another way. (from batch 18's branch review)
- 2026-10-08 A file publishing would write over but cannot write fails partway, earlier files staying written (predates batch 18). Repro: an existing spec/index.md chmod 444, render spec: earlier files written, then Permission denied. (from batch 18's branch review)
- 2026-10-08 spec_faults.py reads a constraint's title and a capability's status without a guard; only a store damaged outside the contract reaches it. (from batch 18's fix-wave re-review)

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
