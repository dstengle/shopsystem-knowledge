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
- Status: green

## Slice 22: Read a decision at every depth, as text or JSON, from wherever the user works

- Kind: capability
- Scenarios: shop-knowledge / read-back-what-the-shop-knows / The user reads the whole decision; shop-knowledge / read-back-what-the-shop-knows / The user reads one section of a decision; shop-knowledge / read-back-what-the-shop-knows / The user reads a decision with the things it points at filled in; shop-knowledge / read-back-what-the-shop-knows / The user takes the same answer as JSON; shop-knowledge / read-back-what-the-shop-knows / The user asks for the links to be followed two steps; shop-knowledge / read-back-what-the-shop-knows / The user reads from a folder inside the shop's knowledge; shop-knowledge / read-back-what-the-shop-knows / The user reads while working elsewhere, having named the knowledge base; shop-knowledge / read-back-what-the-shop-knows / Reading where no knowledge base can be found is refused; shop-knowledge / read-back-what-the-shop-knows / Reading with KB_ROOT naming somewhere that holds no knowledge base is refused; shop-knowledge / read-back-what-the-shop-knows / Reading from inside one knowledge base while KB_ROOT names another is refused
- Observable: A user reads a decision whole with what it points at shown by name, or only its rationale, or whole with what it points at filled in one step when they do not say how far, or two steps so the tag inside the older decision is filled in too, and can take any of those answers as JSON instead of the default; and the user reads from a folder deep inside the shop's knowledge and is answered from the knowledge base found above them, or from elsewhere with KB_ROOT naming the shop's, and is refused with the command reporting failure where none can be found, where KB_ROOT names a directory holding no knowledge base, or where they work inside one knowledge base while KB_ROOT names another.
- Unknown: none
- Needs: none
- Status: green

## Slice 24: Revise a recorded decision, whole or in part

- Kind: capability
- Scenarios: shop-knowledge / revise-what-the-shop-knows / The user revises a recorded decision; shop-knowledge / revise-what-the-shop-knows / The user revises one part of a recorded decision
- Observable: A user replaces a decision from a file and the shop holds the new wording at a later version, or replaces only its rationale and the rest reads as before.
- Unknown: none
- Needs: none
- Status: green

## Slice 26: A decision the shop cannot accept is refused

- Kind: capability
- Scenarios: shop-knowledge / record-a-decision / A decision that does not fit the shop's decision type is refused; shop-knowledge / record-a-decision / A decision recorded by nobody is refused; shop-knowledge / record-a-decision / A decision recorded without a reason is refused
- Observable: A user records a file that does not fit the decision type and is told which artifact and place is at fault with the command exiting non-zero, or records without saying which role they are, or without a message, and is refused for that reason.
- Unknown: none
- Needs: none
- Status: green

## Slice 28: Record a decision from a pipe, under a piece of work, or with a title already used

- Kind: capability
- Scenarios: shop-knowledge / record-a-decision / The user pipes a decision in instead of naming a file; shop-knowledge / record-a-decision / The user records a decision as part of a piece of work; shop-knowledge / record-a-decision / A decision whose title is already used is given a name of its own
- Observable: A user pipes a decision from another command into the record command and the shop holds it as if it had come from a file, a user working as the shopkeeper on a named piece of work records one and the change is attributed to both; and a user records a decision whose title is already used and is shown a name of its own for it, the taken name with a number added, while the earlier decision still reads back by its name.
- Unknown: none
- Needs: none
- Status: green

## Slice 28.1: The command line's arguments sit apart from its handlers

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same 31 failing scenarios as before the slice (31 failed, 31 passed); `shop-knol -h`, `shop-knol <command> -h` for each of the eight commands, and `shop-knol nosuch` give byte for byte what they gave before, with the same exit codes; `grep -cE "argparse|add_parser|add_argument" src/shop_knowledge/cli.py` -> 0; `wc -l < src/shop_knowledge/cli.py` -> under 210; the module that now holds the arguments holds no handler, no kb call and no `print`, and CLAUDE.md's module map has a row for it
- Observable: The command line has room again: slice 28's pipe and slice 30's list each add a few lines to the module holding the handlers without it reaching CLAUDE.md's 250-line limit, because the arguments every command takes are declared in a module of their own.
- Unknown: none
- Needs: none
- Status: green

## Slice 30: List what the shop has recorded

- Kind: capability
- Scenarios: shop-knowledge / list-what-the-shop-has-recorded / The user lists every decision; shop-knowledge / list-what-the-shop-has-recorded / The user lists the decisions that match a field; shop-knowledge / list-what-the-shop-has-recorded / The user lists only the names, to feed another command
- Observable: A user lists the decisions and sees all three with name and title, narrows to the superseded one by a field, or asks for names only and sees three names fit to feed another command.
- Unknown: none
- Needs: none
- Status: green

## Slice 30.1: Third architecture review

- Kind: enabling
- Check: an Opus review of the code and the step definitions against `CLAUDE.md`, after the ten implemented slices since slice 19.1 (19.2, 20, 20.1, 20.2, 22, 24, 26, 28, 28.1 and 30), is in this plan's log, and every refactor it calls for is a slice of its own right after this one with a check -> the log entry and those slices
- Observable: Anyone can read whether the read, revise, record and list commands kept the code in the shape CLAUDE.md sets.
- Unknown: none
- Needs: none
- Status: green

## Slice 32: Follow the links from the command line

- Kind: capability
- Scenarios: shop-knowledge / follow-the-links-between-what-the-shop-knows / The user sees what a decision points at; shop-knowledge / follow-the-links-between-what-the-shop-knows / The user sees what points at a decision; shop-knowledge / follow-the-links-between-what-the-shop-knows / The user narrows the links to one kind of link and one kind of thing; shop-knowledge / follow-the-links-between-what-the-shop-knows / The user follows the links two steps out
- Observable: A user follows the links out of a decision and sees the older decision, in and sees both work items, narrowed to one link and one kind and sees both work items and nothing else, or two steps out and sees the older decision and the tag each with the route taken.
- Unknown: none
- Needs: none
- Status: green

## Slice 32.1: What a command showed is read by one fixture every feature shares

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same failing scenarios as before the slice (23 failed, 39 passed); `grep -c "def shown" tests/*.py | grep -v ":0"` -> one line, `tests/conftest.py:1`
- Observable: The search, history, snapshot, append and retire steps that read what shop-knol showed find one fixture for it in the shared conftest, as CLAUDE.md says of a fixture more than one feature uses, instead of copying a fourth, fifth and sixth one.
- Unknown: none
- Needs: none
- Status: green

## Slice 34: Search what the shop knows

- Kind: capability
- Scenarios: shop-knowledge / search-what-the-shop-knows / The user searches the prose; shop-knowledge / search-what-the-shop-knows / The user searches within one kind of thing; shop-knowledge / search-what-the-shop-knows / The user searches the fields as well as the prose
- Observable: A user searches for a word and sees each result with the section it matched and a snippet with the heaviest section first, narrows to decisions and sees the two decisions and not the process, or includes the fields and also sees a decision whose title carries the word.
- Unknown: none
- Needs: none
- Status: green

## Slice 36: Review by role, piece of work, or date

- Kind: capability
- Scenarios: shop-knowledge / review-who-changed-what / The user reviews what one role did; shop-knowledge / review-who-changed-what / The user reviews what one piece of work did; shop-knowledge / review-who-changed-what / The user reviews the changes since a date
- Observable: A user reviews the shopkeeper's changes and sees only the recording of the decision, a piece of work's changes and sees only the agent's revision, or the changes since yesterday and sees only today's revision.
- Unknown: none
- Needs: none
- Status: green

## Slice 36.1: Each command's request to kb is built apart from its handler

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same failing scenarios as before the slice (17 failed, 45 passed); `grep -cE "kb_pb2\.[A-Za-z]*Request\b|kb_pb2\.Locator\(" src/shop_knowledge/cli.py` -> 0; `wc -l < src/shop_knowledge/cli.py` -> under 205; the module that now builds the requests holds no `print(`, no `connect` and no call on a client, and CLAUDE.md's module map has a row for it
- Observable: The command line keeps room under the 250-line limit through slices 38 to 50, which add snapshot, append and retire and extend the check and the start, because a handler only makes its call, refuses or shows, and turning a command's arguments into kb's request sits in a module of its own, as turning kb's answer into what is shown already does.
- Unknown: none
- Needs: none
- Status: green

## Slice 36.2: An argument shop-knol cannot take is refused the one way every refusal is

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same failing scenarios as before the slice (17 failed, 45 passed); each of `shop-knol`, `shop-knol nosuch`, `shop-knol list`, `shop-knol list --type decision --json`, `shop-knol read decision/x --resolve two` and `shop-knol create decision` prints exactly one line on stderr, with no `usage:`, nothing on stdout, and exits 1; `shop-knol -h` and `shop-knol <command> -h` for every command give byte for byte what they gave before the slice, with exit 0
- Observable: A user who mistypes a command or a flag is told what is wrong in one plain line with exit 1, as CLAUDE.md's rule 4 says of every refusal shop-knol makes, so every command added after it keeps the rule without a scenario of its own.
- Unknown: none
- Needs: none
- Status: green

## Slice 36.3: No name in the code says less or other than it does

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same failing scenarios as before the slice (17 failed, 45 passed); `grep -cE "^\s+validate = " src/shop_knowledge/arguments.py` -> 0; `grep -c "def _show(document: dict," src/shop_knowledge/cli.py` -> 0; `grep -cE "def knol\(.*\binput\b" tests/driver.py` -> 0; `.venv/bin/python -c "import inspect,shop_knowledge.cli as c; assert 'shape =' not in inspect.getsource(c._read)"` succeeds; every public function of the module shaping answers is named in its CLAUDE.md row, and its docstring and that row say it gives lists as well as dicts
- Observable: A reader of the code finds no assignment nothing reads, no hint naming a type an argument is not given, no parameter hiding a built-in or a local hiding a module, and a module map that names every public function the answers module has.
- Unknown: none
- Needs: none
- Status: green

## Slice 38: Record what a piece of work read

- Kind: capability
- Scenarios: shop-knowledge / record-what-a-piece-of-work-read / An agent records what it read
- Observable: An agent records, for its piece of work, the decision and process it read, and the shop's history holds one entry naming each with the version read.
- Unknown: none
- Needs: none
- Status: green

## Slice 40: Add a step to a process

- Kind: capability
- Scenarios: shop-knowledge / add-a-step-to-a-process / The user adds a step written in place; shop-knowledge / add-a-step-to-a-process / The user adds a step that reuses a shared step
- Observable: A user adds a step written in place and it is the last step with the user told its name, or adds a step that uses a shared step with its own settings and the process runs it there with those settings while the shared step and its other users are unchanged.
- Unknown: none
- Needs: none
- Status: green

## Slice 42: Retire what the shop no longer uses

- Kind: capability
- Scenarios: shop-knowledge / retire-what-the-shop-no-longer-uses / The user retires something nothing points at; shop-knowledge / retire-what-the-shop-no-longer-uses / The user retires something that is still pointed at
- Observable: A user retires a tag nothing points at and the shop no longer holds it, or retires a tag a decision carries and is refused, seeing everything that points at it.
- Unknown: none
- Needs: none
- Status: green

## Slice 42.1: Fourth architecture review

- Kind: enabling
- Check: an Opus review of the code and the step definitions against `CLAUDE.md`, after the ten implemented slices since slice 30.1 (32, 32.1, 34, 36, 36.1, 36.2, 36.3, 38, 40 and 42), is in this plan's log, and every refactor it calls for is a slice of its own placed by its risk among the slices not yet begun, with a check -> the log entry and those slices
- Observable: Anyone can read whether the links, search, history, snapshot, append and retire commands kept the code in the shape CLAUDE.md sets.
- Unknown: none
- Needs: none
- Status: green

## Slice 42.2: The check's answer is refused the one way every kb answer is

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same failing scenarios as before the slice; `.venv/bin/python -c "import inspect,shop_knowledge.cli as c; assert 'Refused' not in inspect.getsource(c._validate)"` succeeds; `CLAUDE.md` names one place a kb answer's faults are not refused through `_answered` directly, a renderer's, and not Validate's
- Observable: The check command's faults and violations are refused through the one refusal of kb answers, so slice 44, which extends the check, adds to that path rather than to a second one.
- Unknown: none
- Needs: none
- Status: green

## Slice 44: Check the shop's knowledge is sound

- Kind: capability
- Scenarios: shop-knowledge / check-the-shops-knowledge-is-sound / The user checks a sound knowledge base; shop-knowledge / check-the-shops-knowledge-is-sound / The user checks a knowledge base with faults; shop-knowledge / check-the-shops-knowledge-is-sound / The user is told what is behind its type
- Observable: A user checks a sound knowledge base and is told nothing is wrong, checks one with two faults and sees both with the artifact and place while the command exits non-zero, or sees a decision listed as behind its type and not as a fault.
- Unknown: none
- Needs: none
- Status: green

## Slice 47: The shop's knowledge base sits beside the shop's work, is started by someone for no stated reason, and is not started twice

- Kind: capability
- Scenarios: shop-knowledge / start-a-shop-knowledge-base / The shop's knowledge sits in a place of its own inside the directory it was started in; shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base where the directory already holds one is refused; shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base inside one the shop already has is refused; shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base asks for no reason; shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base without saying who is refused
- Observable: A user starts a shop knowledge base in a directory holding other work of the shop's and finds the knowledge kept in a place of its own inside it, with that work left as it was; starting one where the directory already holds the shop's knowledge, or in a directory inside it, is refused for that reason with everything the shop already knows unchanged; starting one saying who but giving no reason succeeds with everything it was given recorded in the shop's history under a reason the command writes itself, and starting one without saying who is refused for that reason, the directory holding no knowledge base and the command reporting failure.
- Unknown: none
- Needs: Init's answer and bootstrap's Create answers, both dropped today, refused the one way every kb answer is (the two refusals of starting where a knowledge base already is)
- Status: green

## Slice 48: One bad change in a batch leaves the shop untouched

- Kind: capability
- Scenarios: shop-knowledge / make-several-changes-at-once / One bad change in a batch leaves the shop untouched
- Observable: A user applies a batch whose second change does not fit its type; the batch is refused with every fault, and none of it is in the shop.
- Unknown: none
- Needs: none
- Status: green

## Slice 48.1: A whole read the steps make is driven one way

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same failing scenarios as before the slice; `grep -c "def _whole" tests/*.py | grep -v ":0"` -> no line; `grep -c "^def whole" tests/driver.py` -> 1
- Observable: The steps that read an artifact whole through shop-knol find that read in the driver beside `record`, instead of the two word-for-word copies in the revise and add-a-step modules and a third that slice 49's reads of a role, a decision and a tag would add.
- Unknown: none
- Needs: none
- Status: green

## Slice 49: The shop's roles and tags hold their shape

- Kind: capability
- Scenarios: shop-knowledge / start-a-shop-knowledge-base / A role keeps its harness fields apart from its shop identity; shop-knowledge / start-a-shop-knowledge-base / Anything the shop knows can be tagged
- Observable: A user records a role and its harness fields sit in one named group and its shop identity in another, and tags a decision with a tag so the decision names it while the tag's description is held once, on the tag.
- Unknown: none
- Needs: none
- Status: green

## Slice 50: Publish a role as an agent

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / The user publishes a role as an agent
- Observable: A user publishes a role into a directory and finds an agent whose heading block is the role's harness fields and whose body is its prose.
- Unknown: none
- Needs: none
- Status: green

## Slice 50.1: What an argument means is said once, and nothing is named for a use it does not have

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same failing scenarios as before the slice; `grep -cE 'or ""|is None|Path\(' src/shop_knowledge/kb_requests.py` -> 0; `grep -c "Path(args.root)" src/shop_knowledge/cli.py` -> 0; `.venv/bin/python -c "import shop_knowledge.cli as c, shop_knowledge.arguments as a; p=a.command_parser(); assert list(c._HANDLERS) == list(p._subparsers._group_actions[0].choices)"` succeeds; `grep -c "def locator" src/shop_knowledge/kb_requests.py` -> 0, and neither the module's docstring nor its CLAUDE.md row names a helper `cli` does not call; `shop-knol -h` and `shop-knol <command> -h` for every command give byte for byte what they gave before the slice
- Observable: A reader finds each argument's type and default where the argument is declared, the handler table in the order the help lists the commands, and the request module naming only the helper the command line uses, so no default is patched in a second place.
- Unknown: none
- Needs: none
- Status: green

## Slice 50.2: Fifth architecture review

- Kind: enabling
- Check: an Opus review of the code and the step definitions against `CLAUDE.md`, after the eight implemented slices since slice 42.1 (42.2, 44, 47, 48, 48.1, 49, 50 and 50.1), is in this plan's log, and every refactor it calls for is a slice of its own with a check -> the log entry and those slices
- Observable: Anyone can read whether the check, the start, the batch, the role and tag types and the agent renderer kept the code in the shape CLAUDE.md sets.
- Unknown: none
- Needs: none
- Status: green

## Slice 50.3: Every When that runs shop-knol gives what it ran, and every whole read a step makes goes through the driver

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> `62 passed`, the same as before the slice; `grep -h -A3 "^@when" tests/*.py | grep -o 'target_fixture="[a-z_]*"' | sort | uniq -c` -> one line, `42 target_fixture="result"`; `grep -n '"--whole"' tests/*.py` -> two lines, `tests/driver.py` and the When of `test_read_back_what_the_shop_knows.py` that is the user's whole read; `grep -c "does not exist yet" tests/*.py | grep -v ":0"` -> no line; `git diff --stat -- src features` -> empty
- Observable: A reader finds every When that runs shop-knol handing on what it ran as `result`, every whole read a Then makes going through the driver's one way, and no comment saying a command is missing that the shop now has.
- Unknown: none
- Needs: none
- Status: green

## Slice 50.4: No step definition module is over 250 lines

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> `62 passed`; `.venv/bin/python -m pytest --collect-only -q | grep -c ::` -> 62; `find src tests -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'` -> nothing; `grep -l "import \*" tests/*.py` -> exactly `tests/test_read_back_what_the_shop_knows.py` and `tests/test_start_a_shop_knowledge_base.py`; no new module under `tests/` is named `test_*`; `grep -n "250" CLAUDE.md` shows the size rule naming `src/` and `tests/`, and CLAUDE.md's Step definitions section says where a feature's steps go when one module cannot hold them; `git diff --stat -- src features` -> empty
- Observable: A reader finds no module under `src/` or `tests/` over the limit, and CLAUDE.md saying the limit covers both and how a feature's steps are split when they outgrow one module.
- Unknown: none
- Needs: none
- Status: green

## Slice 50.5: The publish feature's markdown steps sit apart from its other steps

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` -> the same ten failing scenarios as before the slice, and `56 passed, 10 failed`; `.venv/bin/python -m pytest --collect-only -q tests/test_publish_what_the_shop_knows.py | grep -c ::` -> 8; `find src tests -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'` -> nothing; `grep -l "import \*" tests/*.py` -> exactly the test modules of publish-what-the-shop-knows, read-back-what-the-shop-knows and start-a-shop-knowledge-base; no new module under `tests/` is named `test_*`; `git diff --stat -- src features` -> empty
- Observable: A reader finds the publish feature's markdown steps in a module of their own beside its test module, so the markdown and agent steps slices 50.6 and 50.7 add keep every module under 250 lines.
- Unknown: none
- Needs: none
- Status: green

## Slice 50.6: Markdown lays out each kind of value as markdown

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / Markdown lays out each kind of value as markdown (both rows: the process's steps, the role's tags)
- Observable: A user publishes a process as markdown and finds its steps as a table with a column for each thing a step says, and a role with tags and finds its tags as a bullet list, with no value on either page written the way a program prints it.
- Unknown: whether every value kb's content model holds, a part collection and the lists and mappings inside its items among them, can be laid out as markdown from the content alone, with no schema read and no type named
- Needs: slice 20's page Then expects the role's `tools` as a bullet list, the layout adrs/0038 and 0041 set; its Then line is unchanged
- Status: green

## Slice 50.7: An agent the harness would reject is not published

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / An agent the harness would reject is not published
- Observable: A user publishing a role whose harness name the harness would not load is told which limit it breaks, and finds nothing written.
- Unknown: whether the agent renderer can hold a role's harness fields to the limits the harness publishes for an agent the way the skill renderer holds a process's body to its limit, before anything is written
- Needs: none
- Status: green

## Slice 50.8: The shop's knowledge base starts where the user works, and elsewhere only when they name the place

- Kind: capability
- Scenarios: shop-knowledge / start-a-shop-knowledge-base / The user starts a knowledge base somewhere else on purpose by naming the place. The six start scenarios rewritten in commit 1133296 go green with it under the tags they keep: The user starts a knowledge base and the shop's types are ready (`@slice-4`); Starting a knowledge base asks for no reason, Starting a knowledge base without saying who is refused, The shop's knowledge sits in a place of its own inside the directory it was started in, Starting a knowledge base where the directory already holds one is refused, Starting a knowledge base inside one the shop already has is refused (`@slice-47`)
- Observable: A user starts the shop's knowledge base from the directory they work in without naming one, is refused there as before where one exists or they are inside one, and starts one elsewhere only by naming the place.
- Unknown: whether a knowledge base started from the working directory with no directory named is made, and refused, just as one started by naming it
- Needs: the suite's shared way of starting a knowledge base starts it from the shop's directory without naming it (adrs/0037, 0042)
- Status: green

## Slice 50.9: Sixth architecture review

- Kind: enabling
- Check: an Opus review of the code and the step definitions against `CLAUDE.md`, after the six implemented slices since slice 50.2 (50.3 to 50.8), is in this plan's log, and every refactor it calls for is a slice of its own with a check -> the log entry and those slices
- Observable: Anyone can read whether the markdown layout, the agent's limits and the init default kept the code in the shape CLAUDE.md sets.
- Unknown: none
- Needs: none
- Status: green

## Slice 50.10: shop-knol refuses, never tracebacks, when the working directory no longer exists

- Kind: capability
- Scenarios: shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base from a directory that has been removed ends in a plain refusal; shop-knowledge / read-back-what-the-shop-knows / Reading from a directory that has been removed ends in a plain refusal
- Observable: A user whose shell sits in a directory that has since been removed is refused in one plain line, not shown a traceback, whether they start a knowledge base or read from one.
- Unknown: whether shop-knol can meet a working directory that no longer exists with its own refusal before it has taken any argument, with the working directory still `init`'s default and that default still declared once (adrs/0032, 0037)
- Needs: a way for the steps to run shop-knol from a directory removed after the user's shell entered it
- Status: green

## Slice 50.11: Markdown spells a yes, a no and an empty value in words

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / Markdown never shows a yes, a no or an empty value the way a program prints it (all four rows: a role's yes and no, a role's empty value, a process step's yes and no, a process step's empty value)
- Observable: A user publishing a role or a process as markdown finds a yes as `yes`, a no as `no` and an empty value as nothing, in the field list and in a table cell alike, and never `True`, `False`, `None`, `true`, `false` or `null` (adrs/0043).
- Unknown: whether a value the user wrote as a yes, a no or an empty value still reaches the page as one after kb has checked and stored it, and is told apart there from text that reads `yes`
- Needs: the Then that no value on the page is a programming language's representation also looks for the spellings adrs/0043 rules out (batch 9 final review, minor 7); slice 50.6's scenarios run under that Then unchanged
- Status: green

## Slice 50.12: The batch 9 review's minor findings are tidied

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> `72 passed`, the same as after slice 50.11; `grep -rn "Task [0-9]" src tests --include="*.py"` -> nothing; `grep -c "role/stock-keeper" tests/publish_as_markdown.py` -> 0; `grep -c "Fault(" src/shop_knowledge/renderers/limits.py` -> 1; in the publish feature's test module every fixture is defined before the first step; a reader of the markdown renderer's table test and field layout, and of the publish feature's markdown steps module, finds each docstring naming everything its code holds and does; the size check lists nothing; `git diff --stat -- features src/shop_knowledge/types` -> empty
- Observable: A reader finds the markdown steps publishing whichever role a Given names, every fixture of the publish feature in one place, the harness limits' faults built one way, no docstring pointing at a task of a batch plan, and the docstrings the review found short or awkward saying what their code does.
- Unknown: none
- Needs: none
- Status: green

## Slice 50.13: A check that finds faults still shows what is behind its type

- Kind: capability
- Scenarios: shop-knowledge / check-the-shops-knowledge-is-sound / The user is told what is behind its type even when the check finds faults
- Observable: A user whose check finds faults sees them, one line each, and in the same run sees which artifacts are behind their type, the command still reporting failure (adrs/0046).
- Unknown: whether a refusal can carry the check's answer on stdout while its faults still reach the user only through the one printer, one line each, exit 1
- Needs: none
- Status: green

## Slice 50.14: Markdown stays well-formed whatever a value holds, an empty list shown as nothing

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / Markdown stays well-formed whatever a value holds (all four rows); shop-knowledge / publish-what-the-shop-knows / Markdown never shows a yes, a no or an empty value the way a program prints it (all six rows; its first four were made green by slice 50.11, and the outline moves here with its two new empty-list rows)
- Observable: A user publishing as markdown finds every table row with one cell per column, no line ending in a space, every value shown, and an empty list shown as its field's name and colon, or an empty cell (adrs/0043, 0045).
- Unknown: whether any text a value holds can be shown in a cell or a line as written, the character that separates cells among it, without the page's layout breaking
- Needs: none
- Status: green

## Slice 50.15: A renderer refuses an artifact of a type it does not render

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / Publishing something as a kind of file it cannot become is refused (all three rows: a process as an agent, a role as a skill, a role as a diagram)
- Observable: A user publishing something as a kind of file it cannot become is refused, told the artifact's type and the type that kind is made from, and finds nothing written.
- Unknown: whether a renderer can tell what type an artifact is from what it reads through the contract before it lays anything out
- Needs: none
- Status: green

## Slice 50.16: Seventh architecture review

- Kind: enabling
- Check: an Opus review of the code and the step definitions against `CLAUDE.md`, after the six implemented slices since slice 50.9 (50.10 to 50.15), is in this plan's log, and every refactor it calls for is a slice of its own with a check -> the log entry and those slices
- Observable: Anyone can read whether the removed working directory, the yes/no/empty spelling, the tidy, the check's answer beside its faults, the well-formed page and the renderers' type check kept the code in the shape CLAUDE.md sets.
- Unknown: none
- Needs: none
- Status: green

## Slice 50.16.1: The steps know kb only through what kb publishes, with a stand-in for kb where the contract cannot reach

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> `80 passed, 21 failed`, the same 21 as before the slice; `grep -rn "kb import canonical\|kb\.canonical\|kb\.store\|kb\.values\|store.yaml\|/ \"schema\"\|\"schema\")\|read_bytes\|_everything_under" tests` -> nothing; `grep -rln "kb.journal" tests` -> only `tests/clock/sitecustomize.py`, which slice 50.23 replaces; `grep -rn '/ "kb" /' tests` -> nothing; `grep -rhoE "^from kb[a-z_.]* import|^import kb[a-z_.]*" tests | sort -u` -> only `kb.client`, `kb.content` and `kb.contract`; `git diff --stat -- features src` -> empty; CLAUDE.md's Step definitions section says what adrs/0047 says (no step reads or writes a knowledge base's files; a stand-in at the contract boundary for a state no contract call can produce), and its rule 1 names `tests/` alongside `src/`
- Observable: A reader finds no step touching a knowledge base's files or any kb module kb does not publish: the damaged, unfit and dangling artifacts the check and read-back scenarios need, and the history on a given day the review scenarios need, come from a stand-in for kb that answers with kb's contract messages, while every other scenario runs against the real kb. The clock the review-by-date scenarios pin stays as it is until kb publishes one (slice 50.23).
- Unknown: whether a stand-in for kb can be put in front of shop-knol's own process at the contract boundary, from `tests/` alone, with nothing under `src/` knowing it is there
- Needs: none
- Status: green

## Slice 50.16.2: No test reaches a knowledge base outside its own temporary directory

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> `80 passed, 21 failed`, the same 21; a throwaway `kb/store.yaml` made in the checkout's parent directory makes the suite refuse to start, saying why (logged, then removed); every shop-knol run the driver makes has a working directory under the test's temporary directory, and a throwaway call of the driver with no working directory is refused (logged, reverted)
- Observable: A developer running the suite in a directory whose parents hold the shop's real knowledge base finds the suite refusing to run rather than reading or writing it.
- Unknown: none
- Needs: none
- Status: green

## Slice 50.16.3: The steps hold kb only to a fault order kb states

- Kind: enabling
- Check: the 50.16 review's R4 check: `grep -n "splitlines()\[0\]\|splitlines()\[1:\]\|lines\[0\]\|lines\[1\]" tests/test_check_the_shops_knowledge_is_sound.py` -> nothing; the batch Then of `tests/test_make_several_changes_at_once.py` compares fault lines as a set; a throwaway reversal of the printer's loop in `cli._refuse` leaves those scenarios green (logged, reverted); the suite -> `80 passed, 21 failed`
- Observable: A reader finds no Then that fails if kb returns the same faults in another order.
- Unknown: none
- Needs: none
- Status: green

## Slice 50.16.4: The steps never spell kb's fault wording

- Kind: enabling
- Check: `.venv/bin/python -m pytest -q` -> `80 passed, 21 failed`; each Then the 50.16 review's coupling point 17 names checks what the shop's spec owns (one line, the artifact and the place, printed as kb returned it), comparing with the fault kb's in-process client (`kb.client.connect`) returns for the same state, or with what the stand-in gave, never a message fragment written in the step; a throwaway rewording of one kb fault message in `.venv` leaves those scenarios green (logged, reverted with `pip uninstall -y shopsystem-kb` then `make dev`)
- Observable: A reader finds kb free to reword its faults without a shop scenario going red, since the shop holds kb only to its `rule` names and to printing what kb returns (kb adrs/0018).
- Unknown: whether every Then that reads kb's words today can get the same words from kb itself for the same state
- Needs: none
- Status: green

## Slice 50.16.5: The markdown pages the publish steps expect are built in one module that holds no step

- Kind: enabling
- Check: the 50.16 review's R1 check (`grep -n "from publish_as_markdown" tests/*.py` -> nothing; the new helper module holds no step; one page reader; `_steps_as_a_table` compares with the built page; `_step_holding` refuses an id it does not find); the suite -> `80 passed, 21 failed`
- Observable: A reader finds the expected markdown pages built in one place, with no step module importing another (adrs/0035).
- Unknown: none
- Needs: none
- Status: green

## Slice 50.16.6: The batch 11 review's minor findings are tidied

- Kind: enabling
- Check: the 50.16 review's R2 check (`_not_a_fault` matches the artifact exactly; `_a_failing_checks_answer` has a docstring; `_after_the_colon` renamed; the type-refusal Then spells its three lines; `renderers/source.py`'s docstring says `refusal` decides; `_role_page`'s docstring plain); the suite -> `80 passed, 21 failed`
- Observable: A reader finds the batch 11 minors gone.
- Unknown: none
- Needs: none
- Status: green

## Slice 50.16.7: Eighth architecture review

- Kind: enabling
- Check: an Opus review of the code and the step definitions against `CLAUDE.md` and adrs/0047, after the six enabling slices 50.16.1 to 50.16.6, is in this plan's log, and every refactor it calls for is a slice of its own with a check -> the log entry and those slices
- Observable: Anyone can read whether the stand-in, the test isolation and the tidies left the suite knowing kb only through what kb publishes.
- Unknown: none
- Needs: none
- Status: planned

## Slice 50.17: A name given empty is refused, starting a knowledge base first

- Kind: capability
- Scenarios: shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base in a directory given an empty name is refused
- Observable: A user who gives `init` an empty directory name is refused, told it names no place, and finds nothing started where they work.
- Unknown: whether an empty name can be refused for every argument that names a place, the one way every argument refusal is (adrs/0023), with each argument's meaning still declared once (adrs/0032)
- Needs: none
- Status: planned

## Slice 50.18: Starting a knowledge base from a removed directory says the directory is gone

- Kind: capability
- Scenarios: shop-knowledge / start-a-shop-knowledge-base / Starting a knowledge base from a directory that has been removed ends in a plain refusal (rewritten in 7b23b54; slice 50.10 made its earlier Thens green)
- Observable: A user starting a knowledge base from a directory that has since been removed is told, in plain words, that the directory they are working in is gone.
- Unknown: whether shop-knol can tell a working directory that is gone from the operating system's other refusals, before kb is called
- Needs: none
- Status: planned

## Slice 50.18.1: Prose the shop cannot keep is refused in plain words

- Kind: capability
- Scenarios: shop-knowledge / record-a-decision / A decision whose prose the shop cannot keep is refused; shop-knowledge / revise-what-the-shop-knows / A revision whose prose the shop cannot keep is refused (both rows); shop-knowledge / add-a-step-to-a-process / A step whose prose the shop cannot keep is refused; shop-knowledge / make-several-changes-at-once / A batch whose prose the shop cannot keep leaves the shop untouched
- Observable: A user recording, revising, adding a step or applying a batch from a file whose prose has a line ending in a space before its last is refused in plain words naming the place, and the shop is unchanged, where today the command ends in a traceback.
- Unknown: whether text kb cannot keep is found where a user's file is read and checked, once, for every command that sends content
- Needs: none
- Status: planned

## Slice 50.18.2: Markdown's remaining well-formed cases

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / Markdown stays well-formed whatever a value holds (all ten rows; its six rows added in b0b535f are red: a title ending in a space; a section title ending in a space; a list of lists with an empty last item; a list holding a mapping with an empty last value; a field group's list of mappings with an empty last value; a column name holding the cell separator; the outline moves from `@slice-50.14` to `@slice-50.18.2`, its first four rows credited to slice 50.14)
- Observable: A user publishing as markdown finds no heading or item line ending in a space and every table's heading row with one cell per column, whatever the artifact holds.
- Unknown: none
- Needs: none
- Status: planned

## Slice 50.18.3: A check with no knowledge base to check shows no answer

- Kind: capability
- Scenarios: shop-knowledge / check-the-shops-knowledge-is-sound / Checking where the shop's knowledge cannot be found is refused (all three rows)
- Observable: A user checking where no single knowledge base can be found is refused as every command is, and shown no check's answer; the behaviour 0c7d199 restored, now held by the suite.
- Unknown: none
- Needs: none
- Status: planned

## Slice 50.19: Recording from a file given an empty name is refused

- Kind: capability
- Scenarios: shop-knowledge / record-a-decision / Recording from a file given an empty name is refused
- Observable: A user recording from a file named with nothing is refused as naming no place, and the shop is unchanged.
- Unknown: none
- Needs: none
- Status: planned

## Slice 50.20: Reading something given an empty name is refused

- Kind: capability
- Scenarios: shop-knowledge / read-back-what-the-shop-knows / Reading something given an empty name is refused
- Observable: A user reading an artifact named with nothing is refused as naming no place.
- Unknown: none
- Needs: none
- Status: planned

## Slice 50.21: Publishing into a directory given an empty name is refused

- Kind: capability
- Scenarios: shop-knowledge / publish-what-the-shop-knows / Publishing into a directory given an empty name is refused
- Observable: A user publishing into a directory named with nothing is refused as naming no place, and nothing is written where they work.
- Unknown: none
- Needs: none
- Status: planned

## Slice 50.22: Reading from a removed directory, refused or served through KB_ROOT

- Kind: capability
- Scenarios: shop-knowledge / read-back-what-the-shop-knows / Reading from a directory that has been removed ends in a plain refusal (rewritten in 7b23b54; slice 50.10 made its earlier Thens green); shop-knowledge / read-back-what-the-shop-knows / The user reads from a directory that has been removed, having named the knowledge base
- Observable: A user reading from a directory that has since been removed is served through `KB_ROOT` when it names a knowledge base, and otherwise told the directory they are working in is gone.
- Unknown: none here; kb finds the store
- Needs: kb's store finding treats a working directory that no longer exists as inside no store (the kb pin-bump request logged 2026-09-27)
- Status: blocked: awaiting a kb release carrying the pin-bump request

## Slice 50.23: shop-knowledge imports nothing of kb but what kb publishes

- Kind: enabling
- Check: `grep -rhoE '^\s*(from kb[a-z_.]* import|import kb[a-z_.]*)' src tests | sort -u` -> only `kb.client`, `kb.content` and `kb.contract` (an indented import caught too, not only one flush against the margin); `grep -rn "kb.journal" tests` -> nothing; `pyproject.toml` pins the kb release carrying kb's slices 100 and 102; `.venv/bin/python -m pytest -q` -> every scenario passes; CLAUDE.md's rule 1 names only what kb publishes (kb adrs/0018); `record_refused_files`' named-once Then catches `kb.content.NotCanonical` and takes the place from its `path`
- Observable: A reader finds `NotCanonical` taken from `kb.content`, where kb publishes it, `record_refused_files`' named-once Then catching `kb.content.NotCanonical` and taking the place from its `path`, the review-by-date scenarios' days given through the clock kb publishes on `kb.client.connect` instead of by replacing a kb function, and nothing else of kb's internals anywhere in the repository.
- Unknown: none
- Needs: the kb release carrying kb slices 100 (`NotCanonical` re-exported from `kb.content`) and 102 (a clock given to the in-process client), pinned
- Status: blocked: awaiting kb 0.3.0 (kb slices 100, 102 and 102.2 to 102.6); the stand-in's `connect(root=None)` must take the `clock` keyword kb publishes (kb batch 20 review)

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
  - QUESTION FOR THE SPEC, answered by rule 4 through slice 36.2 (argument errors are refused as any refusal, adrs/0023) (Review Focus 1): argparse still refuses in its own way, so rule 4 holds for files and paths but not for arguments. Reproduction, `shop-knol nosuch`: argparse's usage on stderr, exit 2. A user would expect one plain line and exit 1. No scenario pins any argument error.
  Next: slice 20.2.
- 2026-09-27 slice 20.2 green. What the user is shown is shaped in `answers.py` (`created`, `glance`, `applied`, `history`, `change`, `written`), and `cli.py` calls it and prints through `_show`. Someone can now add a shape for an answer without touching the command line.
  Moved: `_glance`, `_change`, the history's wrapper, the create, apply and render answers; `CLAUDE.md` has the `answers.py` row. Decision in adrs/0017.
  Check: red first, the grep gave 2 and `cli.py` was 223 lines. Green: diff against `failing-20.1.txt` same 48; `make test` 48 failed, 14 passed; the grep gives 0; `wc -l` gives 190; `grep -cE "print|Request|connect" answers.py` gives 0; shape check 2, 1, 1, no module over 250, no renderer listed.
  Surprised by: nothing.
  Open questions: none. Next: slice 22.
- 2026-09-27 slice 22 green. A user can now read a decision whole with its links as names, or one section, or whole with its links filled in one step or two, and take any of those as JSON; and the store is found above where they work or through `KB_ROOT`, with the three ways of not finding one refused.
  Evidence, the stderr of scenarios 8, 9 and 10, verbatim (each exit 1, stdout empty):
    no store was found, neither above /tmp nor named outright
    KB_ROOT names a directory that holds no store: /tmp/../tmp
    KB_ROOT names a store other than the one <cwd>/a/b is working in: KB_ROOT is <cwd>/other, the working directory is inside <cwd>/a; neither is guessed at
  (the last, real run from `.superpowers/batch4/s22`, has `<cwd>` for /home/vscode/shopsystem-knowledge/.superpowers/batch4/s22.) With `_client` put back to reading `KB_ROOT`, 6, 8, 9 and 10 fail (KeyError traceback, and `the store holds nothing by the name ...` for 9 and 10); 7 passes, since `KB_ROOT` is set there.
  Check: `-m slice-22` 10 passed; `make test` 38 failed, 24 passed; GREEN plus slices 20 and 22 24 passed; shape check 2, 1, 1, no module over 250, no renderer listed; `cli.py` 219 lines.
  Surprised by: nothing in kb; scenarios 5 and 7 to 10 needed no code beyond what the scenarios before them wrote (`--resolve N`, and `_client` connecting with no root), so each was red only on its undefined steps. Decision in adrs/0018.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 2): `--json` is on `read` alone, though the spec says output is "YAML by default and `--json` for the same structure". Reproduction, `shop-knol journal --json`: argparse's usage, `unrecognized arguments: --json`. A user would expect JSON from every command that answers.
  - QUESTION FOR THE SPEC, answered by rule 4 through slice 36.2 (argument errors are refused as any refusal, adrs/0023) (Review Focus 1): argparse still refuses in its own way. Reproduction, `shop-knol read decision/weekly --resolve two`: usage on stderr, `argument --resolve: invalid int value: 'two'`, exit 2. A user would expect one plain line and exit 1.
  - QUESTION FOR THE SPEC: `--section` given with `--whole` or `--resolve` is not refused; the section read is made and the other flag is ignored. Reproduction, `shop-knol read decision/weekly --section Rationale --whole` shows only `title: Rationale` and `body`, exit 0.
  - QUESTION FOR THE SPEC: the scenarios say "no knowledge base"; kb says "no store", and shop-knol passes kb's words through ("errors are printed as returned by kb"). Whether that meets the bet passed-through-errors-are-actionable, or the user's word should be used, is the spec's.
  - QUESTION FOR THE SPEC: scenario 3's "what that older decision points at is shown by name only" is vacuous over the Background, whose older decision points at nothing. The step asserts every link inside the filled-in decision is a string, and the Background cannot tell depth 1 from depth 2 there.
  Next: slice 24.
- 2026-09-27 slice 24 green. A user can now replace a decision from a file and read it back with the new wording at a later version, or replace only one part, named `<name>#<place>`, and have the rest read as before.
  Evidence, `read --whole` before and after the rationale is replaced (real run, `.superpowers/batch4/s24`; `write ... -m y` printed `id: decision/price-reviews-happen-weekly`, `revision: 2`):
    revision: 1 ... Purpose: Keep prices in step with costs. / Rationale, body: Costs move weekly.
    revision: 2 ... Purpose: Keep prices in step with costs. / Rationale, body: Costs now move every day.
  Check: `-m slice-24` 2 passed; `make test` 36 failed, 26 passed; GREEN plus slices 20, 22 and 24 26 passed; shape check 2, 1, 1, no module over 250, no renderer listed; `cli.py` 240 lines.
  Surprised by: kb's WriteResponse carries a revision and faults but no id, so the answer's id is the locator's name. Scenario 2 was red on its undefined When alone, since scenario 1's code already served it. Decision in adrs/0019.
  Open questions:
  - QUESTION FOR THE SPEC: a part is named with kb's link notation, `<name>#<place>` (`decision/price-reviews-happen-weekly#sections/rationale`), while `read` names a section by `--section <title>`. A user who reads a section by title must write its place, lower-cased with hyphens, to replace it.
  - QUESTION FOR THE SPEC: a whole write's file carries no title, and kb refuses one in kb's words. A user who copies their create file into `write` is refused over its title. Reproduction: `shop-knol write decision/x --from <the create file> -m why`.
  Next: slice 26.
- 2026-09-27 slice 26 green. A user who records a file that does not fit the decision type is told the artifact and place at fault, and one who records without a role or without a message is refused for that reason, with nothing written.
  Evidence, real run (`.superpowers/batch4/s26`), stderr, exit 1 each:
    decision/t at sections: the sections the type requires must all be present, in order; 'Rationale' is missing
    every change must say which role made it, through KB_ACTOR as role or role:execution
    every change must carry a message, given with -m
  Check: `-m slice-26` 3 passed; `make test` 33 failed, 29 passed; GREEN plus slices 20, 22, 24 and 26 29 passed; shape check 2, 1, 1, no module over 250, no renderer listed; `cli.py` 250 lines.
  Scenario 1 (does not fit the type) was met by existing behaviour once its steps existed: `create` already refuses through `_answered`. It went red with its Then asserting a wrong line ('Rationale' is absent), then green with the real one. Scenarios 2 and 3 were red as the brief predicted (a traceback; argparse usage). Decision in adrs/0020.
  Surprised by: cli.py is now exactly at the 250-line limit, so the next slice that adds to it needs a split first.
  Open questions:
  - `init` without an actor is refused by the same role check in the same words. Slice 47's scenario wants its own words ("starting one must say which role did it"); slice 47 will reword the refusal for `init`.
  Next: slice 28.
- 2026-09-27 HAND-BACK slice 28, scenario "The user pipes a decision in instead of naming a file": going green needs a change to `cli._document` that `cli.py` (exactly 250 lines) has no room for, and CLAUDE.md says split first; the split is a refactor slice of its own, not improvised here.
  Evidence: red as predicted, `create decision --from -` stderr `-: No such file or directory`, exit 1. Measured the smallest natural change to `_document` (read `sys.stdin` when the source is `-`, and name the source `standard input` in a fault, brief decision 1): `cli.py` 254 lines. The only change that stays at 250 is one line, `loads(sys.stdin.read() if source == "-" else Path(source).read_text())`; it makes the read work but a fault on piped text would name its source `-`, against decision 1, so it was not kept. Candidates to move out of `cli.py` (function line counts measured): `_render` and `_write` (lines 238-250, 13 lines, the render command's handler and file writing); `_init` (146-152, 7); `_document` (154-166, 13, with `Refused` handling), which could sit in a module that owns reading a user's file; `_read_request` and `_read` (198-214, 17); `_parser` (50-101, 52 lines) is the largest single piece. A refactor slice must free at least 4 lines, preferably more, before slice 28's stdin read can land.
  Green in this slice: "The user records a decision as part of a piece of work", "A decision whose title is already used is given a name of its own" (both met by existing behaviour once their steps existed; each first went red on a wrong Then, the execution `restock-the-shelvesx` and the name `-3`). Red: "The user pipes a decision in instead of naming a file" (its steps are not in the tree; the attempt is in `.superpowers/batch4/s28-scenario1-attempt.diff`).
- 2026-09-27 Suite: 31 passed, 31 failed
- 2026-09-27 RE-SLICE after the HAND-BACK of slice 28 (first row of the table: split the remaining work; no Given, When or Then changes, no scenario is added, no feature file is touched). Cut slice 28.1, an enabling refactor with a check, that moves the arguments out of `cli.py` so the handlers and the parser no longer share one module (adrs/0021). Slice 28 keeps its number, tag and two green scenarios; it is in progress, and its pipe scenario finishes after 28.1, the only work it needs first. Slice 30 follows unchanged. Order: 28.1, then slice 28's pipe scenario, then 30, then the 30.1 review, which now counts ten slices.
- 2026-09-27 slice 28.1 green. Moved `cli._parser` whole to the new `src/shop_knowledge/arguments.py` (50 lines, public `command_parser()`, no handler bound); `cli.py` builds it from there and looks the handler up by `args.command` in `_HANDLERS`, a table at the end of the module (after the handlers it names); the CLAUDE.md map has the `arguments.py` row and `cli.py` no longer owns "its arguments". `cli.py` is 208 lines.
  Check: failing scenarios diff against before: same; `make test`: 31 failed, 31 passed; arguments snapshot before and 28.1: no diff; shape check `2 1 1 0`, no module over 250, no renderer listed; `wc -l < cli.py`: 208; `grep -c "arguments.py" CLAUDE.md`: 1; `grep -cE "print|Request|connect|_pb2|handler" arguments.py`: 2, both the word "prints" in the help texts of create and apply, which the snapshot holds byte for byte (with `print\(` in place of `print` it is 0).
  Surprised by: the check's `print` matches two help strings; and `_HANDLERS` cannot sit beside `_MUTATING` because it names functions defined below, so it is the last thing in the module.
  Next: slice 28, its pipe scenario.
- 2026-09-27 slice 28 green. Someone can now: pipe a decision from another command into `shop-knol create decision --from - -m <why>` and have the shop hold it as if it had come from a file.
  Check: `-m slice-28`: 3 passed; `make test`: 30 failed, 32 passed; GREEN plus slice 28: 32 passed; shape check `2 1 1 0`, no module over 250, no renderer listed; `grep -n stdin cli.py`: line 105, inside `_document`; `wc -l < cli.py`: 210; arguments snapshot 28 against 28.1: no diff.
  Red first: the undefined Given; then `-: No such file or directory` (exit 1) once the steps and `knol`'s `input` existed; then, with `_document` reading the pipe, a Then asserting a wrong title failed on the title; then the true Then passed.
  Evidence: `create decision --from -` with the decision piped answered `id: decision/prices-are-reviewed-monthly`, `revision: 1`; `read decision/prices-are-reviewed-monthly --whole` gave the title, the Purpose section ("Keep prices current.") and the Rationale section ("Monthly was enough once."), revision 1. `printf 'title: x\nsections: 3\n' | shop-knol create decision --from - -m why` printed on stderr `decision/x at sections: 3 is not of type 'array'` and exited 1 (the shape check names the artifact by the type and title, so `standard input` shows only in a fault with no such name, e.g. on `apply`: `standard input at changes/0: ... is not valid under any of the given schemas`).
  Surprised by: nothing.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 1): an empty batch still ends in a traceback. Run after this task: `printf 'changes: []\n' > b.yaml; shop-knol apply --from b.yaml -m why` printed a traceback ending `subprocess.CalledProcessError: Command '[git, ... commit, -q, -m, why, --]' returned non-zero exit status 1`, exit 1. The same through the pipe (`printf 'changes: []\n' | shop-knol apply --from - -m why`) gives the same traceback. Rule 4 is broken by kb v0.2.0; either a pin bump once kb refuses an empty Apply, or `minItems: 1` on the batch shape. A user would expect one plain line saying the batch holds no change.
  - QUESTION FOR THE SPEC (Review Focus 5): `apply` takes a pipe the spec's table does not give it. Run after this task: `printf 'changes: []\n' | shop-knol apply --from - -m why` is read from standard input and reaches kb (traceback as above); a valid batch piped in (`changes: [{create: decision, content: {...}}]`) is applied and answers `id: decision/second`, `revision: 1`. A user would expect either every `--from` to take `-` or `apply` to refuse it plainly.
  - Piped text is read to its end with no limit and an empty pipe is text like any other; no scenario says otherwise.
  Next: slice 30.
- 2026-09-27 slice 30 green. Someone can now: list the decisions with `shop-knol list --type decision`, see each with its name and title, narrow them with `--where FIELD=VALUE`, or take the names alone with `--ids`.
  Check: `-m slice-30`: 3 passed; `make test`: 27 failed, 35 passed; GREEN plus slices 28 and 30: 35 passed; 27 FAILED lines, and the later-slices expression collects 27; shape check `2 1 1 0`, no module over 250, no renderer listed; `wc -l < cli.py`: 219; arguments snapshot 30 against 28 (with `list` in the loop): only `list` in the top-level usage and choices, in the command list, in the `nosuch` choices, and the new `list -h` block.
  Red first: the undefined Background Given for all three (then the undefined When); scenario 1 then failed on argparse `invalid choice: 'list'` (exit 2); scenario 2 on `unrecognized arguments: --where status=superseded`; scenario 3 on `unrecognized arguments: --ids`. Each Then passed on first run once its When worked, so no Then was seen red on its own assertion.
  Evidence: the three answers, verbatim (`$` is the command; the sequence is printed indented two spaces):
    list --type decision
      - id: decision/price-reviews-happen-weekly
        type: decision
        title: Price reviews happen weekly
        supersedes: decision/prices-are-reviewed-monthly
      - id: decision/prices-are-reviewed-monthly
        type: decision
        title: Prices are reviewed monthly
      - id: decision/the-shop-opens-at-nine
        type: decision
        title: The shop opens at nine
    list --type decision --where status=superseded
      - id: decision/prices-are-reviewed-monthly
        type: decision
        title: Prices are reviewed monthly
    list --type decision --ids
      - decision/price-reviews-happen-weekly
      - decision/prices-are-reviewed-monthly
      - decision/the-shop-opens-at-nine
  Surprised by: the sequence is printed indented two spaces (kb.content's output); the Thens load it, so no scenario minds.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 2): `list --ids` is YAML, not bare lines. Run after this task: `shop-knol list --type decision --ids | xargs -n1 shop-knol read` first ran `read -` and printed `-: a name is a kind and a plain name of lower-case letters, digits and single hyphens, never a path; '-' is not`, then read each name after it. A user would expect one name to a line, or a JSON array.
  - QUESTION FOR THE SPEC (Review Focus 3): "superseded" is a status the user writes, not the link. Run after this task: two decisions, the second with `supersedes` pointing at the first and neither with a status; `list --type decision --where status=superseded` printed `[]` and exited 0. A user would expect the link to count.
  - QUESTION FOR THE SPEC, answered by rule 4 through slice 36.2 (argument errors are refused as any refusal, adrs/0023) (Review Focus 4): argparse still refuses in its own way. Run after this task: `shop-knol list` printed usage and `shop-knol list: error: the following arguments are required: --type` on stderr, exit 2; `shop-knol list --type decision --json` printed usage and `unrecognized arguments: --json`, exit 2. Rule 4 says one plain line and exit 1.
  - `--where status` (no `=`) is split as field `status` with the empty value; no scenario pins it and it is not refused. Run after this task: `shop-knol list --type decision --where status` printed `[]` and exited 0.
  Next: slice 30.1, the third architecture review, which runs before the next plan (adrs/0011).
- 2026-09-27 Suite: 35 passed, 27 failed. Run in this checkout's virtualenv (kb v0.2.0 from its tag) before the review; the 35 are slices 1, 1.17, 1.24, 1.27, 1.28, 4, 15 to 20, 22, 24, 26, 28 and 30, and every failure is tagged 32 or later.
- 2026-09-27 Third architecture review of shop-knowledge (slice 30.1), on Opus 5.5 against `CLAUDE.md`, over the code under `src/` and the step definitions after slices 19.2, 20, 20.1, 20.2, 22, 24, 26, 28, 28.1 and 30. It took first what batches 4 and 5 left for it.
  Kept: rule 1 (`src/` imports from kb only `kb.client`, `kb.contract`, `kb.content`, and `kb.canonical` for `NotCanonical` in `cli._document`; `jsonschema` only in `shape.py`), rule 2, rule 3 (no other YAML library; JSON only through `json` in `_show`), rule 5 (only the skill and diagram renderers know a process's fields; `bootstrap` knows the types' names alone; the markdown renderer tells only `sections` apart), rule 6 (no renderer prints, opens or writes; `cli._write` alone writes); no module over 250 lines (`cli.py` 219, the largest); a user's file, or the pipe, read only in `cli._document`; every kb answer but Validate's refused through `cli._answered`, every refusal printed by `main` alone; a row in the module map for each module; every When that runs shop-knol gives `result`, the shared Thens in `tests/conftest.py`, the one step calling kb in process (`test_make_several_changes_at_once.py`, the batch's history) saying why, and `tests/clock/` reaching shop-knol only through `driver.at`.
  Broken, and the refactor each calls for:
  - Size, ahead of a break. `cli.py` is 219 lines. Slices 32 to 42 add `refs`, `search`, the history's three filters, `snapshot`, `append` and `delete`. Measured by reading their requests in kb's contract and the handlers of today, each new handler is about seven lines with its blank lines and its entry in the handler table, and `refs`, whose request takes a direction, a link, a kind and a depth, about ten: 32 brings `cli.py` to about 229, 34 to about 238, 36 (three request fields) to about 241, and 38 to about 251, past the limit. Most of what grows is a command's arguments turned into kb's request: `_locator`, `_is_whole`, `_read_request`, the list's `--where` split and form, the create's title split off the content, and each new command's request. Answers are already shaped apart (`answers.py`); requests are not. Slice 36.1 builds every command's request in a module of its own, beside `batch.py`, which already turns a batch file into Apply's operations, leaving each handler to call, refuse and show (adrs/0022). It frees about 40 lines, so slices 38 to 50 fit with room. Placed before 38, the first slice the estimate says crosses; 32, 34 and 36 each stop and hand back if the estimate is wrong for them, as slice 28 did.
  - Rule 4 (one way to refuse, never a traceback) for arguments. Rule 4 says every refusal shop-knol makes is a `Fault` printed by the one printer, one line each, with exit 1. argparse refuses on its own: usage and a message on stderr, exit 2. Reproduced 2026-09-27: `shop-knol nosuch`, `shop-knol list`, `shop-knol list --type decision --json`, `shop-knol read x --resolve two`, `shop-knol create decision`. A rule settles it, not a scenario, so it is a refactor and not a question, as slice 20.1 was for files and paths: slice 36.2 makes argparse's refusal a refusal like any other, argparse's own message on one line through the printer with exit 1, help untouched (adrs/0023). Spike, run in `.superpowers/batch6/` and thrown away: an `ArgumentParser` subclass whose error raises in place of exiting is used by its subparsers too, and raises for an unknown command, a missing required argument, a value of the wrong type, an unrecognized argument and no command at all. What "behaviour does not change" means for it, my call as the user is away: every scenario gives the same answer, every stdout and every help text is as it was, and the one change is that the usage block and exit 2 become the one line and exit 1 rule 4 already states.
  - A fixture defined in two test modules. `shown` is defined word for word in `test_read_back_what_the_shop_knows.py` and `test_list_what_the_shop_has_recorded.py`; CLAUDE.md puts a fixture more than one feature uses in `tests/conftest.py`. Slice 32 will want a third, and 34, 36, 38, 40 and 42 more. Slice 32.1 defines it once in the conftest. Placed after 32, since placing it first would put it ahead of the whole plan; slice 32 defines its own beside its scenarios as the other two did, and 32.1 takes all three.
  - Names that say less or other than the code does, the minors deferred from batches 4 and 5, and one more found here: `validate = commands.add_parser(...)` in `arguments.py` assigns a name nothing reads; `cli._show` is hinted `document: dict` though `answers.listed` and `answers.names` give it lists; `driver.knol`'s parameter `input` hides the built-in; `cli._read`'s local `shape` hides the module `shape` it imports; and `CLAUDE.md`'s `answers.py` row names nine public functions where the module has eleven (`whole` and `section` are missing), while it and the module's docstring say "plain dicts" of a module that gives lists too. Slice 36.3 puts each right. Placed after 36.2, which touches `arguments.py` first; no slice needs it sooner.
  - Validate's answer refused outside `_answered` stays with slice 42.2, and Init's and bootstrap's dropped answers with slice 47, as the second review placed them.
  Not called for: the markdown renderer's list of mappings. Reproduced after slice 20 (Review Focus 5 of batch 4): publishing a process as markdown writes its steps as one Python `repr` line (`- **steps**: {'id': 'check-it', 'title': 'Check it', ...}, {...}`). The spec says what a page shows, "parts as tables" (The CLI section's renderer list), and no CLAUDE.md rule does, so a refactor cannot change it: it is behaviour a scenario must pin. QUESTION FOR THE SPEC: the markdown page's parts, and any field that holds a list of mappings, are shown as tables; which columns, in what order, and what a nested list inside an item becomes. It needs a scenario from formulating-features over publish-what-the-shop-knows before any slice builds it; the role in slice 20's scenario holds no part, so nothing green pins it either way. Nor a pipe read to its end with no bound: neither the spec nor CLAUDE.md bounds what a user gives, and a named file is read whole the same way, so no rule is broken; a bound would be the spec's, and it stays the note slice 28 logged.
  Waiting on kb, not a slice here: an empty batch still ends in kb's git traceback (`printf 'changes: []\n' | shop-knol apply --from - -m why`, slice 28's Review Focus 1). kb is fixing it in kb slice 97. Request to bump the pin once kb releases it under a new tag; until then rule 4 is broken there by kb v0.2.0, and nothing is coded here.
  Found while probing kb v0.2.0 for the next plan, changing no slice: `Refs` at depth 0 reaches nothing, so a command that says no depth asks for one step; `Snapshot` and `Delete` with an empty message end in kb's git traceback, which shop-knol never reaches as long as both are mutating commands that ask for `-m` before any call (adrs/0020); a step appended to a process is named by kb from its title, and its place is `steps/<that name>`.
  Placed, by risk among the slices not yet begun and never ahead of all of them: 32.1 after 32; 36.1 before 38, which needs the room; 36.2 after 36.1, since it adds lines to `main`; 36.3 after 36.2. No scenario is added or moved, so no feature file and no `@slice` tag changes. Slice 42.1, the fourth review, stays where it is and now follows ten implemented slices; its check says which.
  Next: writing-plans over slices 32, 32.1, 34, 36, 36.1, 36.2, 36.3, 38, 40 and 42, one task per slice in that order, to `2026-09-27-shop-knowledge-batch6-implementation.md`.
- 2026-09-27 writing-plans done: `2026-09-27-shop-knowledge-batch6-implementation.md`, ten tasks for slices 32, 32.1, 34, 36, 36.1, 36.2, 36.3, 38, 40 and 42 in slice order. Written under adrs/0011: no code, nothing built or replayed. Each task says why its scenarios or check are red today, found by running them in this checkout (every red scenario stops at an undefined step) and by probing kb v0.2.0 in `.superpowers/batch6/`. Expected counts are taken from the tags (failed/passed): 27/35 before, then 23/39, 23/39, 20/42, 17/45, 17/45, 17/45, 17/45, 16/46, 14/48 and 12/50, the 12 left exactly those tagged 44 or later. Decisions in adrs/0022 to 0026. No request to bump the pin beyond kb slice 97's. No feature file touched. Its Review Focus holds five questions for the spec: a role's review showing the store's start, the narrowed links showing nothing narrowed away, `snapshot`'s two sources for the piece of work, a step added with a title already used, and `--json` on `read` alone. Next: slice 32.
- 2026-09-27 slice 32 green. Someone can now: follow the links out of a decision and see the older decision, follow them in and see both work items, narrow them to one link and one kind and see the same two and nothing else, and go two steps out to see the older decision and the tag, each with the route taken.
  Surprised by: nothing.
  Evidence (`shop-knol refs <decision> ...`, ids abbreviated by nothing; script `.superpowers/batch6/s32.py`):
  `--outbound`: `[{id: decision/prices-are-reviewed-monthly, type: decision, title: Prices are reviewed monthly, via: supersedes, tags: [tag/pricing], route: [{field: supersedes, id: decision/prices-are-reviewed-monthly}]}]`.
  `--inbound`: two entries, `work-item/move-the-review-to-mondays` then `work-item/tell-the-pricing-team`, each `via: decisions`, `decisions: [decision/price-reviews-happen-weekly]`, route one hop `{field: decisions, id: <itself>}`.
  `--inbound --via decisions --type work-item`: the same two entries, byte for byte.
  `--outbound --depth 2`: the older decision as above, then `{id: tag/pricing, type: tag, title: pricing, via: tags, route: [{field: supersedes, id: decision/prices-are-reviewed-monthly}, {field: tags, id: tag/pricing}]}`.
  Open questions: Review Focus 2, the narrowed links show nothing narrowed away. Reproduction: run `refs <decision> --inbound` and `refs <decision> --inbound --via decisions --type work-item` in the Background's shop; the two answers are identical, since the only things pointing at the decision are the two work items through `decisions`, so scenario 3 would pass with the narrowing flags ignored. Next: slice 32.1.
- 2026-09-27 slice 32.1 green.
  Check: diff of the FAILED lines against `failing-32.1.txt`: `same` (23); `make test`: `23 failed, 39 passed`; `grep -c "def shown" tests/*.py | grep -v ":0"`: `tests/conftest.py:1`; shape check `2 1 1 0`, no module over 250, no renderer listed, `cli.py` 230 lines, unchanged from slice 32.
  Surprised by: nothing.
  Next: slice 34.
- 2026-09-27 slice 34 green. Someone can now: search for a word and see each result with the section it matched and a snippet, the heaviest first, narrow the search to decisions and not see the process, or search the fields as well as the prose and also see the decision whose title carries the word.
  Surprised by: a decision must carry both its Purpose and its Rationale sections, so the Background's decisions each carry a Rationale that does not say the word.
  Evidence (`shop-knol search ...` in the Background's shop, script `.superpowers/batch6/s34.py`): `search restocking`: three entries, `decision/restocking-is-weekly` first (section Purpose, snippet "Restocking happens every week. Restocking on Mondays, restocking again..."), then `decision/shelves-are-counted-first`, then `process/close-up` (section Purpose). `--type decision`: the first two only. `--in all`: those three plus `decision/who-owns-restocking` with `field: title`, `snippet: Who owns restocking`; the first decision also appears a second time with `field: title`, since its own title says the word.
  Open questions: Review Focus 5, `--json` is on `read` alone: `shop-knol search restocking --json` is refused by argparse, usage and exit 2 (before Task 6 changes that to one line and exit 1). Whether a match inside a part should be found: the probe created a process whose only mention of "zebrafish" is a step's `does`; `search zebrafish` and `search zebrafish --in all` both show `[]` and exit 0, so the user cannot find a step by what it does. Scenario 3 sees the same title twice for a decision whose title and prose both say the word; the scenarios are silent on whether one artifact should be shown once.
  Next: slice 36.
- 2026-09-27 slice 36 green. Someone can now: review the shopkeeper's changes and see only the recording of the decision, a piece of work's changes and see only the agent's revision, or the changes since 2026-09-22 and see only today's revision.
  Surprised by: nothing.
  Evidence (`shop-knol journal ...` in the Background's shop): `--actor shopkeeper`: one change, `create` of `decision/price-reviews-happen-weekly` by `{role: shopkeeper, execution: ""}`, message "Record weekly reviews". `--execution reprice-dairy`: one change, `write` of the decision by `{role: agent, execution: reprice-dairy}`, dated today, "Accept weekly reviews". `--since 2026-09-22`: the same one change.
  Open questions: Review Focus 1, who started the store. The Background does not say; the step starts it as `founder` (adrs/0027). Reproduction: `mkdir shop; KB_ACTOR=shopkeeper shop-knol init shop; KB_ROOT=shop KB_ACTOR=shopkeeper shop-knol journal --actor shopkeeper | grep -c "op:"` gives `9`, nine `create` entries for the start and the types, so scenario 1's "only the recording of the decision" cannot hold if the shopkeeper started the store; the scenario's first run with `--actor` showed the same nine before the Background's change.
  Next: slice 36.1.
- 2026-09-27 slice 36.1 green. Every command's request to kb is built in `src/shop_knowledge/kb_requests.py` (76 lines; `init_request`, `create_request`, `write_request`, `read_request`, `validate_request`, `apply_request`, `journal_request`, `list_request`, `refs_request`, `search_request`, with `locator` and `is_whole` public); `cli.py` is 203 lines, down from 238, each handler calling its request function, making its call, refusing through `_answered` and showing. CLAUDE.md's module map has the row; adrs/0022 held as written. The over-long `_journal` line went with the move. adrs/0027 records the decision adrs/0025 lacked, that slice 36's Background starts the store as `founder`.
  Check: diff of the FAILED lines against `failing-36.1.txt`: `same` (17); `.venv/bin/python -m pytest -q`: `17 failed, 45 passed`; request grep on `cli.py`: `0`; `cli.py`: 203 lines; `grep -cE "print\(|connect|client" kb_requests.py`: `0`; `grep -c "kb_requests.py" CLAUDE.md`: `1`; shape check `2 1 1 0`, no module over 250, no renderer listed; help snapshot `36.1` against `36.1-before`: no diff.
  Surprised by: the module's first docstring said "connects", which the check's grep for `connect` counted; reworded.
  Next: slice 36.2.
- 2026-09-27 slice 36.2 green. An argument shop-knol cannot take is refused the one way every refusal is: `arguments.py` builds its parser from a subclass whose `error` raises `ArgumentRefused` (the `prog` and argparse's message), and `main` parses inside its handling, turns that into one `Fault` with the `prog` as artifact, and prints it through the same `_refuse` call as a `Refused`. CLAUDE.md's `arguments.py` row says it refuses by raising and never prints. The argparse question raised at slices 20.1, 22 and 30 is answered by rule 4 through this slice. Carry-over from slice 36.1's review done: `init_request` normalises the root again, `str(Path(args.root))`.
  The six lines, verbatim:
  - `shop-knol: the following arguments are required: command`
  - `shop-knol: argument command: invalid choice: 'nosuch' (choose from 'init', 'create', 'read', 'write', 'validate', 'apply', 'journal', 'list', 'refs', 'search', 'render')`
  - `shop-knol list: the following arguments are required: --type`
  - `shop-knol: unrecognized arguments: --json`
  - `shop-knol read: argument --resolve: invalid int value: 'two'`
  - `shop-knol create: the following arguments are required: --from`
  Check: diff of the FAILED lines against `failing-36.2.txt`: `same` (17); `.venv/bin/python -m pytest -q`: `17 failed, 45 passed`; each of `shop-knol`, `nosuch`, `list`, `list --type decision --json`, `read decision/x --resolve two`, `create decision`: exit 1, 1 stderr line, 0 bytes stdout, 0 `usage:` (e.g. `shop-knol list: the following arguments are required: --type`); help snapshot `36.2` against `36.2-before`: no diff, `-h` of every command exit 0; shape check `2 1 1 0`, no module over 250, no renderer listed, `cli.py` 209 lines.
  Surprised by: nothing.
  Next: slice 36.3.
- 2026-09-27 slice 36.3 green. No name says less or other than it does: `arguments.py` adds `validate`'s subparser without an assignment; `cli._show` is hinted `dict | list`; `cli._read`'s local is `answer`, no longer hiding the module `shape`; `driver.knol`'s parameter is `piped` (one caller, in `tests/test_record_a_decision.py`); `answers.py`'s docstring and CLAUDE.md's row say dicts and lists, and the row names all thirteen public functions (`glance`, `whole`, `section`, `change`, `history`, `created`, `written_over`, `applied`, `listed`, `names`, `reached`, `matched`, `written`).
  Check: diff of the FAILED lines against `failing-36.3.txt`: `same` (17); `.venv/bin/python -m pytest -q`: `17 failed, 45 passed`; the four greps: `0`, `0`, `0`, and the `inspect` assertion succeeds; help snapshot `36.3` against `36.3-before`: no diff; shape check `2 1 1 0`, no module over 250, no renderer listed, `cli.py` 209 lines.
  Surprised by: nothing.
  Next: slice 38.
- 2026-09-27 slice 38 green. Someone can now: record, for a piece of work, the decision and the process it read with `shop-knol snapshot --execution ID NAME... -m WHY`, and see in `journal` one entry naming each with the revision read.
  Evidence: `KB_ACTOR=agent shop-knol snapshot --execution restock-the-shelves decision/prices process/close-up -m ...` answers `entry: <name>`; `journal --execution restock-the-shelves` shows one change, `op: snapshot`, `read: [{artifact: decision/prices-are-reviewed-monthly, revision: 1}, {artifact: process/close-up, revision: 1}]`. Seen red first on the Background (no step), then on the missing command, then on the Then (`KeyError: 'read'`) once the command existed. Check: `-m slice-38` 1 passed; `.venv/bin/python -m pytest -q` 16 failed, 46 passed (the failing set is the earlier 17 less slice 38's); GREEN plus slices 32, 34, 36, 38: 46 passed; help snapshot 38 against 38-before: only `snapshot` added; shape check `2 1 1 0`, no module over 250, no renderer listed, `cli.py` 216 lines.
  Surprised by: nothing.
  Open questions: QUESTION FOR THE SPEC (Review Focus 3): `snapshot`'s `--execution` and `KB_ACTOR`'s execution can disagree. Reproduction, run after this task: `KB_ACTOR=agent:one shop-knol snapshot --execution two decision/prices -m read`, then `journal --execution one` answers `changes: []` and `journal --execution two` answers the one snapshot entry, actor `agent`, execution `two`, read `decision/prices` at revision 1. The entry is made under `two` (adrs/0025); a user would expect one source for the piece of work, or a refusal when they differ.
  Next: slice 40.
- 2026-09-27 slice 40 green. Someone can now: add a step to a process with `shop-knol append <process>#steps --from FILE -m WHY`, written in place or using a shared step with its own settings, and be told the name it is known by.
  Evidence (a Close up process of two steps, the shared step `step/check-the-stock` with `settings: [shelf]`): a step written in place answers `id: process/close-up#steps/tidy`, `revision: 2`; a step with `uses: step/check-the-stock` and `with: [{name: shelf, value: dairy}]` answers `id: process/close-up#steps/check-the-dairy`, `revision: 3`. The process whole after both: steps `lock`, `lights`, `tidy` (`does: Tidy up.`), `check-the-dairy` (`uses: step/check-the-stock`, `with: [{name: shelf, value: dairy}]`), revision 3. An append naming no collection is refused, `process/close-up: an item is added to a collection, and '' in 'process/close-up' is not one`, exit 1; with no `-m`, `every change must carry a message, given with -m`, exit 1. Seen red first on the Background (no step), then on the missing command (`invalid choice: 'append'`); scenario 2 red on its undefined When.
  Check: `-m slice-40` 2 passed; `.venv/bin/python -m pytest -q` 14 failed, 48 passed (the FAILED set is the earlier 16 less slice 40's two); GREEN plus slices 32 to 40: 48 passed; shape check `2 1 1 0`, no module over 250, no renderer listed, `cli.py` 224 lines; help snapshot 40 against 40-before: only `append` added.
  Surprised by: nothing.
  Open questions: QUESTION FOR THE SPEC (Review Focus 4): a step added with a title already used. Reproduction, run after this task: append `{title: Tidy, does: Tidy up.}` twice to `process/close-up#steps`; the first answers `process/close-up#steps/tidy`, the second `process/close-up#steps/tidy-2` (revision 4), and the whole read holds both, titled "Tidy", ids `tidy` and `tidy-2`. kb gives the second a name of its own, as slice 28 shows for a decision, so the expectation holds; what the spec says of it is still unwritten.
  Next: slice 42.
- 2026-09-27 slice 42 green. Someone can now: retire an artifact with `shop-knol delete <name> -m WHY`, and be refused, told what still points at it, when something does.
  Evidence (a store with `tag/seasonal`, `tag/pricing` and a decision `decision/d` tagged `tag/pricing`, `KB_ACTOR=shopkeeper`): `delete tag/seasonal -m gone` answers `id: tag/seasonal`, `revision: 2`, exit 0, and `read tag/seasonal` is then refused. `delete tag/pricing -m gone` prints nothing on stdout, exit 1, and on stderr `decision/d at tags/0: 'tag/pricing' cannot be removed while 'decision/d' points at it at 'tags/0'`. `delete tag/pricing` with no `-m` prints `every change must carry a message, given with -m`, exit 1.
  Check: `-m slice-42` 2 passed; `.venv/bin/python -m pytest -q` 12 failed, 50 passed (all 12 tagged 44 or later); GREEN plus slices 32 to 42: 50 passed; shape check `2 1 1 0`, no module over 250, no renderer listed, `cli.py` 232 lines; the arguments snapshot differs from before only by `delete` in the command list and its help line.
  Surprised by: nothing.
  Open questions: QUESTION FOR THE SPEC: several things pointing at one artifact. The scenario has one decision pointing at the tag, so "one line for each thing that points at it" is not observed with two. Reproduction: tag two decisions with `tag/pricing`, run `shop-knol delete tag/pricing -m x`, and count the stderr lines. QUESTION FOR THE SPEC: retiring a place inside an artifact. `delete process/close-up#steps/tidy -m x` hands the place to kb as the locator's path; no scenario says whether that is retiring a step or a refusal. QUESTION FOR THE SPEC: retiring a name the store lacks. `delete tag/nothing -m x`: no scenario in this feature says what the user sees; kb's refusal is passed through.
  Next: slice 42.1, the fourth architecture review, which runs before the next plan (adrs/0011).
- 2026-09-27 slice 42.1 inputs, for the fourth architecture review, from the final review of slices 32 to 42:
  - Flag defaults are handled two ways: `""` on `journal`, `None` patched with `or ""` in `kb_requests` for `refs` and `search`.
  - Command order differs between the help (`arguments.py`) and `_HANDLERS` (`cli.py`).
  - Snapshot entries in `journal` show `artifact: ''` and `revision: 0` (a question for the spec).
  - `answers.written_over` and `answers.deleted` have identical bodies.
  - `init` normalises the root with `Path` twice, in `cli._init` and `kb_requests.init_request`.
  - `refs --depth -1` silently answers `[]`.
- 2026-09-27 Suite: 50 passed, 12 failed (`.venv/bin/python -m pytest -q`; the 12 are exactly the scenarios tagged 44, 47, 48, 49 and 50, each stopping at an undefined step).
- 2026-09-27 Fourth architecture review of shop-knowledge (slice 42.1), on Opus 5.5 against `CLAUDE.md`, over the code under `src/` and the step definitions after slices 32, 32.1, 34, 36, 36.1, 36.2, 36.3, 38, 40 and 42. It took first what batch 6's final review left for it, and `cli.py`'s room.
  Kept: rule 1 (`src/` imports from kb only `kb.client`, `kb.contract`, `kb.content`, and `kb.canonical` in `cli._document`; `jsonschema` only in `shape.py`); rule 2; rule 3 (no other YAML library; JSON only through `json` in `cli._show`); rule 4 for everything shop-knol does itself. A hunt over every command with odd input (a missing name, an empty name, a place in a name, `--depth -1`, `--since garbage`, an empty or `/dev/null` file, a kind the store lacks, `--where` with no `=`, no store, `KB_ROOT` naming nothing) found one traceback, the empty batch, which is kb's. Rule 5 (only the skill and diagram renderers know a process's fields; `bootstrap` knows the types' names alone). Rule 6 (no renderer prints, opens or writes; `cli._write` alone writes). No module is over 250 lines. A user's file or the pipe is read only in `cli._document`. Every kb answer but Validate's and Init's, and bootstrap's Creates, is refused through `cli._answered`. Every refusal is printed by `main` alone. Every module has a row in the module map, and every public function of `answers.py` is named in its row. Every When that runs shop-knol gives `result`. No step text or shared fixture is defined twice. The one in-process kb call in the steps and every hand edit say why.
  Room in `cli.py`: 232 lines. Estimated by reading the handlers each slice left touches: 42.2 turns `_validate`'s own refusal into `_answered`, about -1; 44 adds the check's answer to `_validate`, about +1; 47 refuses Init's and bootstrap's answers in `_init`, about +2 to +3; 48 and 49 touch no code; 50 adds a renderer under `renderers/` and nothing to `cli.py`. So `cli.py` ends near 235, under the limit with room. No split is called for. Slices 44 and 47 each stop and hand back if the estimate is wrong for them, as slice 28 did.
  Batch 6's inputs, each settled:
  - Flag defaults handled two ways (`""` declared for `journal`, `None` patched with `or ""` in the requests for `refs` and `search`, `refs --depth` patched from `None` to 1). With `init`'s root normalised with `Path` in both `cli._init` and `init_request`, this is one fault: what an argument means is said in two places, against the map's row giving `arguments.py` every command's arguments and the requests module only their turning into requests. Refactor: slice 50.1 (adrs/0032).
  - Command order differs between the help and `_HANDLERS`. No rule breaks, but a reader matching a handler to its command reads two orders. The help is what users see and keeps its order. `_HANDLERS` takes it, in slice 50.1.
  - Snapshot entries in `journal` show `artifact: ''` and `revision: 0`. That is what the user is shown, a scenario's to say and no rule's: QUESTION FOR THE SPEC. Reproduction: `KB_ACTOR=agent shop-knol snapshot --execution w decision/x -m read; shop-knol journal --execution w`. The one entry shows `artifact: ''`, `revision: 0` and `read: [...]`. A user would expect the empty fields left out.
  - `answers.written_over` and `answers.deleted` have identical bodies. Not called for: the map gives each answer a public function of its own, and the two answer different commands whose answers may part.
  - `refs --depth -1` silently answers `[]`. Behaviour no scenario pins and no rule settles: QUESTION FOR THE SPEC. Reproduction: `shop-knol refs <a decision with links> --outbound --depth -1` gives `[]`, exit 0. A user would expect a refusal naming the depth.
  Found here:
  - `kb_requests.py`'s docstring and its CLAUDE.md row say `locator` and `is_whole` are there for `cli._read`. `cli` calls `is_whole` alone (`grep -n "kb_requests\.\(locator\|is_whole\)" src -r`: one line, `is_whole`). `locator` is used only inside the module. A name says other than the code does, the standard slice 36.3 held. Refactor: slice 50.1 makes it the module's own and the row names `is_whole` alone.
  - Reading an artifact whole through shop-knol is written word for word as `_whole` in `test_revise_what_the_shop_knows.py` and `test_add_a_step_to_a_process.py`. Slice 49 would add a third, for a role, a decision and a tag. The driver already holds the shared ways of driving shop-knol (`knol`, `start`, `record`). Refactor: slice 48.1 puts the whole read there. Placed before 49, which needs it, and after 48, since placing it first would put it ahead of slices that do not.
  - Validate's answer refused outside `_answered` stays with slice 42.2, and Init's and bootstrap's dropped answers with slice 47, as the second and third reviews placed them.
  Not called for: `source.whole`'s `depth`, which no renderer passes yet. The spec says a renderer reads "the resolved whole artifact", so it is the door to that and says no more than it does. Nor the `"-"` `_by` takes as init's message. It is how "init gives no why" is said, and slice 47's "asks for no reason" is its scenario.
  Questions the batches logged that a rule settles, not a scenario:
  - `init` of a directory that does not exist exits 0 having started nothing (slice 1.29's review, owned by 47). Settled by "a kb answer's faults are refused in one way": kb answers Init with `a store is started in a directory that exists; 'nope' does not`, which shop-knol drops today. Slice 47's refusal of Init's answer shows it, with exit 1, and no scenario is added (adrs/0030).
  - The empty batch's traceback (slice 28's Review Focus 1), rule 4. Waiting on kb, not a slice here: kb fixed it in kb's main as kb slice 97. This is a request to bump the pin to the kb tag that releases it. Until then rule 4 is broken there by kb v0.2.0, and nothing is coded here. Still reproduced today: `printf 'changes: []\n' > b.yaml; shop-knol apply --from b.yaml -m x` ends in `subprocess.CalledProcessError` from kb's git commit, exit 1.
  Every other open question needs a scenario to say what is shown, and no rule does. Each stays a QUESTION FOR THE SPEC where it was logged: `--json` on `read` alone; `list --ids` as YAML; "superseded" as a status and not the link; `--section` with `--whole`; "no store" against "no knowledge base"; a non-process as a skill or a diagram; a branch to no step, `go_to` unchecked; a `"` in a diagram's label; the 500 lines "for optimal performance"; `<name>.mmd` against `<id>.mmd`; the skill's name and description limits; the markdown page's parts as tables; search inside parts and one artifact shown twice; `snapshot`'s two sources for the piece of work; a step added with a title already used; several things pointing at a retired artifact, retiring a place, retiring a name the store lacks.
  Placed, by risk among the slices not yet begun and never ahead of all of them: 48.1 after 48 and before 49, which needs it; 50.1 last, since no slice needs it and it touches `arguments.py`, `kb_requests.py` and `cli._init` after slice 47 has changed `_init` for the last time. No scenario is added or moved, so no feature file and no `@slice` tag changes. Eight slices follow this review (42.2, 44, 47, 48, 48.1, 49, 50 and 50.1), past the six adrs/0010 counts. So slice 50.2, the fifth review, is cut at the plan's end. Under adrs/0011 a review runs before planning and never as a task inside a plan, so it is not a task of batch 7. It runs after batch 7's final review. Batch 7 is the last batch of capability slices; a refactor the fifth review calls for is cut then as an enabling slice of its own.
  Next: writing-plans over slices 42.2, 44, 47, 48, 48.1, 49, 50 and 50.1, one task per slice in that order, to `2026-09-27-shop-knowledge-batch7-implementation.md`, the last batch in the plan.
- 2026-09-27 writing-plans done: `2026-09-27-shop-knowledge-batch7-implementation.md`, eight tasks for slices 42.2, 44, 47, 48, 48.1, 49, 50 and 50.1 in slice order, the last batch of the plan. Written under adrs/0011: no code, nothing built or replayed. Each task says why its scenarios or check are red today, found by running them in this checkout (every red scenario stops at an undefined step) and by probing kb v0.2.0 and shop-knol in `.superpowers/batch7/`. The probes found that 48 and 49, and scenarios 1 to 3 of 47 and 2 of 44, already hold in code once their steps exist. Expected counts are taken from the tags (failed/passed): 12/50 before, then 12/50, 9/53, 4/58, 3/59, 3/59, 1/61, 0/62 and 0/62. Decisions in adrs/0029 to 0032. No request to bump the pin beyond kb slice 97's. No feature file touched. Its Review Focus holds five questions for the spec: a batch's fault naming a change by an artifact that does not exist, stale artifacts unseen beside faults, a non-role published as an agent, the agent's `tools` as a list, and a reason given to `init`. Next: slice 42.2.
- 2026-09-27 slice 42.2 green. Someone can now: extend the check's answer through the one refusal of kb answers, `cli._answered`, which takes Validate's violations as further faults.
  Check: failing ids identical to before (same, 12); `make test` 12 failed, 50 passed; `-m slice-1.28` 1 passed; the `inspect` assertion succeeds; `grep -n Validate CLAUDE.md` finds no line; shape check `2 7 1 0`, nothing listed, `cli.py` 232; arguments snapshot TAG=42.2 no diff.
  Surprised by: `cli.py` stays 232, not 231; the docstring of `_answered` grew as `_validate` shrank.
  Open questions: none. Next: slice 44.
- 2026-09-27 slice 44 green. Someone can now: check the shop's knowledge and be told it is sound, see every fault with its artifact and place while the command exits non-zero, or see what is behind its type without calling the shop unsound.
  Evidence: sound check, stdout `sound: true` / `behind: []`, stderr empty, exit 0. Behind its type (decision type written at version 2), stdout `sound: true` / `behind:` / `  - artifact: decision/old-one` / `    schema_version: 1` / `    current: 2`, stderr empty, exit 0. Two faults, stdout empty, exit 1, stderr `decision/price-reviews-happen-weekly at sections: the sections the type requires must all be present, in order; 'Rationale' is missing` and `work-item/reprice-the-dairy-shelf at decisions/0: a link must land on a node of a kind the type allows; 'decision/nothing' does not`. Checks: `-m slice-44` 3 passed; `make test` 9 failed, 53 passed; GREEN plus slice-44 53 passed; shape check `2 7 1 0`, nothing listed, `cli.py` 232; arguments snapshot TAG=44 no diff.
  Surprised by: scenario 2 passed once its steps existed, as the brief said; seen red first on a wrong Then (`== ["wrong"]`), then made right. Scenario 3 was green as soon as its steps existed, since `checked` written for scenario 1 already carries `behind`; seen red by emptying `behind` for one run, then restored.
  Open questions: QUESTION FOR THE SPEC: what is behind its type is not shown when the check also finds faults, since a refusal prints nothing on stdout (adrs/0029). Reproduction: write `schema/decision` at version 2 through `shop-knol write`, hand-break another decision, run `shop-knol validate`: stdout empty, exit 1, stderr one line for the broken decision, nothing about the decision behind its type (probed here with one decision both behind and broken). A user would expect to be told both. Next: slice 47.
- 2026-09-27 slice 47 green. Someone can now: start a shop knowledge base beside the shop's other work, with no reason given and none asked for, and be refused in kb's words when the directory already holds one or sits inside one.
  Evidence: `init` of a started directory: stderr `a store is never started over another; 'shop' already has a store inside it`, exit 1. `init shop/kb/schema`: stderr `stores do not nest; 'shop/kb/schema' is inside the store at '/home/vscode/shopsystem-knowledge/.superpowers/batch7/ev/shop'`, exit 1. `KB_ACTOR=a shop-knol init nope` (no such directory): `a store is started in a directory that exists; 'nope' does not`, exit 1 (was exit 0, nothing started). Checks: `-m slice-47` 5 passed; `-m slice-4` 1 passed; `make test` 4 failed, 58 passed; GREEN plus slice-44 and slice-47 58 passed; shape check `2 7 1 0`, nothing listed, `cli.py` 233; arguments snapshot TAG=47 no diff.
  Surprised by: scenarios 1, 2 and 3 passed once their steps existed, as the brief said; each seen red first on a wrong Then (`len(changes) == 0`, `stderr == "nothing"` and `exists()`, entries without `kb`), then made right. Scenarios 4 and 5 went red on code, `assert 0 == 1` at "rejected because". `cli.py` is 233, not 234 to 235.
  Open questions: QUESTION FOR THE SPEC: a reason given to `init` is refused. Reproduction: `KB_ACTOR=a shop-knol init shop -m why` gives `shop-knol: unrecognized arguments: -m why`, exit 1. A user who gives one out of habit might expect it taken, or told plainly that starting writes its own. Also: a Create refused mid-load leaves a store holding only some of the types, which no scenario reaches. Next: slice 48.
- 2026-09-27 slice 48 green. Someone can now: apply a batch whose second change does not fit its type, be told every fault at once, and find none of the batch in the shop.
  Evidence: stderr `work-item/reprice-the-dairy-shelf at owner: 3 is not of type 'string'` and `work-item/reprice-the-dairy-shelf at status: 3 is not of type 'string'`, stdout empty, exit 1. After it `shop-knol read decision/price-reviews-happen-weekly`: `decision/price-reviews-happen-weekly: the store holds nothing by the name 'decision/price-reviews-happen-weekly'`, exit 1; `read work-item/reprice-the-dairy-shelf`: `revision: 1`, `title: Reprice the dairy shelf`, `references: []`, no `owner`, no `status`. Checks: `-m slice-48` 1 passed; `make test` 3 failed, 59 passed; GREEN plus slices 44, 47 and 48 59 passed; shape check `2 7 1 0`, nothing listed, `cli.py` 233; arguments snapshot TAG=48 no diff.
  Surprised by: the scenario passed once its steps existed, as the brief said; seen red first on a wrong Then (`returncode == 0`), then made right. Nothing under `src/` changed.
  Open questions: QUESTION FOR THE SPEC: a fault in a batch names a change by an artifact that does not exist. Reproduction: apply a batch whose one change creates a decision titled "Bad one" with `owner: 3`; stderr says `decision/bad-one at owner: 3 is not of type 'string'` (and two lines for the missing sections), exit 1, and `read decision/bad-one` finds nothing. A user fixing the batch in one pass would expect the fault to say which change it is. Next: slice 48.1.
- 2026-09-27 slice 48.1 green. Someone can now: read an artifact whole in a step through one `whole` in `tests/driver.py`, beside `record`.
  Check: baseline `failing-48.1.txt` 3 lines, `grep -c "def _whole" tests/*.py | grep -v ":0"` two lines and `grep -c "^def whole" tests/driver.py` `0` before. After: failing ids diff `same`; `make test` 3 failed, 59 passed; `-m "slice-24 or slice-40"` 4 passed; first grep no line, second `1`; shape check `2 7 1 0`, nothing listed, `cli.py` 233 (unchanged); nothing under `src/` or `features/` changed.
  Surprised by: nothing; `loads` became unused in both modules and its import went.
  Next: slice 49.
- 2026-09-27 slice 49 green. Someone can now: record a role and see its harness fields as one named group and its shop identity as another, and tag a decision with a tag so the decision names it while the tag's description is held once, on the tag.
  Evidence: `read role/stock-keeper --whole`: `harness:` holds `name: stock-keeper`, `description: Keeps the shelves stocked.`, `tools: [Read]`, and `shop:` holds `responsible_for: What is on the shelves`, `answers_to: role/shopkeeper`, none of those keys at the top level. `read decision/price-reviews-happen-weekly --whole`: `tags: [tag/pricing]`, no description. `read tag/pricing --whole`: `title: Pricing`, `description: How the shop sets its prices.` Checks: baseline `failing-49.txt` 3 lines; `-m slice-49` 2 failed on their Givens before, 2 passed after; `make test` 1 failed, 61 passed (slice 50's); GREEN plus slices 44, 47, 48 and 49 61 passed; shape check `2 7 1 0`, nothing listed, `cli.py` 233; arguments snapshot TAG=49 no diff. Nothing under `src/` or `features/` changed.
  Surprised by: both scenarios passed once their steps existed, as the brief said; each seen red first on a wrong Then (`shown[group] == {}`, `tags == []`), then made right.
  Open questions: QUESTION FOR THE SPEC: the scenarios are silent on tagging with a tag that does not exist. Reproduction: create a decision with `tags: [tag/nothing]`; stderr says `decision/price-reviews-happen-daily at tags/0: a link must land on a node of a kind the type allows; 'tag/nothing' does not`, exit 1. Nothing is coded for it. Next: slice 50.
- 2026-09-27 slice 50 green. Someone can now: publish a role as an agent into a directory and find `.claude/agents/stock-keeper.md` whose heading block is the role's harness fields and whose body is its prose.
  Evidence: `shop-knol render agent role/stock-keeper --to out`, exit 0, writes `.claude/agents/stock-keeper.md`: `---`, `name: stock-keeper`, `description: Keeps the shelves stocked.`, `tools:`, `  - Read`, `---`, blank, `# How it works`, blank, `Counts, then orders.`. Checks: baseline `failing-50.txt` 1 line; `-m slice-50` 1 failed on its When before, then on `invalid choice: 'agent' (choose from 'diagram', 'markdown', 'skill')`, then 1 passed; `-m "slice-17 or slice-18 or slice-19 or slice-20"` 4 passed (after the section layout moved to `renderers/sections.py`); `make test` 62 passed, make ends cleanly; GREEN plus slices 44, 47, 48, 49 and 50 62 passed; shape check `2 7 1 0`, nothing listed, `cli.py` 233 (unchanged); arguments snapshot TAG=50 differs from help-now only by `agent` in render's usage and choices.
  Surprised by: nothing; the shared layout needed the module adrs/0033 names.
  Open questions: QUESTION FOR THE SPEC (Review Focus 3): a non-role published as an agent. Reproduction: `shop-knol render agent tag/pricing --to o` exits 0 and writes `.claude/agents/pricing.md` holding `---`, `{}`, `---`; a user would expect a refusal naming the type. QUESTION FOR THE SPEC (Review Focus 4): the agent's `tools` is written as a YAML list (`tools:` then `  - Read`); whether the harness takes a list or wants a comma-separated string is not observed by the suite, and no harness limit on an agent is checked. Reproduction: publish the Background's role and read the heading block. Next: slice 50.1.
- 2026-09-27 slice 50.1 green. Someone can now: find each argument's type and default where it is declared, the handler table in the help's order, and in the request module only the helper the command line uses.
  Check: baseline `failing-50.1.txt` 0 lines, greps `4` and `1`, order assertion `AssertionError`, `def locator` 1, all before; after, `make test` 62 passed; `grep -cE 'or ""|is None|Path\(' kb_requests.py` 0; `grep -c "Path(args.root)" cli.py` 0; order assertion succeeds; `grep -c "def locator"` 0 (now `_locator`); docstring and CLAUDE.md row name `is_whole` alone; arguments snapshot TAG=50.1 no diff against 50.1-before; shape check `2 7 1 0`, nothing listed, `cli.py` 233.
  Surprised by: nothing; adrs/0032 already held the decisions.
  Open questions: none. Next: slice 50.2, the fifth architecture review, which runs after this batch's final review and before any further plan (adrs/0011).
- 2026-09-27 slice 50.2 inputs, for the fifth architecture review, from batch 7's final review (its fixes are commit fb9e5cb):
  - Three test modules are at or over 250 lines (`test_read_back_what_the_shop_knows.py` 276, `test_record_a_decision.py` 251, `test_start_a_shop_knowledge_base.py` 251), and CLAUDE.md is silent on whether its size limit covers `tests/`.
  - The agent renderer checks no harness limit, where the spec says `skill` and `agent` both validate their output against the limits the harness publishes. That needs a scenario, so it is a question for the spec unless a rule settles it.
  - Six minors, fixed in fb9e5cb: render's `--to` typed as a path where it is declared, not wrapped in `cli._render`; `_validate`'s docstring naming `answers.checked`; the check's step reading `schema/decision` whole through `driver.whole`; the agent's Then asserting each section heading stands on a line of its own; a parameter in `test_revise_what_the_shop_knows.py` named `whole`, shadowing the driver's, renamed; the start feature's Whens sharing one `_init` in place of one When calling another.
- 2026-09-27 Suite: 62 passed, 0 failed (`make test`, 62 passed, make ends cleanly).
- 2026-09-27 Fifth architecture review of shop-knowledge (slice 50.2), on Opus 5.5 against `CLAUDE.md`, over the code under `src/` and the step definitions after slices 42.2, 44, 47, 48, 48.1, 49, 50 and 50.1 and the final review's fixes. It took first what batch 7 left for it.
  CLAUDE.md's rules the code meets in full:
  - Rule 1. `src/` imports from kb only `kb.client`, `kb.contract`, `kb.content`, and `kb.canonical` in `cli._document` for `NotCanonical`. `jsonschema` is imported only in `shape.py`. Nothing under `src/` opens a file inside a store or runs git.
  - Rule 2. kb is installed from v0.2.0 and nothing of it is edited here.
  - Rule 3. No other YAML library is imported. JSON is written only through `json`, in `cli._show`.
  - Rule 5. Only the renderers for a type know its fields: skill and diagram a process's, agent a role's `harness` and `sections`. `bootstrap` knows the types' names alone. The markdown renderer tells only `sections` apart (adrs/0015).
  - Rule 6. No renderer prints, opens or writes. `cli._write` alone writes, after `_answered` has passed the `Rendered`.
  - The module map. Every module has a row. `agent.py` and `sections.py` came in with slice 50 (adrs/0031, 0033). `answers.py`'s row names every public function it holds. `kb_requests.py`'s row names `is_whole` alone, the one helper `cli` calls.
  - Reading and refusing in one place. A user's file, or the pipe, is read only in `cli._document`. Every kb answer is refused through `cli._answered`, including Validate's with its violations (42.2), Init's and each bootstrap Create's (47), and a renderer's `Rendered`. `main` alone prints a refusal.
  - Under `src/`, no module is over 250 lines. `cli.py` is the largest at 233.
  - Most of the step rules. Every step drives shop-knol through `tests/driver.py`. The one in-process kb call (`test_make_several_changes_at_once.py`, the batch's history) and every hand edit or direct read of a store says why, or is what its Given says. No step text is defined twice. `tests/clock/` reaches shop-knol only through `driver.at`.
  Not met in full:
  - Rule 4. The empty batch's traceback is kb's (below). Everything shop-knol does itself meets it. A hunt over the commands the batch added or changed with odd input found no other traceback: `validate` with KB_ROOT naming nothing, `render agent` of a missing role, `--to` naming a file, `init ""`. The last is a question below.
  - Size and shape, read with adrs/0034. Three test modules are over 250 lines.
  - "A When that runs shop-knol gives what it ran as the fixture `result`". Two Whens slice 49 added in `test_start_a_shop_knowledge_base.py`, "the user records a role, saying who they are and why" and "the user tags a decision with "pricing", saying who they are and why", run shop-knol through `record` and give the id as `role` and `decision`. That is 40 of 42 Whens giving `result` (`grep -h -A3 "^@when" tests/*.py | grep -o 'target_fixture="[a-z_]*"' | sort | uniq -c`). Refactor: slice 50.3.
  Batch 7's inputs, each settled:
  - The test modules over 250 lines. CLAUDE.md's rules govern "anything under `src/` or `tests/`", so its limit holds for step definitions too (adrs/0034). Squeezing lines to fit is not a split (slice 28's hand-back). `test_record_a_decision.py` comes under the limit through slice 50.3's own work, and the other two need a split. A spike here (a throwaway feature under `.superpowers/`, since deleted) found that under pytest-bdd 8.1 steps defined in a sibling module reach a feature's test module by a star import, and are not found through a plain import. So one concern of each feature's steps moves to a module beside it (adrs/0035): where the knowledge base is found, for reading back, and roles and tags, for the start. Refactor: slice 50.4, after 50.3, which changes the lines it measures.
  - The agent renderer checks no harness limit. No rule settles it. `renderers/limits.py`'s row says what that module holds, not which renderers must check. Adding a check adds behaviour no scenario asks for, and which limits the harness publishes for an agent's file is for the spec to name. QUESTION FOR THE SPEC. Reproduction: record a role with `harness.name: Stock Keeper!`, a 1500-character `description` and a 700-line section, then `shop-knol render agent role/stock-keeper --to out`. It exits 0 and writes `.claude/agents/stock-keeper.md`, 707 lines, headed `name: Stock Keeper!`. The spec says `agent` fails rather than emit something the harness would reject.
  - The six minors fixed in fb9e5cb. Each holds today. Two of them are the standards slice 50.1 (a type declared where the argument is) and slice 48.1 (a whole read through the driver) set, and reviewing the second found two whole reads it left. `test_record_a_decision.py`'s "the decision recorded earlier still reads back by the name it had" and "the shop holds the decision just as if it had come from a file" each read whole by hand (`grep -n '"--whole"' tests/*.py`). Slice 48.1's check counted only functions named `_whole`, so these slipped by. Refactor: slice 50.3.
  Found here:
  - `test_read_back_what_the_shop_knows.py`'s Given "the older decision is tagged "seasonal"" says it uses `apply` "since `write` does not exist yet". `write` exists (slice 36), so the comment says other than the code does, the standard slice 36.3 held. The step still drives shop-knol as a user does, and a batch is a fair way to create a tag and write the decision as one change. Only the stale clause goes. Refactor: slice 50.3.
  - QUESTION FOR THE SPEC: `init` given an empty root starts a store in the working directory. Reproduction: from an empty directory, `KB_ACTOR=a shop-knol init ""` exits 0, and the working directory now holds `kb/`. argparse types `""` as the path `.`, as it did before slice 50.1 through `Path` in the handler. A user who gives an empty root might expect a refusal naming it.
  Not called for: the example artifacts the steps record (the weekly decision, the stock keeper) repeated across modules, with small differences in wording. No rule is broken, and the scenarios that assert on the wording differ. `_validate`'s and `kb_requests.py`'s docstrings run past 120 columns, which no rule sets. `source.whole`'s unused `depth` stays as the fourth review left it.
  Still waiting on kb: the empty batch's traceback (slice 28's Review Focus 1), rule 4. This is a request to bump the pin to the kb tag that releases kb slice 97. Nothing is coded here. Reproduced today: `printf 'changes: []\n' > b.yaml; shop-knol apply --from b.yaml -m x` ends in `subprocess.CalledProcessError` from kb's git commit, exit 1.
  Every other open question stays a QUESTION FOR THE SPEC where it was logged, batch 7's included: stale artifacts unseen beside faults; a batch's fault naming a change by an artifact that does not exist; a reason given to `init`; tagging with a tag that does not exist; a non-role published as an agent; the agent's `tools` as a list.
  Placed after 50.2, in the order they run: 50.3, then 50.4. Neither adds or moves a scenario, so no feature file and no `@slice` tag changes, and nothing under `src/` changes. Decisions in adrs/0034 and 0035.
  Next: writing-plans over slices 50.3 and 50.4, one task per slice in that order, to `2026-09-27-shop-knowledge-batch8-implementation.md`.
- 2026-09-27 writing-plans done: `2026-09-27-shop-knowledge-batch8-implementation.md`, two tasks for slices 50.3 and 50.4 in slice order. Written under adrs/0011: no code, nothing built or replayed. Each task says why its check fails today, from this checkout (the greps and the size check run 2026-09-27). The one unknown, how a feature's steps reach its test module from a sibling module, was settled by a throwaway spike: by star import, not by a plain import. Expected counts: 0 failed, 62 passed before and after each task; the touched modules collect 12, 8 and 10, and `-m slice-49` selects 2. Decisions in adrs/0034 and 0035. No request to bump the pin beyond kb slice 97's. No feature file touched. Its Review Focus holds three failure modes of the split, and two questions for the spec from this review: the agent renderer checking no harness limit, and `init ""`. Next: slice 50.3.
- 2026-09-27 slice 50.3 green.
  Check: `pytest -q` gives `62 passed`; `-m slice-49` gives `2 passed, 60 deselected`; `test_record_a_decision.py` gives `10 passed`; `test_read_back_what_the_shop_knows.py` gives `12 passed`; the Whens grep gives `42 target_fixture="result"`; `"--whole"` gives `tests/driver.py:35` and `tests/test_read_back_what_the_shop_knows.py:90`; "does not exist yet" gives no line; `git diff --stat -- src features` is empty. Lines after: `test_record_a_decision.py` 246, `test_start_a_shop_knowledge_base.py` 255, `test_read_back_what_the_shop_knows.py` 276 (the last two are slice 50.4's).
  Surprised by: nothing, except that the start module grew from 251 to 255 lines, since the two Whens now write and run `create` themselves.
  Seen red: each changed Then was seen red once by breaking its assertion for one run, then restored: `_kept_as_one_group` failed on `read[group] == {}`; `_decision_names_tag` on `tags == []`; `_description_held_once` on `description == "x"`; `_earlier_still_reads_back` on `"Nope." in bodies`; `_holds_the_piped_decision` on `revision == 2`.
  Next: slice 50.4.
- 2026-09-27 slice 50.4 green.
  Check: `pytest -q` gives `62 passed`; `--collect-only -q | grep -c ::` gives `62`; the size check lists nothing; `grep -l "import \*" tests/*.py` lists `tests/test_read_back_what_the_shop_knows.py` and `tests/test_start_a_shop_knowledge_base.py`; the two siblings are `tests/read_back_from_elsewhere.py` and `tests/start_roles_and_tags.py`, neither named `test_*`, and their constants (`THE_HARNESS_FIELDS`, `THE_SHOP_IDENTITY`, `TAG_DESCRIPTION`) are assigned in no test module; `grep -n "250" CLAUDE.md` shows the rule naming `src/` and `tests/`, and Step definitions says where a feature's steps go; `git diff --stat -- src features` is empty; `make test` ends with `62 passed`. Before: read-back 276 and start 255. Lines after: `test_read_back_what_the_shop_knows.py` 194, `read_back_from_elsewhere.py` 88, `test_start_a_shop_knowledge_base.py` 182, `start_roles_and_tags.py` 80. With the two star imports commented out, read-back gave 5 failed and start 2 failed, 7 `StepDefinitionNotFound` in all.
  Surprised by: the sibling of the tag scenario needs `record` from the driver as well as `knol`, `start` and `whole`, and the start test module no longer uses `dumps` or `whole`, so those two imports went.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 4): the agent renderer checks no harness limit. Reproduced after this task: a role with `harness.name: Stock Keeper!`, a 1500-character `description` and a 700-line section, then `shop-knol render agent role/stock-keeper --to out` exits 0 and writes `.claude/agents/stock-keeper.md`, 709 lines here, headed `name: Stock Keeper!`. The spec says `agent` fails rather than emit something the harness would reject.
  - QUESTION FOR THE SPEC (Review Focus 5): `init ""` starts a store in the working directory. Reproduced after this task: from an empty directory, `KB_ACTOR=a shop-knol init ""` exits 0 and the directory then holds `kb/`. A user might expect a refusal naming the empty root.
  Next: none. Every slice in the plan is green. What remains is the QUESTION FOR THE SPEC lines in the log, for formulating-features and the human, and the kb pin bump for the empty batch's traceback.
- 2026-09-27 kb v0.2.1 pinned (commit below). The empty batch is now refused in one line, `a set must hold at least one change`, exit 1: rule 4 holds everywhere. The question logged at slice 28 is closed.
- 2026-09-27 Suite: 56 passed, 10 failed. The ten are the scenarios commit 1133296 added or rewrote, each red on a missing step definition (`StepDefinitionNotFoundError`): the six start scenarios on "Given the user is working in ...", the named-place scenario, both rows of the markdown outline, and the agent past the limits. Settled by the spec and adrs/0037, 0038 and 0039, so they are sliced without approval.
  Probed in a throwaway store under `.superpowers/` (since deleted): `shop-knol init` with no directory is refused by argparse, `the following arguments are required: root`; `init .` starts one, and from inside it is refused `stores do not nest; '.' is inside ...`, naming `.`. `render markdown` of the Background's process prints its steps as one field of Python dict reprs; of a role with two tags prints `- **tags**: tag/stock, tag/dairy`. `render agent` of a role with `harness.name: shop:steward` exits 0 and writes the file.
  Spike: the harness's subagent documentation (code.claude.com/docs/en/sub-agents, read today) publishes that an agent's `name` may not contain `:` or start with `-`, and no length limit on the name, the description or the body. This answers which limits the agent is held to, the QUESTION FOR THE SPEC logged at slice 50.2; the 1500-character description and `Stock Keeper!` in that reproduction break no published limit.
  Cut, in order: 50.5, enabling, splits the publish feature's markdown steps into a sibling module first, since 50.6 and 50.7 together take that test module past 250 lines (CLAUDE.md, split first; adrs/0035). 50.6, markdown, the largest unknown: every value of the content model laid out without a schema. 50.7, the agent's limits, its unknown narrowed by the spike. 50.8, init, its unknown the smallest after the probe; it carries the named-place scenario and the six rewritten scenarios, which keep `@slice-4` and `@slice-47` as asked. 50.9, the sixth architecture review, falls due after 50.8, six slices after 50.2.
  Tags written: `@slice-50.6` on the markdown outline (2 selected), `@slice-50.7` on the agent (1), `@slice-50.8` on the named-place scenario (1); `-m "slice-4 or slice-47 or slice-50.8"` selects 7. 66 collected in all.
  Decisions: adrs/0040 (an agent is held to the name limits the harness publishes), 0041 (lists, tables and what sits inside them on a markdown page), 0042 (init starts in the absolute working directory, never reads `KB_ROOT`, and the suite starts it that way).
  Next: writing-plans over slices 50.5 to 50.9, one task per slice in that order, to `2026-09-27-shop-knowledge-batch9-implementation.md`.
- 2026-09-27 writing-plans done: `2026-09-27-shop-knowledge-batch9-implementation.md`, five tasks for slices 50.5 to 50.9 in slice order. Written under adrs/0011: no code, nothing built or replayed. Each task says why it is red today from this checkout's run (56 passed, 10 failed, every one on a missing step definition) and from probes of `init`, `render markdown` and `render agent`. Expected counts from the tags: `-m slice-50.6` 2, `-m slice-50.7` 1, `-m "slice-4 or slice-47 or slice-50.8"` 7; 56/10 after 50.5, 58/8 after 50.6, 59/7 after 50.7, 66/0 after 50.8. Decisions in adrs/0040, 0041 and 0042. No request to bump the pin. Its Review Focus holds five probes: a pipe in a table cell, other types' lists and an empty list on a markdown page, a name breaking one agent limit, `init` beside a `KB_ROOT` naming elsewhere, and `init ""` (still a QUESTION FOR THE SPEC). Next: slice 50.5.
- 2026-09-27 slice 50.5 green.
  Check: `pytest -q -rf | grep ^FAILED | sort` diffs empty against the baseline and gives `56 passed, 10 failed`; `--collect-only -q tests/test_publish_what_the_shop_knows.py | grep -c ::` gives `8`; the size check lists nothing; `grep -l "import \*" tests/*.py` lists exactly `tests/test_publish_what_the_shop_knows.py`, `tests/test_read_back_what_the_shop_knows.py` and `tests/test_start_a_shop_knowledge_base.py`; `git diff --stat -- src features` is empty. Lines after: `test_publish_what_the_shop_knows.py` 166, `publish_as_markdown.py` 33.
  Surprised by: nothing; the two moved steps needed only `knol` from the driver, as decision 2 expected, and the split left the test module well under the limit with room for slices 50.6 and 50.7's ~60 lines.
  Next: slice 50.6.
- 2026-09-27 slice 50.6 green.
  Check: `pytest -q -m slice-50.6` gives `2 passed`; `-m "slice-20 or slice-17 or slice-18 or slice-19 or slice-50"` gives `5 passed`; `pytest -q` gives `58 passed, 8 failed`, and the eight are the start scenarios and the agent; the size check lists nothing; `git diff --stat -- features` is empty. `markdown.py` is 81 lines after.
  Seen red: the process row's table Then failed on a plain `AssertionError` while the page still held `- **steps**: {'id': 'check-it', ...}`, Python reprs joined with commas (step 2); the role row's tags Then failed the same way while the page still held `- **tags**: tag/stock, tag/dairy` and `- **tools**: Read` (step 4); `-m slice-20` went from green to `1 failed` on the `tools` line the moment the list-of-plain-values bullet layout landed (step 5), then green again once `_a_page`'s expectation followed decision 5.
  Surprised by: kb orders a written artifact's fields by the type's schema, not by the order given to `write` or `create` — the role's `tags` (from `shop-artifact`, unioned first) prints before `harness` and `shop` (from `role`'s own schema), not after them as the content dict I wrote it from suggested. Caught by probing before writing the role row's Then, not by a wrong run. Also: implementing decisions 1, 2 and 3 together in one edit (step 3) let the role row start passing before its Given and Then existed yet — undone before it could hide a real red run, back to decision 2/3 only, then decision 1 added at step 5 as the outline asks.
  Settled: every value kb's content model holds — a mapping, a list of mappings (a part collection among them), a list of scalars, and a plain value, nested inside each other to any depth — lays out as markdown from the content alone, with no schema read and no type named; the two rows and the Review Focus probes cover a part collection, an empty list and a value with a `|`, and none needed a schema.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 1): a `|` in a value is not escaped. Reproduced: a step's `does: "Count a | b.\n"` renders its table row as `| count-it | Count it | Count a | b. |`, which reads as five cells instead of three to a markdown renderer. adrs/0041 says nothing of a pipe. A person would expect the pipe shown as written, but that reads as a broken table; escaping it as `\|` is markdown, not behaviour of its own, so it is not implemented here.
  - Review Focus 2, settled: a feature's `scenarios` (a list of mappings) lays out as a table, `| id | title | pins |` with one row a scenario, same as the process's steps. A decision's empty `tags` list lays out as `- **tags**` with nothing under it, no repr, no `[]` — a QUESTION FOR THE SPEC in its own right: a person reading the page cannot tell an empty list from a mapping with nothing shown yet.
  Next: slice 50.7.
- 2026-09-27 slice 50.7 green.
  Check: `pytest -q -m "slice-50.7 or slice-50 or slice-18"` gives `3 passed`; `pytest -q` gives `59 passed, 7 failed`, and the seven are the start scenarios; the size check lists nothing; `git diff --stat -- features` is empty.
  Seen red: `_rejected_agent_for_the_limits` failed on `[] == ['role/shop-steward at harness.name: ...]`, with `result.returncode == 0` and `.claude/agents/shop-steward.md` written, before `limits.agent` and `agent._agent` existed.
  Surprised by: nothing; `renderers/agent.py` held its own `_agent` split out from `render` exactly as `skill.py` splits `_skill` from `render`, once the harness group was pulled out of `render` before `dumps`.
  Settled: this answers the QUESTION FOR THE SPEC logged at slice 50.2 about the agent's limits. The harness's subagent documentation publishes exactly two limits on an agent's `name` — no `:`, no leading `-` — and no length limit on the name, the description or the body; `render agent` now checks both, in that order, before writing anything, giving one fault each, and writes nothing when either is broken.
  Review Focus 3 probes (throwaway store under `.superpowers/batch9/`, deleted after): a role with `harness.name: -steward` published as an agent gave exactly one line, `role/steward-a at harness.name: an agent's name does not start with "-", the limit the harness publishes; this one is -steward`, exit 1, nothing written. A role with `harness.name: shop:steward` gave exactly one line, `role/steward-b at harness.name: an agent's name holds no ":", the limit the harness publishes; this one is shop:steward`, exit 1, nothing written. `-m slice-50` (the Background's `stock-keeper` role) still gives `1 passed`.
  Next: slice 50.8.
- 2026-09-27 slice 50.8 green.
  Check: `pytest -q -m "slice-4 or slice-47 or slice-50.8"` gives `7 passed`; `pytest -q` gives `66 passed`, and `make test` ends cleanly; `python -m shop_knowledge init -h` shows `root` as `[root]`, optional, with the help text "where to start it; the working directory unless one is named"; the size check lists nothing; `git diff --stat -- features` is empty.
  Seen red: two stages, as the task predicted. First, the baseline, `7 failed`, each `StepDefinitionNotFoundError` on a Given now reading "the user is working in…". Second, once the Givens and Whens were renamed to match but before `root` was made optional: six scenarios failed on `AssertionError`s against `shop-knol init: the following arguments are required: root` (three on `returncode == 0`, two on the refusal text `already has a store` / `stores do not nest` not appearing, one — "without saying who" — on the no-role wording itself, since argparse's required-argument refusal fires before shop-knol's own no-role check ever runs); the named-place scenario passed already, since it names a directory `init` already accepted.
  Surprised by: `grep -c "in that directory" tests/test_start_a_shop_knowledge_base.py` gives `1`, not the `0` the task predicted. The one line is `@then("the work that was already in that directory is left as it was")` — a Then, unchanged since commit 1133296's rewrite and still matching the feature file verbatim (line 36). The task's rule (decision 4) only renames Given/When texts the feature no longer uses; this Then's text was never stale, so it was never a candidate for renaming, and pytest-bdd requires the registered text to match the feature line exactly. All Given/When texts are clear of the old "in that directory" phrasing; the grep's residual hit is this one correct, unrelated Then.
  Settled: `root` defaults to the working directory as an absolute path (`Path.cwd()`, `nargs="?"`), taken fresh each time `arguments.py`'s `command_parser()` runs inside `cli.main` — once per subprocess, so it reflects that process's own working directory. `kb_requests.init_request` and `cli._init` needed no change, since both already read `args.root`. `driver.start` now runs `init` with `cwd=shop` and no positional argument, so every existing caller (~20 Givens across other feature modules, and `read_back_from_elsewhere.py`'s `start(env, other)`) starts a store in the directory it's given without change to its own call site.
  Review Focus 4 probe (throwaway dirs under `.superpowers/batch9/`, `probe4` and `probe4-kbroot`): `KB_ACTOR=a KB_ROOT=<probe4-kbroot> shop-knol init` run with cwd `probe4` exits 0, writes `probe4/kb/`, and leaves `probe4-kbroot` empty — confirms adrs/0042: init never reads `KB_ROOT`.
  Open questions:
  - QUESTION FOR THE SPEC (Review Focus 5, unchanged from the task's framing, not fixed here): `KB_ACTOR=a shop-knol init ""` from an empty directory still exits 0 and makes `kb/` there. Reproduced under `.superpowers/batch9/probe5`. Because `""` is given outright, `nargs="?"`'s default is bypassed and `""` goes through `type=Path` as `Path("")`, which resolves (through kb's own connect) to the working directory anyway — the same outcome as naming nothing, by accident of how empty strings and `Path` interact, not by anything `arguments.py` declares on purpose.
  Next: slice 50.9.
- 2026-09-27 Sixth architecture review of shop-knowledge (slice 50.9), on Opus 5.5 against `CLAUDE.md`, over the code under `src/` and the step definitions after slices 50.3, 50.4, 50.5, 50.6, 50.7 and 50.8 (diff `0d770fb..9121be7`). Every finding was verified against the code in this checkout before being logged here, independently of the review's own transcript: the traceback below was reproduced directly, the size check and the step-definition greps (`import \*`, the `target_fixture="result"` count, the size check) were re-run and matched, and `markdown.py` was read in full to confirm the boolean/null finding.

  Met in full:
  - Rule 1 (kb only through its contract): `src/` imports only `kb.client`, `kb.contract.kb_pb2`, `kb.content`, and `kb.canonical` (for `NotCanonical` alone, in `cli.py:117`); `jsonschema` only in `shape.py`; nothing under `src/` opens a store's files or runs git. The batch's new modules (`limits.py`, `agent.py`) add no new kb import.
  - Rule 2: kb pinned at v0.2.1, installed from that tag, not edited.
  - Rule 3: no other YAML library; `agent._agent` writes through `kb.content.dumps` as `skill._skill` does.
  - Rule 4, for the agent's new faults: `limits.agent` builds `Fault`s and prints nothing (`limits.py:23-37`); `agent._agent` returns them as `refused(faults)` (`agent.py:22-24`); `cli._render` refuses them through `_answered`/`Refused`, the same path the skill's fault takes; `main` alone prints, one line each, exit 1. Verified: the scenario's Then and the Review Focus 3 probes logged at 50.7 both show exactly this.
  - Rule 5, for the markdown layout: `markdown.py` branches only on a value's shape (`_is_table`, `_items`, `_inline`), never a field name; the only name it knows is `sections` (adrs/0015's one exception). Verified by grepping `markdown.py`/`sections.py` for every field name the batch's scenarios touch (`steps`, `tags`, `tools`, `harness`, `with`, `branches`, `uses`, `does`, `id`, `title`, `scenarios`, `name`) — none found.
  - Rule 6, for the agent's limit check: `_agent` checks and returns faults before the file map is built; nothing is written when refused; `cli._write` runs only after `_answered` lets the `Rendered` through.
  - The module map: every module has an accurate row; `renderers/limits.py`'s docstring names both limits' sources and when each was read (2026-09-27 for the agent's).
  - Reading and refusing in one place: unchanged, `cli._document` and `cli._answered` still the only places.
  - Size limit: `find src tests -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'` -> nothing. Largest: `test_record_a_decision.py` 246, `cli.py` 233, `test_start_a_shop_knowledge_base.py` 210, `test_publish_what_the_shop_knows.py` 198.
  - One thing at one level: every new function in `markdown.py`, `agent.py` and `limits.py` is a single-purpose function with no phase-separating comment.
  - The step definitions' rules: `tests/publish_as_markdown.py` matches the two existing siblings' pattern (never imports its test module, reached only by star import, `ROLE` reached through the `role_content` fixture, not a direct import); the start feature's rewritten steps still drive shop-knol only through `tests/driver.py`; `grep -h -A3 "^@when" tests/*.py | grep -o 'target_fixture="[a-z_]*"' | sort | uniq -c` -> `43 target_fixture="result"`, matching `grep -c "^@when" tests/*.py`'s total of 43; `"--whole"` appears only at `tests/driver.py` and the read-back feature's own whole-read When; no step text defined twice; `tests/clock/` reached only through `driver.at`.

  Not met in full:
  - **Rule 4 regression: shop-knol tracebacks, does not refuse, when the working directory no longer exists.** Cause: `arguments.py`'s `root` argument is declared `default=Path.cwd()` (`arguments.py:34`), evaluated when `command_parser()` builds the parser — for every command, not only `init` — and `cli._parsed` catches only `ArgumentRefused`, not the `FileNotFoundError` `os.getcwd()` raises. Reproduced independently in this session, both for `init` and for `read` (a command that takes no `root` argument at all, since the parser is still built): a `mktemp -d` directory removed out from under the shell, then `KB_ACTOR=a shop-knol init` and `KB_ACTOR=a shop-knol read decision/x` each end in `FileNotFoundError` raised from `pathlib.py`'s `Path.cwd()`, a full Python traceback on stderr, not shop-knol's own one-line refusal. Before slice 50.8 (commit 049bb00), the same `read` from a removed directory gave one line, `No such file or directory`, exit 1 — so this is a regression slice 50.8 introduced, not new behaviour that was never held. Cut as slice 50.10 below.

  Not called for:
  - `limits.py` takes a field's dotted path (`"harness.name"`, `"steps"`) as a string from its callers, which is arguably a renderer's own field knowledge leaking into a shared module; but it sits under `renderers/`, only `skill` and `agent` call it, and four prior reviews (through 50.2) have passed the same shape for the skill's `steps`. Not a new violation, and fixing it would move no knowledge out of `renderers/` since only renderers call `limits.py`.
  - `markdown.py`'s docstrings undersell what their code does in a couple of places (`_items`'s docstring calls out "plain values" but its list branch is more general; `_is_table`'s docstring reads awkwardly) — no rule sets docstring completeness or style.
  - `publish_as_markdown.py`'s `_publish_as_markdown` still names `"role/stock-keeper"` itself rather than taking `role_name` the way the agent's When now does; no scenario overrides the markdown role, so nothing is broken by this asymmetry.
  - Lines over 120 columns in a few places (`cli.py`, a step text in `publish_as_markdown.py`); no rule sets a line-length limit.
  - The repr-detection Then (`publish_as_markdown.py`) checks only bracket/quote markers, not `True`/`False`/`None` — it covers exactly what this task's two scenarios can hold; widening it is for whichever scenario the open question below leads to, not a defect today.

  Open questions:
  - QUESTION FOR THE SPEC: `render markdown` shows a boolean or a null the way Python spells it (`True`, `False`, `None`), not a YAML/markdown-appropriate spelling. Cause: `_inline`'s plain-value fallback is `" ".join(str(value).splitlines())` (`markdown.py:80`), and `str()` of a Python `bool`/`NoneType` is its Python name. Reproduced: a decision recorded with `urgent: true` and `waived: null` (its schema leaves extra fields open) renders as `- **urgent**: True` and `- **waived**: None`; a table cell holding `false` renders `False`. No shop type declares a boolean or null field today and no scenario holds one, so this is left a question rather than a slice, per CLAUDE.md's "never adds behaviour no scenario asks for" — but adrs/0038's "no repr is ever shown" arguably already answers it. Logged for formulating-features and the human.
  - Carried unchanged from earlier entries: `init ""` (50.2, 50.8); an unescaped `|` in a table cell (50.6); an empty list shown as its field's name with nothing under it (50.6); stale artifacts unseen beside faults; a batch's fault naming a change by an artifact that does not exist; a reason given to `init`; tagging with a tag that does not exist; a non-role published as an agent; the agent's `tools` as a list.
  - Closed since 50.2: the agent renderer checking no harness limit (adrs/0040, slice 50.7); the empty batch's traceback (kb v0.2.1).

  Cut: slice 50.10, enabling, right after 50.9 — shop-knol refuses, never tracebacks, when the working directory no longer exists. It adds or moves no scenario, so no feature file or `@slice` tag changes. Not implemented in this batch (adrs/0011: this plan carries no code, and this finding surfaced after the plan was written); it waits for its own plan, the way slice 50.2 cut 50.3 and 50.4 into batch 8 rather than fixing them inline.
  Next: writing-plans over slice 50.10, when it is next taken up.
- 2026-09-27 Final whole-branch review of batch 9 (slices 50.5-50.9), on Opus 5.5 against the plan, CLAUDE.md and the ADRs it rests on, over commits `11669fc..77ffb5b`. Declined to judge, as out of this batch's scope: an unrelated concurrent commit (`92c2a4f`, adrs/0011 and 0039 prose) that landed on `main` mid-batch from a different process; `init ""`; an empty list shown as its field's name with nothing under it; the harness's whole-tree limits (a combined-description token warning, cross-file name uniqueness), neither reachable from rendering one role. Ready to merge: with fixes, all of them follow-up slices rather than changes to this batch — the suite gave `66 passed, 0 failed` under both `pytest -q` and `make test`, and no CLAUDE.md rule was found broken in the diff itself.

  Three Important findings, each adjudicated here (spec is the binding authority, the plan its argument):
  - The working-directory traceback (rule 4), already found and cut as slice 50.10 above. The reviewer confirms the reproduction and calls the deferral "defensible", noting slice 50.10's check should be widened to catch a regression returning: whoever plans it should consider pinning it with a scenario, or saying why not. Ruling: stands as cut, unchanged. Cost if wrong: the regression stays open one plan longer; nothing in this batch depends on it.
  - **A `|` in a table cell breaks the row**, which the reviewer reads as already settled by Review Focus 1's wording ("QUESTION FOR THE SPEC, unless the layout escapes it as `\|`, which is markdown and not behaviour of its own") to mean escaping should have been added. Ruling: parked, not a defect. Review Focus 1's sentence is permissive, not a mandate: it clarifies that *if* an implementer chose to escape the pipe, doing so would be mechanics, not a product-behaviour decision needing the spec's sign-off — it does not instruct that escaping be added, and Task 2's own Step 7 asked only to "run the probes... and log what each shows". Task 2 did: it logged the unescaped outcome as the QUESTION FOR THE SPEC branch, which is one of the two outcomes the sentence names. Adding escaping now, with no scenario driving it, would itself add behaviour no scenario asks for (CLAUDE.md). Stays a QUESTION FOR THE SPEC, as logged at slice 50.6. Cost if wrong: a step's text holding a literal `|` still breaks its table row until a scenario settles the spelling; no current scenario holds one.
  - **A boolean or null renders as `True`/`False`/`None`, not a page's own spelling**, which the reviewer argues adrs/0038 ("A Python repr on a page is a defect") already settles as a defect, not an open question — stronger than the 50.9 review's "arguably" hedge. Ruling: agreed; re-classified from open question to a cut slice, 50.11, above. It is not implemented here: no shop type declares a boolean or null field today, so a fix has no scenario to pin it, and CLAUDE.md forbids adding behaviour no scenario asks for. What remains open is only the spelling (YAML's `true`/`false`/`null`, or something else), not whether Python's spelling is wrong — adrs/0038 already answers that. Cost if wrong: a future artifact holding such a value (a type's open `additionalProperties` can already carry one) shows a Python spelling until 50.11 lands; nothing in this batch's own scenarios is affected, since none holds one.

  Seven Minor findings (a sibling module's docstring undercounting what it holds; a step reading a fixture defined out of its usual place; `_publish_as_markdown` hardcoding a role name a future outline row could silently mis-target; a docstring pointing at this plan instead of an ADR; a repeated `Fault(...)`-building shape across `skill` and `agent` in `limits.py`; an awkward docstring sentence in `_is_table`; the repr-detection Then not covering the item-3 gap) are logged here, not fixed: the reviewer confirms none breaks a CLAUDE.md rule. Left for a future enabling tidy-up slice, alongside 50.10 and 50.11.
  Next: push. Every slice in this plan (50.5-50.9) is green; 50.10 and 50.11 wait for their own plan.
- 2026-09-27 Suite: 66 passed, 6 failed. The six failing are the scenarios commit 6e205f7 added, each on `StepDefinitionNotFoundError`: the two removed-working-directory scenarios (feature-formulator, marked settled on "shop-knol never shows a traceback") and the four rows of the markdown yes/no/empty outline. The formulator marked the outline settled; it was raised to deciding here, since its step must say whether YAML's own `true`/`false`/`null` count as a program's representation. The user chose `yes`, `no` and nothing (adrs/0043, spec amended in 4dc0068), which settles it.
- 2026-09-27 Re-slice: slice 50.10 turns capability, pinned by the two new scenarios as the batch 9 final review asked, rather than a manual check that would not catch the regression returning. Slice 50.11 takes the outline, its spelling no longer open. Slice 50.12 cut, enabling: the batch 9 final review's minor findings 1 to 6 (minor 7, the repr Then, rides with 50.11) and the 50.9 review's `_items` docstring. The three are independent of each other in behaviour, ordered by unknown, the tidy last so it tidies what 50.11 leaves. Tags: `@slice-50.10` selects 2, `@slice-50.11` selects 4. Three implemented slices since the sixth review, so no review is due.
- 2026-09-27 Answered by this re-slice: the QUESTION FOR THE SPEC on a boolean or null's spelling (adrs/0043). Still open, from the formulator: what reason a refusal from a removed working directory gives (the scenarios ask only for one plain line); whether `KB_ROOT` still serves a user whose working directory was removed; whether `init <absolute path>` works from one.
- 2026-09-27 Plan batch 10: slices 50.10 to 50.12, `docs/superpowers/plans/2026-09-27-shop-knowledge-batch10-implementation.md`. A spike, run and thrown away, settled how the steps can run shop-knol from a removed working directory: a child process removes its own working directory after entering it and before shop-knol starts. Next: execute it, then the batch's final review, then push.
- 2026-09-27 slice 50.10 green. Someone can now: start a knowledge base, or read from one, from a directory that has been removed, and be refused in one plain line (`No such file or directory`, exit 1), never shown a traceback.
  Red runs seen: before any step, `-m slice-50.10` gave `2 failed`, each on `StepDefinitionNotFoundError` (the two Givens). With the steps written and nothing under `src/` changed, the start scenario was red on its Then, `assert "Traceback" not in result.stderr + result.stdout` (`FileNotFoundError: [Errno 2] No such file or directory` raised from `Path.cwd()` in `arguments.command_parser`). The read-back scenario went green at once once its Given was written, its cause fixed by the start scenario's change; run against the pre-fix `arguments.py` (stashed), it was red on the same assertion, the same traceback from `Path.cwd()`.
  Change: `init`'s `root` defaults to `Path(".")` rather than `Path.cwd()`, so building the parser reads no working directory; kb resolves `.` where `cli._run`'s guard already turns an `OSError` into a fault. `init -h` still shows `[root]`, "the working directory unless one is named". The seven start scenarios under `-m "slice-4 or slice-47 or slice-50.8"` stay green. The steps: `driver.Removed` is a working directory `knol` removes in the child after it has entered it and before shop-knol starts; the start Given gives it as `start_in`, the read-back Given (in `read_back_from_elsewhere.py`, now "six scenarios") as `workdir`, with `KB_ROOT` removed.
  What `init` and `read` print from a removed directory: `No such file or directory`, one line on stderr, exit 1, nothing on stdout, for both.
  Review Focus 1, each from a removed directory under `.superpowers/batch10/` with `KB_ACTOR=a`, each one stderr line, no `Traceback`, exit 1, empty stdout: `init elsewhere` `a store is started in a directory that exists; 'elsewhere' does not`; `list --type decision` `No such file or directory`; `create decision --from x.yaml -m m` `x.yaml: No such file or directory`; `render markdown decision/x --to out` `No such file or directory`; `validate` `No such file or directory`.
  Review Focus 2: `read decision/x` from a removed directory with `KB_ROOT` naming a started store refuses, `No such file or directory`, exit 1; it does not read through `KB_ROOT`. QUESTION FOR THE SPEC (the formulator's question 2): the spec finds the store "upward from the working directory ... or through `KB_ROOT`" and says nothing of a working directory that is gone. Reproduction: `cd` into a directory, remove it from another shell, run `KB_ROOT=<a started store> KB_ACTOR=a shop-knol read decision/x`.
  Review Focus 3: `init <absolute path to an empty directory>` from a removed directory works: exit 0, nothing on stderr, `kb/` started there. Not a question.
  Surprised by: the one-line part of rule 4 could not sit on the shared body of "the user is shown that fault in plain words, never a traceback": it turned slice 1.28's "The user checks a knowledge base holding a file the shop cannot read" red, since `validate` rightly prints one line per fault (two there). So "the user is shown the refusal in plain words, never a traceback" has a body of its own that calls the shared one and adds the one-line assertion.
  Open questions: QUESTION FOR THE SPEC (the formulator's question 1), what a refusal from a removed working directory says: today the operating system's words, `No such file or directory`, naming no path. QUESTION FOR THE SPEC, `KB_ROOT` from a removed working directory (Review Focus 2 above). Carried unchanged from earlier entries.
  Suite: `68 passed, 4 failed`, the four `-m slice-50.11`'s outline rows; 72 collected; size check lists nothing; `git diff --stat -- features` empty. Next: slice 50.11.
- 2026-09-27 slice 50.11 green. Someone can now: publish a role or a process as markdown and find a yes as `yes`, a no as `no` and an empty value as nothing, in the field list (`- **deputy**:`, ending at the colon) and in a table cell alike.
  Red runs seen: before any step, `-m slice-50.11` gave `4 failed`, each on `StepDefinitionNotFoundError` (each row's Given). With the role's yes/no Given and the Then "that directory holds a page of the <thing>" written and nothing under `src/` changed, that row was red on the page: `- **on_call**: True`, `- **retired**: False`. The `bool` branch in `markdown._inline` made it green. The role's empty value was red on `- **deputy**: None`; with `_inline`'s `None` branch alone it was red again on the trailing space, `- **deputy**: `; `_items` now ends the line at the colon when the inline value lays out as nothing (`_after_the_colon`), with no second spelling of nothing. The two process rows went green as soon as their Givens existed, credited to those two branches: with the `bool` branch reverted (throwaway) the process yes/no row was red on the cells `| True | False |`, and with the `None` branch reverted the process empty row was red on the cell `| None |`. Writing the whole read's steps back, ids included, was accepted.
  The unknown: answered. A yes, a no and an empty value the user writes reach the renderer as a boolean and a null after kb checks and stores them, and are told apart there by kind of value, never by spelling. Text quoted as `"yes"`, `"True"` or `"null"` stays text and is shown as written.
  The widened Then: `_no_repr_on_the_page` also refuses `True`, `False`, `None`, `true`, `false` or `null` standing as a whole value (after a field's colon, a bullet or `; `, or in a table cell), not a word in prose. With `_inline`'s two new branches reverted and the page Then made a no-op (throwaway), all four rows were red on it (`': True'`, `': None'`, `'| True'`, `'| None'`). Restored: `-m slice-50.6` `2 passed`, `-m slice-50.11` `4 passed`.
  Review Focus 4: a role holding `motto: "yes"`, `flag: "True"`, `none: "null"` publishes `- **motto**: yes`, `- **flag**: True`, `- **none**: null`, each as written. A text `True` is the user's words; no scenario holds one, and the widened Then would refuse it if one did.
  Review Focus 5: a step holding `flags: {urgent: true, rushed: false, owner: null}` shows the cell `urgent: yes, rushed: no, owner: ` (so `| ... owner:  |`), no line ending in a space. kb refused a shared-step use binding `shelf` to null (`process/restock-null at steps/0/with/0/value: None is not of type 'string'`), and a role whose `harness` holds `background: true` (`Additional properties are not allowed ('background' was unexpected)`): kb's refusals, not defects. Beyond the probe: a role field holding the list `[true, null, false]` shows `  - yes`, `  - ` and `  - no`, the middle line ending in a space.
  Surprised by: kb's own refusal of a null binding spells it `None`, a program's spelling in a refusal kb words (kb is pinned; not this slice's page).
  Open questions: QUESTION FOR THE SPEC, a null in a list of plain values leaves a bullet line ending in a space (`  - `); reproduction: publish as markdown a role holding `answers: [true, null, false]`. QUESTION FOR THE SPEC, a null inside an inline mapping is `owner: ` then the next separator; whether `owner:` drops its space there is not said. Carried: whether a field holding nothing is left off the page (adrs/0043 keeps it); how an empty list is shown (from 50.6).
  Suite: `72 passed`; size check lists nothing; `git diff --stat -- features src/shop_knowledge/types` empty; `grep -n "sections"` in the markdown renderer names `sections` alone. Next: slice 50.12.
- 2026-09-27 slice 50.12 green. No behaviour changed; every check's before and after:
  - `.venv/bin/python -m pytest -q`: before `72 passed`; after `72 passed`.
  - `grep -rn "Task [0-9]" src tests --include="*.py"`: before one line, `role_content`'s docstring ending "(Task 1, decision 2)"; after nothing (reworded to point at adrs/0035).
  - `grep -c "role/stock-keeper" tests/publish_as_markdown.py`: before 5 (Task 2's role Givens had grown the count past the brief's own recorded 2); after 0. The When and every Given that writes over the Background role now take `role_name` instead.
  - `grep -c "Fault(" src/shop_knowledge/renderers/limits.py`: before 3; after 1, in a new `_fault` helper `skill` and `agent` both call.
  - size check: before nothing listed; after nothing listed.
  - `git diff --stat -- features src/shop_knowledge/types`: before empty; after empty.
  - the publish feature's test module, every fixture before the first step: before, `role_name` sat at line 155 among the agent steps while `role_content`, `target` and `before` sat together at 49-66; after, all four sit together at 49-73 — but the check narrowed to before this module's first `@when`/`@then`, missing the Background `@given` (`_shop_with_a_process_and_a_role`) that still sat above the fixture block at line 21. The final whole-branch review caught it (finding 2) and the batch's fix wave moved that `@given` below the fixture block on 2026-09-27, so every fixture now precedes every step definition in the module, `@given` included.
  - the docstrings the review found short or awkward: `markdown._is_table` and `markdown._items` reworded to say plainly what each decides; `publish_as_markdown`'s module docstring now names its Givens too, added by Task 2, not only its When and Thens.

  Items 1-7 (the brief): 1) the module docstring now names the Givens (process steps saying more than one thing, or gaining a yes/no or an empty value; role gaining a tag, a yes/no or an empty value) alongside the When and Thens. 2) `role_name` moved to sit with `role_content`, `target` and `before`. 3) `_publish_as_markdown` and every Given that writes over the Background role (`_role_holds_more_than_one_tag`, `_role_holds_a_yes_and_a_no`, `_role_holds_no_value`) take `role_name` instead of naming `"role/stock-keeper"` themselves. 4) `role_content`'s docstring now points at adrs/0035 (a sibling module reaches the test module's content only through a fixture) instead of "Task 1, decision 2". 5) `renderers/limits.py` gained one private `_fault(artifact, path, message)` that `skill` and `agent` both call; each limit's source stays in its own docstring. 6) `markdown._is_table`'s docstring reworded, dropping the awkward "and not, say, a part collection's own kind of emptiness" aside. 7) `markdown._items`'s docstring no longer calls a list's items "plain values"; it says the list branch lays any item out inline, mappings alone going to a table instead.

  Items 8-13 (added by the controller's ruling from the batch 10 task reviews):
  8) The role page's 13 base lines, before written out in `_a_page` and in both `_role_holds_a_yes_and_a_no` and `_role_holds_no_value`, now come from one `_role_page(extra=())` that splices a row's own lines in before the section; the process table's first rows, before written out in both `_process_step_holds_a_yes_and_a_no` and `_process_step_holds_no_value`, now come from one `_process_page(columns, cells)` over a shared `_STEP_ROWS` table. Every expected page is unchanged, byte for byte (confirmed by the unchanged `-m "slice-20 or slice-50 or slice-50.6 or slice-50.7 or slice-50.11"` -> `9 passed`).
  9) `_process_step_holds_a_yes_and_a_no` and `_process_step_holds_no_value`, before indexing `steps[2]` and `steps[3]`, now use a new `_step_holding(steps, step_id, **fields)` that finds the step by its `id` ("order-more", "stop"), matching what each docstring already named.
  10) `_a_page_of` moved from between the two role Givens (`_role_holds_a_yes_and_a_no` and `_role_holds_no_value`) to sit with the module's other Thens, right after `_a_page`.
  11) `_no_repr_on_the_page` now binds `_PROGRAM_SPELLING.search(text)` to `match` once, asserting on that instead of calling `.search` a second time inside the assertion message.
  12) `driver.py` gained `removed(tmp_path) -> Removed`, the one place that builds `tmp_path / "gone"`, makes it, and wraps it in `Removed`; both `tests/test_start_a_shop_knowledge_base.py`'s `_a_removed_directory` and `tests/read_back_from_elsewhere.py`'s `_working_in_a_removed_directory` call it instead of repeating the three lines.
  13) `conftest.py`'s "the user is shown the refusal in plain words, never a traceback" docstring reworded: it says plainly that this Then, unlike the shared body it calls, is never used where a command reports more than one fault, which is why it alone also asserts the one line count.

  Seen red: none: this slice changes no feature file and no scenario's steps, only how the existing ones are written; every check ran green on the first attempt after each item.
  Suite: `72 passed`; size check lists nothing; `git diff --stat -- features src/shop_knowledge/types` empty. Next: the batch's final whole-branch review, then push.
- 2026-09-27 Final whole-branch review of batch 10 (slices 50.10-50.12) found three findings; all three fixed in this session, no feature file touched, `72 passed` before and after.
  Finding 1 (IMPORTANT, regression): slice 50.10's `arguments.py:34` made `init`'s `root` default `Path(".")` instead of an eager `Path.cwd()`, so kb now sees the relative `"."` and quotes it, not the absolute working directory, in its own refusals. Reproduced against 504841a with `KB_ACTOR=a .venv/bin/shop-knol init`:
  - existing store, before: `a store is never started over another; '.' already has a store inside it`; after: `a store is never started over another; '/…/shop' already has a store inside it`.
  - nesting, from `shop/notes`, before: `stores do not nest; '.' is inside the store at '/…/shop'`; after: `stores do not nest; '/…/shop/notes' is inside the store at '/…/shop'`.
  - permission denied, before: `kb: Permission denied`; after: `/…/ro/kb: Permission denied`.
  Fix: `kb_requests.init_request` (`src/shop_knowledge/kb_requests.py:11`) now sends `root=str(args.root.resolve())`, so kb always quotes an absolute path; `arguments.py`'s default stays `Path(".")`, declared once (adrs/0032). A removed working directory still ends in exactly one stderr line, exit 1 (`No such file or directory`), since `_init` runs inside `cli._run`'s `OSError` guard whether the `FileNotFoundError` comes from `kb_client.connect` or from `.resolve()` itself. Verified: `.venv/bin/python -m pytest -q -m "slice-4 or slice-47 or slice-50.8 or slice-50.10"` → `9 passed`.
  Finding 2 (MINOR): fixed as the checkpoint line above is now corrected to say — every fixture in `tests/test_publish_what_the_shop_knows.py` now sits before every step definition, `@given` included: the Background `@given` (`_shop_with_a_process_and_a_role`) moved from line 21, above the fixture block, to just after `role_name` (the last fixture, ending line 73) and before the module's first `@when`.
  Finding 3 (MINOR): `tests/publish_as_markdown.py`'s module docstring reworded; it no longer places the `page` fixture "among" the Thens (`_a_page_of` is the Then that reads it, not one that gives it) and now says the yes/no/empty Givens give it.
  Suite: `.venv/bin/python -m pytest -q` → `72 passed`; size check (`find src tests -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'`) lists nothing.
- 2026-09-27 Final whole-branch review of batch 10 (slices 50.10-50.12), on Fable 5.1 against the plan, CLAUDE.md and the ADRs, over `504841a..cdc2a0c`, the reviewer running the suite (`72 passed`) and every check itself. Ready to merge with fixes: one Important, a no-argument `init`'s refusals quoting `'.'` where they named the directory (slice 50.10's relative default, which kb quotes as named), fixed in 4c08614 by sending kb the root resolved; and a Minor, slice 50.12's fixture-order check reported met when the Background's Given still preceded the fixtures, fixed the same commit. A scoped re-review found both addressed and nothing broken by the fix. Ruling: an explicitly named relative root is now quoted absolute too, the cost of stating the root one way. Left as QUESTION FOR THE SPEC: a removed working directory's refusal names no path (`No such file or directory`); `KB_ROOT` does not serve a user whose working directory was removed (kb's `connect`). Deferred to a future tidy slice: a null item in a plain-value list lays out as a bullet with a trailing space (layout mechanics, not a spec question); `_steps_as_a_table` still spells out the table `_process_page` builds; the `_role_page` and conftest refusal Then docstrings; `_step_holding` passing silently on a missing id; `preexec_fn`'s thread-safety; `cli._init` connecting with the unresolved root while its request carries the resolved one (harmless, kb ignores it). Declined as out of scope: floats laid out by `str()`; a text `"True"` shown as written; `|` in a cell; whether an empty field or list is shown at all.
  Next: push. Every slice in this plan is green.
- 2026-09-27 Spec amended in bdbd580 (decisions 0044-0046): refusals of shop-knol's own name their place and an empty name is refused; a working directory that no longer exists is inside no store; a failing check still shows what is behind its type; a renderer refuses a type it does not render; markdown stays well-formed and shows an empty list as nothing. Under adrs/0044 the open QUESTION FOR THE SPEC lines were sorted against the spec's principles: answered as defects, and cut below: a non-role published as an agent (and a non-process as a skill or diagram), an unescaped `|` in a cell, `init ""`, a removed working directory's refusal naming no path, `KB_ROOT` from a removed working directory, the trailing spaces after a null, an empty list's layout, the check's answer beside its faults. Answered as already right, and closed: a reason given to `init` is refused (the init row: "its messages are fixed"); tagging with a tag that does not exist is refused by kb (a tag is a reference with integrity); a batch's fault names the artifact kb names ("Errors are printed as returned by kb"). Closed as a fact: the harness's subagent documentation (code.claude.com/docs/en/sub-agents, read 2026-09-27) takes `tools` "as a comma-separated string such as `Read, Grep, Bash` or a YAML list", so the agent's list loads unchanged. Carried: a Create refused mid-way through `init` leaving some types, which no scenario reaches.
- 2026-09-27 Formulation (feature-formulator, spec only), written in 7b23b54: eight new scenarios and three rewritten. Four came back deciding; the user approved the readings: `init` from a removed directory is refused as the directory being gone; a renderer refusing a type names the artifact's type and the type it takes; "whatever a value holds" reaches text over several lines and text ending in a space, the trailing space not shown. Three rewrites of the store-finding refusals ("naming the directory") were dropped at the user's choice: those refusals are kb's, and name their place already. The formulator's nine questions are answered by stated principles (adrs/0044): `init` never reads `KB_ROOT` (adrs/0042), so from a removed directory it refuses; "the working directory" said in words names a directory that no longer has a path; `KB_ROOT` set empty is refused by kb today; an empty `--section` or `--type` is a name given empty, refused by slice 50.17's rule, while search text names no place; `init`'s nesting refusals are kb's and name the directory (4c08614); an empty mapping is an empty value (adrs/0045, one spelling of nothing); a space inside a line before a separator is allowed, only a line's end is held; a name of spaces is not empty; `markdown` for any type includes schema artifacts.
- 2026-09-27 Suite: 70 passed, 17 failed. The 17: the eleven new rows, the two new empty-list rows of the yes/no/empty outline, the new `KB_ROOT` scenario, and the two rewritten removed-directory scenarios, now red on their new Then.
- 2026-09-27 KB PIN-BUMP REQUEST: kb's in-process client reads the working directory (`Path.cwd()`) before it looks at `KB_ROOT`, so from a working directory that no longer exists every call but Init raises the operating system's `No such file or directory` instead of finding the store. The spec now says such a directory is inside no store: `KB_ROOT` still serves, and with none set the command refuses, saying the working directory is gone. Requested of kb: its store finding treats a working directory that no longer exists that way. Slice 50.22 waits for the release carrying it and the pin that follows.
- 2026-09-27 Re-slice: slices 50.13 to 50.22 cut. Ordered by unknown: the check's answer beside a refusal (it touches the one way to refuse) first, then the well-formed page, then the renderers' type check. Six implemented slices since the sixth review then fall due for the seventh (50.16, adrs/0010), which runs before the next plan (adrs/0011), so batch 11 is 50.13 to 50.15. After it: the empty-name rule (50.17, its unknown) and its three other commands (50.19 to 50.21, none), the removed directory's refusal at `init` (50.18), and 50.22, blocked on kb. The yes/no/empty outline moves from `@slice-50.11` to `@slice-50.14`, its first four rows credited to 50.11; the two rewritten removed-directory scenarios move from `@slice-50.10`, to 50.18 and 50.22, their earlier Thens credited to 50.10.
- 2026-09-27 Plan batch 11: slices 50.13 to 50.15, `docs/superpowers/plans/2026-09-27-shop-knowledge-batch11-implementation.md`. After it, slice 50.16 (the seventh architecture review) runs before 50.17 to 50.21 are planned; 50.22 waits for kb. Next: execute batch 11.
- 2026-09-27 HAND-BACK slice 50.13, scenario "The user checks a knowledge base holding a file the shop cannot read" (slice 1.28): a previously green scenario breaks and the fix would change what a step means.
  Evidence: with `answers.checked` answering `sound` from the check's faults and violations and `cli._validate` showing the answer on stdout before refusing through `_answered` (the handler shows, then refuses; no second printer, no second way to refuse), slice 50.13's scenario is green and slice 1.28's is red on the shared Then "the user is shown that fault in plain words, never a traceback" (`tests/conftest.py`, `_shown_in_plain_words`), whose body asserts nothing on stdout: `assert result.stdout == ""` / `AssertionError: assert 'sound: false\nbehind: []\n' == ''`. adrs/0046 says a failing check shows `sound: false` and `behind:` on stdout, so the step's "nothing on stdout" cannot hold for any check with faults; the same Then serves read-back and record-a-decision, where a refusal prints nothing on stdout. Holding both needs a decision the brief does not settle: drop "nothing on stdout" from the shared body (weakening it for every refusal), override the step for the check's feature alone, or say it only for commands other than `validate`. Each changes what the step means in some scenario.
  Red runs: before steps, `-m slice-50.13` → `1 failed` on `StepDefinitionNotFoundError`; with the Given and Thens written and `src/` untouched, red on stdout: `_other_listed_as_behind` → `KeyError: 'behind'` (stdout empty, adrs/0029's refusal). Throwaway red of the old scenario's exit (`_validate` returning 1, `shown`'s exit check lifted): `_not_a_fault` → `assert result.returncode == 0` / `AssertionError: assert 1 == 0`; both reverted.
  Probes (`.superpowers/batch11/probe-t1/`): Review Focus 1, an unreadable decision beside one behind its type → stderr one line, the unreadable file's fault; stdout one YAML document, `sound: false` and the `behind` list naming the weekly decision at 1 of 2; exit 1. `validate` takes no `--json`, so there is no JSON form to compare. Review Focus 2, slice 44's two faults and nothing behind → `sound: false`, `behind: []` on stdout, both fault lines on stderr, exit 1; slice 44's two-fault scenario passes.
  Suite: `.venv/bin/python -m pytest -q` → `17 failed, 70 passed`: slice 1.28's scenario plus the sixteen of slices 50.14, 50.15 and 50.17 to 50.22. `-m "slice-44 or slice-42.2"` → `3 passed`. Size check lists nothing. `git diff --stat -- features` empty.
  Green in this slice: The user is told what is behind its type even when the check finds faults. Red: The user checks a knowledge base holding a file the shop cannot read (previously green, slice 1.28).
- 2026-09-27 RE-SLICE after the HAND-BACK of slice 50.13: no row of the hand-back table applies, since no Given, When or Then line reads differently, no scenario is added or removed, and no feature file is touched. The Then "the user is shown that fault in plain words, never a traceback" says that the fault is on stderr in plain words and that there is no traceback. Its step body's "nothing on stdout" was the step definition's own addition, right for every refusal until adrs/0046 let one refusal, a check that finds faults, carry its answer on stdout. Ruling: the shared body keeps "nothing on stdout" for every refusal except a check's answer. stdout is empty, or it is exactly the check's answer document with `sound: false`. So the read-back and record refusals are held as strictly as before, and slice 1.28's check shows its answer as the spec says. Slice 50.13 stays in progress, with no reorder.

- 2026-09-27 slice 50.13 green after the ruling. Someone can now: check the shop's knowledge and, when the check finds faults, see them one line each on stderr and, in the same run, `sound: false` and what is behind its type on stdout, exit 1.
  Way chosen to show and refuse: `cli._validate` shows `answers.checked` on stdout, then refuses through `_answered`. `Refused` and `main`'s one printer are unchanged, so rule 4 holds with no second printer and no second way to refuse. `answers.checked` answers `sound` from the check's faults and violations.
  After the ruling: `_shown_in_plain_words` (`tests/conftest.py`) holds stdout empty, or exactly a failing check's answer (a mapping of `sound: false` and `behind`), told apart by stdout's content. Red runs and probes: as in the HAND-BACK entry above.
  Checks: `-m "slice-1.28 or slice-44 or slice-42.2 or slice-50.13"` → `5 passed`. The record and read-back modules fail only in their four scenarios of slices 50.17 to 50.22.
  Suite: `.venv/bin/python -m pytest -q` → `16 failed, 71 passed`. Size check lists nothing. `git diff --stat -- features` empty.
  Surprised by: the shared refusal Then's "nothing on stdout" also held slice 1.28's check (handed back, ruled above). Open questions: none. Next: slice 50.14.
- 2026-09-27 slice 50.14 green. Someone can now: publish anything as markdown and find every table row with one cell per column whatever a cell's own text holds, a plain value's own line never ending in a space, every value shown, and an empty list among a field's items shown as nothing: its field's name and colon, or an empty cell (adrs/0043, 0045). Corrected 2026-09-27 (final review, finding 2): this overstated what the scenarios hold. A title, a section title, a header cell built from a mapping's own key, a nested list's last item, and a list of mappings inside a field group are none of them reached by any scenario here and can still end a line in a space or, for the header cell, break a table's cells; those cases, reproduced, are logged below as adrs/0044 routes to formulation.
  Red runs: before steps, `-m slice-50.14` → `6 failed, 4 passed`, each of the six on `StepDefinitionNotFoundError`. With the steps written and `src/` untouched: the separator row red on "every table row has one cell for each column" (`markdown_well_formed._one_cell_for_each_column`: the order-more row `| ... | milk | cream |`, 8 cells under 7 columns); the empty item among a list's items red on "no line on the page ends in a space" (`AssertionError: ['  - ']`); the text ending in a space red on the same Then (`AssertionError: ['- **motto**: Full shelves ']`); the role's empty list red on "that directory holds a page of the role" (`_a_page_of`, the page showing `- **deputies**` with no colon). Green as soon as their steps existed, with and without this slice's `src/` change: the text over more than one line, credited to adrs/0041's layout (slice 50.6), a plain value's lines joined by a space; the process step's empty list, credited to adrs/0041's inline list (slice 50.6), an empty list's items joined by `; ` being nothing, so an empty cell.
  Escape chosen and where: in `renderers/markdown.py`, `_cell`, where `_table` makes a cell's text and nowhere else: the character that separates cells is written `\|` (GFM's escape), and any backslash the text holds right before it is doubled, so a reader shows the user's backslash and the row keeps its cells. The field list is not a table and escapes nothing. A bullet's item goes through `_after_the_colon`, so an empty item is `  -`; a field holding an empty list falls through to the field line, so `_after_the_colon` gives adrs/0043's one spelling of nothing; `_inline` drops the spaces a plain value ends in (the trailing space not shown, as the user chose on 2026-09-27).
  Probes (`.superpowers/batch11/probe-t2/`): Review Focus 3, a role whose top-level `motto` is `a | b` shows `- **motto**: a | b`, unescaped; a step holding the mapping `detail: {say: a | b}` shows the cell `say: a \| b`, escaped like any cell text. Review Focus 4, a step whose `does` is `a \| b`: with only the separator escaped the cell was `a \\| b`, the user's own backslash indistinguishable from the escape; the backslash right before a separator is doubled instead, the cell `a \\\| b`, which shows `a \| b`, so every value is shown as the user wrote it (adrs/0044). Corrected 2026-09-27 (final review, finding 5): the reason logged here was wrong ("a markdown reader reads [`a \\| b`] as an escaped backslash then a cell boundary, 5 cells under 4 columns"); GitHub's GFM keeps `a \\| b` in one cell and only drops the backslash, so no cell boundary was ever at risk there. The right reason is "every value shown", above. No GFM parser is installed; cells are counted by `tests/markdown_well_formed._cell_count`'s own rule, stricter than GFM's (it escapes a separator only behind an odd run of backslashes, left to right, where GFM escapes one behind any backslash at all), so it never counts fewer boundaries than GFM does; its docstring is corrected to say so.
  Checks: `-m slice-50.14` → `10 passed`; `-m "slice-20 or slice-50.6"` → `3 passed`, their pages compared line for line and unchanged. `grep -n "sections" src/shop_knowledge/renderers/markdown.py` shows the one name the renderer knows and no field name. `git diff --stat -- features src/shop_knowledge/types` empty. Size check lists nothing; the well-formed outline's steps are in `tests/markdown_well_formed.py`, which imports `_write_over`, `_role_page`, `_process_page` and `_step_holding` from `tests/publish_as_markdown.py`, and the test module star-imports it (adrs/0035).
  Suite: `.venv/bin/python -m pytest -q` → `10 failed, 77 passed`, the ten of slices 50.15 and 50.17 to 50.22.
  Surprised by: a backslash before the separator needed escaping too (Review Focus 4). Open questions: a list of mappings inside a field group is laid out as bullets of inline mappings, and one whose last value is empty ends its line in a space (`_items({"x": [{"a": None}]}, 0)` gives `  - a: `); the spec's "no line ends in a space" answers it (adrs/0044), but no scenario holds it, so it is left for slicing. Next: slice 50.15.
- 2026-09-27 slice 50.15 green. Someone can now: publish a process as an agent, or a role as a skill or a diagram, and be refused in one line naming the artifact, the type that kind of file is made from and the type it is, exit 1, with nothing written.
  Red runs: before steps, `-m slice-50.15` → `3 failed`, each on `StepDefinitionNotFoundError` (the When "the user publishes the process as agent into a directory" and its two siblings). With the When and Then written in `tests/test_publish_what_the_shop_knows.py` and `src/` untouched, the process-as-agent row red on the Then "the agent is rejected because it is not made from a process, naming the type process" (`_rejected_for_its_type`: `assert [] == ['process/restock-a-shelf: an agent is made from a role; this one is a process']`, stderr empty since the render exited 0 and wrote its file). With the agent renderer taking the check, the role-as-skill and role-as-diagram rows red on the same Then (`assert [] == ['role/stock-keeper: a skill is made from a process; this one is a role']`, and `a diagram`); the skill renderer took the check and its row went green, then the diagram's. "nothing is written to the directory" is slice 18's Then, reused; its body asserts the `target` directory is empty.
  Where the check lives: `renderers/source.py`, `refusal(artifact, kind, made_from)`: the read's own faults first, then one fault if kb's `ReadResponse.type` is not the type the kind is made from; no field of the content is read. `agent`, `skill` and `diagram` each call it once on the artifact published, naming the type they are made from, before anything is laid out; the skill renderer's reads of the shared steps are not checked. `markdown` takes no check. `cli._render` refuses the `Rendered` through `_answered`, as for the harness limits. CLAUDE.md's `renderers/source.py` row now says so.
  Fault: on the artifact published from, no path, rule `renderer-type`, worded like the harness limits' faults, what the kind takes and then what this one is: `process/restock-a-shelf: an agent is made from a role; this one is a process`.
  Probes (`.superpowers/batch11/probe-t3/`, Review Focus 5): `render markdown tag/pricing` → `written: [pricing.md]`, exit 0; `render markdown schema/decision` → `written: [decision.md]`, exit 0; `render agent role/nobody` → `role/nobody: the store holds nothing by the name 'role/nobody'`, exit 1, kb's read fault, not the type check; `render agent|skill|diagram tag/pricing` → `tag/pricing: an agent is made from a role; this one is a tag` (and `a skill`/`a diagram` ... `a process`), exit 1, nothing written.
  Checks: `-m slice-50.15` → `3 passed`; `-m "slice-17 or slice-18 or slice-19 or slice-50 or slice-50.7"` → `5 passed`. Size check lists nothing (`tests/test_publish_what_the_shop_knows.py` 224 lines). `git diff --stat -- features src/shop_knowledge/types` empty.
  Suite: `.venv/bin/python -m pytest -q` → `7 failed, 80 passed`, the seven of slices 50.17 to 50.22.
  Surprised by: nothing. Open questions: none. Next: slice 50.16.
- 2026-09-27 The final review of batch 11's routed cases: nine cases a stated spec principle already answers (adrs/0044), each reproduced and logged for formulation and slicing, not coded now.
  Markdown gaps (adrs/0043, 0045; finding 2), each reproduced with `KB_ACTOR=a` in a scratch store (`.superpowers/batch11/repro/`) through `create` then `render markdown`: a title ending in a space (a `role` titled `"Stock keeper "`) renders the heading `# Stock keeper ` (`markdown.py`); a section title ending in a space (a `decision` whose third section is titled `"How it works "`) renders `## How it works ` (`sections.py`); a nested list whose last item is empty (a `work-item` with `topics: [["x", null]]`) renders the bullet `  - x; `; a mixed list holding a mapping whose last value is empty (`topics: ["a", {b: 1, c: null}]`) renders `  - b: 1, c: `; a list of mappings inside a field group whose last value is empty (`extra: {items: [{a: null}]}`) renders `    - a: `; a `|` in a mapping key, a column header (`topics: [{"a|b": 1, name: x}]`) renders the header row `| a|b | name |` over the separator row `| --- | --- |`, three cells over two columns, since header cells go through no cell escaping (deciding whether the escape belongs in `_row` goes with that scenario). Common root: `_inline` ends in a space whenever its last part is empty; headings and header cells pass through no cell or line handling. Dropped from the ledger this carried: "a section body line ending in a space before its last" is unreachable, since kb refuses to store such prose at all (next).
  The NotCanonical traceback (pre-existing; finding 3): `create`, `write` and `append` show a Python traceback, not a refusal, for multi-line prose whose first line ends in a space. Reproduced again here, `KB_ACTOR=a` in the same scratch store: a `decision` whose `sections[0].body` is `"a \nb\n"` reads fine (`cli._document`'s `loads` accepts it) and passes its shape; `kb_requests.create_request` (kb_requests.py:20; the same at :24 for `write_request`, :28 for `append_request`) then calls `dumps(content)` outside `_document`'s guard, and `kb.content.dumps` raises `kb.canonical.NotCanonical` ("every piece of prose is written as a block, and this prose could not be written back as one; its line 1 ends in a space") uncaught: a full Python traceback on stderr, exit 1, no fault printed. Breaks rule 4 and "shop-knol never shows a traceback"; a spec principle (prose a user gives is checked the one place a file is read and checked, before it can reach a call kb never returns from) answers it, so it is routed to formulation, not fixed this wave.
  Also routed under adrs/0044 (finding 6, not a markdown gap): a scenario holding that checking where no knowledge base can be found shows no answer (finding 1's case, fixed in code this wave; its scenario is still to be written); and that slice 50.13's scenario pins `sound: false`, a Then line change to an approved scenario, answered by adrs/0046.
  Also corrected here, in place: slice 50.14's checkpoint above overstated what its scenarios hold (finding 2), and gave the wrong reason for doubling a backslash before a separator (finding 5); `_cell_count`'s docstring (`tests/markdown_well_formed.py`) is corrected the same way. adrs/0046 is corrected to supersede the last three sentences of 0029, not two (finding 4).
  Suite (with finding 1's fix to `cli._validate` and `answers.checked` also in): `.venv/bin/python -m pytest -q` → `7 failed, 80 passed`, the seven still of slices 50.17 to 50.22. Size check lists nothing. `git diff --stat -- features` empty.
- 2026-09-27 Final whole-branch review of batch 11 (slices 50.13-50.15), on Fable 5.1 over `3153e74..de374a2`. The reviewer ran the suite (`80 passed, 7 failed`, the seven being slices 50.17 to 50.22's) and probed every renderer against every type. Verdict: ready to merge with fixes. The fixes landed in 0c7d199 and a scoped re-review found every finding addressed:
  - a check that never ran printed an answer, a regression from slice 50.13, now fixed;
  - the principle-answered markdown gaps and a pre-existing traceback for prose with a line ending in a space were logged above for formulation;
  - adrs/0046 now supersedes the last three sentences of 0029;
  - the 50.14 checkpoint's backslash rationale was corrected.

  Ruling: the regression is fixed without a scenario of its own, since it restores the pre-batch behaviour. Its scenario is routed to formulation. Until it lands, the fix is held only by probes.
  Deferred to slice 50.16's review, as the final review triaged: `_not_a_fault`'s prefix match; `_a_failing_checks_answer`'s docstring; `_every_value_shown` repeating `_a_page_of`; `_after_the_colon`'s name; the type-refusal Then's recomputed wording; `renderers/source.py`'s module docstring.
  Declined as out of scope: trailing spaces in the agent's body; the skill not type-checking the steps a process uses; markdown syntax inside field names; `validate` taking no `--json`. To check the escape, the reviewer rendered a synthetic table through GitHub's markdown API (`gh api markdown`); no project content was sent.
  Next: push. Then slice 50.16, the seventh architecture review, before 50.17 to 50.21 and the routed cases are formulated and planned.
- 2026-09-27 Slice 50.16, seventh architecture review (Opus), report kept at `.superpowers/batch12/arch-review-50.16.md` and summarised here. Suite `80 passed, 7 failed` (the seven slices 50.17 to 50.22's); size check clean. Every CLAUDE.md rule and module-map row met in full, but for: `tests/markdown_well_formed.py` importing from its sibling step module (adrs/0035); `_defines_nothing` reading `kb/schema` where `list --type schema --ids` now shows it (CLAUDE.md Step definitions); the batch 10 and 11 deferred minors. Refactors called for: R1 (markdown pages in one module with no step), R2 (the batch 11 minors), R3 (the steps observe through shop-knol and name kb's storage in one place), R4 (no Then relies on kb's fault order). Not called for, with reasons: `preexec_fn`'s thread-safety (no threads or workers); `cli._init`'s root on `connect` (the bootstrap Creates go to it; kb's Init ignores it). Coupling to kb beyond its contract: eighteen points, nine in `src/` and nine in `tests/`, eleven of which would break if kb changed behind its contract: `kb.content` and `kb.canonical.NotCanonical` in `src/`; content kb cannot keep refused outside `cli._document` (already a traceback, slice 50.18.1); `kb.content` and `kb.canonical` in the steps; hand-edits of stored files; `kb/store.yaml` and `kb/schema` observed; every byte under `kb/` compared; `kb.journal.now` replaced; kb's fault wording spelled; kb's fault order relied on. Three open questions, answered by the user on 2026-09-27: kb publishes `kb.content`, with `NotCanonical`, as part of its versioned contract; shop-knowledge knows nothing of kb's internals in any code, tests included, a stand-in for kb at the contract boundary giving the states the contract cannot produce, and no test ever reaching live data; kb's fault `rule` names are contract and its wording is not, the shop checking that what it prints is kb's (adrs/0047, kb adrs/0018; both specs amended in e23a0c3 and kb 00710a6).
- 2026-09-27 Re-slice after slice 50.16. R3 becomes 50.16.1 under adrs/0047, widened from confining kb's storage to removing it: a stand-in for kb at the contract boundary replaces every hand-edit, `kb.canonical`, the clock patch, the byte snapshot and the storage names. The test isolation the user asked for is 50.16.2. R4 is 50.16.3; the fault wording (question 3) is 50.16.4, with the unknown; R1 is 50.16.5; R2 is 50.16.6. They run first, the stand-in's unknown the largest, and the eighth review (50.16.7) follows the six. The routed scenarios of b0b535f are 50.18.1 (prose kb cannot keep, its unknown), 50.18.2 (markdown's six rows; the outline moves to `@slice-50.18.2`, its first four rows credited to 50.14) and 50.18.3 (the check with no store). 50.23 swaps `NotCanonical`'s import for kb's published one once kb's slice 100 is released and pinned. The batch 11 final review's note that 50.13's scenario should pin `sound: false` is dropped: the formulator found its Thens already say the shop is unsound through "the command reports failure to whatever ran it", as the feature does throughout.
- 2026-09-27 KB REQUEST: kb slice 99 (a call from a removed working directory) is green in kb at e1ce2cf, reviewed clean; with kb slices 100 (publishing `kb.content`'s `NotCanonical`) and 101 (kb's own test isolation), it waits for a kb release, the user's decision (adrs/0006).
- 2026-09-27 Plan batch 12: slices 50.16.1 to 50.16.6, `docs/superpowers/plans/2026-09-27-shop-knowledge-batch12-implementation.md`. Next: execute it; then the eighth review (50.16.7); then the capability slices; 50.22 and 50.23 wait for kb's release.
- 2026-09-27 slice 50.16.1 green (enabling). A reader now finds no step touching a knowledge base's files or any kb module kb does not publish.
  Stand-in: `tests/stand_in/sitecustomize.py`, put on shop-knol's `PYTHONPATH` by `driver.answering(env, tmp_path, *answers)` alone, which writes the answers to a YAML file named by `KB_STAND_IN`. Loaded, it replaces `kb.client.connect` with a client wrapping the real one: a call an answer describes (`call`, optional `asking` request fields) is answered with the `kb_pb2` response the step wrote (`answer`), plus any repeated fields taken from the real kb's answer (`from_kb`); every other call reaches the real client unchanged. It imports `kb.client`, `kb.content`, `kb.contract` (and protobuf's `json_format`). Nothing under `src/` changed.
  Moved to it: the read-back Given (a `ReadResponse` fault for the decision) and the check's three Givens (a `ValidateResponse`'s violations, with `stale` from the real check), each recording what it can through shop-knol first; their faults are the steps' own words and their Thens compare with what the stand-in gave. `kb.canonical` is gone from `tests/`. The start steps observe through shop-knol (`list --type schema --ids`; a `journal` run from the directory with no `KB_ROOT` finds a history); `_holds_none` and the directory listings name `kb/` through `driver.store_in`, the Init row's name, commented. The publish "unchanged" Then compares `journal` and the process's and shared step's whole reads before and after. `test_make_several_changes_at_once.py` imports `connect` from `kb.client`. CLAUDE.md's rule 1 and Step definitions say what adrs/0047 says.
  Throwaway red: the read-back stand-in answering a different fault turned `-m slice-1.27` red on the Then (`a throwaway different fault` against the step's words); reverted, `1 passed`.
  Review Focus 1: with the stand-in on every shop-knol's `PYTHONPATH` (throwaway `env` fixture) and told nothing, the suite gave `21 failed, 80 passed`, the same 21; reverted.
  Checks: `-m slice-1.27` 1 passed; the check markers 7 passed; the start and publish markers 9 passed (each as before). The greps give nothing, `kb.journal` only in `tests/clock/sitecustomize.py`, no `/ "kb" /`, kb imports only `kb.client`, `kb.content`, `kb.contract`; `git diff --stat -- features src` empty; size check lists nothing.
  Suite: `.venv/bin/python -m pytest -q` -> `21 failed, 80 passed`, `failing-before.txt` unchanged.
  Surprised by: nothing. Open questions: the stand-in and the clock are both `sitecustomize` modules, so one process can load only the first on its path; no scenario needs both before 50.23 replaces the clock. Next: slice 50.16.2.
- 2026-09-27 Slice 50.16.2 green (enabling). No test reaches a knowledge base outside its own temporary directory.
  Driver: `tests/driver.py`'s `knol` takes its working directory from `cwd`, or, with none given, from module-level `_default_cwd`; with neither set it refuses (`RuntimeError`). `tests/conftest.py`'s autouse `_working_directory` fixture sets `_default_cwd` to the test's own `tmp_path` for every test, so every shop-knol run the driver makes, named or not, stays inside it; no call site elsewhere changed. The read-back `workdir` fixture's default is now `tmp_path` (was `None`, "where the suite runs"); the six Givens that move the user still return their own directory, so no scenario's meaning changed.
  Guard: `tests/conftest.py`'s `pytest_configure` now calls `_refuse_near_a_real_store` before collecting anything: from the checkout (`config.rootpath`) and from the system's temporary directory (`tempfile.gettempdir()`), it asks kb's own `connect().Journal(...)`, with the shell's own `KB_ROOT` set aside for the call and restored after, whether a store is found upward; an answer carrying no faults means one was, and the suite refuses to run (`pytest.UsageError`), naming where. Only `kb.client.connect` and `kb.contract.kb_pb2` are used; no file under a store is opened.
  Controller's ruling, three more guards: (a) `driver.at` and `driver.answering` each refuse when the other's directory is already on the environment's PYTHONPATH (`_refuse_if_combined`), since both are `sitecustomize` modules and a process loads only the first, until 50.23 removes the clock's; (b) demonstrated, not a code change: the publish feature's "the shop's knowledge base is unchanged" Then can go red; (c) `driver.answering` refuses a second call in one scenario, which would silently replace the first call's answers.
  Throwaway demonstrations, logged then reverted:
  - a `kb/store.yaml` written at `/home/vscode/kb` (the checkout's parent) made the suite refuse before running any test (`pytest -q` -> exit 4, "a knowledge base is reachable above /home/vscode/shopsystem-knowledge; refusing to run near one"), and stopped `tests/test_check_the_shops_knowledge_is_sound.py` (a stand-in scenario) the same way; the store removed, the suite ran as before (Review Focus 2).
  - a bare call of `driver.knol` with no `cwd` and no default set (outside pytest) raised `RuntimeError: shop-knol was run with no working directory, and the suite set no default`.
  - a throwaway store started at `.superpowers/batch12/devstore`, the developer's own shell `KB_ROOT` naming it: `pytest -q` (that `KB_ROOT` exported) gave `21 failed, 80 passed`, the same as without it, and kb's own `connect(root).Journal(...)` showed the same 9 entries before and after; the store removed (Review Focus 3).
  - `driver.at` then `driver.answering` on the same environment, and the reverse order, each raised `RuntimeError` naming the sitecustomize already on the path.
  - a second `driver.answering` call for one `tmp_path` raised `RuntimeError: driver.answering was already called for this scenario; it does not replace answers`.
  - `record(...)` inserted in `_unchanged` (`tests/test_publish_what_the_shop_knows.py`) between reading `before` and the assertion turned `test_the_user_publishes_a_process_as_a_skill` red (`AssertionError`); reverted, `1 passed`, `git diff` on the file empty.
  Checks: size check clean; `git diff --stat -- features src` empty.
  Suite: `.venv/bin/python -m pytest -q` -> `21 failed, 80 passed`, `failing-before.txt` unchanged.
  Surprised by: the controller's three extra guards, beyond the brief's check line; each demonstrated above. Next: slice 50.16.3.
- 2026-09-27 Slice 50.16.3 green (enabling). A reader finds no Then that fails if kb returns the same faults in another order.
  Reshaped, each holding its lines to a set rather than a position: `tests/test_check_the_shops_knowledge_is_sound.py`'s `_unreadable_listed` (membership, not `splitlines()[0]`), `_the_rest_listed` (the two lines as a set, not `splitlines()[1:]`), `_both_listed` (the two lines as a set, not `lines[0]`/`lines[1]`) and `_the_fault_listed` (a one-element list compared whole, dropping `lines[0]` so the R4 grep finds nothing); `tests/test_make_several_changes_at_once.py`'s `_every_fault` (the `(at, field)` pairs as a set, not a positional list).
  Throwaway reversal: `cli._refuse`'s loop over `reversed(list(faults))` turned `test_the_user_checks_a_knowledge_base_with_faults`, `test_the_user_checks_a_knowledge_base_holding_a_file_the_shop_cannot_read` and `test_one_bad_change_in_a_batch_leaves_the_shop_untouched` red before the reshape (confirmed, all three), green after (confirmed, all three; the rest of both files' other failures were the baseline's own, unchanged); reverted, `git diff --stat -- src` empty.
  Checks: the R4 grep on `tests/test_check_the_shops_knowledge_is_sound.py` gives nothing; size check clean (158 and 88 lines); `git diff --stat -- features src` empty.
  Suite: `.venv/bin/python -m pytest -q` -> `21 failed, 80 passed`, `failing-before-t3.txt` and `failing-after-t3.txt` identical to `failing-before.txt`.
  Surprised by: the R4 grep still matched `_the_fault_listed`'s `lines[0]`, a single-fault Then with no ordering question; reshaped anyway to satisfy the check literally. Next: slice 50.16.4.
- 2026-09-27 Slice 50.16.4 green (enabling). A reader finds kb free to reword its faults without a shop scenario going red: no step spells kb's wording.
  Unknown answered: yes. Every Then that read kb's words gets them from kb itself for the same state, through `tests/driver.py`'s `kb_answer(env, call, request, cwd=None)`: kb's published `connect()` asked in-process, from the directory shop-knol ran in with the scenario's `KB_ROOT` (or none), the suite's own directory and environment restored after; asked after shop-knol's own call was refused, so a refused call changes nothing. `driver.printed(fault)` is the shop's one-line form (artifact, ` at ` place, `: `, kb's message, lines joined); `driver.actor(env)` is KB_ACTOR as a `kb_pb2.Actor`; `NO_STORE` moved from conftest to driver, and conftest's guard now asks through `kb_answer`.
  Each Then and its source of truth: read-back's three store Thens (`read_back_from_elsewhere.py`, one `_refused_as_kb_refuses`) -> kb's `Read` of the decision from `workdir` with the Given's `KB_ROOT`, rule `store` asserted, stderr exactly that one line; record's "does not fit" and "which artifact and which place" (moved with their Givens to `tests/record_refused_files.py`, star-imported by the record module alone, which had passed 250 lines) -> kb's `Create` of the same file, message and actor, the artifact `decision/prices-are-reviewed-monthly` and place `sections` asserted as the spec's; record's "named once and only once" -> the refusal `kb.content.loads` raises (a `ValueError`) for the same text, the file and place `sections/0/body` the step's own; start's "already holds" and "inside" -> kb's `Init` of the same `start_in`, rule `root` asserted; retire's two Thens -> kb's `Delete` of `tag/pricing` with the When's message, rule `on_delete` asserted, the one pointer `decision/prices-are-reviewed-monthly` named. Record's no-role and no-message Thens and start's `_NO_ROLE` are shop-knol's own words (`cli._NO_ROLE`, `_NO_MESSAGE`), left as they are.
  Review Focus 4: the stand-in's faults are compared only with what the stand-in gave: the check feature's `_line` (now `printed(kb_pb2.Fault(**fault))`) over `UNREADABLE`, `NO_BODY`, `DANGLING` and `_without_its_rationale`, and read-back's unreadable Then over its `UNREADABLE`, each message the step's own words; no Then compares a stand-in fault with kb's words.
  Throwaway rewording in `.venv` (kb v0.2.1's installed files): the eight messages behind these Thens prefixed or reworded (`store.py` five, `refusals.py`'s `still_linked`, `validation.py`'s sections, `canonical.py`'s named-once). The five features: old Thens (stashed) 18 failed, the 8 extra being every Then named above; reshaped 10 failed, the baseline's own; the whole suite `21 failed, 80 passed`, the same 21. Repeated for the record module after the move. Restored: `make dev` alone leaves an installed kb in place, so `pip uninstall -y shopsystem-kb` then `make dev` reinstalled the pinned tag; the four files' md5s match the originals; the clean suite `21 failed, 80 passed`.
  Checks: `git diff --stat -- features src` empty; size check lists nothing (record module 201, `record_refused_files.py` 80); a grep of the tests for kb's message fragments finds only feature step text.
  Suite: `.venv/bin/python -m pytest -q` -> `21 failed, 80 passed`, `failing-after-t4.txt` identical to `failing-before-t4.txt` and `failing-before.txt`.
  Surprised by: `make dev` does not restore an edited installed kb by itself. Open questions: the named-once Then spells the place `sections/0/body` itself, since kb v0.2.1 publishes no `NotCanonical` to read its `path` from (slice 50.23). Next: slice 50.16.5.
- 2026-09-27 Slice 50.16.5 green (enabling). A reader finds the expected markdown pages built in one place, with no step module importing another (adrs/0035).
  New helper module `tests/markdown_pages.py` (74 lines, no step, imported plainly as `driver.py` is): holds `_write_over`, `_role_page`, `_row`, `_STEP_ROWS`, `_process_page`, `_step_holding` (moved from `publish_as_markdown.py`, unchanged but for `_step_holding`), plus one page reader, `pages(target)`, the dict `_a_page_of` and `_every_value_shown` (`markdown_well_formed.py`) both now assert with instead of each spelling out `target.iterdir()` its own way. `markdown_well_formed.py` no longer imports from its sibling `publish_as_markdown`; both import `markdown_pages` plainly. `_steps_as_a_table` (`publish_as_markdown.py`) now compares `pages(target)` with `_process_page([], {})` rather than a spelled-out table. `_step_holding` raises `ValueError` for an id no step holds, rather than passing `steps` through unchanged. CLAUDE.md's Step definitions section gained a bullet naming this pattern (a helper more than one step module needs, imported plainly, not star-imported).
  Throwaway: `_step_holding(steps, "no-such-step", x=1)` against `[{"id": "a"}, {"id": "b"}]` raised `ValueError: no step holds the id 'no-such-step'` (logged here, not kept as a test).
  Checks: `grep -n "from publish_as_markdown" tests/*.py` -> one line, `test_publish_what_the_shop_knows.py`'s own `from publish_as_markdown import *`, the feature's test module star-importing its sibling step module as adrs/0035 requires; no sibling step module imports another. `grep -c "@given\|@when\|@then" tests/markdown_pages.py` -> `0`. `grep -c '"| check-it' tests/publish_as_markdown.py` -> `0`. Size check lists nothing (`markdown_pages.py` 74, `publish_as_markdown.py` 157, `markdown_well_formed.py` 104). `git diff --stat -- features src` empty. `-m "slice-20 or slice-50.6 or slice-50.11 or slice-50.14 or slice-50.18.2"` -> `6 failed, 13 passed`, the six being 50.18.2's own, unchanged from before the move.
  Suite: `.venv/bin/python -m pytest -q` -> `21 failed, 80 passed`; `failing-after-t5.txt` identical to `failing-before-t5.txt`.
  Surprised by: nothing. Next: slice 50.16.6.
- 2026-09-27 Slice 50.16.6 green (enabling). A reader finds the batch 11 minors gone.
  All six were still present, none already met by Tasks 1-4's reshapes: `_not_a_fault` (`test_check_the_shops_knowledge_is_sound.py`) now matches the artifact a fault line names exactly, through a new `_artifact_named` (before ` at ` or `:`, whichever comes first), so `decision/…-weekly-2` no longer passes a Then checking `…-weekly` is absent. `_a_failing_checks_answer` (`conftest.py`) gained a docstring. `markdown._after_the_colon` renamed `_after_the_mark`, both call sites and its own def, docstring unchanged (already said "a colon or a bullet's dash"). The type-refusal Then (`test_publish_what_the_shop_knows.py`) now compares with a module-level `_REFUSAL` dict, one literal line per outline row (agent/role/process, skill/process/role, diagram/process/role), spelled in `renderers.source.refusal`'s own words; `_MADE_FROM` and `_a` (a copy of `source._a`) are gone from the file. `renderers/source.py`'s module docstring now says `refusal` decides what stops a render (the read's own faults, then the type), replacing "whether its faults refuse the render is the renderer's to say". `_role_page`'s docstring (`tests/markdown_pages.py`) now says plainly what `extra` is: the lines a Given's own field adds or changes.
  Checks: all six R2 greps give nothing (logged individually); `-m "slice-50.13 or slice-50.14 or slice-50.15 or slice-50.18.2"` -> `6 failed, 14 passed`, the six being 50.18.2's own, unchanged. Size check lists nothing. `git diff --stat -- src` touches only `renderers/markdown.py` (6 lines) and `renderers/source.py` (4 lines), as the brief requires.
  Suite: `.venv/bin/python -m pytest -q` -> `21 failed, 80 passed`; `failing-after-t6.txt` identical to `failing-after-t5.txt`.
  Surprised by: nothing. Next: push, then slice 50.16.7, the eighth architecture review.
- 2026-09-27 Batch 12 final review fixes. Findings and rulings from `.superpowers/sdd/2026-09-27-shop-knowledge-batch12-implementation/final-findings.md`, all fixed:
  1. IMPORTANT: `tests/conftest.py`'s scenario `env` fixture copied the whole developer shell (`_shells_own_environment`), stripping only two names; a shell `GIT_DIR` had made a scenario commit its knowledge base into the reviewer's own scratch repository, the suite passing throughout. Replaced with `_allowlisted(home)`: PATH, LANG and LC_* alone, taken from the shell if set there, plus HOME pointed at a directory under the scenario's own `tmp_path` - never the developer's; KB_ROOT and KB_ACTOR still set by the fixture as before. `tests/driver.py`'s `kb_answer` now runs its in-process call under exactly the `env` it is given (`os.environ` cleared and replaced, restored after) rather than merging just `KB_ROOT` into the ambient shell; `conftest.py`'s session guard (`_refuse_near_a_real_store`) builds its own allowlisted `env`, a throwaway HOME of its own (`tempfile.TemporaryDirectory`), and passes it to `_reachable_from`/`kb_answer` instead of asking with the ambient shell answer. CLAUDE.md's Step definitions section gained bullets naming these: every shop-knol run inside the test's own temporary directory, the session guard, the environment built from an allowlist, no Then relying on fault order, and Thens comparing with `driver.kb_answer` or the stand-in's own answer, never kb's spelled wording.
     Demonstrated, then removed: a throwaway git repository at `.superpowers/batch12/scratch-repo` (one empty commit, `97cedf7`), a throwaway `sitecustomize.py` under `.superpowers/batch12/` that marks a file if imported, and `GIT_DIR` pointing at the scratch repo's `.git`, all exported in one shell, then `.venv/bin/python -m pytest -q` run in it: `21 failed, 80 passed`, unchanged, and the scratch repo still held its one original commit after - the suite's own subprocesses and the guard's in-process call never saw `GIT_DIR` or that `PYTHONPATH`, by construction (`_allowlisted` copies neither; `subprocess.run(env=env)` and the rebuilt `kb_answer` replace the environment wholesale, never merge it). The outer pytest process itself, started with that shell's `PYTHONPATH` already set, did load the throwaway `sitecustomize.py` at its own interpreter boot (Python's `site` machinery, not code under `tests/` or `src/`) - orthogonal to the fix, which governs what a scenario's own subprocess and the guard's own call are given, not the harness process the suite runs under. Repo and sitecustomize removed after.
  2. MINOR: `tests/test_check_the_shops_knowledge_is_sound.py`'s `_checked_as` had the stand-in replace the whole `violations` list; its `from_kb` now names `violations` alongside `stale`, so the real check's own findings for the same call are kept beside the stand-in's.
  3. MINOR: `tests/stand_in/sitecustomize.py`'s `answered` asked a matching description first, only falling back to the real kb when nothing matched; it now asks the real kb first and returns its answer unchanged whenever that answer carries faults (a refusal, such as no store found), answering from a description only when the real kb's own answer carries none.
  4. MINOR: CLAUDE.md's Step definitions section now states the rules slices 50.16.2-50.16.4 hold, alongside this batch's allowlist (see finding 1's entry above).
  5. MINOR: the slice plan's slice 50.23 check line now greps `^\s*(from kb[a-z_.]* import|import kb[a-z_.]*)`, catching an indented import the old flush-left pattern would miss; run today it still finds only `kb.client`, `kb.content` and `kb.contract`, the two standing exceptions (`kb.canonical` in `cli.py`, `kb.journal` in `tests/clock/sitecustomize.py`) unchanged.
  Suite: `failing-before-final.txt` and `failing-after-final.txt` (`.superpowers/batch12/`) both `21 failed, 80 passed`, identical lists.
  Next: push.
- 2026-09-27 Whole-branch review of batch 12 (Fable 5.1, `feeef37..ce1dec0`): suite `80 passed, 21 failed`, the same 21; kb imports only `kb.client`, `kb.content`, `kb.contract` (and `kb.canonical` in `cli.py` until 50.23); `kb.journal` only in `tests/clock`; no step names kb's storage or spells its wording (51 message fragments searched); the stand-in transparent when told nothing (loaded into 486 processes, the same 21); the installed kb identical to v0.2.1. Ready with one fix, landed in 9091103 and re-reviewed clean: scenarios inherited the developer's whole shell, and a shell `GIT_DIR` made a scenario commit its knowledge base into that repository while the suite passed; the scenario environment is now an allowlist with `HOME` inside `tmp_path`. Folded in: the stand-in keeps kb's real violations and returns the real answer when it carries faults; CLAUDE.md states the 50.16.2-4 rules; 50.23's import grep catches indented imports. The same leak lives in kb itself (its git calls inherit `GIT_*`), logged there as a request and fixed as kb's slice 102.6.1. Routed: `kb_answer` cannot reproduce a removed working directory (50.18, 50.22); "naming the file" Thens now name the artifact (adrs/0047; formulation if the wording should say so). Deferred: the stand-in's `_response` keeps two unused parameters; `_asks`' exact-match docstring; protobuf used directly but undeclared in `pyproject.toml`; cosmetic step tidies.
  Next: slice 50.16.7, the eighth architecture review, before batch 13.

