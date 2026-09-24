"""Suite wiring. Step definitions live beside the scenarios they serve; shared Givens are added here by slice 1."""
import re
from pathlib import Path


def pytest_configure(config):
    """Register every @slice-<n> tag in the feature files as a marker, so -m slice-<n> selects a slice."""
    tags = set()
    for feature in Path(config.rootpath, "features").glob("*.feature"):
        tags.update(re.findall(r"@(slice-\d+)", feature.read_text()))
    for tag in sorted(tags):
        config.addinivalue_line("markers", f"{tag}: scenario of that slice in the plan")
