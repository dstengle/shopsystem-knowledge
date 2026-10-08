# shop-knowledge

## Purpose

shop-knowledge is the only interface a shopsystem user or agent uses to the shop's knowledge base. Its command line is `shop-knol`. It is a client of kb (repository `shopsystem-kb`). It owns everything the shop knows that kb does not: the shop's artifact types, the seed content, the renderers and the command line. kb never learns a domain type.

Unless a capability says otherwise, "the user" means a shopsystem user or agent working at the command line.

## Constraints carried

Each promise below holds for every command. Its scenarios sit in the capability where it shows.

- **kb only through its contract.** kb is reached only through its published contract, pinned by version. Today the pin is kb v0.6.0, which publishes contract v1. In v1 every rpc was renamed or reshaped. shop-knol uses the calls Create, Replace, Add, Remove, BatchCreate, BatchReplace, Read, List, Follow, Search, History, Snapshot and Check. In its own process it also uses `kb.init`, which refuses by raising `kb.NotStarted`. shop-knowledge's rule that it knows kb only through what kb publishes names `kb.init` and `kb.NotStarted`. shop-knowledge never touches kb's files or git. A change it needs from kb is a request to bump the pin.
- **One behaviour, wherever the store is.** shop-knol calls kb through kb's client, which reaches the store in-process or through a server hosting it, whichever kb's search finds. shop-knol does nothing different between the two. Tested in find-the-knowledge-base.
- **Files are YAML 1.2, read the way kb reads content.** This covers every file shop-knol reads or writes, on `create`, `write`, `append`, `apply`, and in its own output. A title that looks like a date or a yes is still text when it reaches kb. A file kb would not read is refused the way kb refuses it, naming the place: a tag, an anchor, a directive, a second document, or a duplicate key. Tested in record-an-artifact.
- **Answers are YAML, with JSON where a command offers it.** JSON is the same structure. Today only `read` offers it. Tested in read-an-artifact.
- **No traceback.** shop-knol never shows a traceback. Every refusal, kb's or shop-knol's own, reports failure to whatever ran the command. Tested wherever a refusal is.
- **kb's refusals are passed through.** They are printed as kb returned them, naming the artifact, the place in it, and what is wrong. Tested in record-an-artifact and check-the-knowledge-base.
- **shop-knol's own refusals are in plain words.** Each says what was refused and names the place it concerns: the file, the directory or the artifact. A name given empty names no place and is refused. Tested in start-a-knowledge-base, record-an-artifact, read-an-artifact, publish-an-artifact and publish-a-shops-spec.
- **Every change says who and why.** Every mutating command requires an actor and a message. `init` requires an actor and no message. Tested in record-an-artifact and start-a-knowledge-base.
- **kb mints the ids.** Ids are minted by kb from titles and never supplied by the user. Tested in record-an-artifact.
- **Publishing only reads.** Publishing reads the knowledge base and never changes it. Files are written, and files published earlier deleted, only when the renderer refused nothing. Tested in publish-an-artifact and publish-a-shops-spec.
- **Corpus-only roles.** The boundary for a corpus-only role is a harness permission allowlist of exactly `shop-knol *`. The harness provides it; shop-knowledge does not implement it.
- **Bounds:**
  - `--resolve` with no depth means depth 1.
  - `refs` with no `--depth` follows one step.
  - An agent's harness `name` may not contain `:` and may not start with `-`.
  - A gist or a statement is at most 200 characters, and a part's title at most 80; neither holds a line break. Tested in use-the-shops-types.

### Mechanisms every command shares (may change)

- Answers are printed on stdout as YAML 1.2, written through `kb.content`. JSON is the same document written by the standard library's `json`.
- Refusals are printed on stderr, one line per fault, with exit 1.
- A fault carries `artifact`, `place` (its parts joined with `/`), `rule` and `message`, and is printed as `artifact at place: rule: message`. A message over several lines is joined into one line. A fault with no artifact is printed without `artifact at place: `, and one with no rule without `rule: `.
- An operating-system error on a path is a fault: its artifact is the path the error names (empty if it names none), and its message is the operating system's reason.
- An argument shop-knol cannot take is refused as one fault: the command as argparse names it (`shop-knol list`), then argparse's message. No usage block is printed. `-h` is help on stdout, with exit 0.
- Every file the user gives is read as YAML 1.2 through `kb.content`. Text kb cannot keep is refused by `kb.content`'s own refusal, `NotCanonical`. A file that is not UTF-8 is a fault with rule `content` and message `it is not text that can be read: <reason>`.
- A file the user gives is checked against its shape, written as JSON Schema. Each violation is one fault: `artifact` is the file as named, `place` is its parts joined with `/`, `rule` is the JSON Schema keyword, and `message` is jsonschema's.
- Each command maps to one contract v1 call, named in its capability, except `coverage`, `dependencies` and `render spec`, which read through Read, List and Follow, and `validate`, which makes Check and then reads through List and Read. Every kb response is a result or a refusal, never both.
- Every change sends kb one signature: the role, the piece of work and the message.
- A place inside an artifact, the part of a locator after `#`, is sent as kb's `place`.
- An answer keeps shop-knol's own keys whatever kb names them: it says `type` where kb's v1 says `kind`.

## Composition (reading order)

1. [start-a-knowledge-base](capabilities/start-a-knowledge-base.md): set up a knowledge base holding the shop's types.
2. [find-the-knowledge-base](capabilities/find-the-knowledge-base.md): have every other command find the one knowledge base it works on.
3. [use-the-shops-types](capabilities/use-the-shops-types.md): see and read the shop's ten types, and record things that use them, a shop's spec and its capabilities' lifecycle among them.
4. [record-an-artifact](capabilities/record-an-artifact.md): record something new under a name the shop mints.
5. [read-an-artifact](capabilities/read-an-artifact.md): read one artifact at a chosen level.
6. [revise-an-artifact](capabilities/revise-an-artifact.md): replace an artifact, or one section of it.
7. [add-a-step-to-a-process](capabilities/add-a-step-to-a-process.md): add a step, written in place or shared.
8. [retire-an-artifact](capabilities/retire-an-artifact.md): take out something nothing depends on.
9. [make-several-changes-at-once](capabilities/make-several-changes-at-once.md): apply a batch of creates, or of replacements, that lands whole or not at all.
10. [list-what-the-shop-holds](capabilities/list-what-the-shop-holds.md): see everything of one kind.
11. [follow-the-links](capabilities/follow-the-links.md): see what an artifact points at and what points at it, who depends on a capability among it.
12. [search-what-the-shop-knows](capabilities/search-what-the-shop-knows.md): find knowledge by its words.
13. [review-who-changed-what](capabilities/review-who-changed-what.md): read the history.
14. [record-what-a-piece-of-work-read](capabilities/record-what-a-piece-of-work-read.md): anchor a piece of work to the versions it read.
15. [check-the-knowledge-base](capabilities/check-the-knowledge-base.md): learn whether the shop's knowledge is sound and what is behind its type.
16. [publish-an-artifact](capabilities/publish-an-artifact.md): publish an artifact into files as a skill, an agent, a diagram or a markdown page.
17. [publish-a-shops-spec](capabilities/publish-a-shops-spec.md): publish a shop's whole spec, ledger, decision records and feature files into its repository, deleting what it published earlier that nothing stands behind now.
18. [see-what-is-formulated](capabilities/see-what-is-formulated.md): see which of a shop's Behaviour lines no scenario, or more than one, formulates.
19. [see-what-a-shop-depends-on](capabilities/see-what-a-shop-depends-on.md): see which of a shop's capabilities depend on a deprecated or retired capability, in any shop.

## Order of building

shop-knowledge and kb were one effort until the walking skeleton was green, and two after that.

1. Feature files for both were formulated in one session from both specs. This repository's scenarios are the outer loop; every kb scenario cites the scenario here that needs it.
2. Slice 1 was "create a decision and read it back through `shop-knol`". It could touch both repositories, and kb was an editable path dependency until it was green.
3. Once slice 1 was green, kb was tagged and pinned here. From then on, a kb change needed here is a request to bump the pin, and each repository plans alone. kb v0.6.0 is pinned today.

## Testing

- Built with the shopsystem-bdd workflow. Feature files are formulated from this spec, from the perspective of a shopsystem user at the command line.
- kb is exercised through its in-process transport. Where a scenario says the shop works with a server, the server comes from a served-store double kb publishes for its clients' tests; shop-knowledge's tests never start a kb server or write a connection to one themselves. Until kb publishes it, those scenarios wait.
- shop-knowledge knows kb only through what kb publishes, in its tests as in its code. Where a scenario needs kb in a state no contract call can produce, a stand-in for kb at the contract boundary answers with kb's contract messages.
- No test reaches a knowledge base outside its own temporary directory, and no test calls a server but the one kb's double gives it.
