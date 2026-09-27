# 0042 init starts where the user works, and the suite starts it that way

2026-09-27. Fills in 0037. With no directory named, `shop-knol init` starts the knowledge base in the working directory, taken as an absolute path, so a refusal names the directory the user is in rather than `.`. init never reads `KB_ROOT`: that finds a store that exists, and init makes one. The suite's shared way of starting a knowledge base runs `init` from the shop's directory without naming it; only the scenario that starts one somewhere else names a directory.
