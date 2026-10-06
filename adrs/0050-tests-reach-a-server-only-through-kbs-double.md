# 0050 Tests reach a kb server only through a double kb publishes

2026-10-06. A scenario that needs a kb server gets it from a served-store double kb publishes for its clients' tests. shop-knowledge's tests never start `kb serve` or write `kb/server.yaml` themselves; until kb publishes the double, those scenarios wait (a KB REQUEST in the slice plan). Supersedes 0049's testing sentence; the rest of 0049 stands. The user's decision.
