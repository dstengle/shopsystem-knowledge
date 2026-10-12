"""pytest plugin: a test tagged to a slice not yet built is expected to fail, strictly.

Written into a repository by shopsystem-bdd's `features plugin <directory>`, beside the conftest.py that
registers it with `from slice_expectations import *` (`from .slice_expectations import *` in a package). Change it
in the plugin, not here.

A test carries its slice as a marker, `slice-<n>`: pytest-bdd makes one of every `@slice-<n>` tag, and a plain test
that waits for a slice takes `@pytest.mark.<the same name>` through `getattr(pytest.mark, "slice-<n>")`. While the
living plan gives that slice the Status `planned` or `blocked`, the test is marked `xfail(strict=True)`: failing
is expected, and passing is a failure, since something built it early or it does not test what its tag says. A
slice that is `in progress` or `green`, or is no longer in the plan because its batch was archived, is run as it
is. So is a slice named with `--slice <n>`, which is how the slice being built is run: red is red, green is green.

The plan is the one `docs/superpowers/plans/*-slices.md` under the root directory, or the ini value `slice_plan`.
"""
import glob
import os
import re

import pytest

MARK = re.compile(r"^slice-(\d+(?:\.\d+)*)$")
HEAD = re.compile(r"^## Slice (\d+(?:\.\d+)*):")
STATUS = re.compile(r"^- Status:\s*([a-z ]+)")


def pytest_addoption(parser):
    parser.getgroup("slices").addoption(
        "--slice", action="append", default=[], metavar="N",
        help="a slice being built: its tests are run as they are, not expected to fail (may be given again)")
    parser.addini("slice_plan", "the living slice plan, relative to the root directory", default="")


def plan_of(config):
    named = config.getini("slice_plan")
    if named:
        return os.path.join(str(config.rootpath), named)
    found = glob.glob(os.path.join(str(config.rootpath), "docs", "superpowers", "plans", "*-slices.md"))
    return found[0] if len(found) == 1 else None


def waiting(path):
    """The slices whose Status is planned or blocked: {number: status}."""
    found, number = {}, None
    with open(path, encoding="utf-8") as lines:
        for line in lines:
            head = HEAD.match(line)
            if head:
                number = head.group(1)
            elif line.startswith("## "):
                number = None
            status = STATUS.match(line)
            if status and number and status.group(1).strip() in ("planned", "blocked"):
                found[number] = status.group(1).strip()
    return found


def pytest_collection_modifyitems(config, items):
    path = plan_of(config)
    config._slices = {"plan": path, "expected": 0, "slices": set()}
    if not path or not os.path.isfile(path):
        return
    building = {text.replace("slice-", "") for text in config.getoption("slice")}
    wait = {number: status for number, status in waiting(path).items() if number not in building}
    for item in items:
        for mark in list(item.iter_markers()):
            match = MARK.match(mark.name)
            if match and match.group(1) in wait:
                number = match.group(1)
                item.add_marker(pytest.mark.xfail(strict=True, reason="slice %s is %s" % (number, wait[number])))
                config._slices["expected"] += 1
                config._slices["slices"].add(number)
                break


def pytest_report_header(config):
    path = plan_of(config)
    return "slices: %s" % (os.path.relpath(path, str(config.rootpath)) if path else "no one living plan found; nothing is expected to fail")


def pytest_terminal_summary(terminalreporter, config):
    seen = getattr(config, "_slices", None)
    if seen and not seen["plan"]:
        terminalreporter.write_line("slices: no one living plan found; nothing is expected to fail")
    if seen and seen["expected"]:
        order = sorted(seen["slices"], key=lambda n: [int(part) for part in n.split(".")])
        terminalreporter.write_line("slices: %d expected to fail, of slice %s" % (seen["expected"], ", ".join(order)))
