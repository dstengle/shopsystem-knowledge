# 0014 Renderers read what they publish through `renderers/source.py`

2026-09-27. The module is named `source`, the source a renderer publishes from, to keep it apart from `cli._read`, the command. It returns kb's answer as it is and decides nothing; a renderer hands the faults back as `Rendered` faults. The whole read's depth defaults to 0, links left as names.
