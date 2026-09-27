"""Drive shop-knol the way a user does: a subprocess per command, YAML in files and on stdout."""
import os
import subprocess
import sys
from pathlib import Path

from kb.content import dumps, loads


def knol(env, *args, cwd=None):
    """Run one shop-knol command, from `cwd` when the user works somewhere other than where the suite runs."""
    return subprocess.run(
        [sys.executable, "-m", "shop_knowledge", *args],
        env=env, capture_output=True, text=True, cwd=cwd,
    )


def start(env, shop):
    result = knol(env, "init", str(shop))
    assert result.returncode == 0, result.stderr


def record(env, tmp_path, type_name, content, message):
    """Write content to a file, record it, and return the id the user is shown."""
    path = tmp_path / f"{content['title']}.yaml"
    path.write_text(dumps(content))
    result = knol(env, "create", type_name, "--from", str(path), "-m", message)
    assert result.returncode == 0, result.stderr
    return loads(result.stdout)["id"]


CLOCK = Path(__file__).parent / "clock"


def at(env, moment):
    """The environment shop-knol runs in when the history is to say it ran at `moment` (ISO, UTC)."""
    path = os.pathsep.join(filter(None, [str(CLOCK), env.get("PYTHONPATH")]))
    return {**env, "PYTHONPATH": path, "TEST_NOW": moment}
