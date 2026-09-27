# 0018 Read levels, and JSON on read

2026-09-27. `shop-knol read` takes `--section TITLE` (a section read, the title as given), `--whole` (a whole read, links as names) and `--resolve [DEPTH]` (a whole read with links filled in, one step when no depth is given). `--resolve` implies a whole read, and `--section` wins when given with either. `--json` writes the same document as JSON and is on `read` alone. A whole read shows kb's identity then its content; a section read shows what kb gives and nothing else. The store is found by kb (`connect()` with no root), and kb's refusals pass through.
