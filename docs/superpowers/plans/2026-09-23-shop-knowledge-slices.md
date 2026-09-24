# shop-knowledge slices

One living plan for shop-knowledge and kb until slice 1 is green, as both
specs' "Order of building" say. Every slice names the repository each
scenario runs in: `kb / <feature file> / <scenario>` runs in
`shopsystem-kb`, `shop-knowledge / <feature file> / <scenario>` runs here.
When slice 1 and slices 54 to 63 are green, kb is tagged 0.1, this
repository pins it, and the slices made only of kb scenarios move to kb's
own plan. Slices 54 to 63 sit between slice 1 and the tag because each one
decides what kb 0.1 writes to disk or refuses on Init, Create, or Read: the
canonical form of a file, the title travelling beside the content, how a
store is found, the first entry in the history, and what a bad title, bad
content, or bad name is met with. Tagging before them would tag a disk
form and a contract that the next slice rewrites.

Slice 0 is the enabling slice the skeleton stands on: both checkouts run
their feature suites and this repository imports kb from the checkout
beside it. Slice 1 is the walking skeleton the specs define. Then the slices
kb 0.1 waits on: five that each settle one unknown, ordered by the size of
it, then five with none, then the tag. Then come the slices
that each settle one unknown, ordered by the size of it. Then the slices with
no unknown: scenarios that share a feature and step definitions bundle into
one slice, and the slices are ordered by value, kb's slice ahead of the
shop-knowledge slice that needs it.

The order of the sections in this file is the order of the work. A slice's
number is the name its tag carries and does not change once given, so slices
cut after the first plan carry numbers above 47 wherever they sit: 48 and 49
among the slices with an unknown, 50 at the end of them, 51 to 53 in the
tail, 54 to 63 between slice 1 and the tag.

## Slice 0: Both checkouts run their feature suites

- Kind: enabling
- Check: `python -m pytest -q` in `shopsystem-kb` -> 0 passed, 65 failed, every approved scenario collected and failing for want of steps, not "no tests ran"; `python -m pytest -q` in this repository -> 0 passed, 50 failed, the same; `python -c "import kb"` from this repository's checkout -> succeeds, with kb resolved from the sibling checkout as an editable path dependency; the protobuf compiler run over kb's contract file -> exits 0 and the code it generates imports
- Observable: A developer in either checkout runs the feature suite and sees every approved scenario collected and failing for want of steps rather than skipped for want of wiring, and this repository imports kb from the checkout beside it.
- Unknown: Does one Python environment serve both side-by-side checkouts, with this repository importing kb as an editable path dependency?
- Needs: none
- Status: green

## Slice 1: Record a decision and read it back

- Kind: capability
- Scenarios: kb / start-a-store / The client starts a store; kb / define-a-type / The client defines a type; kb / create-an-artifact / The client creates an artifact; kb / read-an-artifact / The client reads a summary; shop-knowledge / record-a-decision / The user records a decision; shop-knowledge / read-back-what-the-shop-knows / The user reads a decision at a glance
- Observable: At a shell, a user starts a shop knowledge base, records a decision from a file saying who they are and why, is shown the name the decision was given without having chosen it, and reads it back by that name at a glance with stubs of what it points at and counts of what points at it, while the decision sits on disk as a file inside a commit.
- Unknown: Does one round trip pass through every layer: the command line, the in-process client, the contract's messages, schema validation, canonical YAML on disk, and a git commit?
- Needs: the contract's messages that starting a store, defining a type, creating, and reading a summary need (every scenario); the metaschema written when a store starts (the start scenario); writes landing as files and one commit in the store's git repository, which nothing here asserts on but without which the skeleton is not through every layer (the create and record scenarios); the shop's start command loading bootstrap types for decision, work item, and tag, flat or on a base as the implementer chooses since nothing here asserts on composition (the two shop-knowledge scenarios); the name of a new artifact made by kb from its title, since neither the client nor the user chooses one (the create and record scenarios); the role a store is started under, carried on the start request (the start scenario, rewritten 2026-09-24)
- Status: green

## Slice 54: An artifact's file on disk is in canonical form

- Kind: capability
- Scenarios: kb / look-after-a-store / The operator reads an artifact's file on disk
- Observable: An operator opens the file of a decision whose purpose is one short line and finds every piece of prose standing as a block of its own however short, each list written beneath and indented under the name it belongs to, no line of prose broken to fit a width, and nothing that tells a reader how to build a value.
- Unknown: Can the YAML emitter kb writes with be made to give every prose body as a literal block however short, every sequence indented under its key, no line folded at any width and no tag, or must kb write the canonical form itself?
- Needs: none
- Status: green

## Slice 55: The title travels beside the content, never inside it

- Kind: capability
- Scenarios: kb / create-an-artifact / Content carrying a title of its own is refused
- Observable: A client creates a decision giving a title alongside content that also carries a title and is refused, told that a title is given alongside the content and never inside it, with the title the content carried named back.
- Unknown: When the title travels beside the content as a field of the message, what becomes of the title every type, and the type that describes types, declares among its content, while the file on disk still carries the title among its identity keys?
- Needs: the shop's record command lifting the title out of the user's file and sending it beside the rest, so slice 1's record scenario stays green (this scenario)
- Status: green

## Slice 56: The store is found above where the client works

- Kind: capability
- Scenarios: kb / read-an-artifact / The client works in a folder inside the store
- Observable: A client working in a folder deep inside the directory a store sits in reads a decision and is answered from the store found above where it is working, having named no store.
- Unknown: How does a client's call find the store from the folder it works in, upward like git, when the store is marked only by a file inside its own subdirectory and the folder may be any depth below?
- Needs: none
- Status: green

## Slice 57: Starting a store is recorded in its history

- Kind: capability
- Scenarios: kb / start-a-store / Starting a store is recorded in the store's history
- Observable: A client starts a store saying which role it is and the store's history holds one entry, under that role, with the message "initialise store", being the writing of the type that describes types at its first version with a fingerprint of what was written.
- Unknown: What does the first entry in a store's history hold and how is it read back, when it is written for the type that describes types before any other type exists?
- Needs: the journal entry the metaschema write leaves, inside the commit that starts the store (this scenario)
- Status: green

## Slice 58: A title that reads as a date is still a title

- Kind: capability
- Scenarios: kb / create-an-artifact / A title that reads as a date is still a title
- Observable: A client creates a decision titled "2026-09-24" and the title reads back as that text and not as a date, with the name made from that text.
- Unknown: Does a title YAML would read as a date survive the trip to disk and back as text, when the file is written by kb's emitter and loaded by a YAML parser?
- Needs: none
- Status: green

## Slice 59: Create refuses what it cannot name or hold, and names plainly what it can

- Kind: capability
- Scenarios: kb / create-an-artifact / An artifact created without a title is refused; kb / create-an-artifact / Content that settles what only the store settles is refused; kb / create-an-artifact / A title with capitals and punctuation gives a plain name; kb / create-an-artifact / A title that leaves nothing to make a name from is refused; kb / create-an-artifact / A title that reads as yes is still a title; kb / create-an-artifact / Content telling the store how to build a value is refused; kb / create-an-artifact / Content holding more than one document is refused; kb / create-an-artifact / A section carrying anything besides its title, its body and its own sections is refused
- Observable: A client creating a decision is refused when no title is given, when the title leaves nothing to make a name from, when the content carries a name or a version of its own with each named back, when a value carries a tag, when the content holds two documents, or when a section carries an entry besides its title, its body and its sections with the entry named; a title with capitals and punctuation gives a lower-case name with single hyphens and none at either end, and a title that reads as yes reads back as text.
- Unknown: none
- Needs: none
- Status: green

## Slice 60: A read of a name the store lacks, or of a name or place that is not plain, is refused

- Kind: capability
- Scenarios: kb / read-an-artifact / Reading something the store does not hold is refused; kb / read-an-artifact / A name that is not a plain name is refused; kb / read-an-artifact / A name that begins at the root of the disk is refused; kb / read-an-artifact / A place inside an artifact that is not a plain place is refused
- Observable: A client reading by a name the store holds nothing under is refused with that name given back, and reading by a name that climbs out of its kind, a name that begins at the root of the disk, or a place inside the decision that climbs out of it, is refused before any content, from inside the store or outside it, comes back.
- Unknown: none
- Needs: none
- Status: green

## Slice 61: The store KB_ROOT names is used, and a store that cannot be found or is named twice is refused

- Kind: capability
- Scenarios: kb / read-an-artifact / The client names the store instead of working inside it; kb / read-an-artifact / A call with no store to be found is refused; kb / read-an-artifact / Naming a store that is not there is refused; kb / read-an-artifact / Working in one store while naming another is refused
- Observable: A client working outside any store reads from the store KB_ROOT names; with nothing naming one it is refused for that reason; with KB_ROOT naming a directory that holds no store it is refused naming KB_ROOT; and working inside one store while KB_ROOT names another it is refused with neither store guessed at and no content from either.
- Unknown: none
- Needs: none
- Status: planned

## Slice 62: The same content always lands on disk as the same bytes

- Kind: capability
- Scenarios: kb / look-after-a-store / The same content always lands on disk as the same bytes
- Observable: An operator compares the files two stores wrote for the same decision from the same client and finds them the same, byte for byte.
- Unknown: none
- Needs: none
- Status: planned

## Slice 63: Starting a store without saying which role is refused

- Kind: capability
- Scenarios: kb / start-a-store / Starting a store without saying which role is refused
- Observable: A client starts a store without saying which role it is and is refused because a store can only be started under a role, and the directory holds no store.
- Unknown: none
- Needs: none
- Status: planned

kb 0.1 is tagged here, once slices 1 and 54 to 63 are green, and not before.
The "After slice 1" step of the skeleton implementation plan runs at this
point in the order, not after slice 1 alone.

## Slice 2: Two types share a shape

- Kind: capability
- Scenarios: kb / define-a-type / Two types share a shape
- Observable: A client defines a type that refers to a shape another stored type defines, and an artifact of the second type is checked against that shape.
- Unknown: Does a reference from one stored type into another resolve through the validator's registry when every type is itself an artifact in the store?
- Needs: none
- Status: planned

## Slice 3: A type built on a base

- Kind: capability
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

- Kind: capability
- Scenarios: kb / make-several-changes-in-one-go / The client makes several changes in one go
- Observable: A client sends a create and a change in one request, is given a name for the set it never asked for and a result for each change, and the store's history shows the two as one change.
- Unknown: Can the second operation in a set point at the artifact the first one creates, before either has landed?
- Needs: none
- Status: planned

## Slice 6: A bad set changes nothing

- Kind: capability
- Scenarios: kb / make-several-changes-in-one-go / One bad change in a set leaves the store untouched
- Observable: A client sends a set whose second change is missing a required section; the set is refused with every fault in it, and the store holds neither change.
- Unknown: Does a refusal at the second operation leave no trace of the first, both on disk and in the store as the same client then reads it?
- Needs: none
- Status: planned

## Slice 7: Every fault at once

- Kind: capability
- Scenarios: kb / create-an-artifact / An artifact with several faults reports them all
- Observable: A client creates a decision missing its purpose and pointing at a decision the store does not hold; both faults come back, each naming the artifact, the place, and the rule, and the store is unchanged.
- Unknown: Can violations from the JSON Schema validator and from kb's own rules be collected into one list, with the place given in the node-path form the contract uses?
- Needs: none
- Status: planned

## Slice 8: A refused change leaves the artifact as it was

- Kind: capability
- Scenarios: kb / change-an-artifact / A change that would break the type leaves the artifact as it was
- Observable: A client replaces a decision with content that has no purpose; the change is refused, and reading the decision gives what it held before at the version it held before.
- Unknown: After a refused write, does the store as the same client reads it, not only the files, still hold the old content at the old version?
- Needs: none
- Status: planned

## Slice 9: Every change leaves an entry

- Kind: capability
- Scenarios: kb / read-the-journal / Every change leaves an entry
- Observable: After a decision is created on one day and changed two days later, the journal for that decision shows two entries, each with when, which role, which piece of work, what it did, where, the version left behind, a fingerprint, the message, and the set of changes it landed with.
- Unknown: How do step definitions set the time kb stamps on an entry, so that two changes can be two days apart within one run?
- Needs: a journal entry written for every operation, as slice 57 writes one when a store starts, each naming the set it landed with and its own name when it landed alone (this scenario); an outside control of the clock (this scenario, and the since scenario later)
- Status: planned

## Slice 10: Every violation is reported

- Kind: capability
- Scenarios: kb / check-the-store / Every violation is reported
- Observable: A client checks a store holding an artifact missing a required section and another pointing at nothing, and both are reported, each naming the artifact, the place, and the rule.
- Unknown: How does a store come to hold a violation when every write is validated, and does loading such a store report it without failing?
- Needs: none
- Status: planned

## Slice 11: Search the prose, ranked

- Kind: capability
- Scenarios: kb / search-the-store / The client searches the prose
- Observable: A client searches for a word and gets each match with the title of the section it came from and a snippet, with the section that says the word most often first.
- Unknown: What index over sections gives ranking by how often the term occurs in a section, with the section title and a snippet in each result?
- Needs: none
- Status: planned

## Slice 12: Follow the links two steps out

- Kind: capability
- Scenarios: kb / follow-the-links / The client follows the links two steps out
- Observable: A client follows the links out of a decision two steps and gets the older decision and the tag it carries, each with the route taken to it.
- Unknown: How is the route to each artifact reached in two steps given back beside its stub?
- Needs: none
- Status: planned

## Slice 48: A loop in the links stops

- Kind: capability
- Scenarios: kb / read-an-artifact / A loop in the links stops instead of going round
- Observable: A client reads one of two decisions that point at each other, following its links three steps, and gets the other decision filled in, with the decision being read given as a name where the other points back rather than filled in again.
- Unknown: How does resolution know which artifacts are already filled in on the path it is following, so a loop comes back as a name while the same artifact reached by another path is still filled in?
- Needs: none
- Status: planned

## Slice 13: Change one node inside an artifact

- Kind: capability
- Scenarios: kb / change-an-artifact / The client changes one node inside an artifact
- Observable: A client replaces only the rationale of a decision, and the rest of the decision reads as before.
- Unknown: Can a write be addressed at a section inside an artifact and the whole artifact re-validated afterwards?
- Needs: none
- Status: planned

## Slice 49: Items keep their names when put in a different order

- Kind: capability
- Scenarios: kb / add-an-item-to-a-collection / Putting items in a different order does not rename them
- Observable: A client puts the items of a collection, each named by its place when it was added, in a different order, and every item keeps its name, so anything pointing at one of them still lands on the same item.
- Unknown: How does an item keep the name kb minted for it across a write that moves it, when the client never chooses names and an item named by its place no longer sits there?
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

## Slice 50: Starting a store inside a store is refused

- Kind: capability
- Scenarios: kb / start-a-store / Starting a store inside a store is refused
- Observable: A client starts a store in a directory that sits inside a store and is refused for that reason, and the store it sits inside holds what it held before.
- Unknown: How does kb tell that a directory sits inside a store, when a store is marked only by a file inside its own subdirectory and the directory may be any depth below it?
- Needs: none
- Status: planned

## Slice 20: Read an artifact at every depth, following its links as far as asked

- Kind: capability
- Scenarios: kb / read-an-artifact / The client reads the whole artifact; kb / read-an-artifact / The client reads one section by its title; kb / read-an-artifact / The client reads the whole artifact with what it points at filled in; kb / read-an-artifact / Without being asked to follow them, links come back as names; kb / read-an-artifact / The client reads an artifact following its links two steps; kb / read-an-artifact / The branches inside a process are not followed
- Observable: A client reads a decision whole and gets every field, section, and part in the order the type declares, with what it points at given as names; asks for its rationale and gets that section and nothing else; reads it following its links one step and gets the older decision in place of the link, as the store holds it now, with what that older decision points at given as names; follows them two steps and gets the tag in place of the link inside the older decision; and reads a process whose steps branch to each other and gets the branches as written, naming the steps.
- Unknown: none
- Needs: none
- Status: planned

## Slice 21: Read a decision at every depth, as text or JSON, from wherever the user works

- Kind: capability
- Scenarios: shop-knowledge / read-back-what-the-shop-knows / The user reads the whole decision; shop-knowledge / read-back-what-the-shop-knows / The user reads one section of a decision; shop-knowledge / read-back-what-the-shop-knows / The user reads a decision with the things it points at filled in; shop-knowledge / read-back-what-the-shop-knows / The user takes the same answer as JSON; shop-knowledge / read-back-what-the-shop-knows / The user asks for the links to be followed two steps; shop-knowledge / read-back-what-the-shop-knows / The user reads from a folder inside the shop's knowledge; shop-knowledge / read-back-what-the-shop-knows / The user reads while working elsewhere, having named the knowledge base; shop-knowledge / read-back-what-the-shop-knows / Reading where no knowledge base can be found is refused; shop-knowledge / read-back-what-the-shop-knows / Reading with KB_ROOT naming somewhere that holds no knowledge base is refused; shop-knowledge / read-back-what-the-shop-knows / Reading from inside one knowledge base while KB_ROOT names another is refused
- Observable: A user reads a decision whole with what it points at shown by name, or only its rationale, or whole with what it points at filled in one step when they do not say how far, or two steps so the tag inside the older decision is filled in too, and can take any of those answers as JSON instead of the default; and the user reads from a folder deep inside the shop's knowledge and is answered from the knowledge base found above them, or from elsewhere with KB_ROOT naming the shop's, and is refused with the command reporting failure where none can be found, where KB_ROOT names a directory holding no knowledge base, or where they work inside one knowledge base while KB_ROOT names another.
- Unknown: none
- Needs: none
- Status: planned

## Slice 22: Change an artifact, behind its type or not, and refuse what cannot be changed

- Kind: capability
- Scenarios: kb / change-an-artifact / The client changes an artifact; kb / change-an-artifact / Changing an artifact that is behind its type brings it up to date; kb / change-an-artifact / Changing an artifact that is behind its type with content the current version will not have is refused; kb / change-an-artifact / A change whose content settles what only the store settles is refused; kb / change-an-artifact / Changing something the store does not hold is refused; kb / change-an-artifact / A change aimed at a name that is not a plain name writes nothing
- Observable: A client replaces a decision; its version goes up by one and it records the current version of its type. A decision behind its type, replaced with content that fits the current version, records that version and is no longer listed as behind it; replaced with content that does not fit, the change is refused like any other, the decision reads as it was at the version it was, and it is still listed as behind its type; a change whose content carries a version of its own is refused with that named back, a change to a name the store holds nothing under is refused with the name given back, and a change aimed at a name that climbs out of the store is refused, each writing nothing anywhere and leaving the decision as it was.
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

## Slice 24: Create names what it stores and refuses what breaks its type

- Kind: capability
- Scenarios: kb / create-an-artifact / The name of a new artifact is made from its title, not asked for; kb / create-an-artifact / A second artifact with a title already used gets a name of its own; kb / create-an-artifact / Two parts with the same title are given names of their own; kb / create-an-artifact / An artifact missing a required section is refused; kb / create-an-artifact / An artifact pointing at something that is not there is refused
- Observable: A client creates a decision and is given a name made from its title that it never chose; a second decision with the same title is given that name with a number added while the first keeps its own; two options with the same title are each given a name of their own; and a decision with no purpose, or one superseding a decision the store does not hold, is refused naming the rule it broke.
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

- Kind: capability
- Scenarios: kb / define-a-type / Something that is not a well-formed type is refused
- Observable: A client defines a type that does not match the type that describes types and is refused for that reason.
- Unknown: none
- Needs: none
- Status: planned

## Slice 27: Record a decision from a pipe, under a piece of work, or with a title already used

- Kind: capability
- Scenarios: shop-knowledge / record-a-decision / The user pipes a decision in instead of naming a file; shop-knowledge / record-a-decision / The user records a decision as part of a piece of work; shop-knowledge / record-a-decision / A decision whose title is already used is given a name of its own
- Observable: A user pipes a decision from another command into the record command and the shop holds it as if it had come from a file, a user working as the shopkeeper on a named piece of work records one and the change is attributed to both; and a user records a decision whose title is already used and is shown a name of its own for it, the taken name with a number added, while the earlier decision still reads back by its name.
- Unknown: none
- Needs: none
- Status: planned

## Slice 28: List artifacts of a kind

- Kind: capability
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

- Kind: capability
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

- Kind: capability
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

## Slice 34: Read the journal by role, piece of work, time, or set

- Kind: capability
- Scenarios: kb / read-the-journal / The client reads the journal for one role; kb / read-the-journal / The client reads the journal for one piece of work; kb / read-the-journal / The client reads the journal since a time; kb / read-the-journal / The journal alone shows what landed together
- Observable: A client reads the journal for the shopkeeper and gets only the creation of the decision, for a piece of work and gets only the agent's change, or since yesterday and gets only today's change; and, reading the journal of a store where two artifacts changed in one go and a third alone, sees the two entries name the same set and the third name itself as its own, so what landed together is plain from the journal alone.
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

- Kind: capability
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

## Slice 38: Add an item to a collection, named by kb

- Kind: capability
- Scenarios: kb / add-an-item-to-a-collection / The client adds an item to a collection; kb / add-an-item-to-a-collection / An item that uses another artifact keeps its settings on itself; kb / add-an-item-to-a-collection / The name of a new item comes from its title; kb / add-an-item-to-a-collection / An item of a kind that carries no title is named by its place; kb / add-an-item-to-a-collection / A second item with a title already used in the collection gets a name of its own; kb / add-an-item-to-a-collection / Taking an item out does not rename the items left; kb / add-an-item-to-a-collection / An item whose content settles what only the store settles is refused; kb / add-an-item-to-a-collection / Adding an item to something the store does not hold is refused
- Observable: A client adds a step to a process and gets the item's name and the artifact's new version with the item after those already there; the name is made from the step's title, or from its place when items of that kind carry no title, and a second step with a title already used gets that name with a number added while the first keeps its own; a step that points at the shared step with its own settings keeps those on the new item while the shared step is unchanged; and taking the first item out of a collection leaves every other item with the name it was given when it was added; an item whose content carries a name of its own is refused with that named back and the process holds what it held at the version it held, and adding to a process by a name the store holds nothing under is refused with the name given back and nothing written.
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

- Kind: capability
- Scenarios: kb / remove-an-artifact / The client removes an artifact nothing points at; kb / remove-an-artifact / A removal something points at is refused; kb / remove-an-artifact / Removing something the store does not hold is refused
- Observable: A client removes a tag nothing points at and the store no longer holds it with the removal in the journal, or removes a tag a decision points at and is refused with every link that blocks it, or removes by a name the store holds nothing under and is refused with the name given back, the store holding what it held.
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

## Slice 42: A check reports nothing when sound, stale when behind, and both when behind and broken

- Kind: capability
- Scenarios: kb / check-the-store / A store with nothing wrong reports nothing; kb / check-the-store / An artifact behind its type is reported as stale; kb / check-the-store / An artifact behind its type that no longer fits it is reported both ways
- Observable: A client checks a store where everything fits its type and is told of no violation, or one holding a decision last checked against an older version of its type and sees it listed as behind its type and not as a violation; or one holding a decision behind its type that no longer fits the current version and sees it listed both as behind its type and as a violation naming the artifact, the place, and the rule, while the check itself does not fail.
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

## Slice 51: A store sits beside other things, and is not started twice

- Kind: capability
- Scenarios: kb / start-a-store / A directory holding other things can still be given a store; kb / start-a-store / Starting a store in a directory that already has one inside it is refused
- Observable: A client starts a store in a directory holding unrelated files and finds the store made inside it in a place of its own, with those files left alone and none of them the store's concern; starts one in a directory that already has a store inside it and is refused for that reason, with the store there holding what it held before.
- Unknown: none
- Needs: none
- Status: planned

## Slice 44: The operator looks after a store

- Kind: capability
- Scenarios: kb / look-after-a-store / The operator sets up a store; kb / look-after-a-store / Setting up a store where the directory already has one inside it is refused; kb / look-after-a-store / Setting up a store inside a store is refused; kb / look-after-a-store / The operator checks the whole store; kb / look-after-a-store / The command line does nothing to content; kb / look-after-a-store / Setting up a store without naming which role is refused; kb / look-after-a-store / The operator checks the store from a folder inside it; kb / look-after-a-store / The operator names the store instead of standing in it; kb / look-after-a-store / Running the command line where no store can be found is refused; kb / look-after-a-store / Naming a store that is not there is refused; kb / look-after-a-store / Standing in one store while naming another is refused
- Observable: An operator runs kb's own command line to set up a store inside a directory, in a place of its own, ready for a client to define types in; is refused where the directory already has a store inside it or sits inside one, with the store there left as it was; runs the check from a shell and is told of everything that does not fit its type and everything behind its type, and asks what the command line offers and sees only those two things; running kb init with nothing naming the role is refused naming KB_ACTOR and no store is made; kb validate run from a folder deep inside a store checks the store found above, run outside any store with KB_ROOT naming one checks that one, and is refused where no store can be found, where KB_ROOT names a directory that holds no store, or where the operator stands in one store while KB_ROOT names another.
- Unknown: none
- Needs: kb's own console entry point (every scenario)
- Status: planned

## Slice 52: The shop's knowledge base sits beside the shop's work, is started by someone for no stated reason, and is not started twice

- Kind: capability
- Scenarios: shop-knowledge / start-a-shop-knowledge-base / The shop's knowledge sits in a place of its own inside the directory it was started in; shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base where the directory already holds one is refused; shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base inside one the shop already has is refused; shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base asks for no reason; shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base without saying who is refused
- Observable: A user starts a shop knowledge base in a directory holding other work of the shop's and finds the knowledge kept in a place of its own inside it, with that work left as it was; starting one where the directory already holds the shop's knowledge, or in a directory inside it, is refused for that reason with everything the shop already knows unchanged; starting one saying who but giving no reason succeeds with everything it was given recorded in the shop's history under a reason the command writes itself, and starting one without saying who is refused for that reason, the directory holding no knowledge base and the command reporting failure.
- Unknown: none
- Needs: none
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

## Slice 53: The set's name finds the set in the history

- Kind: capability
- Scenarios: kb / make-several-changes-in-one-go / The name given for a set finds the set in the history
- Observable: A client makes two changes in one go and, under the name it was given for the set, the history shows exactly those two.
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
- 2026-09-23 Suite (shop-knowledge): 0 passed, 0 failed. `python -m pytest -q` reports "no tests ran". Same for kb.
- 2026-09-23 Re-plan under the current slicing rules: slice order and every `@slice-<n>` tag unchanged. Kind now follows what each slice delivers, not the repository it runs in: every slice with a Scenarios line is capability, so slices 2, 3, 5 to 13, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, and 44 change from stack to capability. No slice is stack: neither spec states a bound outside a scenario. Slice 0 added, enabling, verified by checks: the runnable packages, the suites wired to pytest-bdd, kb as an editable path dependency, and the contract file generating code, taken out of slice 1's Needs line. Slice 0 has no scenarios, so no feature file changes.
- 2026-09-23 Suite (shop-knowledge): 0 passed, 0 failed. `python -m pytest -q` reports "no tests ran". Same for kb.
- 2026-09-23 Both specs revised and both feature sets approved since the last cut: kb now mints every name, from the title or the item's place, once for life; a set of changes is given a name and every journal entry carries the set it landed with; a resolved read takes a depth and stops at a loop; a store is made in a place of its own inside the directory it is started in and refused where one already is or inside one; an artifact behind its type is checked against the current type. 27 scenarios added, 22 in kb and 5 here, and one removed: kb / create-an-artifact / An artifact with two parts of the same name is refused, gone from slice 24 since kb now names such parts apart. Seven scenarios already in slices 1, 5, 9, 20, 21, and 44 say more than they did; those slices' Observable lines now say it too.
- 2026-09-23 QUESTION answered by the spec: "one change" is a named set. Every journal entry names the set it landed with, and a change made alone names itself. Slices 5 and 9 now observe it; slice 53 and the scenario added to slice 34 read it back.
- 2026-09-23 QUESTION answered by the spec: a resolved read takes a depth, one step when none is given, and a target already filled in on the path is given as a name. Slice 48 carries the loop; the depths join slices 20 and 21.
- 2026-09-23 QUESTION answered by the spec: kb mints an item's name from its title or its place, once for life, and gives it back. The naming scenarios join slices 24 and 38; slice 49 carries the one with an unknown.
- 2026-09-23 QUESTION answered by the spec: an artifact behind its type is checked against the current type: still fitting, it is stale; no longer fitting, it is stale and in violation; a write to it is checked against the current type. Those scenarios join slices 22 and 42.
- 2026-09-23 Placed: 18 of the 27 join an existing slice that shares their feature and step definitions (slices 20, 21, 22, 24, 27, 34, 38, 42, 44). Three carry an unknown of their own and are new slices among the unknown slices, placed by the size of it: 48, a loop in the links, after 12; 49, names survive a reorder, after 13; 50, a store inside a store, after 19. The remaining six have no unknown and no tail slice of their feature to join: 51 (two kb start scenarios) before 44, so kb's own command line does not build the refusal first; 52 (three shop-knowledge start scenarios) after 44; 53 (the set's name) last. Order and tags of slices 0 to 47 unchanged. Every scenario in both repositories carries one `@slice-<n>` tag.
- 2026-09-23 QUESTION FOR THE SPEC: kb / add-an-item-to-a-collection / Putting items in a different order does not rename them. The spec says the client never supplies an item's name and that reordering does not rename; it does not say what the client sends when it reorders. Does it write the collection back carrying the names kb gave the items, or does kb match the items some other way? Slice 49's unknown is cut on the first reading; the second changes what a client sends, not what it observes.
- 2026-09-23 QUESTION FOR THE SPEC: kb / make-several-changes-in-one-go / The name given for a set finds the set in the history. The journal's filters are artifact, role, piece of work, and time; the set's name is not among them. Does the journal take the set's name as a filter, or does the client read the journal and keep the entries that name the set? Slice 53 passes either way.
- 2026-09-24 slice 0 green. A user can now: run the feature suite in either checkout and see every scenario collected and failing for want of steps, and import kb from this checkout as an editable path dependency of the sibling checkout. Assumption "one Python environment serves both side-by-side checkouts, with this repository importing kb as an editable path dependency": held. Evidence: `pip show shopsystem-kb` in this checkout's environment reported `Editable project location: /home/vscode/shopsystem-kb`, and `kb.__file__` resolved to `/home/vscode/shopsystem-kb/src/kb/__init__.py` while `shop_knowledge.__file__` resolved to this checkout. Surprised by: nothing. Open questions: none. Next: slice 1.
- 2026-09-24 slice 1 green. A user can now: start a shop knowledge base, record a decision from a file saying who and why, be shown the name kb gave it, and read it back at a glance with stubs and inbound counts, the decision on disk as canonical YAML inside a commit by the actor.
  Assumption "one round trip passes through every layer: the command line, the in-process client, the contract's messages, schema validation, canonical YAML on disk, and a git commit": held. Evidence: at a shell, `shop-knol init`, `create decision --from` and `read` round-tripped decision/price-reviews-happen-weekly at revision 1, the file under /tmp/skeleton/kb/decision/ was canonical YAML with identity keys first and `|` section bodies, and `git log` there showed `shopkeeper: Move price reviews to weekly` on top of the three `shopkeeper: Define the shop's ... type` commits and `kb: Start the store`.
  Surprised by: `-k the_user_records_a_decision` also selects "The user records a decision as part of a piece of work", so that scenario was run by its node id; once the shared Background Given existed, other scenarios' stores appeared under pytest's tmp directory beside the one being checked; content.py was built on PyYAML by reusing canonical's dump and load, not on ruamel.yaml, which kb does not depend on.
  Open questions:
  - ANSWERED 2026-09-24 by the kb spec (commit f4174a9): schemas and the journal live under <root>/kb/, and <root>/kb/ is itself the git repository. Built that way.
  - ANSWERED 2026-09-24: content crosses the contract as canonical YAML text, so order and number types are preserved by construction.
  - QUESTION FOR THE SPEC: init's bootstrap creates use KB_ACTOR and a fixed message; does init take -m?
  - QUESTION FOR THE SPEC: a create without a title, a read of an id the store lacks, KB_ROOT unset: what is shown?
  - QUESTION FOR THE SPEC: a create whose content carries id, type, schema_version or revision: kb now ignores them and mints its own (a client-supplied id overwrote another record and could write outside the store until this was fixed); should such a create be refused instead?
  - QUESTION FOR THE SPEC: the write path's "on git failure restore the files from HEAD and report" has no scenario; a failed commit leaves the saved file in the working tree (commits now name their files, so it cannot land under another actor). Needs a scenario.
  - QUESTION FOR THE SPEC: canonical form is not pinned by any scenario: PyYAML folds scalars longer than 80 columns, sequences under a mapping are not indented, and only multi-line strings are written as literal blocks. Decide before kb 0.1 is tagged, since a change rewrites every file.
  - QUESTION FOR THE SPEC: a title YAML 1.1 reads as a date or a bool (2026-09-24, yes) crashes id minting; a section carrying keys other than title, body, sections loses them on write; a read locator such as ../../x reads a file outside the store. What is shown or refused?
  Next: tag kb 0.1, pin it here, then slicing moves the kb-only slices to kb's own plan.
- 2026-09-24 Suite (kb): 3 passed, 97 failed. Suite (shop-knowledge): 2 passed, 55 failed. Slice 1's kb / start-a-store / The client starts a store is red again: its When now says which role starts the store and no step matches. The other five scenarios of slice 1 pass.
- 2026-09-24 Both specs revised and both feature sets approved since the last cut: the canonical form is pinned (every prose body a literal block, sequences indented, no folding, no tags, same tree same bytes); the identity keys are typed fields of the messages and content carrying one, title included, is refused on Create, Write, and Append alike; a store is found the way git finds a repository, upward from the working directory or through KB_ROOT, with three named refusals; every id and place is checked before any file is resolved from it; content is read plainly, one document, a section holding exactly its title, body, and sections; a title is text whatever it reads as, and one that leaves nothing to make a name from is refused; Read, Write, Append, and Delete of an id the store lacks are refused naming it; and Init takes an actor, no message, and leaves a journal entry. 42 scenarios added, 35 in kb and 7 here; one rewritten, slice 1's start scenario.
- 2026-09-24 QUESTION answered by the spec: init takes no -m; it runs under KB_ACTOR, required, with the message "initialise store", and leaves a journal entry for the metaschema write. Slices 57 and 63 carry it in kb, slice 52 here.
- 2026-09-24 QUESTION answered by the spec: a create without a title is refused; a read of an id the store lacks is refused naming the id, as are a write, an append, and a delete; KB_ROOT unset means the store is found upward from the working directory, and a call with none to be found is refused. Slices 59, 60, 61, 22, 38, and 40.
- 2026-09-24 QUESTION answered by the spec: content carrying id, type, schema_version, revision, or title is refused, each key named back, never ignored. Slice 55 carries the title, slice 59 the rest on Create, slices 22 and 38 on Write and Append.
- 2026-09-24 QUESTION answered by the spec: the canonical form is pinned, and two scenarios of look-after-a-store observe it. Slices 54 and 62.
- 2026-09-24 QUESTION answered by the spec: a title that reads as a date or a bool is text; a section carrying any other key is refused with the key named; a locator that climbs out of its kind or the store is refused before any file is read. Slices 58, 59, and 60.
- 2026-09-24 Still open from the slice-1 checkpoint: the write path's restore on git failure has no scenario; the spec now says so itself and defers it.
- 2026-09-24 Placed: of the 42, 19 join an existing slice that shares their feature and step definitions: five shop read scenarios of finding the knowledge base join slice 21, two shop start scenarios join slice 52, three change refusals join 22, two append refusals join 38, one delete refusal joins 40, and the six operator scenarios of look-after-a-store that are not about the file's form (init without a role, validate from inside, under KB_ROOT, and its three refusals) join 44, since kb's own command line is built there. The Write, Append, and Delete refusals go to the tail rather than ahead of the tag because kb 0.1's contract is what slice 1 needed, Init, Create, and Read, and the first Write belongs to slice 8. Five carry an unknown of their own and are new slices, one scenario each: 54 the canonical form, 55 the title beside the content, 56 the store found upward, 57 the first journal entry, 58 a title that reads as a date. The remaining 18 have no unknown and no tail slice ahead of the tag to join, so they form the pre-tag bundles by feature and step definitions: 59 the eight create scenarios, 60 the four read refusals of a bad or missing name, 61 the four read scenarios of KB_ROOT and its refusals, 62 the same bytes, 63 init without a role. Every scenario in both repositories carries one `@slice-<n>` tag.
- 2026-09-24 Order: slices 54 to 63 sit between slice 1 and slice 2, the five with an unknown first by the size of it (an emitter that may have to be written, a contract change that reaches every type, a discovery walk, a journal entry, a scalar's quoting), then the five without, each after the slice it stands on. kb 0.1 is tagged only when slices 1 and 54 to 63 are green; the skeleton plan's "After slice 1" step waits on all eleven. Slices 0 and 2 to 53 keep their order and their tags.
- 2026-09-24 Slice 56's unknown, how a directory is known to sit inside a store, is the mechanism slice 50 also needs. Slice 50 keeps its place; if 56 settles it, 50 is a slice with a spent unknown at the next re-plan and is dropped or bundled into 51 then, not now.
- 2026-09-24 Next: writing-plans over slices 1 and 54 to 63, one task per slice in that order, to `2026-09-24-pretag-implementation.md`.
- 2026-09-24 slice 1 green again. Someone can now: start a store saying which role they are, and find that role as the author of the store's first commit; the other five scenarios of the skeleton are as they were.
  Surprised by: nothing.
  Open questions: none. Next: slice 54.
- 2026-09-24 slice 54 green. Someone can now: open any artifact's file and find every body a literal block however short, every list indented under its key, no line folded, and no tag.
  Assumption "PyYAML's emitter can be made to write the canonical form": held. Evidence:
  ```
  id: decision/price-reviews-happen-weekly
  type: decision
  schema_version: 1
  revision: 1
  title: Price reviews happen weekly
  sections:
    - title: Purpose
      body: |
        Keep prices in step with costs.
    - title: Rationale
      body: |
        Costs move weekly.
  options:
    - id: keep-weekly
      title: Keep weekly
      body: |-
        Review every Monday.
    - id: go-monthly
      title: Go monthly
      body: |-
        Review on the first of the month.
  ```
  A marker class on `body` values, an `increase_indent` override, and `width=float("inf")` were enough; kb writes no YAML of its own.
  Surprised by: nothing.
  Open questions:
  - QUESTION FOR THE SPEC: a body with a space at the end of a line, or an empty body, cannot be a block scalar in YAML; PyYAML writes it double-quoted. Is such a body refused on the way in, or is a quoted string acceptable in the canonical form? No scenario pins it.
  Next: slice 55.
- 2026-09-24 slice 55 green. Someone can now: create an artifact giving its title beside its content, and is refused, with the title named back, when the content carries one too; shop-knol lifts the title out of the user's file.
  Assumption "the title as a message field leaves the types and the metaschema as they are": held. Evidence: kb validates the artifact with its title in place, so every type's `title` property and `required: [title]` still hold, and `schema/decision.yaml` on disk is unchanged but for the emitter.
  Surprised by: nothing.
  Open questions: none. Next: slice 56.
- 2026-09-24 slice 56 green. Someone can now: work in any folder inside the directory a store sits in and have a client's call go to that store without naming it.
  Assumption "a walk upward from the working directory to the first directory holding kb/store.yaml finds the store at any depth": held. Evidence: the scenario "kb / read-an-artifact / The client works in a folder inside the store" put the client three folders down, at `<root>/shelves/pricing/notes`, with `KB_ROOT` unset, and `kb.client.connect()` with no root walked up through `notes`, `pricing`, and `shelves` to find `<root>/kb/store.yaml` and answer with the decision; `cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-56` gave `1 passed, 99 deselected`.
  Surprised by: nothing.
  Open questions:
  - Slice 50's unknown (how a directory is known to sit inside a store) is this walk; slicing decides at the next re-plan whether 50 is spent.
  Next: slice 57.
- 2026-09-24 slice 57 green. Someone can now: start a store and find, in its history, one entry under their role with the message "initialise store", being the metaschema write at revision 1 with the digest of the file, inside the commit that started the store.
  Assumption "the first entry is written like any later one, one file under journal/<date>/, read back from disk": held. Evidence: `cat kb/journal/*/*/*/*.yaml` gave:
  ```
  id: 20260924T162924536104Z-1
  at: '2026-09-24T16:29:24.536104+00:00'
  actor:
    role: client
    execution: ''
  op: create
  artifact: schema/schema
  path: ''
  revision: 1
  schema_version: 1
  digest: 47fd035f39bc977175f29de65c91a585d451112a907b7e67a0c195d89d1bbaa0
  message: initialise store
  batch: 20260924T162924536104Z-1
  ```
  and `git -C kb show --stat --format='%an %s' HEAD` gave:
  ```
  client initialise store

   journal/2026/09/24/20260924T162924536104Z-1.yaml | 13 +++++++++++++
   schema/schema.yaml                               | 19 +++++++++++++++++++
   store.yaml                                       |  1 +
   3 files changed, 33 insertions(+)
  ```
  The step reads the file; the Journal rpc arrives with slice 9.
  Surprised by: nothing.
  Open questions: none. Next: slice 58.
- 2026-09-24 slice 58 green. Someone can now: create an artifact titled "2026-09-24" and read that title back as text, from the store and from the file, with the name made from it.
  Assumption "a title YAML would read as a date survives as text": held with no code of this slice's own. Evidence: the file carries `title: '2026-09-24'`; the emitter quotes any string whose plain form resolves to another type, and the title has been a string field since slice 55.
  Surprised by: the unknown was spent by slices 54 and 55 together; the scenario went green on its step definitions.
  Open questions: none. Next: slice 59.
- 2026-09-24 slice 59 green. Someone can now: create an artifact and be refused, with the cause named, for no title, a title that yields no name, an identity key in the content, a tag on a value, a second document, or a stray key in a section; a title with capitals and punctuation gives a plain hyphenated name, and "yes" reads back as text.
  Surprised by: scenario 6's red was not the JSON Schema type refusal the brief expected. Sections aren't reachable by the top-level JSON Schema properties check (only "title" and "supersedes" are declared there), so before `content.py`'s tag check existed, `yaml.safe_load` quietly built the `!!binary` value into bytes and the create went straight through with `refused.faults == []`; the Then failed on a missing fault, not a wrong rule.
  Open questions:
  - QUESTION FOR THE SPEC: content that is not a mapping (a list, a bare scalar) or is not YAML at all raises through to the client instead of coming back as a fault. What is shown? No scenario pins it.
  - QUESTION FOR THE SPEC: `sections` that is not a list (a string, a number) reaches the section check before JSON Schema has refused it, and the check reports nonsense paths or raises. No scenario pins it.
  Next: slice 60.
- 2026-09-24 slice 60 green. Someone can now: read by a name the store lacks and be told so with the name given back, and read by a name or a place that is not plain and be refused before any file, inside the store or outside it, is opened.
  Surprised by: nothing; scenarios 3 and 4 went green on their step definitions alone, answered by the ID and PLACE grammar written for scenario 2, exactly as the brief predicted.
  Open questions:
  - shop-knol read of a refused name prints an empty artifact and exits 0; slice 21 pins the shop's discovery refusals, but a not-found or not-plain name has no shop scenario. QUESTION FOR THE SPEC, or a scenario for slice 21.
  Next: slice 61.
