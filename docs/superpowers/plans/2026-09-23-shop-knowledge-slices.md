# shop-knowledge slices

One living plan for shop-knowledge and kb until slice 1 is green, as both
specs' "Order of building" say. Every slice names the repository each
scenario runs in: `kb / <feature file> / <scenario>` runs in
`shopsystem-kb`, `shop-knowledge / <feature file> / <scenario>` runs here.
When slice 1 is green, kb is tagged 0.1, this repository pins it, and the
slices made only of kb scenarios move to kb's own plan.

Slice 1 is the walking skeleton the specs define. Slices 2 to 19 each
settle one unknown and are ordered by the size of it. Slices 20 to 47 have
no unknown: scenarios that share a feature and step definitions bundle into
one slice, and the slices are ordered by value, kb's slice ahead of the
shop-knowledge slice that needs it.

## Slice 1: Record a decision and read it back

- Kind: capability
- Scenarios: kb / start-a-store / The client starts a store; kb / define-a-type / The client defines a type; kb / create-an-artifact / The client creates an artifact; kb / read-an-artifact / The client reads a summary; shop-knowledge / record-a-decision / The user records a decision; shop-knowledge / read-back-what-the-shop-knows / The user reads a decision at a glance
- Observable: At a shell, a user starts a shop knowledge base, records a decision from a file saying who they are and why, and reads it back at a glance with stubs of what it points at and counts of what points at it, while the decision sits on disk as a file inside a commit.
- Unknown: Does one round trip pass through every layer: the command line, the in-process client, the contract's messages, schema validation, canonical YAML on disk, and a git commit?
- Needs: a runnable package in each repository with its feature suite wired to pytest-bdd, and shop-knowledge installing kb as an editable path dependency (every scenario); the contract file with the messages that starting a store, defining a type, creating, and reading a summary need (every scenario); the metaschema written when a store starts (the start scenario); writes landing as files and one commit in the store's git repository, which nothing here asserts on but without which the skeleton is not through every layer (the create and record scenarios); the shop's start command loading bootstrap types for decision, work item, and tag, flat or on a base as the implementer chooses since nothing here asserts on composition (the two shop-knowledge scenarios)
- Status: planned

## Slice 2: Two types share a shape

- Kind: stack
- Scenarios: kb / define-a-type / Two types share a shape
- Observable: A client defines a type that refers to a shape another stored type defines, and an artifact of the second type is checked against that shape.
- Unknown: Does a reference from one stored type into another resolve through the validator's registry when every type is itself an artifact in the store?
- Needs: none
- Status: planned

## Slice 3: A type built on a base

- Kind: stack
- Scenarios: kb / define-a-type / A type built on a shared base carries the base's fields and sections
- Observable: A client defines a decision type on a base that gives every artifact an owner and a status and a purpose section; a decision without an owner is refused, and one with everything reads back with the base's purpose before its own rationale.
- Unknown: Do kb's own keywords, required sections, references, parts, and summary fields, merge through composition with the base's part coming first?
- Needs: none
- Status: planned

## Slice 4: The shop's seven types

- Kind: capability
- Scenarios: shop-knowledge / start-a-shop-knowledge-base / The user starts a knowledge base and the shop's types are ready
- Observable: One command in an empty directory leaves a knowledge base that can hold decisions, features, work items, roles, processes, steps, and tags, and the user defines nothing of their own first.
- Unknown: Can the process type, whose steps are each either written in place or a reuse of a shared step with bindings, and which carry branches, be said in kb's schema language?
- Needs: the seven bootstrap types, the base they all build on, and whatever shared shapes the process and feature types refer to (this scenario)
- Status: planned

## Slice 5: Several changes land as one change

- Kind: stack
- Scenarios: kb / make-several-changes-in-one-go / The client makes several changes in one go
- Observable: A client sends a create and a change in one request, gets a result for each, and the store's history shows the two as one change.
- Unknown: Can the second operation in a set point at the artifact the first one creates, before either has landed?
- Needs: none
- Status: planned

## Slice 6: A bad set changes nothing

- Kind: stack
- Scenarios: kb / make-several-changes-in-one-go / One bad change in a set leaves the store untouched
- Observable: A client sends a set whose second change is missing a required section; the set is refused with every fault in it, and the store holds neither change.
- Unknown: Does a refusal at the second operation leave no trace of the first, both on disk and in the store as the same client then reads it?
- Needs: none
- Status: planned

## Slice 7: Every fault at once

- Kind: stack
- Scenarios: kb / create-an-artifact / An artifact with several faults reports them all
- Observable: A client creates a decision missing its purpose and pointing at a decision the store does not hold; both faults come back, each naming the artifact, the place, and the rule, and the store is unchanged.
- Unknown: Can violations from the JSON Schema validator and from kb's own rules be collected into one list, with the place given in the node-path form the contract uses?
- Needs: none
- Status: planned

## Slice 8: A refused change leaves the artifact as it was

- Kind: stack
- Scenarios: kb / change-an-artifact / A change that would break the type leaves the artifact as it was
- Observable: A client replaces a decision with content that has no purpose; the change is refused, and reading the decision gives what it held before at the version it held before.
- Unknown: After a refused write, does the store as the same client reads it, not only the files, still hold the old content at the old version?
- Needs: none
- Status: planned

## Slice 9: Every change leaves an entry

- Kind: stack
- Scenarios: kb / read-the-journal / Every change leaves an entry
- Observable: After a decision is created on one day and changed two days later, the journal for that decision shows two entries, each with when, which role, which piece of work, what it did, where, the version left behind, a fingerprint, and the message.
- Unknown: How do step definitions set the time kb stamps on an entry, so that two changes can be two days apart within one run?
- Needs: a journal entry written for every operation from here on (this scenario); an outside control of the clock (this scenario, and the since scenario later)
- Status: planned

## Slice 10: Every violation is reported

- Kind: stack
- Scenarios: kb / check-the-store / Every violation is reported
- Observable: A client checks a store holding an artifact missing a required section and another pointing at nothing, and both are reported, each naming the artifact, the place, and the rule.
- Unknown: How does a store come to hold a violation when every write is validated, and does loading such a store report it without failing?
- Needs: none
- Status: planned

## Slice 11: Search the prose, ranked

- Kind: stack
- Scenarios: kb / search-the-store / The client searches the prose
- Observable: A client searches for a word and gets each match with the title of the section it came from and a snippet, with the section that says the word most often first.
- Unknown: What index over sections gives ranking by how often the term occurs in a section, with the section title and a snippet in each result?
- Needs: none
- Status: planned

## Slice 12: Follow the links two steps out

- Kind: stack
- Scenarios: kb / follow-the-links / The client follows the links two steps out
- Observable: A client follows the links out of a decision two steps and gets the older decision and the tag it carries, each with the route taken to it.
- Unknown: How is the route to each artifact reached in two steps given back beside its stub?
- Needs: none
- Status: planned

## Slice 13: Change one node inside an artifact

- Kind: stack
- Scenarios: kb / change-an-artifact / The client changes one node inside an artifact
- Observable: A client replaces only the rationale of a decision, and the rest of the decision reads as before.
- Unknown: Can a write be addressed at a section inside an artifact and the whole artifact re-validated afterwards?
- Needs: none
- Status: planned

## Slice 14: Make several changes at once from the command line

- Kind: capability
- Scenarios: shop-knowledge / make-several-changes-at-once / The user makes several changes at once
- Observable: A user applies a batch that records a decision and points a work item at it, and both are in the shop as one change in its history.
- Unknown: What shape does a batch take in a file, given each change carries its own content and the set carries one actor and one message?
- Needs: none
- Status: planned

## Slice 15: Review the changes to one thing

- Kind: capability
- Scenarios: shop-knowledge / review-who-changed-what / The user reviews the changes to one thing
- Observable: A user reviews a decision recorded two days ago by the shopkeeper and revised today by an agent, and sees both changes with who, when, what, and why.
- Unknown: How does the command line let step definitions set the day, so a change made two days ago and one made today appear as such?
- Needs: none
- Status: planned

## Slice 16: Publish a process as a skill

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / The user publishes a process as a skill
- Observable: A user publishes a process into a directory and finds a skill whose heading block is the process's identity and whose body is its steps with the reused step written out in full; the knowledge base is unchanged.
- Unknown: Is a resolved whole read, with the stubs of its references and its type, enough for a renderer to write a reused step out in full?
- Needs: none
- Status: planned

## Slice 17: A skill the harness would reject is not published

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / A skill the harness would reject is not published
- Observable: A user publishes a process whose steps run past the harness's limits; the skill is refused for that reason and the directory stays empty.
- Unknown: Which limits does the harness publish for a skill, and can the renderer check its output against them before writing anything?
- Needs: none
- Status: planned

## Slice 18: Publish a process as a diagram

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / The user publishes a process as a diagram
- Observable: A user publishes a process into a directory and finds a diagram of its steps and their branches.
- Unknown: Do steps and branches carry enough structure to draw the diagram without hand layout?
- Needs: none
- Status: planned

## Slice 19: Publish anything as markdown

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / The user publishes anything as markdown
- Observable: A user publishes a role into a directory and finds a page with its identity as a heading, its fields as a list, its sections at their levels, and its parts as tables.
- Unknown: Can the page be laid out from the type alone, so the renderer knows nothing about any one type?
- Needs: none
- Status: planned

## Slice 20: Read an artifact at every depth

- Kind: stack
- Scenarios: kb / read-an-artifact / The client reads the whole artifact; kb / read-an-artifact / The client reads one section by its title; kb / read-an-artifact / The client reads the whole artifact with what it points at filled in
- Observable: A client reads a decision whole and gets every field, section, and part in the order the type declares; asks for its rationale and gets that section and nothing else; and reads it with its links resolved and gets the older decision in place of the link, as the store holds it now.
- Unknown: none
- Needs: none
- Status: planned

## Slice 21: Read a decision at every depth, as text or JSON

- Kind: capability
- Scenarios: shop-knowledge / read-back-what-the-shop-knows / The user reads the whole decision; shop-knowledge / read-back-what-the-shop-knows / The user reads one section of a decision; shop-knowledge / read-back-what-the-shop-knows / The user reads a decision with the things it points at filled in; shop-knowledge / read-back-what-the-shop-knows / The user takes the same answer as JSON
- Observable: A user reads a decision whole, or only its rationale, or whole with what it points at filled in, and can take any of those answers as JSON instead of the default.
- Unknown: none
- Needs: none
- Status: planned

## Slice 22: Change an artifact

- Kind: stack
- Scenarios: kb / change-an-artifact / The client changes an artifact
- Observable: A client replaces a decision; its version goes up by one and it records the current version of its type.
- Unknown: none
- Needs: none
- Status: planned

## Slice 23: Revise a recorded decision, whole or in part

- Kind: capability
- Scenarios: shop-knowledge / revise-what-the-shop-knows / The user revises a recorded decision; shop-knowledge / revise-what-the-shop-knows / The user revises one part of a recorded decision
- Observable: A user replaces a decision from a file and the shop holds the new wording at a later version, or replaces only its rationale and the rest reads as before.
- Unknown: none
- Needs: none
- Status: planned

## Slice 24: An artifact that breaks its type is refused

- Kind: stack
- Scenarios: kb / create-an-artifact / An artifact missing a required section is refused; kb / create-an-artifact / An artifact pointing at something that is not there is refused; kb / create-an-artifact / An artifact with two parts of the same name is refused
- Observable: A client creates a decision with no purpose, or one superseding a decision the store does not hold, or one carrying two options of the same name, and each is refused naming the rule it broke.
- Unknown: none
- Needs: none
- Status: planned

## Slice 25: A decision the shop cannot accept is refused

- Kind: capability
- Scenarios: shop-knowledge / record-a-decision / A decision that does not fit the shop's decision type is refused; shop-knowledge / record-a-decision / A decision recorded by nobody is refused; shop-knowledge / record-a-decision / A decision recorded without a reason is refused
- Observable: A user records a file that does not fit the decision type and is told which artifact and place is at fault with the command exiting non-zero, or records without saying which role they are, or without a message, and is refused for that reason.
- Unknown: none
- Needs: none
- Status: planned

## Slice 26: A malformed type is refused

- Kind: stack
- Scenarios: kb / define-a-type / Something that is not a well-formed type is refused
- Observable: A client defines a type that does not match the type that describes types and is refused for that reason.
- Unknown: none
- Needs: none
- Status: planned

## Slice 27: Record a decision from a pipe or under a piece of work

- Kind: capability
- Scenarios: shop-knowledge / record-a-decision / The user pipes a decision in instead of naming a file; shop-knowledge / record-a-decision / The user records a decision as part of a piece of work
- Observable: A user pipes a decision from another command into the record command and the shop holds it as if it had come from a file, and a user working as the shopkeeper on a named piece of work records one and the change is attributed to both.
- Unknown: none
- Needs: none
- Status: planned

## Slice 28: List artifacts of a kind

- Kind: stack
- Scenarios: kb / list-artifacts-of-a-kind / The client lists every artifact of a kind; kb / list-artifacts-of-a-kind / The client lists the artifacts matching a field; kb / list-artifacts-of-a-kind / The client lists names only
- Observable: A client lists the decisions and gets a stub of each of the three, narrows to the superseded one by a field, or asks for names and gets three names and nothing else.
- Unknown: none
- Needs: none
- Status: planned

## Slice 29: List what the shop has recorded

- Kind: capability
- Scenarios: shop-knowledge / list-what-the-shop-has-recorded / The user lists every decision; shop-knowledge / list-what-the-shop-has-recorded / The user lists the decisions that match a field; shop-knowledge / list-what-the-shop-has-recorded / The user lists only the names, to feed another command
- Observable: A user lists the decisions and sees all three with name and title, narrows to the superseded one by a field, or asks for names only and sees three names fit to feed another command.
- Unknown: none
- Needs: none
- Status: planned

## Slice 30: Follow the links one step, narrowed or not

- Kind: stack
- Scenarios: kb / follow-the-links / The client follows the links out of an artifact; kb / follow-the-links / The client follows the links into an artifact; kb / follow-the-links / The client narrows the links to one link and one kind
- Observable: A client follows the links out of a decision and gets a stub of the older decision, follows them in and gets a stub of each work item, or narrows to one link and one kind and gets both work items and nothing else.
- Unknown: none
- Needs: none
- Status: planned

## Slice 31: Follow the links from the command line

- Kind: capability
- Scenarios: shop-knowledge / follow-the-links-between-what-the-shop-knows / The user sees what a decision points at; shop-knowledge / follow-the-links-between-what-the-shop-knows / The user sees what points at a decision; shop-knowledge / follow-the-links-between-what-the-shop-knows / The user narrows the links to one kind of link and one kind of thing; shop-knowledge / follow-the-links-between-what-the-shop-knows / The user follows the links two steps out
- Observable: A user follows the links out of a decision and sees the older decision, in and sees both work items, narrowed to one link and one kind and sees both work items and nothing else, or two steps out and sees the older decision and the tag each with the route taken.
- Unknown: none
- Needs: none
- Status: planned

## Slice 32: Search within one kind, and the fields too

- Kind: stack
- Scenarios: kb / search-the-store / The client searches within one kind; kb / search-the-store / The client searches the fields as well as the prose
- Observable: A client searches the prose among decisions only and gets the two decisions and not the process, or searches fields and prose and also gets a decision whose title carries the word.
- Unknown: none
- Needs: none
- Status: planned

## Slice 33: Search what the shop knows

- Kind: capability
- Scenarios: shop-knowledge / search-what-the-shop-knows / The user searches the prose; shop-knowledge / search-what-the-shop-knows / The user searches within one kind of thing; shop-knowledge / search-what-the-shop-knows / The user searches the fields as well as the prose
- Observable: A user searches for a word and sees each result with the section it matched and a snippet with the heaviest section first, narrows to decisions and sees the two decisions and not the process, or includes the fields and also sees a decision whose title carries the word.
- Unknown: none
- Needs: none
- Status: planned

## Slice 34: Read the journal by role, piece of work, or time

- Kind: stack
- Scenarios: kb / read-the-journal / The client reads the journal for one role; kb / read-the-journal / The client reads the journal for one piece of work; kb / read-the-journal / The client reads the journal since a time
- Observable: A client reads the journal for the shopkeeper and gets only the creation of the decision, for a piece of work and gets only the agent's change, or since yesterday and gets only today's change.
- Unknown: none
- Needs: none
- Status: planned

## Slice 35: Review by role, piece of work, or date

- Kind: capability
- Scenarios: shop-knowledge / review-who-changed-what / The user reviews what one role did; shop-knowledge / review-who-changed-what / The user reviews what one piece of work did; shop-knowledge / review-who-changed-what / The user reviews the changes since a date
- Observable: A user reviews the shopkeeper's changes and sees only the recording of the decision, a piece of work's changes and sees only the agent's revision, or the changes since yesterday and sees only today's revision.
- Unknown: none
- Needs: none
- Status: planned

## Slice 36: Snapshot what a piece of work read

- Kind: stack
- Scenarios: kb / snapshot-what-a-piece-of-work-read / The client snapshots what a piece of work read
- Observable: A client snapshots a decision and a process for a piece of work; the journal holds one entry listing each with the version read and a fingerprint, and the client gets that entry's name.
- Unknown: none
- Needs: none
- Status: planned

## Slice 37: Record what a piece of work read

- Kind: capability
- Scenarios: shop-knowledge / record-what-a-piece-of-work-read / An agent records what it read
- Observable: An agent records, for its piece of work, the decision and process it read, and the shop's history holds one entry naming each with the version read.
- Unknown: none
- Needs: none
- Status: planned

## Slice 38: Add an item to a collection

- Kind: stack
- Scenarios: kb / add-an-item-to-a-collection / The client adds an item to a collection; kb / add-an-item-to-a-collection / An item that uses another artifact keeps its settings on itself
- Observable: A client adds a step to a process and gets the item's name and the artifact's new version with the item after those already there, and adds a step that points at the shared step with its own settings, which sit on the new item while the shared step is unchanged.
- Unknown: none
- Needs: none
- Status: planned

## Slice 39: Add a step to a process

- Kind: capability
- Scenarios: shop-knowledge / add-a-step-to-a-process / The user adds a step written in place; shop-knowledge / add-a-step-to-a-process / The user adds a step that reuses a shared step
- Observable: A user adds a step written in place and it is the last step with the user told its name, or adds a step that uses a shared step with its own settings and the process runs it there with those settings while the shared step and its other users are unchanged.
- Unknown: none
- Needs: none
- Status: planned

## Slice 40: Remove an artifact, or be refused

- Kind: stack
- Scenarios: kb / remove-an-artifact / The client removes an artifact nothing points at; kb / remove-an-artifact / A removal something points at is refused
- Observable: A client removes a tag nothing points at and the store no longer holds it with the removal in the journal, or removes a tag a decision points at and is refused with every link that blocks it.
- Unknown: none
- Needs: none
- Status: planned

## Slice 41: Retire what the shop no longer uses

- Kind: capability
- Scenarios: shop-knowledge / retire-what-the-shop-no-longer-uses / The user retires something nothing points at; shop-knowledge / retire-what-the-shop-no-longer-uses / The user retires something that is still pointed at
- Observable: A user retires a tag nothing points at and the shop no longer holds it, or retires a tag a decision carries and is refused, seeing everything that points at it.
- Unknown: none
- Needs: none
- Status: planned

## Slice 42: A check reports nothing when sound and stale when behind

- Kind: stack
- Scenarios: kb / check-the-store / A store with nothing wrong reports nothing; kb / check-the-store / An artifact behind its type is reported as stale
- Observable: A client checks a store where everything fits its type and is told of no violation, or one holding a decision last checked against an older version of its type and sees it listed as behind its type and not as a violation.
- Unknown: none
- Needs: none
- Status: planned

## Slice 43: Check the shop's knowledge is sound

- Kind: capability
- Scenarios: shop-knowledge / check-the-shops-knowledge-is-sound / The user checks a sound knowledge base; shop-knowledge / check-the-shops-knowledge-is-sound / The user checks a knowledge base with faults; shop-knowledge / check-the-shops-knowledge-is-sound / The user is told what is behind its type
- Observable: A user checks a sound knowledge base and is told nothing is wrong, checks one with two faults and sees both with the artifact and place while the command exits non-zero, or sees a decision listed as behind its type and not as a fault.
- Unknown: none
- Needs: none
- Status: planned

## Slice 44: The operator looks after a store

- Kind: stack
- Scenarios: kb / look-after-a-store / The operator sets up a store; kb / look-after-a-store / The operator checks the whole store; kb / look-after-a-store / The command line does nothing to content
- Observable: An operator runs kb's own command line to set up a store in a directory ready for a client to define types in, runs the check from a shell and is told of everything that does not fit its type and everything behind its type, and asks what the command line offers and sees only those two things.
- Unknown: none
- Needs: kb's own console entry point (every scenario)
- Status: planned

## Slice 45: One bad change in a batch leaves the shop untouched

- Kind: capability
- Scenarios: shop-knowledge / make-several-changes-at-once / One bad change in a batch leaves the shop untouched
- Observable: A user applies a batch whose second change does not fit its type; the batch is refused with every fault, and none of it is in the shop.
- Unknown: none
- Needs: none
- Status: planned

## Slice 46: The shop's roles and tags hold their shape

- Kind: capability
- Scenarios: shop-knowledge / start-a-shop-knowledge-base / A role keeps its harness fields apart from its shop identity; shop-knowledge / start-a-shop-knowledge-base / Anything the shop knows can be tagged
- Observable: A user records a role and its harness fields sit in one named group and its shop identity in another, and tags a decision with a tag so the decision names it while the tag's description is held once, on the tag.
- Unknown: none
- Needs: none
- Status: planned

## Slice 47: Publish a role as an agent

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / The user publishes a role as an agent
- Observable: A user publishes a role into a directory and finds an agent whose heading block is the role's harness fields and whose body is its prose.
- Unknown: none
- Needs: none
- Status: planned

## Satisfied by existing behaviour

- none

## Log

- 2026-09-23 Suite (shop-knowledge): 0 passed, 0 failed. `python -m pytest -q` reports "no tests ran": no step definitions exist.
- 2026-09-23 Suite (kb): 0 passed, 0 failed. Same run, same result.
- 2026-09-23 Plan cut: 84 slices over 89 approved scenarios, 44 in kb and 45 here. Slice 1 is the skeleton both specs define. Slices 2 to 19 carry one unknown each and are ordered by risk; slices 20 to 84 carry none and are ordered by value with kb ahead of the shop-knowledge scenario that needs it. Every scenario carries one `@slice-<n>` tag.
- 2026-09-23 When slice 1 is green: tag kb 0.1, pin it here, and move slices made only of kb scenarios into kb's own plan file, as both specs' "Order of building" say. Until then this is the only plan for either repository.
- 2026-09-23 A slice with no unknown that turns out green after an earlier slice's work is credited to that slice in this log and dropped.
- 2026-09-23 QUESTION FOR THE SPEC: kb / make-several-changes-in-one-go and shop-knowledge / make-several-changes-at-once say the history shows the set "as one change". The kb spec commits a set once but writes one journal entry per operation, and does not store the commit in the entry. Is "one change" the single commit, or must journal entries say which set they landed in? Slices 5 and 14 are cut on the one-commit reading; the other reading changes what they observe.
- 2026-09-23 QUESTION FOR THE SPEC: kb / read-an-artifact and shop-knowledge / read-back-what-the-shop-knows, the resolved read. When the resolved target itself points at something, is that resolved too, and what stops a cycle? The scenarios' older decision points at nothing, so slices 20 and 21 pass either way.
- 2026-09-23 QUESTION FOR THE SPEC: kb / add-an-item-to-a-collection and shop-knowledge / add-a-step-to-a-process say the client "is given the new item's name". Does the client name the item in its content, as parts carry their own id, or does kb mint it? Slices 38 and 39 pass either way.
- 2026-09-23 QUESTION FOR THE SPEC: kb / check-the-store and shop-knowledge / check-the-shops-knowledge-is-sound, the stale scenarios. Is an artifact behind its type checked against the current type at all? If the current type would refuse it, is it stale, a fault, or both? Slices 42 and 43 bump the type's version without changing what it requires, so they pass either way.
- 2026-09-23 Suite (shop-knowledge): 0 passed, 0 failed. `python -m pytest -q` reports "no tests ran". Same for kb.
- 2026-09-23 Re-slice: slices 1 to 19 unchanged. The tail, once 65 one-scenario slices, is now 28 slices, 20 to 47, each bundling the scenarios of one feature that share step definitions: the variants of one read, list, follow, search, journal, check, add, or remove, or the refusals of one command. Where a feature's tail scenarios split into two operations that do not share steps (record-a-decision's refusals and its two ways of recording) they are two slices. Slices that stand alone do so because nothing else in their feature is in the tail. The order and the kb-before-shop rule are as before. Every `@slice-<n>` tag in both repositories rewritten to match.
