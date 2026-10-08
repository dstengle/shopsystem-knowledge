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

## Slice 60: The shop's ten types
- Kind: capability
- Scenarios: start-a-knowledge-base / The user starts a knowledge base and the shop's types are ready; use-the-shops-types / The user asks which types the shop holds; use-the-shops-types / Every artifact of the shop's ten types can carry an owner, a status and tags (all rows)
- Observable: a new knowledge base holds products, shops, capabilities, the reshaped decision and the new feature beside the five kept types, and each of the ten carries an owner, a status and tags
- Unknown: whether the reshaped decision, whose required shop needs a shop and a product, can stand in for every decision today's scenarios record without changing what any of them says
- Needs: every existing scenario that records a decision gives it the reshaped decision's required fields (statement, date, number, shop) as step data only, per integration answer 2; no Given, When or Then changes
- Status: green

## Slice 61: Publish a shop's index
- Kind: capability
- Scenarios: publish-a-shops-spec / The user publishes a shop's spec and the directory holds its index
- Observable: the user publishes a shop into a directory and finds spec/index.md laid out from the shop, its constraints and its reading order, with the knowledge base unchanged
- Unknown: whether a publisher made from a shop can read the shop's other artifacts through the contract and give back files in more than one directory
- Needs: none
- Status: green

## Slice 62: Short fields and links into Behaviour lines
- Kind: capability
- Scenarios: use-the-shops-types / The user reads a product, a shop, a capability, a decision or a feature at a glance (all rows); The user reads an artifact holding parts at a glance; The user records an artifact holding parts; The user records a gist or a statement longer than 200 characters (all rows); The user records a gist or a statement that holds a line break (all rows); The user records a part whose title is longer than 80 characters; The user records a part whose title holds a line break; The user records a scenario whose uses points at anything but a capability; The user records a feature; The user records a scenario with labels
- Observable: the user records a feature whose scenarios link into a capability's Behaviour lines, sees parts by title at a glance, and is refused a gist, statement or part title that is too long or breaks a line
- Unknown: whether a link into a capability's Behaviour line, given in a file the user records, is kept and shown back through shop-knol as the link it was given
- Needs: none
- Status: green

## Slice 63: Publish a shop's capabilities
- Kind: capability
- Scenarios: publish-a-shops-spec / The user publishes a shop's spec and the directory holds a file for each capability; The user publishes a shop's spec and a capability's file is named from its title (all rows)
- Observable: the user publishes a shop and finds one file per capability, named from its title, with frontmatter, Purpose, Behaviour, Implementation and Not yet
- Unknown: whether a capability page can keep its frontmatter first and lay out its sections with the layout the markdown and agent publishers share
- Needs: none
- Status: green

## Slice 64: Publish a shop's decisions
- Kind: capability
- Scenarios: publish-a-shops-spec / The user publishes a shop's spec and the directory holds its ledger; The user publishes a shop's spec and the directory holds a record for each decision; The user publishes a shop's spec and a decision's record is named from its number and title (all rows); The user publishes a shop's spec and every ledger entry is a decision the knowledge base holds; The user publishes a shop's spec whose capabilities rest on a decision of another shop
- Observable: the user publishes a shop and finds its ledger, listing its own decisions and then those of other shops its capabilities rest on, and one numbered record per decision of its own
- Unknown: how a publisher finds the decisions of other shops that a shop's capabilities rest on, and those shops' names, through the contract
- Needs: none
- Status: green

## Slice 65: Publish a shop's feature files
- Kind: capability
- Scenarios: publish-a-shops-spec / The user publishes a shop's spec and the directory holds a feature file for each formulated capability
- Observable: the user publishes a shop and finds a Gherkin feature file for each formulated capability, its scenarios, labels, steps, tables and examples laid out as the shop writes them
- Unknown: whether a feature's scenarios, as parts holding steps, tables, docstrings and examples, lay out as Gherkin the shop's own feature files would accept as written
- Needs: none
- Status: green

## Slice 66: See what is formulated
- Kind: capability
- Scenarios: see-what-is-formulated / The user asks what is formulated in a shop, and is shown each line no scenario formulates; The user asks what is formulated in a shop, and is shown each line more than one scenario formulates; Where some of the shop's lines have no scenario, the user asks what is formulated and is answered, not refused; Every one of the shop's lines is formulated by exactly one scenario, and the user is shown none unformulated and none formulated twice; The user asks what is formulated in a shop the knowledge base does not hold
- Observable: the user asks shop-knol coverage for a shop and is shown the Behaviour lines no scenario formulates and those more than one does
- Unknown: how to count the scenarios that formulate each of a shop's Behaviour lines through the contract, given a link into a part counts as a link into its artifact
- Needs: none
- Status: green

## Slice 67: The published-from line and publishing refusals
- Kind: capability
- Scenarios: publish-a-shops-spec / The user publishes a shop's spec and every file it writes carries the published-from line (all rows); Publishing is refused when a capability names the shop but is not in the shop's reading order; Publishing is refused when a capability in the shop's reading order names another shop; Publishing is refused when two of the shop's capabilities would be published under one file name; Publishing is refused when two of the shop's decisions would be published under one file name; Publishing is refused when two of the shop's decisions carry one number; Publishing is refused when two features formulate one of the shop's capabilities; Publishing is refused when a scenario's uses points at a capability of its own shop
- Observable: every file a publish writes says it was published from the knowledge base and must not be edited, and a shop whose spec would publish inconsistently is refused with nothing written
- Unknown: none
- Needs: none
- Status: green

## Slice 67.1: A ragged feature table is refused
- Kind: capability
- Scenarios: publish-a-shops-spec / Publishing is refused when a table in a feature has rows of different widths
- Observable: publishing a shop whose feature holds a table with rows of different widths is refused in plain words naming the scenario, never a traceback
- Unknown: none
- Needs: none
- Status: green

## Log
- 2026-10-07 Batch batch15 archived to archive/2026-09-23-shop-knowledge-slices-batch15.md; last 2026-10-07 Suite: 134 passed, 0 failed at 09bc387 in 10.7 s
- 2026-10-07 Suite: 134 passed, 0 failed at 09bc387 in 10.7 s
- 2026-10-07 Suite: 132 passed, 21 failed at f965ec0 in 12.8 s; failing: the new and changed scenarios of use-the-shops-types and start-a-knowledge-base (publish-a-shops-spec and see-what-is-formulated not yet collected)
- 2026-10-07 Probe: kb v0.6.0, a schema with maxLength 200 and pattern ^[^\n]*$ on gist -> a 201-character gist refused (rule maxLength, place gist), a gist holding a line break refused (rule pattern)
- 2026-10-07 Probe: kb v0.6.0, a feature scenario's formulates ref with parts: true -> capability/checkout#behaviour/show-the-price accepted; #behaviour/nope refused (rule ref, place scenarios/0/formulates); a glance at the capability shows the part's title and counts the feature inbound
- 2026-10-07 Probe: kb v0.6.0, Read whole at locator place behaviour/show-the-price -> the whole capability comes back, not the one item (no scenario relies on reading one part)
- 2026-10-07 Probe: kb v0.6.0 BatchCreateRequest and BatchReplaceRequest fields -> items, signature only: no validate-only mode
- 2026-10-07 REQUEST kb: a validate-only mode on BatchCreate and BatchReplace, checking a batch as it would land and landing nothing (adrs/0053; spec/capabilities/make-several-changes-at-once.md Not yet). No slice of batch 16 waits on it.
- 2026-10-07 REQUEST shopsystem-bdd: capability-writer and feature-formulator read kb through a read-only shop-knol allowlist (read, list, refs, search, types) and draft shop-knol apply batch files; integrating-a-proposal's and formulating-features' apply steps validate, gate, apply creates then writes, publish with render spec, and commit; the capability format notes the published-from line (adrs/0052, 0053). Moving a shop's real spec into kb waits on it.
- 2026-10-07 QUESTION FOR THE SPEC: publish-a-shops-spec, a decision named by the decisions of two shops: refused (a decision belongs to one shop, naming both shops, nothing written), or allowed (each shop publishes it as its own, each judging its numbers apart)? No principle decides it; for the person. No slice of batch 16 depends on it.
- 2026-10-07 Slice 67 gains publish-a-shops-spec / Publishing is refused when a capability of the shop rests on a decision no shop names (line added 2026-10-07 under the person's delegation, settled by principle; formulated by the small-change path)
- 2026-10-07 Slice 60's Unknown, re-read after decision/a-shop-names-its-decisions: whether the reshaped decision (statement, date and number required, no shop link) can stand in for every decision today's scenarios record without changing what any of them observes; its Needs reads statement, date and number only
- 2026-10-07 slice 60 green. Someone can now: start a knowledge base holding the shop's ten types (product, shop, capability, the reshaped decision and the new feature beside the five kept), and record each with an owner, a status and tags.
  Surprised by: kb's Replace takes a decision's whole content, so the four steps that write a whole decision (batch_writes, review-who-changed-what, revise-an-artifact, read-an-artifact's tagging of the older decision) give statement, date and number too, beside the creates. Type-order probe (.superpowers/batch16/slice60/probe_order.py, fresh v0.6.0 stores): kb accepts a link whose targets name a kind not yet defined, so shop and capability load in either order; TYPES is shop-artifact, tag, product, shop, capability, decision, work-item, feature, role, step, process. 16 test modules gained decision fields, all from tests/decision_fields.py (decided(n)). Needing nothing but data: every existing scenario that records a decision, and the decision and feature rows of the ten-types outline (the work item, role, process, step and tag rows needed nothing); the two Thens that count the types needed new step text. Types carry title as required beside the listed fields, as every existing type does; no length or line-break limits yet (slice 62).
  Open questions: none. Next: slice 61.
- 2026-10-07 Suite: 137 passed, 16 failed at e6044f0 in 13.7 s; failing: slice 62's 16 rows of use-the-shops-types
- 2026-10-07 slice 61 green. Someone can now: run shop-knol render spec <shop> --to <dir> and get spec/index.md from the shop, with the shared test shop built by tests/spec_shop.py. Surprised by: a shop's complete content (reading order, constraints) can only be written after its capabilities exist, since they link both ways, and a write refuses the title in content. Open questions: a constraint pinned in no capability is unhandled (no scenario covers it; the index code would raise); the published-from line is not yet written (slice with that scenario). Next: slice 62.
- 2026-10-07 Suite: 138 passed, 46 failed at f4f1826 in 221 s; failing: slice 62's 16 rows of use-the-shops-types and 30 other rows of publish-a-shops-spec
- 2026-10-07 slice 61 open question ruled by the controller: a constraint with no pinned_in (absent or empty) is laid out without a Pinned-in clause; fixed at 1359d57, probed by hand, no new scenario.
- 2026-10-07 slice 62 green. Someone can now: record a product, shop, capability, decision or feature and be refused when a gist or statement runs past 200 characters, a part title past 80, or either holds a line break, read it at a glance as short lines and links, and record scenarios linking to one Behaviour line. Surprised by: nothing; the limits were the only change under src/ and the uses scenario was already enforced by the link's target. Open questions: a pattern ^[^\n]*$ lets one trailing line break through where the matcher's $ stops before it; no scenario asks. Next: slice 63.
- 2026-10-07 Suite: 154 passed, 30 failed at 0cc0361 in 245 s; failing: the 30 publish-a-shops-spec scenarios still red at the start
- 2026-10-07 slice 62 open question ruled: a trailing line break is a defect; the pattern is now ^[^\n]*(?!\n)$, probed against kb v0.6.0 (abc kept; abc+newline and a+newline+b refused as rule pattern).
- 2026-10-07 slice 63 green. Someone can now: publish a shop's spec and find one page for each capability in its reading order under spec/capabilities, named from its title, with frontmatter, Purpose, Behaviour, other sections and Not yet.
  Surprised by: the outline's Then for the feature file cannot see the file (slice 65 writes it), so it reads the capability page's formulated_as naming features/<name>.feature; the Given adds its capability to the Background's shop and its reading order; names.from_title already held the whole rule; List filters on the link field formulates. Review Focus 1: a title leaving no name (such as a lone registered-sign) is refused by kb at record, so no empty file name reaches the publisher; 'Café ®' publishes as caf.md. Review Focus 3: publishing over an older spec writes the files over; a removed capability's page stays in the directory (no line says otherwise, recorded, not changed).
  Open questions: should publishing remove pages of capabilities no longer in the shop (no line says)? Next: slice 64.
- 2026-10-07 Suite: 162 passed, 22 failed at 5bbb681 in 18 s; failing: the 22 publish-a-shops-spec scenarios of slices 64 to 67
- 2026-10-07 slice 64 green. Someone can now: publish a shop's ledger and one ADR record per decision with shop-knol render spec. Surprised by: the brief carried no Review Focus 2 text, so it was not probed; a decision a capability rests on that no shop names raises IndexError in spec_decisions._others (Task 8 turns it into the refusal); spec_shop gained supersedes/extends/revisit_when on its second decision so the ledger and record cover them. Open questions: a foreign decision's source names the shop by its kb name (shop/<slug>), not its title. Next: slice 65.
- 2026-10-07 Suite: 170 passed, 14 failed at 1f28dbb in 273 s; failing: the 14 publish-a-shops-spec scenarios of slices 65 to 67
- 2026-10-07 slice 65 green. Someone can now: publish a feature file per formulated capability with render spec, parseable by the Gherkin parser with the scenario count and titles of the feature. Surprised by: nothing; the feature file is laid out in renderers/gherkin.py (new row in the module map) and the Task 4 outline Then now checks the file exists. Open questions: none (Review Focus 5: docstring with triple quotes, a pipe in a cell, and a step with table and docstring all publish unparseable files; logged as Backlog). Next: slice 66.
- 2026-10-07 Suite: 171 passed, 13 failed at 2f2c7c6 in 268 s; failing: the 13 publish-a-shops-spec scenarios of slices 66 and 67
- 2026-10-07 slice 66 green. Someone can now: run shop-knol coverage <shop> and see which of the shop's Behaviour lines no scenario formulates and which more than one does.
  Surprised by: nothing; the line handle is the part id kb already gives, so no renaming rule was needed. Review Focus 4: coverage named a capability gives one line, 'a coverage is made from a shop; this one is a capability', exit 1; a decision or missing shop gives kb's 'holds nothing by the name', exit 1; no traceback, no Backlog line needed.
  Open questions: none. Next: slice 67.
- 2026-10-07 Suite: 176 passed, 13 failed at 8e80fe4 in 271 s; failing: the 13 publish-a-shops-spec scenarios of slice 67
- 2026-10-07 slice 67 green. Someone can now: publish a shop's spec with every file carrying its published-from line, and be refused, with nothing written and every fault named, when the shop would publish inconsistently. Surprised by: the earlier slices' whole-file expectations (index, capabilities, ledger, records) had to carry the line; the unowned-decision IndexError in spec_decisions is now unreachable because spec_faults runs first. Open questions: none. Next: none (batch 16 ends).
- 2026-10-07 Suite: 189 passed, 0 failed at 0e1e354 in 21 s
- 2026-10-07 QUESTION FOR THE SPEC: use-the-shops-types, what a capability rests on: the capability type's rests_on targets decisions only, but all 18 of this repository's capabilities rest on other capabilities too (e.g. start-a-knowledge-base rests on capability/find-the-knowledge-base), so the types cannot hold this repository's own spec as written. Widen rests_on to capabilities, or move such links to a field of their own? For the person; it blocks moving a real shop's spec into kb, not batch 16. (batch 16's branch review)
- 2026-10-07 QUESTION FOR THE SPEC: see-what-is-formulated, which capabilities coverage counts: only those in the shop's reading order today, so a capability naming the shop but left out of the order has its lines silently omitted. Count every capability naming the shop, or refuse as publishing does? For the person. (batch 16's branch review)
- 2026-10-07 QUESTION FOR THE SPEC: publish-a-shops-spec, a capability removed from the shop keeps its old page and feature file when publishing over an older spec, and the stale feature file keeps running as a test. Should publishing remove files of artifacts no longer in the shop? Deleting files is the person's call. (Review Focus 3; batch 16's branch review)
- 2026-10-07 Next batch: the plan's kb-import check matches from kb_oracle; use grep -rnE "^\s*(from kb[ .]|import kb\b)" src tests | grep -vE "kb\.client|kb\.content|kb\.contract|import kb$|from kb import (init|NotStarted)|kb\.testing" (from batch 16's branch review)
- 2026-10-08 slice 67.1 green. Someone can now: publish a shop's spec and be refused, naming the scenario, where a table's rows differ in width. Surprised by: nothing. Open questions: none. Fix wave items 2-5 (CLAUDE.md rows per adr 0057, coverage's own wording, tests read kb's minted ids, pytest-bdd<9) done at e81bc91; publish_spec_index.py and publish_spec_capabilities.py still derive page names from minted slugs.
- 2026-10-08 Suite: 190 passed, 0 failed at e81bc91 in 23 s
- 2026-10-08 Suite: 190 passed, 0 failed at e7d73ea in 22.4 s (batch 16's fix-wave re-review, make test at HEAD)
- 2026-10-08 Batch 16 branch review: with fixes; fix wave (slice 67.1, CLAUDE.md per adrs/0057, coverage wording, tests read kb's ids, pytest-bdd <9) re-reviewed, all addressed
