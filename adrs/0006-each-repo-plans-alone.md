# 0006 Each repository plans alone; kb is consumed by tag

2026-09-24. After kb 0.1, kb and shop-knowledge each keep their own slice plan. shop-knowledge pins kb by git tag in pyproject and installs it into its own virtualenv. A kb change shop-knowledge needs is a request to bump the pin, never a slice that edits kb. Tags and releases are the user's decision.
