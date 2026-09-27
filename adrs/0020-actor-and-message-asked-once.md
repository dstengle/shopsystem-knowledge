# 0020 Actor and message are asked once, before the handler runs

2026-09-27. `cli._run` asks `cli._by` for every mutating command (`init`, `create`, `write`, `apply`) before its handler runs, so before any file is read or kb called. Unset and empty are the same: no role, no message. Each lack is a fault with no artifact (rule `actor` or `message`), both when both are lacking. `-m` is not required at the argument level, `init` takes only the actor, and handlers pass `**args.by` (actor and message) to kb.
