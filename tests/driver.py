"""Drive shop-knol the way a user does: a subprocess per command, YAML in files and on stdout."""
import os
import subprocess
import sys
from pathlib import Path

from kb.content import dumps, loads


class Removed:
    """A directory the user works in that is removed once the command's process has entered it, so shop-knol starts in
    a working directory that no longer exists."""

    def __init__(self, path: Path):
        self.path = path

    def __fspath__(self) -> str:
        return str(self.path)

    def remove(self) -> None:
        """Run in the child after it has entered the directory, before shop-knol starts."""
        os.rmdir(self.path)


def knol(env, *args, cwd=None, piped=None):
    """Run one shop-knol command, from `cwd` when the user works somewhere other than where the suite runs,
    with `piped` on its standard input when another command's output is piped in; a `Removed` cwd is gone by the
    time shop-knol starts."""
    return subprocess.run(
        [sys.executable, "-m", "shop_knowledge", *args],
        env=env, capture_output=True, text=True, cwd=cwd, input=piped,
        preexec_fn=cwd.remove if isinstance(cwd, Removed) else None,
    )


def start(env, shop):
    """Start a knowledge base the way the user now does: run init from the shop's directory, naming none."""
    result = knol(env, "init", cwd=shop)
    assert result.returncode == 0, result.stderr


def record(env, tmp_path, type_name, content, message):
    """Write content to a file, record it, and return the id the user is shown."""
    path = tmp_path / f"{content['title']}.yaml"
    path.write_text(dumps(content))
    result = knol(env, "create", type_name, "--from", str(path), "-m", message)
    assert result.returncode == 0, result.stderr
    return loads(result.stdout)["id"]


def whole(env, name):
    """Read an artifact whole, as the user does, and return the document shown; the read must succeed."""
    result = knol(env, "read", name, "--whole")
    assert result.returncode == 0, result.stderr
    return loads(result.stdout)


CLOCK = Path(__file__).parent / "clock"


def at(env, moment):
    """The environment shop-knol runs in when the history is to say it ran at `moment` (ISO, UTC)."""
    path = os.pathsep.join(filter(None, [str(CLOCK), env.get("PYTHONPATH")]))
    return {**env, "PYTHONPATH": path, "TEST_NOW": moment}
