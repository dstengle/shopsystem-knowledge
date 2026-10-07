"""A store served by kb's own server, for the scenarios of find-the-knowledge-base.feature and
start-a-knowledge-base.feature that reach a knowledge base through a connection to its server. The server is kb's
served-store double, `kb.testing.served` (adrs/0050): no test starts a server or writes a connection itself. The one
module that imports `kb.testing`; `conftest.py` alone star-imports it (adrs/0048)."""
from contextlib import ExitStack

import kb.testing
import pytest


@pytest.fixture
def served_store():
    """`serve(store_root, connection_dir)`: the store at `store_root` served on 127.0.0.1, its connection written in
    `connection_dir`, both chosen by the Given that asks; gives back the address, `host:port`. Every store it served
    is stopped, and its connection removed, when the scenario ends."""
    with ExitStack() as serving:
        def serve(store_root, connection_dir) -> str:
            return serving.enter_context(kb.testing.served(store_root, connection_dir))
        yield serve
