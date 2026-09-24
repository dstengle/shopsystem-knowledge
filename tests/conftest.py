"""Suite wiring. Step definitions live beside the scenarios they serve; shared Givens are added here by slice 1."""
import os
import re
from pathlib import Path

import pytest
from pytest_bdd import given

from driver import start


def pytest_configure(config):
    """Register every @slice-<n> tag in the feature files as a marker, so -m slice-<n> selects a slice."""
    tags = set()
    for feature in Path(config.rootpath, "features").glob("*.feature"):
        tags.update(re.findall(r"@(slice-\d+(?:\.\d+)?)", feature.read_text()))
    for tag in sorted(tags):
        config.addinivalue_line("markers", f"{tag}: scenario of that slice in the plan")


@pytest.fixture
def shop(tmp_path):
    """The directory the shop's knowledge base is started in, there before it starts; the store is its kb/ subdirectory."""
    shop = tmp_path / "shop"
    shop.mkdir()
    return shop


@pytest.fixture
def env(shop):
    return {**os.environ, "KB_ROOT": str(shop), "KB_ACTOR": "shopkeeper"}


@given("a shop knowledge base holding the shop's types")
def _shop_knowledge_base(env, shop):
    start(env, shop)
