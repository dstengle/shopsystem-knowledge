"""Loaded by every Python process started with this directory on PYTHONPATH, as the steps start shop-knol when a
scenario says what day it is. With TEST_NOW set, kb stamps its history from that moment, a second later at each
stamp, instead of from the machine's clock. kb's journal clock is a module function for this purpose."""
import os

if os.environ.get("TEST_NOW"):
    from datetime import datetime, timedelta, timezone

    import kb.journal

    _moments = iter(
        datetime.fromisoformat(os.environ["TEST_NOW"]).replace(tzinfo=timezone.utc) + timedelta(seconds=tick)
        for tick in range(10_000)
    )
    kb.journal.now = lambda: next(_moments)
