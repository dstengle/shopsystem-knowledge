---
id: capability/start-a-knowledge-base
title: Start a knowledge base
narrator: the user, setting up the shop's knowledge base
rests_on:
  - decision/init-beside-the-shops-work
  - decision/init-starts-where-the-user-works
  - decision/init-furnishes-the-knowledge-base-kb-finds
  - decision/init-refuses-kbs-answers
  - decision/init-furnishes-an-empty-knowledge-base
  - decision/init-furnishes-only-an-empty-knowledge-base
  - decision/init-refuses-a-knowledge-base-holding-the-shops-types
  - decision/a-working-directory-holding-the-shops-knowledge-keeps-its-reasons
  - decision/furnishing-is-built-on-kb-v0-5-0
  - decision/init-edge-cases-settled-by-principle
  - decision/seven-types-on-a-shop-artifact-base
  - capability/find-the-knowledge-base
formulated_as: features/start-a-knowledge-base.feature
---

# Start a knowledge base

## Purpose

`shop-knol init` sets up an empty knowledge base with the shop's types. When it finishes, the knowledge base holds the shop's types and nothing else of the shop's yet.

Which knowledge base it sets up depends on whether the user names a directory:
- **A directory is named.** init starts a knowledge base there, on purpose.
- **No directory is named, and kb finds an empty knowledge base from the working directory.** kb may find it upward, through `KB_ROOT`, or as a connection to a server, the way find-the-knowledge-base describes. If kb's operator started it empty, init furnishes it with the shop's types.
- **No directory is named, and nothing is found.** init starts a knowledge base beside the shop's work, in the working directory.

init says which role set it up and writes its own message. It refuses rather than overwrite or nest the shop's knowledge, and it furnishes only a knowledge base that is empty. It records nothing of the shop's beyond its types.

## Behaviour

- When the user starts a knowledge base, saying which role they are, the shop can hold decisions, features, work items, roles, processes, steps and tags, and the user defines nothing of their own before recording the first one.
- Where no knowledge base is found from the working directory, when the user starts a knowledge base without naming a directory, saying which role they are, the shop's knowledge is kept in a place of its own inside the working directory, and what that directory already held is left as it was.
- When the user starts a knowledge base by naming another directory, saying which role they are, the shop's knowledge is kept in a place of its own inside the named directory, and the working directory holds no knowledge base.
- When the user starts a knowledge base, saying which role they are and giving no message, the knowledge base is started, and everything it was given is recorded in the history under a message the command writes itself.
- Where no directory is named and the knowledge base kb finds from the working directory (upward or through `KB_ROOT`) was started empty by kb's operator, when the user starts a knowledge base, saying which role they are, that knowledge base holds the shop's types and nothing else of the shop's.
- Where no directory is named and the knowledge base kb finds from the working directory is a connection to a server hosting a store that kb's operator started empty, when the user starts a knowledge base, saying which role they are, that knowledge base holds the shop's types and nothing else of the shop's.
- When the user starts a knowledge base by naming a directory that holds a knowledge base kb's operator started empty, saying which role they are, that knowledge base holds the shop's types and nothing else of the shop's.
- If the user starts a knowledge base without naming a directory and finding the knowledge base is refused (`KB_ROOT` names a directory holding none, or names one other than the one the user is working in), starting is refused for the reason finding gives, and no knowledge base is started.
- If the user starts a knowledge base without saying which role they are, starting is refused because starting one must say which role did it, and the directory holds no knowledge base.
- Where no directory is named and finding is not refused, if the working directory already holds the shop's knowledge, starting is refused because that directory already holds a knowledge base, and everything the shop knows is unchanged.
- Where no directory is named and finding is not refused, if the working directory sits inside a knowledge base that holds the shop's knowledge, starting is refused because that directory is inside a knowledge base, and everything the shop knows is unchanged.
- Where the knowledge base init would furnish is found through `KB_ROOT` elsewhere than the working directory, or through a server, or sits in a named directory, if it already holds the shop's types, starting is refused because it already holds the shop's knowledge, and nothing changes.
- If the knowledge base init would furnish does not hold the shop's types but holds something else (other types, or content), starting is refused because it is not empty, naming what it holds, and nothing changes.
- If the working directory has been removed, no directory is named and nothing names a knowledge base, starting is refused because the working directory is gone.
- If the user starts a knowledge base in a directory whose name is given empty, starting is refused because that directory's name is empty, which names no place, and the working directory holds no knowledge base.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol init <root>` | `kb.init(<root>, role)` in shop-knol's own process, which creates `<root>/kb/`; then the bootstrap set loaded through Create |
| `shop-knol init` | kb's client finds a knowledge base from the working directory. If one is found and empty, the bootstrap set is loaded into it through Create, and no store is started. If none is found, `kb.init` starts a store in the working directory in shop-knol's own process, and the bootstrap set is loaded through Create |

- kb has no Init call on the wire. shop-knol starts a store with `kb.init` only where it starts one, and loads the shop's types through Create in every case.
- Naming `<root>` starts a knowledge base there, on purpose.
- With no root named, the working directory is taken as an absolute path, so a refusal names the directory the user is in rather than `.`.
- The finding is kb's: upward from the working directory, through `KB_ROOT`, or a connection to a server found in the same place. It is the same finding every other command uses (find-the-knowledge-base).
- The actor comes from `KB_ACTOR` and is asked for before kb is called. `init` takes no `-m`; its messages are fixed.
- When `kb.init` refuses, it raises `kb.NotStarted` with the faults, and they reach the user in kb's words. These cover a directory that already holds a store, a directory inside one, and a named directory that does not exist. The types are loaded only after `kb.init` returns without refusing, and loading stops at the first Create kb refuses.
- kb records the start and the bootstrap set as creates under the role that ran `init`.

## Not yet

Nothing deferred.
