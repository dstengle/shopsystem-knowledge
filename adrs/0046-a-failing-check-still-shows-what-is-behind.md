# 0046 A check that finds faults still shows what is behind its type

2026-09-27. Supersedes the last three sentences of 0029. `shop-knol validate` that finds faults refuses with them as every refusal does, one line each on stderr, exit 1, and also shows its answer on stdout: `sound: false` with the `behind:` list, empty when nothing is behind. A check that finds none is unchanged: `sound: true`, `behind:`, exit 0. The user chose the whole finding in one run over a refusal that prints nothing on stdout.
