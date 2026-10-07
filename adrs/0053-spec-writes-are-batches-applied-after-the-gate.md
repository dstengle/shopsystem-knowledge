# 0053 Spec changes are batches drafted by agents and applied after the gate

2026-10-07. The writer agents draft `shop-knol apply` batch files, never markdown; the controller validates them before the human gate and applies them after it, creates before writes, then renders and commits. A validate-only mode on kb's batch calls is requested from kb; mixed-kind batches are not, since kb removed them on purpose. The user's decision.
