"""Loaded by every Python process started with this directory on PYTHONPATH, as the steps start shop-knol when a
scenario says what day it is. With TEST_NOW set, kb stamps its history from that moment, a second later at each
stamp, instead of from the machine's clock: it puts itself in front of `kb.client.connect` and `kb.init` and gives
each the clock kb publishes for that (kb adrs/0018), one clock for the whole process, so the seconds run on across
the start and every client. It knows kb only through what kb publishes: `kb.init` and `kb.client`."""
import os

if os.environ.get("TEST_NOW"):
    from datetime import datetime, timedelta, timezone

    import kb
    import kb.client

    _real_connect = kb.client.connect
    _moments = iter(
        datetime.fromisoformat(os.environ["TEST_NOW"]).replace(tzinfo=timezone.utc) + timedelta(seconds=tick)
        for tick in range(10_000)
    )

    def _clock() -> datetime:
        return next(_moments)

    def connect(root=None, *, clock=None):
        """kb's own client, stamping from TEST_NOW unless the caller gives a clock of its own."""
        return _real_connect(root, clock=clock or _clock)

    _real_init = kb.init

    def init(root, role, *, execution="", clock=None):
        """kb's own start, stamping from TEST_NOW unless the caller gives a clock of its own."""
        _real_init(root, role, execution=execution, clock=clock or _clock)

    kb.client.connect = connect
    kb.init = init
