# 0064 A scenario's uses is kept; drift between facts is caught by consistency checks

2026-10-08. A scenario's `uses` stays beside its capability's `depends_on`, so a dependency can be seen down to the scenario that exercises it. The two can drift, as can what a shop's code actually calls; drift is caught by consistency checking of the knowledge base (shop-knol's check), not by removing facts. Checking declared dependencies against the code is recorded as not yet. The user's decision.
