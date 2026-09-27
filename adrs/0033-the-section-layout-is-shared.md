# 0033 The section layout is shared

2026-09-27. The layout of a content model's `sections`, a heading and its body with the sections inside it a level down, lives in `renderers/sections.py` as `laid_out(sections, level)`. The markdown renderer calls it from level 2, the agent renderer from level 1. Neither keeps a copy.
