# 0060 A capability declares the capabilities it depends on, in any context

2026-10-08. A capability declares its upstream dependencies on capabilities, in its own context or another, as a link of its own (`depends_on`), kept apart from the decisions it rests on, so that dependencies across contexts can be queried. A scenario is part of its capability: its `uses` names the dependencies it exercises, which must be among its capability's. The rule that a scenario points at another context's capability, never its scenario, stands. The user's decision.
