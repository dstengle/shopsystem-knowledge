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

## Slice 1.17: A title in a user's file reaches kb as the text the user wrote

- Kind: capability
- Scenarios: shop-knowledge / record-a-decision / A title in a file that reads as a date is still a title; shop-knowledge / record-a-decision / A title in a file that reads as a yes is still a title
- Observable: A user records a decision from a file whose title is written 2026-09-24, or yes, and reads the title back as that text, with the name made from it.
- Unknown: none
- Needs: every file shop-knol reads, the shop's own type files included, and everything it prints, read and written the way kb reads content, in place of the YAML 1.1 reading and writing it does now (both scenarios, and slice 1's two shop scenarios, which must stay green)
- Status: green

## Slice 1.24: shop-knol refuses a file it cannot read in plain words

- Kind: capability
- Scenarios: shop-knowledge / record-a-decision / A file naming the same entry twice is refused
- Observable: A user records a decision from a file that names the same entry twice and is told in plain words that an entry is named once and only once, with the place in the file, the command reporting failure and no traceback shown.
- Unknown: How does shop-knol give every refusal, kb's and its own reading of the user's file alike, as plain words and a non-zero exit, so that no traceback reaches the user?
- Needs: none
- Status: green

## Slice 1.27: Reading a decision whose file the shop cannot read is refused in plain words

- Kind: capability
- Scenarios: shop-knowledge / read-back-what-the-shop-knows / Reading something whose file the shop cannot read is refused
- Observable: A user reads a decision whose file was mangled by hand and is told in plain words that the file cannot be read, naming it, with the command reporting failure and no traceback shown.
- Unknown: none
- Needs: the shop's read reporting a refusal kb returns, where today it prints an empty artifact and succeeds (this scenario)
- Status: green

## Slice 1.28: A check of the shop's knowledge lists a file it cannot read

- Kind: capability
- Scenarios: shop-knowledge / check-the-shops-knowledge-is-sound / The user checks a knowledge base holding a file the shop cannot read
- Observable: A user checks a knowledge base holding a decision file mangled by hand and sees that file listed as a fault naming it, in plain words, alongside the check of everything else, with the command reporting failure.
- Unknown: none
- Needs: the shop's check command, as far as listing what kb's check reports; slice 44 extends it (this scenario)
- Status: green

kb 0.1 was tagged here, `v0.1.0`, once slices 1 and 1.1 to 1.28 were green
(all but 1.17, 1.24, 1.27, and 1.28 now in kb's plan), and this repository
pins it. The "After slice 1" step of the skeleton implementation plan ran at
this point in the order. Every later finding is placed by its unknown among
slices 2 onward, never ahead of them.

## Slice 1.29: First architecture review

- Kind: enabling
- Check: this repository's `CLAUDE.md` states the module map, the rules and the size limits its code keeps; an Opus review of the code and the step definitions against it, after slices 0, 1, 1.17, 1.24, 1.27 and 1.28, is in this plan's log, and every refactor it calls for is a slice of its own right after this one with a check -> the log entry and those slices
- Observable: Anyone can read how shop-knowledge's code is meant to be shaped, which of those rules the code keeps and which it breaks, and which slice brings each broken one into place, before the command line grows from four commands to fourteen.
- Unknown: none
- Needs: a `CLAUDE.md` for this repository, which it does not have: the review has nothing to hold the code to without one (the check)
- Status: green

## Slice 1.30: The steps every feature shares are defined once

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same 55 failing scenarios as before the slice (55 failed, 7 passed), and `grep -rnE "never a traceback|reports failure to whatever ran it" tests/*.py | grep -v conftest.py` prints nothing
- Observable: The step definitions follow the rule that a step used by more than one feature lives in the shared conftest, so the next slice that needs a refusal step finds it there rather than copying a fourth one.
- Unknown: none
- Needs: the "shown that fault in plain words, never a traceback" and "reports failure to whatever ran it" steps, now defined in three test files each under different fixture names, defined once (the check)
- Status: green

## Slice 1.31: Reading the user's file is one function of its own

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same 55 failing scenarios as before (55 failed, 7 passed), and `.venv/bin/python -c "import inspect,shop_knowledge.cli as c; s=inspect.getsource(c._create); assert 'try' not in s and 'read_text' not in s"` succeeds, and `grep -c read_text src/shop_knowledge/cli.py` prints 1
- Observable: Reading a user's file and turning a file kb cannot read into a refusal happens in one place that create and every later command that takes a file (apply, append) call, so "a file is read in one place" stays true as commands are added.
- Unknown: none
- Needs: the create handler split so it does one thing at one level (the check)
- Status: green

## Slice 1.32: Turning a read answer into what is shown is one function of its own

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same 55 failing scenarios as before (55 failed, 7 passed), and `.venv/bin/python -c "import inspect,shop_knowledge.cli as c; s=inspect.getsource(c._read); assert ' for ' not in s and len(s.splitlines())<=6"` succeeds
- Observable: The read command makes its call, refuses or shows, and the shaping of a whole answer sits apart, so the depth, format and follow-the-links slices that extend it add to one function rather than a growing handler.
- Unknown: none
- Needs: the read handler split so it does one thing at one level (the check)
- Status: green

## Slice 4: The shop's seven types

- Kind: capability
- Scenarios: shop-knowledge / start-a-shop-knowledge-base / The user starts a knowledge base and the shop's types are ready
- Observable: One command in an empty directory leaves a knowledge base that can hold decisions, features, work items, roles, processes, steps, and tags, and the user defines nothing of their own first.
- Unknown: Can the process type, whose steps are each either written in place or a reuse of a shared step with bindings, and which carry branches, be said in kb's schema language?
- Needs: the seven bootstrap types, the base they all build on, and whatever shared shapes the process and feature types refer to (this scenario)
- Status: green

## Slice 15: Make several changes at once from the command line

- Kind: capability
- Scenarios: shop-knowledge / make-several-changes-at-once / The user makes several changes at once
- Observable: A user applies a batch that records a decision and points a work item at it, and both are in the shop as one change in its history.
- Unknown: What shape does a batch take in a file, given each change carries its own content and the set carries one actor and one message?
- Needs: none
- Status: green

## Slice 16: Review the changes to one thing

- Kind: capability
- Scenarios: shop-knowledge / review-who-changed-what / The user reviews the changes to one thing
- Observable: A user reviews a decision recorded two days ago by the shopkeeper and revised today by an agent, and sees both changes with who, when, what, and why.
- Unknown: How does the command line let step definitions set the day, so a change made two days ago and one made today appear as such?
- Needs: none
- Status: green

## Slice 17: Publish a process as a skill

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / The user publishes a process as a skill
- Observable: A user publishes a process into a directory and finds a skill whose heading block is the process's identity and whose body is its steps with the reused step written out in full; the knowledge base is unchanged.
- Unknown: Is a resolved whole read, with the stubs of its references and its type, enough for a renderer to write a reused step out in full?
- Needs: none
- Status: green

## Slice 18: A skill the harness would reject is not published

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / A skill the harness would reject is not published
- Observable: A user publishes a process whose steps run past the harness's limits; the skill is refused for that reason and the directory stays empty.
- Unknown: Which limits does the harness publish for a skill, and can the renderer check its output against them before writing anything?
- Needs: none
- Status: green

## Slice 19: Publish a process as a diagram

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / The user publishes a process as a diagram
- Observable: A user publishes a process into a directory and finds a diagram of its steps and their branches.
- Unknown: Do steps and branches carry enough structure to draw the diagram without hand layout?
- Needs: none
- Status: green

## Slice 19.1: Second architecture review

- Kind: enabling
- Check: an Opus review of the code and the step definitions against `CLAUDE.md`, after the six implemented slices since slice 1.29, is in this plan's log, and every refactor it calls for is a slice of its own right after this one with a check -> the log entry and those slices
- Observable: Anyone can read whether the shop's types, the batch file, the history and the first two renderers kept the code in the shape CLAUDE.md sets.
- Unknown: none
- Needs: none
- Status: green

## Slice 19.2: A renderer offers only its render, and every renderer reads what it publishes one way

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same 49 failing scenarios as before the slice (49 failed, 13 passed); `grep -nE "^def [a-z]" src/shop_knowledge/renderers/skill.py src/shop_knowledge/renderers/diagram.py` -> the two `render` lines and nothing else; `grep -rl "ReadRequest.WHOLE" src/shop_knowledge/renderers` -> one module; `grep -rc 'split("/", 1)' src/shop_knowledge | grep -v ":0"` -> one line, a count of 1
- Observable: The markdown renderer of slice 20 and the agent renderer of slice 50 read the artifact they publish, and name it without its kind, the one way the skill and diagram renderers do, and a renderer's module shows the command line only the function it calls.
- Unknown: none
- Needs: none
- Status: green

## Slice 20: Publish anything as markdown

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / The user publishes anything as markdown
- Observable: A user publishes a role into a directory and finds a page with its identity as a heading, its fields as a list, its sections at their levels, and its parts as tables.
- Unknown: Can the page be laid out from the type alone, so the renderer knows nothing about any one type?
- Needs: none
- Status: green

## Slice 20.1: No file or directory a user names ends in a traceback

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same 48 failing scenarios as before the slice (48 failed, 14 passed); and each of these, run in a started knowledge base, prints exactly one line on stderr with no `Traceback`, nothing on stdout, and exits 1: `apply` of a batch whose change names no content (`changes: [{delete: tag/pricing}]`), of one with no `changes`, of one whose `changes` is not a list, and of a file that is a list; `create` from a file that is a list, from a path that is not there, from a directory, and from a file that is not text; `render skill` and `render diagram` with `--to` naming a file; `create` of a kind naming no type, whose line begins with no colon
- Observable: A user who names a file or a directory shop-knol cannot use, or gives a file of the wrong shape, is told so in one plain line naming it, never a traceback, for every command that takes one, so CLAUDE.md's rule 4 holds by construction rather than scenario by scenario.
- Unknown: Can the shape of every file a user gives be checked where it is read, in the words kb uses for a violation, with the shapes held as data as the shop's types are?
- Needs: none
- Status: green

## Slice 20.2: What the user is shown is shaped apart from the command line

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same 48 failing scenarios as before the slice (48 failed, 14 passed); `grep -cE "def _glance|def _change" src/shop_knowledge/cli.py` -> 0; `wc -l < src/shop_knowledge/cli.py` -> under 200; the module that now shapes answers holds no `print`, no `Request` and no `connect`
- Observable: The command line stays under the 250-line limit through slices 22 to 30, which add the whole, section and filled-in reads, JSON, revising, piping and listing, because turning each kb answer into what the user is shown sits in a module of its own.
- Unknown: none
- Needs: none
- Status: planned

## Slice 22: Read a decision at every depth, as text or JSON, from wherever the user works

- Kind: capability
- Scenarios: shop-knowledge / read-back-what-the-shop-knows / The user reads the whole decision; shop-knowledge / read-back-what-the-shop-knows / The user reads one section of a decision; shop-knowledge / read-back-what-the-shop-knows / The user reads a decision with the things it points at filled in; shop-knowledge / read-back-what-the-shop-knows / The user takes the same answer as JSON; shop-knowledge / read-back-what-the-shop-knows / The user asks for the links to be followed two steps; shop-knowledge / read-back-what-the-shop-knows / The user reads from a folder inside the shop's knowledge; shop-knowledge / read-back-what-the-shop-knows / The user reads while working elsewhere, having named the knowledge base; shop-knowledge / read-back-what-the-shop-knows / Reading where no knowledge base can be found is refused; shop-knowledge / read-back-what-the-shop-knows / Reading with KB_ROOT naming somewhere that holds no knowledge base is refused; shop-knowledge / read-back-what-the-shop-knows / Reading from inside one knowledge base while KB_ROOT names another is refused
- Observable: A user reads a decision whole with what it points at shown by name, or only its rationale, or whole with what it points at filled in one step when they do not say how far, or two steps so the tag inside the older decision is filled in too, and can take any of those answers as JSON instead of the default; and the user reads from a folder deep inside the shop's knowledge and is answered from the knowledge base found above them, or from elsewhere with KB_ROOT naming the shop's, and is refused with the command reporting failure where none can be found, where KB_ROOT names a directory holding no knowledge base, or where they work inside one knowledge base while KB_ROOT names another.
- Unknown: none
- Needs: none
- Status: planned

## Slice 24: Revise a recorded decision, whole or in part

- Kind: capability
- Scenarios: shop-knowledge / revise-what-the-shop-knows / The user revises a recorded decision; shop-knowledge / revise-what-the-shop-knows / The user revises one part of a recorded decision
- Observable: A user replaces a decision from a file and the shop holds the new wording at a later version, or replaces only its rationale and the rest reads as before.
- Unknown: none
- Needs: none
- Status: planned

## Slice 26: A decision the shop cannot accept is refused

- Kind: capability
- Scenarios: shop-knowledge / record-a-decision / A decision that does not fit the shop's decision type is refused; shop-knowledge / record-a-decision / A decision recorded by nobody is refused; shop-knowledge / record-a-decision / A decision recorded without a reason is refused
- Observable: A user records a file that does not fit the decision type and is told which artifact and place is at fault with the command exiting non-zero, or records without saying which role they are, or without a message, and is refused for that reason.
- Unknown: none
- Needs: none
- Status: planned

## Slice 28: Record a decision from a pipe, under a piece of work, or with a title already used

- Kind: capability
- Scenarios: shop-knowledge / record-a-decision / The user pipes a decision in instead of naming a file; shop-knowledge / record-a-decision / The user records a decision as part of a piece of work; shop-knowledge / record-a-decision / A decision whose title is already used is given a name of its own
- Observable: A user pipes a decision from another command into the record command and the shop holds it as if it had come from a file, a user working as the shopkeeper on a named piece of work records one and the change is attributed to both; and a user records a decision whose title is already used and is shown a name of its own for it, the taken name with a number added, while the earlier decision still reads back by its name.
- Unknown: none
- Needs: none
- Status: planned

## Slice 30: List what the shop has recorded

- Kind: capability
- Scenarios: shop-knowledge / list-what-the-shop-has-recorded / The user lists every decision; shop-knowledge / list-what-the-shop-has-recorded / The user lists the decisions that match a field; shop-knowledge / list-what-the-shop-has-recorded / The user lists only the names, to feed another command
- Observable: A user lists the decisions and sees all three with name and title, narrows to the superseded one by a field, or asks for names only and sees three names fit to feed another command.
- Unknown: none
- Needs: none
- Status: planned

## Slice 30.1: Third architecture review

- Kind: enabling
- Check: an Opus review of the code and the step definitions against `CLAUDE.md`, after the nine implemented slices since slice 19.1 (19.2, 20, 20.1, 20.2, 22, 24, 26, 28 and 30), is in this plan's log, and every refactor it calls for is a slice of its own right after this one with a check -> the log entry and those slices
- Observable: Anyone can read whether the read, revise, record and list commands kept the code in the shape CLAUDE.md sets.
- Unknown: none
- Needs: none
- Status: planned

## Slice 32: Follow the links from the command line

- Kind: capability
- Scenarios: shop-knowledge / follow-the-links-between-what-the-shop-knows / The user sees what a decision points at; shop-knowledge / follow-the-links-between-what-the-shop-knows / The user sees what points at a decision; shop-knowledge / follow-the-links-between-what-the-shop-knows / The user narrows the links to one kind of link and one kind of thing; shop-knowledge / follow-the-links-between-what-the-shop-knows / The user follows the links two steps out
- Observable: A user follows the links out of a decision and sees the older decision, in and sees both work items, narrowed to one link and one kind and sees both work items and nothing else, or two steps out and sees the older decision and the tag each with the route taken.
- Unknown: none
- Needs: none
- Status: planned

## Slice 34: Search what the shop knows

- Kind: capability
- Scenarios: shop-knowledge / search-what-the-shop-knows / The user searches the prose; shop-knowledge / search-what-the-shop-knows / The user searches within one kind of thing; shop-knowledge / search-what-the-shop-knows / The user searches the fields as well as the prose
- Observable: A user searches for a word and sees each result with the section it matched and a snippet with the heaviest section first, narrows to decisions and sees the two decisions and not the process, or includes the fields and also sees a decision whose title carries the word.
- Unknown: none
- Needs: none
- Status: planned

## Slice 36: Review by role, piece of work, or date

- Kind: capability
- Scenarios: shop-knowledge / review-who-changed-what / The user reviews what one role did; shop-knowledge / review-who-changed-what / The user reviews what one piece of work did; shop-knowledge / review-who-changed-what / The user reviews the changes since a date
- Observable: A user reviews the shopkeeper's changes and sees only the recording of the decision, a piece of work's changes and sees only the agent's revision, or the changes since yesterday and sees only today's revision.
- Unknown: none
- Needs: none
- Status: planned

## Slice 38: Record what a piece of work read

- Kind: capability
- Scenarios: shop-knowledge / record-what-a-piece-of-work-read / An agent records what it read
- Observable: An agent records, for its piece of work, the decision and process it read, and the shop's history holds one entry naming each with the version read.
- Unknown: none
- Needs: none
- Status: planned

## Slice 40: Add a step to a process

- Kind: capability
- Scenarios: shop-knowledge / add-a-step-to-a-process / The user adds a step written in place; shop-knowledge / add-a-step-to-a-process / The user adds a step that reuses a shared step
- Observable: A user adds a step written in place and it is the last step with the user told its name, or adds a step that uses a shared step with its own settings and the process runs it there with those settings while the shared step and its other users are unchanged.
- Unknown: none
- Needs: none
- Status: planned

## Slice 42: Retire what the shop no longer uses

- Kind: capability
- Scenarios: shop-knowledge / retire-what-the-shop-no-longer-uses / The user retires something nothing points at; shop-knowledge / retire-what-the-shop-no-longer-uses / The user retires something that is still pointed at
- Observable: A user retires a tag nothing points at and the shop no longer holds it, or retires a tag a decision carries and is refused, seeing everything that points at it.
- Unknown: none
- Needs: none
- Status: planned

## Slice 42.1: Fourth architecture review

- Kind: enabling
- Check: an Opus review of the code and the step definitions against `CLAUDE.md`, after the six implemented slices since slice 30.1, is in this plan's log, and every refactor it calls for is a slice of its own right after this one with a check -> the log entry and those slices
- Observable: Anyone can read whether the links, search, history, snapshot, append and retire commands kept the code in the shape CLAUDE.md sets.
- Unknown: none
- Needs: none
- Status: planned

## Slice 42.2: The check's answer is refused the one way every kb answer is

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same failing scenarios as before the slice; `.venv/bin/python -c "import inspect,shop_knowledge.cli as c; assert 'Refused' not in inspect.getsource(c._validate)"` succeeds; `CLAUDE.md` names one place a kb answer's faults are not refused through `_answered` directly, a renderer's, and not Validate's
- Observable: The check command's faults and violations are refused through the one refusal of kb answers, so slice 44, which extends the check, adds to that path rather than to a second one.
- Unknown: none
- Needs: none
- Status: planned

## Slice 44: Check the shop's knowledge is sound

- Kind: capability
- Scenarios: shop-knowledge / check-the-shops-knowledge-is-sound / The user checks a sound knowledge base; shop-knowledge / check-the-shops-knowledge-is-sound / The user checks a knowledge base with faults; shop-knowledge / check-the-shops-knowledge-is-sound / The user is told what is behind its type
- Observable: A user checks a sound knowledge base and is told nothing is wrong, checks one with two faults and sees both with the artifact and place while the command exits non-zero, or sees a decision listed as behind its type and not as a fault.
- Unknown: none
- Needs: none
- Status: planned

## Slice 47: The shop's knowledge base sits beside the shop's work, is started by someone for no stated reason, and is not started twice

- Kind: capability
- Scenarios: shop-knowledge / start-a-shop-knowledge-base / The shop's knowledge sits in a place of its own inside the directory it was started in; shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base where the directory already holds one is refused; shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base inside one the shop already has is refused; shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base asks for no reason; shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base without saying who is refused
- Observable: A user starts a shop knowledge base in a directory holding other work of the shop's and finds the knowledge kept in a place of its own inside it, with that work left as it was; starting one where the directory already holds the shop's knowledge, or in a directory inside it, is refused for that reason with everything the shop already knows unchanged; starting one saying who but giving no reason succeeds with everything it was given recorded in the shop's history under a reason the command writes itself, and starting one without saying who is refused for that reason, the directory holding no knowledge base and the command reporting failure.
- Unknown: none
- Needs: Init's answer and bootstrap's Create answers, both dropped today, refused the one way every kb answer is (the two refusals of starting where a knowledge base already is)
- Status: planned

## Slice 48: One bad change in a batch leaves the shop untouched

- Kind: capability
- Scenarios: shop-knowledge / make-several-changes-at-once / One bad change in a batch leaves the shop untouched
- Observable: A user applies a batch whose second change does not fit its type; the batch is refused with every fault, and none of it is in the shop.
- Unknown: none
- Needs: none
- Status: planned

## Slice 49: The shop's roles and tags hold their shape

- Kind: capability
- Scenarios: shop-knowledge / start-a-shop-knowledge-base / A role keeps its harness fields apart from its shop identity; shop-knowledge / start-a-shop-knowledge-base / Anything the shop knows can be tagged
- Observable: A user records a role and its harness fields sit in one named group and its shop identity in another, and tags a decision with a tag so the decision names it while the tag's description is held once, on the tag.
- Unknown: none
- Needs: none
- Status: planned

## Slice 50: Publish a role as an agent

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
- 2026-09-24 Placed: of the 42, 19 join an existing slice that shares their feature and step definitions: five shop read scenarios of finding the knowledge base join slice 21, two shop start scenarios join slice 52, three change refusals join 22, two append refusals join 38, one delete refusal joins 40, and the six operator scenarios of look-after-a-store that are not about the file's form (init without a role, validate from inside, under KB_ROOT, and its three refusals) join 44, since kb's own command line is built there. The Write, Append, and Delete refusals go to the tail rather than ahead of the tag because kb 0.1's contract is what slice 1 needed, Init, Create, and Read, and the first Write belongs to slice 8. Five carry an unknown of their own and are new slices, one scenario each: 54 the canonical form, 55 the title beside the content, 56 the store found upward, 57 the first journal entry, 58 a title that reads as a date. The remaining 18 have no unknown and no tail slice ahead of the tag to join, so they form the pre-tag bundles by feature and step definitions: 59 the eight create scenarios, 60 the four read refusals of a bad or missing name, 61 the four read scenarios of KB_ROOT and its refusals, 62 the same bytes, 63 init without a role. Every scenario in both repositories carries one `@slice-<n>` tag.
- 2026-09-24 Order: slices 54 to 63 sit between slice 1 and slice 2, the five with an unknown first by the size of it (an emitter that may have to be written, a contract change that reaches every type, a discovery walk, a journal entry, a scalar's quoting), then the five without, each after the slice it stands on. kb 0.1 is tagged only when slices 1 and 54 to 63 are green; the skeleton plan's "After slice 1" step waits on all eleven. Slices 0 and 2 to 53 keep their order and their tags.
- 2026-09-24 Next: writing-plans over slices 1 and 54 to 63, one task per slice in that order, to `2026-09-24-pretag-implementation.md`.
- 2026-09-24 slice 1 green again. Someone can now: start a store saying which role they are, and find that role as the author of the store's first commit; the other five scenarios of the skeleton are as they were.
  Surprised by: nothing.
  Open questions: none. Next: slice 54.
- 2026-09-24 Whole-branch review of slices 1 and 54 to 63 before the tag. Each of these is reproducible, is pinned by no scenario, and under bdd-red-green got no code; each needs a scenario or a spec line before kb 0.1 is tagged knowingly:
  - QUESTION FOR THE SPEC (slice 59): `CreateRequest.type` is never checked. It is joined straight into the id and into the schema path, so `type="../schema/decision"` writes `<root>/schema/decision/<slug>.yaml` outside `kb/`, and a deeper `../` chain writes outside the root; git then refuses the add and the file is left uncommitted. An unknown type raises `FileNotFoundError` instead of a fault. The spec says a type "is an existing schema" and a file is written "only at the path derived from a validated id, inside `<root>/kb/`". Create of a kind that is not plain, or not held, has no scenario.
  - QUESTION FOR THE SPEC (slice 54): YAML anchors and aliases in content are loaded as shared objects and written back as `&id001` / `*id001` in field values (sections and part items are rebuilt by `order()` and escape this). The canonical form says "no anchors". Refuse aliases on the way in like tags, or have the dumper ignore aliases; either needs a scenario.
  - QUESTION FOR THE SPEC (slice 59): a section missing `title` or `body` passes validation (the section check only refuses extra keys) and then raises `KeyError` in `canonical._section`. The spec says a section has exactly `title`, `body` and `sections`.
  - QUESTION FOR THE SPEC (slice 58, shop-knowledge): `shop-knol create` reads the user's file with `yaml.safe_load`, so `title: 2026-09-24` arrives as a date and `title: yes` as a bool, and `CreateRequest(title=...)` raises `TypeError`. kb's contract holds the title as text, as slice 58 showed; the shop's coercion "to text" has no scenario, and `str()` alone would turn `yes` into `True`.
  - QUESTION FOR THE SPEC (slice 61): a client built by `connect()` with no root over a refusal, or over no store, has no servicer, and `Init` on it raises `AttributeError`. Init takes its root on the request and never goes through discovery; what a client that discovers nothing and then starts a store is told has no scenario.
  - QUESTION FOR THE SPEC (slice 59): content is parsed by PyYAML, which is YAML 1.1: `1:20` loads as `80`, `yes`/`on`/`off` as booleans, and unquoted dates as dates, in field values. The spec names YAML 1.2.
  - Noted for the tag: Create writes no journal entry until slice 9, so stores started under 0.1 will hold no Create entries in their history.
- 2026-09-24 Suite (kb): 27 passed, 80 failed. Suite (shop-knowledge): 2 passed, 57 failed. The 27 and the 2 are slices 1 and 54 to 63; none of the nine new scenarios passes, each failing for want of a step.
- 2026-09-24 Both specs revised and both feature sets approved since the last cut: every request is turned into checked values where it enters kb; the canonical form is one check run on content in and bytes out; kb's structural rules are a schema fragment composed with the type's; a client is readied without a store and finds one on each call; all YAML in kb, and every file shop-knol reads or writes, is YAML 1.2. Nine scenarios added, seven in kb and two here, none changed.
- 2026-09-24 QUESTIONS answered by the spec, from the whole-branch review: a kind that is not plain is refused like any input (slice 67); aliases are refused (slice 65); a section without a title or a body does not fit its type (slice 66); shop-knol reads a user's file as YAML 1.2 (slice 70); a client that finds no store is refused on the call, never raises (slice 68); content is YAML 1.2, so `1:20` and `on` are text (slice 64).
- 2026-09-24 Placed: none of the nine joins a slice after the tag, since each decides what kb 0.1 writes or refuses on Init, Create, or Read. Five carry an unknown of their own and are new slices, ordered by the size of it: 64, a second YAML library under the canonical form; 65, one check on content in and bytes out, which stands on the library 64 chose; 66, the structural rules as a composed schema; 67, checked values at the boundary; 68, finding the store on each call. Two have none: 69, one start scenario, whose step definitions it shares with no other untagged scenario; 70, the two shop record scenarios, which share their steps and stand on 64's library. Slices 65, 66, 67, 68 and 70 each replace the check or the reading an earlier pre-tag slice built, rather than adding one beside it, and that slice's scenarios must stay green. Every scenario in both repositories carries one `@slice-<n>` tag.
- 2026-09-24 kb 0.1 now waits on slices 64 to 70 as well as 1 and 54 to 63: the tag, the pin here, and the move of the kb-only slices to kb's own plan come after slice 70, and the skeleton plan's "After slice 1" step waits on all of them. Slices 0 to 63 keep their order and their tags.
- 2026-09-24 Next: writing-plans over slices 64 to 70, one task per slice in that order, to `2026-09-24-pretag2-implementation.md`.
- 2026-09-24 writing-plans done: `2026-09-24-pretag2-implementation.md`, seven tasks for slices 64 to 70 in slice order. It was assembled and run in scratch copies of both repositories (kb 34 passed, 73 failed; shop-knowledge 4 passed, 55 failed once all seven are green). Slice 69 went green there on its step definitions alone. Next: execute it, then the tag.
- 2026-09-24 slice 70 green. Someone can now: record a decision from a file whose title is written 2026-09-24 or yes and read that title back as text, with the name made from it.
  Surprised by: the shop-knowledge full suite before the change was `57 failed, 2 passed` (the two slice-70 scenarios red, so 55 failed once they are green). Scenario 2 had no red of its own on code: after scenario 1's production change only its Then step was missing (StepDefinitionNotFoundError), so it went green on that step definition alone, as with slice 69. Red for scenario 1 was the StepDefinitionNotFoundError for the new Given, then the create's `TypeError: bad argument type for built-in operation` from PyYAML's date. The grep for `import yaml` over src and tests prints nothing, and no diff under features/. Evidence: `-m "slice-70 or slice-1"` `4 passed, 55 deselected`; shop-knowledge full suite `55 failed, 4 passed`; kb full suite `73 failed, 34 passed`.
  Open questions:
  - QUESTION FOR THE SPEC: a title in a file that YAML 1.2 still reads as something other than text (`title: true`, `title: 12`, `title: 2026-9-24`) reaches kb as `True`, `12`, `2026-09-24`, not as the text written. No scenario pins it.
  - QUESTION FOR THE SPEC: a user file holding a tag, an anchor or alias, or a second document now makes shop-knol create fail with an uncaught NotCanonical traceback (PyYAML's safe_load accepted anchors). Should shop-knol answer with a fault or a message? No scenario pins it.
  Next: the plan's remaining work (tag kb 0.1, pin it here, move the kb-only slices to kb's own plan) is deliberately not done here and awaits the user.
- 2026-09-24 Suite (kb): 34 passed, 84 failed. Suite (shop-knowledge): 4 passed, 58 failed. The 34 and the 4 are slices 1 and 54 to 70 (1 and 1.1 to 1.17 below); none of the fourteen new scenarios passes, each failing for want of a step.
- 2026-09-24 Both specs revised and both feature sets approved since the last cut: content is read with YAML 1.2's core schema, so only true, false, null, integers and floats are typed; a `%YAML` or `%TAG` directive and a duplicate key are faults naming the place; a title is text whatever arrives, `true` and `12` included; Init's root is an input checked like any other; a stored file that fails to parse is a violation for the check and a refusal on Read, never an exception; and shop-knol never shows a traceback. Fourteen scenarios added, eleven in kb and three here, none changed.
- 2026-09-24 QUESTIONS answered by the spec: a duplicate key is a fault naming the place (slice 65's question; slices 1.21 and 1.24); a `%YAML` directive is refused (slice 65's question; slice 1.22); Init's root is a checked value, and an empty one is refused rather than taken as the working directory (slice 67's question; slices 1.23 and 1.26); a hand-edited stored file is a refusal on Read and a violation for the check (slice 65's question; slices 1.19 and 1.20); a kind naming no type is its own fault (slice 67's question; slice 1.25); a title arriving as true or 12 is text (slice 70's question, now answered by kb; slices 1.18 and 1.25); a user file shop-knol cannot read is refused in plain words (slice 70's question; slice 1.24).
- 2026-09-24 Placed at the user's instruction as the last batch ahead of slice 2, since kb 0.1 waits on them, cut and ordered by the same rules as the two cuts before it. Seven carry an unknown of their own and are one-scenario slices, ordered by the size of it: 1.18, a title that is not text reaching kb through a text field, which may reach the contract; 1.19, a stored file that fails to parse turned into a fault everywhere kb loads one; 1.20, kb's first check of a whole store, which stands on 1.19; 1.21, the place of a duplicate key given in the contract's form; 1.22, a directive seen before the reader takes it up; 1.23, Init's root as a checked value; 1.24, shop-knol's plain-words refusal, which stands on 1.21's fault. Four have none: 1.25, the three remaining create scenarios, after 1.18 whose title steps one of them shares; 1.26, the two remaining start scenarios, after 1.23; 1.27, the shop's read refusal, after 1.19 and 1.24; 1.28, the shop's check, after 1.20 and 1.24. Slices 1.20 and 1.28 bring the check, kb's and the shop's, into 0.1 only as far as these scenarios need it; slices 43 and 44 build the rest.
- 2026-09-24 This is the final pre-tag batch. After slice 1.28 is green, kb 0.1 is tagged, pinned here, and the kb-only slices move to kb's own plan; every finding after it, from a review, a hand-back, or a spec amendment, is placed by its unknown among the remaining slices, never ahead of them.
- 2026-09-24 Re-plan of spent unknowns: old slice 50's unknown, how kb tells a directory sits inside a store, was settled by old slice 56's upward walk (slice 56's checkpoint), so its scenario joins old slice 51, the start refusals it shares its steps with (new slice 45). Old slice 10's unknown, how a store comes to hold a violation and whether loading it reports rather than fails, is settled by slice 1.20's hand-edited file, so its scenario joins old slice 42, the check-the-store bundle (new slice 43).
- 2026-09-24 Renumbered in execution order, and every `@slice-<n>` tag in both repositories rewritten to match; both suites' marker registration now takes a dotted number. Pre-tag slices are numbered under slice 1, so the first slice after the tag is 2: 54 to 70 are now 1.1 to 1.17, in the same order, and this batch is 1.18 to 1.28. After the tag: 2 to 9 unchanged; 11 is 10, 12 is 11, 48 is 12, 13 is 13, 49 is 14, 14 to 19 are 15 to 20, 20 to 41 are 21 to 42, 42 with old 10 is 43, 43 is 44, 51 with old 50 is 45, 44 is 46, 52 is 47, 45 to 47 are 48 to 50, 53 is 51. Log entries above this one, the implementation plans, and the commit messages keep the numbers they were written with.
- 2026-09-24 Still open, no scenario, so no slice builds them: a bare date in a field value is text under the core schema but ruamel still loads it as a date (slice 64's question); a `%TAG` directive, which the spec refuses beside `%YAML`; content that is not YAML at all or not a mapping raises through the client (slices 59 and 65); an empty KB_ROOT (slice 61); a write whose own output fails the canonical check (slice 65); a read of a refused name through shop-knol other than an unreadable file (slice 60).
- 2026-09-24 Next: writing-plans over slices 1.18 to 1.28, one task per slice in that order, to `2026-09-24-pretag3-implementation.md`.
- 2026-09-24 writing-plans done: `2026-09-24-pretag3-implementation.md`, eleven tasks for slices 1.18 to 1.28 in slice order. It was assembled and run in scratch copies of both repositories (kb 45 passed, 73 failed; shop-knowledge 7 passed, 55 failed once all eleven are green). Two of slice 1.25's three scenarios went green there on their step definitions alone. Slice 1.26 makes shop-knowledge's test fixture create the directory a knowledge base starts in, since kb no longer builds it. Next: execute it, then the tag.
- 2026-09-24 slice 1.24 green. Someone can now: record a file that names an entry twice and be told in plain words where, with a non-zero exit and no traceback; any fault kb returns on create is printed the same way.
  Assumption "one printer serves kb's faults and shop-knol's own reading of a file": held. Evidence: in a scratch shop, `shop-knol create decision --from f.yaml -m why` with a repeated `body` key printed on stderr "/tmp/tmp.EYVgDOqnrX/f.yaml at sections/0/body: an entry is named once and only once; 'body' is named again at line 5" and exited 1.
  Surprised by: nothing.
  Open questions:
  - QUESTION FOR THE SPEC: shop-knol still shows a traceback with KB_ACTOR unset (KeyError) and for --from a file that is not there (FileNotFoundError); the spec says never. (Review Focus 4)
  Next: slice 1.25.
- 2026-09-24 slice 1.27 green. Someone can now: read a decision whose file was mangled by hand and be told in plain words which file cannot be read, with a non-zero exit; any refusal kb gives a read is printed the same way (slice 60's open question on the shop's read of a refused name).
  Surprised by: nothing.
  Open questions: none. Next: slice 1.28.
- 2026-09-24 slice 1.28 green. Someone can now: check the shop's knowledge and see a file mangled by hand listed as a fault in plain words, beside every other fault, with a non-zero exit.
  Surprised by: nothing.
  Open questions: none.
  Next: the tag, kb 0.1 (the section after the last task of 2026-09-24-pretag3-implementation.md).
- 2026-09-24 Whole-batch review of slices 1.18 to 1.28 (no scenario changed, no code changed after it). All eleven green; kb `73 failed, 45 passed`, shop-knowledge `55 failed, 7 passed`; generated contract files regenerate byte-identical from `kb.proto`. Findings with no scenario, so nothing is coded; each needs a scenario from formulating-features and is placed by its unknown among the remaining slices, never ahead of them:
  - QUESTION FOR THE SPEC (regression this batch made easy to hit): `shop-knol init /tmp/none` (a directory that is not there) is refused by kb, but shop-knol ignores the Init response and exits 0 having started nothing (`cli.py` init). Before slice 1.23/1.26 kb built the directory. Slice 47 owns it; consider taking it before the tag.
  - QUESTION FOR THE SPEC: an empty stored file, or one that is YAML but not a mapping, loads as `None`, so Validate raises `AttributeError` and Read raises `TypeError`, tracebacks in shop-knol. The fix would sit in `Store.load` (a non-mapping becomes `Unreadable`); a truncated file is the likeliest "cannot be read" case. Slice 1.19/1.20's scenarios use a mangled bracket only.
  - QUESTION FOR THE SPEC: still raising against "nothing raises": Create for a kind whose schema file is unreadable; Read of a sound artifact refused for a different unreadable file; content that is YAML but not a mapping on Create; `KB_ACTOR` unset and `create --from` a missing file in shop-knol; Validate on a stray kind directory with no schema (`FileNotFoundError`).
  - Minor: a complex YAML key raises `TypeError` in the duplicate check, and `{1: a, "1": b}` is wrongly refused as a duplicate; a fault with no artifact prints with a leading `: `; Create's save-path fault drops `path`; `KbServicer()` with no root fails on anything but Init.
  Next: the tag, pin and plan split, which the user reserved.
- 2026-09-24 Split: kb 0.1 is tagged `v0.1.0` and this repository pins it (commit 90b90ee), so the kb-only slices moved to kb's own plan, `shopsystem-kb/docs/superpowers/plans/2026-09-24-kb-slices.md`, with their numbers, tags, status, and log entries: slices 1.1 to 1.16, 1.18 to 1.23, 1.25, 1.26, 2, 3, 5 to 14, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 46, and 51. Their checkpoint entries and the log entries about them alone went with them; entries about both repositories stay here and are copied there. Left here: slice 0, which checks both checkouts, and slice 1, which mixes kb and shop-knowledge scenarios; kb's plan notes it waits on them. Nothing renumbered, retagged, or re-cut.
- 2026-09-24 From here each repository plans alone. A kb change this repository needs is a request to bump the pin, not a slice here that touches kb: the shop-knowledge slice stands on a kb slice in kb's plan (kb slice 21 for slice 22, kb slice 23 for slice 24, and so on, kb's slice ahead of the one here as before), and waits until kb has released it under a new tag and this repository pins that tag. A shop scenario kb cannot meet at all goes to kb as a question for its spec.
- 2026-09-24 Next: slice 4. Its process and feature types stand on kb slices 2 and 3, a shape shared between types and a type built on a base, so it waits on kb releasing them and this repository bumping the pin.
- 2026-09-26 Suite: 7 passed, 55 failed. Run in this checkout's virtualenv with kb v0.2.0 installed from its tag (`pip show shopsystem-kb` 0.2.0, commit 70d1e88). The 7 are slices 1, 1.17, 1.24, 1.27 and 1.28; every failure is tagged 4 or later.
- 2026-09-26 Re-check against kb v0.2.0. Its contract carries every rpc (Init, Create, Read, Write, Append, Delete, Apply, List, Refs, Search, Journal, Snapshot, Validate), and every kb slice this plan's log names is green in kb's plan: kb 2, 3 and 71 (a shared shape, a base, a base carried in full) for slice 4 and slice 49; kb 5, 6, 7, 51 and 85 (a set as one named change, all or nothing, every fault) for slices 15 and 48; kb 9, 35 and 91 (the history and its filters) for slices 16 and 36; kb 21, 72 and 88 (the resolved read, a link into a part) for slices 17 to 20, 22 and 50; kb 1.3, 1.8 and 94 (finding the store) for slice 22; kb 13, 23 and 90.1 (a whole or a placed write) for slice 24; kb 25, 1.6 and 8.1 (create's refusals, a title already used) for slices 26 and 28; kb 29 for 30; kb 11, 31 and 89 (links in, out, narrowed, two steps with the route) for 32; kb 10 and 33 for 34; kb 37 and 93 for 38; kb 39, 77 and 83.2 for 40; kb 41 and 87 for 42; kb 43 and 81 for 44; kb 1.10, 45 and 94 for 47. The one kb slice not green, 89.2 (links out of one place inside an artifact), is needed by no scenario here. No slice here waits on kb, and none needs a kb change: no request to bump the pin.
- 2026-09-26 What kb v0.2.0 leaves to shop-knol, found in the re-check and changing no slice: kb's Create takes an empty role and an empty message without refusing them, so slice 26's two refusals (nobody, no reason) are shop-knol's own, made before any call; kb stamps the history from its own clock with no clock on the contract, and shop-knol runs as a process of its own, so slice 16's unknown, how step definitions set the day, is settled on this side of the contract or comes back as a request to bump the pin. Slice 16's unknown stands as written.
- 2026-09-26 Order kept. Slice 4 first (the schema language may not say the process type, which could only be answered by a kb release), then 15 to 20 by the size of their unknowns, then the slices with none, by value. v0.2.0 settles none of these unknowns, which are all on this side of the contract, and spends none, so nothing bundles or moves.
- 2026-09-26 Architecture reviews cut, all enabling, none with scenarios, so no feature file changes and no tag moves. Slice 1.29, the first: six slices are implemented here (0, 1, 1.17, 1.24, 1.27, 1.28) and none has been reviewed, and this repository has no `CLAUDE.md` yet, which that slice writes; it is dotted under 1 after 1.28 so no number moves, and a refactor it calls for takes 1.30 onward, ahead of slice 4. Then after every six implemented slices, counting refactors as kb's plan does: 19.1 after 4 to 19, 30.1 after 20 to 30, 42.1 after 32 to 42. Slices 44 to 50 are five, so none follows them. If a review cuts refactors, or a slice turns out green on an earlier slice's work, the reviews after it are recounted and moved.
- 2026-09-26 Next: writing-plans over slices 1.29, 4, 15, 16, 17 and 18, one task per slice in that order, to `2026-09-26-shop-knowledge-batch1-implementation.md`. Slice 1.29's task writes `CLAUDE.md` and runs the review; if the review calls for any refactor, the batch stops there, the refactors are cut as 1.30 onward, and the remaining tasks are re-planned over the new shape.
- 2026-09-26 writing-plans done: `2026-09-26-shop-knowledge-batch1-implementation.md`, six tasks for slices 1.29, 4, 15, 16, 17 and 18 in slice order. It was assembled in a scratch clone and replayed from its own text in a second clone, in the foreground, to the same counts: suite 55/7 before, then 55/7, 54/8, 53/9, 52/10, 51/11 and 50/12 (failed/passed), the 50 left all tagged 19 or later. Task 1 writes `CLAUDE.md` and runs the review; if it cuts any refactor, the batch stops there and the rest is re-planned. What it settled for the slices: slice 4's process type is said in kb's schema language, a step inline or reused through a shared binding shape, refusing neither-or-both, an unbound setting and a link to no step; slice 16's day is set by a test-only `sitecustomize` pointing kb's settable journal clock at a moment, with nothing in `src/` and no kb change; slice 17's resolved whole read is not enough, since kb leaves a link inside an item as a name, so the renderer also reads each reused step whole, with no kb change; slice 18's limits are Anthropic's published skill limits, of which only the 500-line body is one steps can pass. No request to bump the pin. Its Review Focus holds five questions for the spec: a batch file of the wrong shape, a non-process published as a skill, a skill name holding a reserved word, `render --to` a file and `journal` with no `KB_ROOT`, and a branch to no step. No feature file touched. Nothing implemented in this repository. Next: slice 1.29.
- 2026-09-26 First architecture review of shop-knowledge (slice 1.29), by an Opus subagent against `CLAUDE.md` (commit b4834f7), after slices 0, 1, 1.17, 1.24, 1.27 and 1.28. Kept: rules 1, 2, 3, 5, 6, the 250-line limit, a file read in one place, steps drive shop-knol through the driver, hand-editing only to set up and said so; module rows for cli.py, bootstrap.py, types/*.yaml and __main__.py. Broken: rule 4 (one way to refuse, never a traceback) at cli.py:40, 44, 66, 73, 75, 76 and argparse's exit 2; one thing at one level in `_create` (cli.py:71-83) and `_read` (cli.py:86-104); a kb answer's faults refused in one way (cli.py:66 drops Init's faults, bootstrap.py:15-18 drops every Create answer); shared steps in conftest, where "never a traceback" and "reports failure to whatever ran it" are each defined three times (test_check_the_shops_knowledge_is_sound.py:46 and :51, test_read_back_what_the_shop_knows.py:87 and :92, test_record_a_decision.py:126 and :131). Refactors: slice 1.30: the shared refusal steps live in the shared conftest; slice 1.31: reading the user's file lives in its own function in cli.py; slice 1.32: turning a read answer into the shown document lives in its own function in cli.py. The rule-4 and faults-refused-in-one-way breaks call for no refactor, since fixing them changes what shop-knol prints or its exit code. Defects that are not shape: `KB_ROOT` unset gives a KeyError traceback (cli.py:44; slice 22 owns it); `KB_ACTOR` unset gives a KeyError traceback on create and init (cli.py:40; slice 26 for create, slice 47 for init); `KB_ACTOR=` empty or `-m ""` makes kb's git commit fail with a CalledProcessError traceback and leaves staged files in kb/ (slice 26; the kb side may need a pin-bump request), and a missing `-m` gives argparse usage with exit 2 (slice 26); `init` over an existing store or inside one ignores kb's refusal, exits 0 and creates duplicate types `schema/tag-2` and so on (slice 47); `init` of a directory that does not exist exits 0 having started nothing (slice 47); QUESTION FOR THE SPEC: `--from` a missing file or a directory gives a FileNotFoundError or IsADirectoryError traceback (`shop-knol create decision --from /nope.yaml -m x`), no slice owns it; QUESTION FOR THE SPEC: `--from` a file that is YAML but not a mapping gives a TypeError or AttributeError traceback (`echo "- a" > l.yaml; shop-knol create decision --from l.yaml -m x`); QUESTION FOR THE SPEC: a NotCanonical fault prints on two lines (`head -c 50 /bin/ls > b.yaml; shop-knol create decision --from b.yaml -m x`); QUESTION FOR THE SPEC: a fault with no artifact prints with a leading colon (`shop-knol create nosuch --from d.yaml -m x`).
- 2026-09-26 Batch 1 stops after slice 1.29: the review cut slices 1.30 to 1.32. Next: writing-plans over those refactors, then Tasks 2 to 6 of 2026-09-26-shop-knowledge-batch1-implementation.md re-planned over the new shape.
- 2026-09-26 writing-plans done: `2026-09-26-shop-knowledge-batch2-implementation.md`, eight tasks for slices 1.30, 1.31, 1.32, 4, 15, 16, 17 and 18 in slice order. Batch 1's Tasks 2 to 6 are re-planned there as Tasks 4 to 8 over the shape the refactors leave, with a section saying what changed. It was assembled in a scratch clone and replayed from its own text in a second clone, in the foreground, every file under `src/` and `tests/` and `CLAUDE.md` byte-identical to the scratch run's after each task. Suite counts (failed/passed): 55/7 before, the same 55 failing test ids after each refactor, then 54/8, 53/9, 52/10, 51/11 and 50/12, the 50 left all tagged 19 or later. The refactors implement each of `CLAUDE.md`'s refusal rules once rather than as a check in each handler: `cli.Refused` carries every refusal and `main` alone prints it; `cli._document` is the one reader of a user's file; `cli._answered` refuses every kb answer, and a renderer's `Rendered` too; `cli._glance` shapes a read; each subparser names its handler, so a new command is added in one place. Every When that runs shop-knol gives `result`, which the shared Thens in `tests/conftest.py` read. What batch 1 settled still holds and is carried over: slice 4's process type and its four probed refusals, the batch file's shape, the test-only clock, the renderer's own read of each reused step, the 500-line body limit. Found while prototyping: kb v0.2.0's history entry message is `kb_pb2.Entry`. `_validate` raises its faults and violations together; Init's and bootstrap's answers stay ignored, as slice 47 owns refusing them. No request to bump the pin. The five Review Focus questions of batch 1 were reproduced again over the new shape. No feature file touched. Nothing implemented in this repository. Next: slice 1.30.
- 2026-09-26 slice 1.30 green. The shared refusal steps, "the user is shown that fault in plain words, never a traceback" and "the command reports failure to whatever ran it", are defined once in `tests/conftest.py` over the fixture `result`, which every When that runs shop-knol now gives. Check: `same 55` (the 55 failing ids identical to before), `55 failed, 7 passed, 48 warnings in 13.87s` from make test, and the grep for the two step texts outside conftest.py printed nothing.
  Surprised by: nothing.
  Next: slice 1.31.
- 2026-09-26 slice 1.31 green. A file the user gives is read only by `cli._document`, which raises `cli.Refused` where kb cannot read it; `main` catches `Refused` and prints it through `_refuse`, the one printer, and each subparser names its handler. Check: `same 55`, `55 failed, 7 passed, 48 warnings in 14.01s` from make test, `create reads no file`, and `1` from the grep count of read_text in cli.py.
  Surprised by: nothing.
  Next: slice 1.32.
- 2026-09-26 slice 1.32 green. Every kb answer is refused through `cli._answered`, which raises `Refused`, so `main` is the only caller of `_refuse`; `_read` calls, refuses or shows, and `_glance` shapes the answer. `_validate` raises its faults and violations together, as it printed them before. Check: `same 55`, `55 failed, 7 passed, 48 warnings in 13.87s` from make test, `read calls, refuses or shows`; shape check: grep counts `2`, `1`, `1` (`_refuse(`, `if response.faults:`, `read_text`) and no module over 250 lines.
  Surprised by: nothing.
  Open questions: none. The review's rule-4 breaks that change behaviour (Init's answer and bootstrap's Create answers dropped, the `KB_ACTOR` and `KB_ROOT` tracebacks) stay with slices 22, 26 and 47.
  Next: slice 4.
- 2026-09-26 slice 4 green. A user can now: start a knowledge base that holds decisions, features, work items, roles, processes, steps and tags on one base, defining nothing first.
  Assumption "the process type, steps inline or reused with bindings and carrying branches, can be said in kb's schema language": held. Evidence:
  ```text
  process/p at steps/0: {'title': 'Neither'} is not valid under any of the given schemas
  process/p at steps/1: {'title': 'Both', 'does': 'x', 'uses': 'step/check-the-stock'} is valid under each of {'required': ['uses']}, {'required': ['does']}
  process/p at steps/3/with/0: 'value' is a required property
  process/p at steps/2/uses: a link must land on a node of a kind the type allows; 'step/nothing' does not
  exit 1
  ```
  Surprised by: nothing.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 5): a branch's go_to names a step of the same process as a plain string kb does not check; `go_to: nowhere` is stored. Refuse it client-side, or leave it?
  Next: slice 15.
- 2026-09-26 slice 15 green. A user can now: apply a batch file that records a decision and points a work item at it, as one change in the history under one role and one message.
  Assumption "a batch is a file of changes, each with its own content, and the set's actor and message come from the command line like any other change": held. Evidence: `shop-knol apply` printed `batch: 20260926T234829614712Z-1`, `results:` decision/price-reviews-happen-weekly revision 1 and work-item/reprice-the-dairy-shelf revision 2; the Journal under that batch shows `create decision/price-reviews-happen-weekly` and `write work-item/reprice-the-dairy-shelf`, both with message "Review prices weekly, starting with dairy".
  Surprised by: nothing.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 1): a batch file of the wrong shape (`changes:` holding `- delete: tag/pricing`, or no `changes:`) gives `KeyError: 'content'` / `KeyError: 'changes'` tracebacks. What is it told?
  Next: slice 16.
- 2026-09-26 slice 16 green. A user can now: review every change to one decision, oldest first, each with who made it and for which piece of work, when, what it did and why.
  Assumption "step definitions can set the day kb stamps without kb taking a clock on its contract": held. Evidence: `shop-knol journal --artifact decision/price-reviews-happen-weekly` on the scenario's store gave `changes:` with `at: '2026-09-21T10:00:00+00:00'` (shopkeeper, create, "Record weekly reviews", revision 1) then `at: '2026-09-23T10:00:00+00:00'` (role agent, execution reprice-dairy, write, "Accept weekly reviews", revision 2).
  Surprised by: nothing.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 4): `shop-knol journal` with `KB_ROOT` unset gives `KeyError: 'KB_ROOT'`; slice 22 owns finding the knowledge base.
  Next: slice 17.
- 2026-09-26 slice 17 green. A user can now: publish a process into a directory as a skill whose heading block is its identity and whose body is its steps, the reused step written out in full with its settings, leaving the shop's knowledge unchanged.
  Assumption "a resolved whole read, with the stubs of its references and its type, is enough for a renderer to write a reused step out in full": failed, and no kb change was needed. kb v0.2.0 fills in only links in an artifact's own fields ("a link inside one of its items stays a name", kb/read.py), and stubs come only with a summary read. The renderer reads the process whole, then each reused step whole. Evidence: the SKILL.md the scenario publishes, restock-a-shelf/SKILL.md, complete:
    ---
    name: restock-a-shelf
    description: Restock a shelf
    ---

    # Restock a shelf

    ## 1. Check it

    This is the shared step Check the stock, where shelf is dairy.

    Count what is on the shelf, front and back.

    ## 2. Decide

    Decide whether the shelf is short.

    - If the shelf is short, go to step 3 (Order more).
    - If it is not, go to step 4 (Stop).

    ## 3. Order more

    Order enough to fill the shelf.

    ## 4. Stop

    Leave the shelf as it is.
  Surprised by: nothing.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 2): `shop-knol render skill tag/pricing` writes a SKILL.md with no steps and succeeds. Refuse anything that is not a process?
  - QUESTION FOR THE SPEC (Review Focus 4): `render --to` a path that is a file gives a `NotADirectoryError` traceback.
  - QUESTION FOR THE SPEC (Review Focus 5): a branch whose go_to names no step is published as "go to nowhere."
  - The spec says a renderer reads "the resolved whole artifact, the stubs of its references, and its schema"; the skill renderer needs a whole read of each step it reuses as well. If the spec should keep that sentence, the request is for kb to fill in links inside items on a resolved read, a bump of the pin.
  Next: slice 18.
- 2026-09-26 slice 18 green. A user can now: publish a process whose steps run past the 500 lines the harness publishes for a skill's body, and be refused for that reason with nothing written.
  Assumption "the harness publishes limits a renderer can check before writing": held. Anthropic's Agent Skills documentation publishes name (64 characters; lowercase letters, numbers, hyphens; no XML tags; not "anthropic" or "claude"), description (non-empty, 1024 characters, no XML tags), and "Keep SKILL.md body under 500 lines". Evidence: the scenario's stderr was "process/count-every-shelf at steps: a skill's body is under 500 lines, the limit the harness publishes; this one is 801" with exit 1, and the target directory listing was [].
  Surprised by: nothing.
  Open questions:
  - QUESTION FOR THE SPEC: the 500 lines is published "for optimal performance", not as a rejection; the spec's "fail rather than emit" treats it as a limit.
  - QUESTION FOR THE SPEC (Review Focus 3): the name and description limits have no scenario, so a process titled "Ask Claude first" publishes `ask-claude-first/SKILL.md`.
  Next: slice 19.
- 2026-09-27 writing-plans done: `2026-09-27-shop-knowledge-batch3-implementation.md`, one task for slice 19. It was assembled in a scratch clone and replayed from its own text in a second clone, in the foreground, every file under `src/` and `tests/` and `CLAUDE.md` byte-identical to the scratch run's. Suite counts (failed/passed): 50/12 before, 49/13 after, the 49 left all tagged 20 or later. What it settles: the diagram is a Mermaid flowchart, `<name>.mmd`, one node a step numbered in order (a reused step in the subroutine shape), a step without branches going on to the next and a step with them going where each says, labelled with its condition; Mermaid lays it out, so nothing places a node. Of what slice 17 settled, `Rendered`, `_answered` and `_write` are reused with `cli.py` untouched; reading each reused step is not, since a diagram labels a reused step with the title the process gives it. Node ids are `step<n>`, not kb's step names, which a user may write and Mermaid may read as its own words (`end`). No request to bump the pin. Its Review Focus holds five questions for the spec: a `"` in a title or condition breaks the file, a non-process or a process with no steps gives an empty diagram, a branch to no step is drawn to a bare node, `--to` a file gives a `FileExistsError` traceback, and no Mermaid tool here judges whether the drawn diagram is readable. The file name `<name>.mmd` against the spec's `<id>.mmd` is logged as a question too. No feature file touched. Nothing implemented in this repository. Next: slice 19.
- 2026-09-27 slice 19 green. A user can now: publish a process into a directory as a Mermaid diagram of its steps and their branches, `<name>.mmd`, which places no node itself.
  Assumption "steps and branches carry enough structure to draw the diagram without hand layout": held. The steps' order gives each step without branches its next step, each branch gives a labelled edge to the step it names, and a reused step is known from its own item, so the renderer reads the process whole once and nothing else; Mermaid lays the flowchart out. Evidence: `restock-a-shelf.mmd` holds `flowchart TD`, `    step1[["1. Check it"]]`, `    step2["2. Decide"]`, `    step3["3. Order more"]`, `    step4["4. Stop"]`, `    step1 --> step2`, `    step2 -->|"the shelf is short"| step3`, `    step2 -->|"it is not"| step4`, `    step3 --> step4`, one to a line.
  Surprised by: nothing.
  Open questions:
  - QUESTION FOR THE SPEC: the spec names the file `<id>.mmd`; it is `<name>.mmd`, the process's name without its kind, as the skill's directory is. Literally `<id>` would put it at `process/<name>.mmd`.
  - QUESTION FOR THE SPEC (Review Focus 1): a step title or branch condition holding `"` gives a label Mermaid cannot parse (`step1["1. Greet with "hi""]`), and the command exits 0.
  - QUESTION FOR THE SPEC (Review Focus 2): `shop-knol render diagram tag/pricing` writes `pricing.mmd` holding only `flowchart TD` and succeeds; so does a process with no steps.
  - QUESTION FOR THE SPEC (Review Focus 3): a branch whose go_to names no step is drawn to a bare node of that name.
  - QUESTION FOR THE SPEC (Review Focus 4): `render diagram --to` a path that is a file gives a `FileExistsError` traceback.
  - QUESTION FOR THE SPEC (Review Focus 5): no Mermaid tool is installed here, so the bet's "needs manual arrangement to be readable" is judged by a person opening the file, not by the suite.
  Next: slice 19.1.
- 2026-09-27 Suite: 13 passed, 49 failed. Run in this checkout's virtualenv (kb v0.2.0 from its tag) before the review; the 13 are slices 1, 1.17, 1.24, 1.27, 1.28, 4, 15, 16, 17, 18 and 19, and every failure is tagged 20 or later.
- 2026-09-27 Second architecture review of shop-knowledge (slice 19.1), on Opus against `CLAUDE.md`, over the code under `src/` and the step definitions after slices 1.30, 1.31, 1.32, 4, 15, 16, 17, 18 and 19. It took first what the batch 2 and 3 reviews left.
  Kept: rule 1 (`src/` imports from kb only `kb.client`, `kb.contract`, `kb.content` and `kb.canonical` for `NotCanonical`), rule 2, rule 3 (no other YAML library), rule 5 (only the two process renderers know a process's fields; `bootstrap` knows the types' names and nothing else), rule 6 (neither renderer prints, raises, opens or writes); no module over 250 lines (`cli.py` 208, the largest); a user's file read only in `cli._document`; every kb answer but two refused through `cli._answered`, and every refusal printed by `main` alone; the module map, a row for each module; every When that runs shop-knol gives `result`, the shared Thens live in `tests/conftest.py`, each step that reads a knowledge base's files or calls kb in process says why, and `tests/clock/` reaches shop-knol only through `driver.at`.
  Broken, and the refactor each calls for:
  - Rule 4 (one way to refuse, never a traceback), for input no scenario lists. Every one of these exits 1 with a traceback today, reproduced in a started knowledge base: a batch file whose change names no content (`KeyError: 'content'`), with no `changes` (`KeyError: 'changes'`), whose `changes` is not a list, or that is a list (`TypeError`); `create --from` a file that is a list (`TypeError: pop expected at most 1 argument`), a path not there (`FileNotFoundError`), or a directory (`IsADirectoryError`); `render skill --to` a file (`NotADirectoryError`) and `render diagram --to` a file (`FileExistsError`). Two more break "one line each": a file that is not text prints kb's message over two lines, and a fault naming no artifact (`create nosuch`) prints with a leading colon. These are one class, not nine questions: nothing checks the shape of a file a user gives before its entries are indexed, and nothing turns an operating system's refusal of a path into a fault. Slice 20.1 makes the class unreachable with the rule implemented once: each file a user gives is checked, where `_document` reads it, against a shape held as data as the types are, its violations worded as kb words a type's; `main` turns an operating system's refusal of a path into a fault naming it, as it turns `Refused`; and the one printer prints each fault as one line, the place omitted when the fault names none. It answers the QUESTION FOR THE SPEC lines logged at slices 1.29 (`--from` a missing file or a directory; a file that is YAML but not a mapping; a fault on two lines; a leading colon), 15 (a batch file of the wrong shape), 17 and 19 (`--to` a file). The spec already says "shop-knol never shows a traceback" and CLAUDE.md's rule 4 says it too, so no scenario is needed and none is added. What "behaviour does not change" means for that slice, my call as the user is away: every scenario gives the same answer, and every stdout and exit status is as it was; the only change is that a traceback both documents forbid becomes one plain line. A catch-all turning any exception into a line was weighed and not taken: its words would be Python's (`'content'`), and it would hide a defect as a refusal.
  - The two refusals that bypass `_answered`. Validate's answer is raised as `Refused` in `_validate` over its faults and violations; slice 42.2 refuses it through `_answered`, placed by its risk, nil, right before slice 44, the next slice to touch the check. Init's answer, and each Create answer bootstrap makes, is dropped rather than refused; refusing them changes what `init` exits with where a knowledge base already is, which is slice 47's scenarios, so no refactor is cut and slice 47's Needs line now carries it.
  - `renderers/skill.py`'s `body` and `renderers/diagram.py`'s `flowchart` are public and used only inside their modules, and the two renderers read the artifact whole and cut its kind off its name each in their own words (`skill._whole`, and `diagram.render` inline; `split("/", 1)` twice). Slices 20 and 50 would copy both a third and fourth time. Slice 19.2 gives the renderers one way to read what they publish and makes every renderer function but `render` private. Slice 20 needs it, so it alone goes ahead of slice 20.
  - Size, ahead of a break: `cli.py` is 208 lines, and slices 22 to 30 add the whole, section and filled-in reads, JSON, finding the knowledge base, `write`, refusals, a pipe and `list`, which cross 250. "When a change would cross the limit, split first": slice 20.2 moves the shaping of each kb answer into what the user is shown (`_glance`, `_change`, the apply and create answers) into a module of its own with a row in `CLAUDE.md`, and precedes slice 22, the first slice that needs the room.
  Not called for: the title split off a user's content, in `_create` and in `batch`, is two lines each and slice 24's write takes no title; slice 16's Given starting shop-knol inline under a set day, beside `driver.start`, is one call; `skill.render` makes its two reads and its refusal at one level.
  Still QUESTION FOR THE SPEC, since each needs a scenario to say what is shown and no rule does: `KB_ROOT` unset (slice 22 owns it), `KB_ACTOR` unset (slices 26 and 47), `KB_ACTOR=` empty or `-m ""` ending in kb's git failure and a missing `-m` giving usage with exit 2 (slice 26); a non-process published as a skill or a diagram, a process with no steps, a branch to no step, a `"` in a title or condition in a diagram, a skill name holding a reserved word, the 500 lines published "for optimal performance", and `<name>.mmd` against the spec's `<id>.mmd`.
  Placed, by risk among the slices not yet begun and never ahead of all of them: 19.2 before 20, which needs it; 20.1 after 20, since slice 20's unknown, a page from the type alone, is the larger; 20.2 after 20.1 and before 22, which needs the room; 42.2 before 44, which needs it. No scenario is added or moved, so no feature file and no `@slice` tag changes. Slice 30.1, the third review, stays where it is, as 19.1 stayed after 1.30 to 1.32 were cut: it now follows nine implemented slices, 19.2, 20, 20.1, 20.2, 22, 24, 26, 28 and 30, and its check says nine.
  Next: writing-plans over slices 19.2, 20, 20.1, 20.2, 22, 24, 26, 28 and 30, one task per slice in that order, to `2026-09-27-shop-knowledge-batch4-implementation.md`.
- 2026-09-27 writing-plans done: `2026-09-27-shop-knowledge-batch4-implementation.md`, nine tasks for slices 19.2, 20, 20.1, 20.2, 22, 24, 26, 28 and 30 in slice order. Written under adrs/0011: the plan carries no code, and nothing was built or replayed. Each task says why its scenarios or check are red today, found by running them in this checkout and probing shop-knol and kb v0.2.0 by hand in `.superpowers/`. Expected counts are taken from the tags (failed/passed): 49/13 before, then 49/13, 48/14, 48/14, 48/14, 38/24, 36/26, 33/29, 30/32 and 27/35. The 27 left are exactly the scenarios tagged 32 or later.
  Decisions it makes for the implementer:
  - the renderers read through one module, `renderers/source.py`;
  - the markdown page is laid out from kb's content model, `sections` apart from fields, with no schema read; parts are not coded, since the role the scenario publishes holds none;
  - a user's file is checked where `_document` reads it, against JSON Schema shapes held as data in `shapes/`, with kb's own validator class. A throwaway spike showed the batch shape gives one violation line for each bad batch the 20.1 check lists;
  - `main` turns an `OSError` into a fault naming the path;
  - the printer prints one line per fault and leaves out the place when a fault names none;
  - answers are shaped in `answers.py`;
  - the store is found by `kb.client.connect()` with no root, and kb's three refusals pass through;
  - `read` takes `--section`, `--whole`, `--resolve [N]` and `--json`, with JSON written by the standard library (CLAUDE.md rule 3 amended);
  - `write <name>#<place>` uses kb's link notation for a part;
  - one function refuses a missing actor or message before any file is read or any kb call is made;
  - `--from -` reads standard input in `_document`;
  - `list` answers a sequence.

  Found while probing, and set down in the plan's tasks:
  - slice 26's type-mismatch scenario, and slice 28's piece-of-work and title-used scenarios, already pass on existing behaviour once their steps exist;
  - slice 22's one-step resolve Then is vacuous over the Background.

  No request to bump the pin. No feature file touched. Nothing implemented. Its Review Focus holds five questions for the spec: argparse's usage errors bypass rule 4; `--json` is on `read` alone; `list --ids` is YAML, not bare lines; "superseded" is a status the user writes, not the link; parts as tables are unpinned. Next: slice 19.2.
- 2026-09-27 slice 19.2 green. New `renderers/source.py` holds `whole` (read whole, depth 0 by default) and `slug` (name without kind); skill and diagram call it, `body` and `flowchart` are private, CLAUDE.md has the row. Check: `same 49`, `49 failed, 13 passed`, defs grep gives only the two `render` lines, WHOLE grep gives `renderers/source.py`, split grep gives `src/shop_knowledge/renderers/source.py:1`; GREEN expression `13 passed`; shape check 2, 1, 1, no long module, no renderer listed.
  Surprised by: nothing. Decision recorded in adrs/0014 (module name `source`).
  Next: slice 20.
- 2026-09-27 slice 20 green. A user can now publish a role into a directory and find `stock-keeper.md`: its title as a heading, its fields as a list (a field group nested, a list of plain values joined), and its section as a heading one level down.
  Assumption "the page can be laid out from the type alone": held. Evidence, the page the scenario publishes, complete:
  ```
  # Stock keeper

  - **harness**
    - **name**: stock-keeper
    - **description**: Keeps the shelves stocked.
    - **tools**: Read
  - **shop**
    - **responsible_for**: What is on the shelves

  ## How it works

  Counts, then orders.
  ```
  It rests on kb's content model: the whole read's own order, and `sections` told apart from fields. No schema is read and no type is named (`grep -nE "harness|shop|role" renderers/markdown.py` finds only the `shop_knowledge` import paths).
  Surprised by: the title is on the read's answer (`ReadResponse.title`), never in the content, so the page takes its heading from there. Decision recorded in adrs/0015 (the file is `<name>.md`, the page's shape, read at depth 0, parts not coded).
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 5): parts as tables are not pinned. The role holds no part collection, so the scenario checks none. Reproduction, `.superpowers/batch4/repro5.py`, publishing `process/restock-a-shelf` (three steps) as markdown, real output:
    ```
    0
    # Restock a shelf

    - **steps**: {'id': 'check-it', 'title': 'Check it', 'uses': 'step/check-the-stock', 'with': [{'name': 'shelf', 'value': 'dairy'}]}, {'id': 'decide', 'title': 'Decide', 'does': 'Decide.\n', 'branches': [{'when': 'short', 'go_to': 'order-more'}]}, {'id': 'order-more', 'title': 'Order more', 'does': 'Order.\n'}
    ```
    Worse than the plan predicted: a list of mappings is not a nested list but Python's own repr on one line. A user would expect the table the scenario's title promises, and a page of readable steps.
  - The scenario is silent on the file's name (`<name>.md` chosen), on depth (0 chosen), and on a list of mappings, a field group inside a list, or a section with no body.
  Next: slice 20.1.
- 2026-09-27 slice 20.1 green. Every file a user gives is checked where `_document` reads it against a JSON Schema shape held as data in `shapes/` (by `shape.py`), a file that is not text is refused as a fault on it, `main` turns an `OSError` into a fault naming the path, and the printer joins a multi-line message and leaves out an empty artifact.
  Assumption "the shape of every file a user gives can be checked where it is read, in kb's words, with the shapes held as data": held. Evidence, the eleven stderr lines of Step 1's cases, verbatim (each exit 1, stdout 0, one line, 0 tracebacks):
    nocontent.yaml at changes/0: {'delete': 'tag/pricing'} is not valid under any of the given schemas
    nochanges.yaml: 'changes' is a required property
    notalist.yaml at changes: 3 is not of type 'array'
    list.yaml: ['a'] is not of type 'object'
    list.yaml: ['a'] is not of type 'object'
    nope.yaml: No such file or directory
    adir: Is a directory
    nottext.yaml: it is not text that can be read: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
    afile/say-hello: Not a directory
    afile: File exists
    a kind must name a type the store holds; the store holds no type called 'nosuch'
  Check: same 48, 48 failed, 14 passed.
  Surprised by: nothing in the shapes; the render cases name the file the write reached (`afile/say-hello`), not the directory given. Decision in adrs/0016.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 1): argparse still refuses in its own way, so rule 4 holds for files and paths but not for arguments. Reproduction, `shop-knol nosuch`: argparse's usage on stderr, exit 2. A user would expect one plain line and exit 1. No scenario pins any argument error.
  Next: slice 20.2.
