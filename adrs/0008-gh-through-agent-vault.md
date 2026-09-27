# 0008 The GitHub CLI runs through agent-vault

2026-09-22. Every gh invocation is `agent-vault run -- gh ...`. Credentials come from the agent-vault proxy; bare gh is not used.
