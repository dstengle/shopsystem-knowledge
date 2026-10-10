# 0084 Another context is read by its capabilities, not its decisions

2026-10-10. Work here reads another bounded context, such as kb, only through its capabilities (`spec/capabilities/`), never its `adrs/`. A request to it is worded as a change to those capabilities; its decisions are its own session's to read and record. The user's decision.
