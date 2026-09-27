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


def removed(tmp_path: Path) -> Removed:
    """A directory under `tmp_path`, there and then gone: the one way a step gives a removed working directory."""
    gone = tmp_path / "gone"
    gone.mkdir()
    return Removed(gone)


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


def store_in(root: Path) -> Path:
    """Where kb keeps the store it starts in `root`: the subdirectory kb/, which kb's contract names (its Init row).
    The one place a step names it; what kb keeps inside it is kb's own."""
    return root / "kb"


CLOCK = Path(__file__).parent / "clock"
STAND_IN = Path(__file__).parent / "stand_in"


def _on_path(env, directory: Path) -> dict:
    """`env` with `directory` first on shop-knol's PYTHONPATH, so its sitecustomize loads when shop-knol starts."""
    return {**env, "PYTHONPATH": os.pathsep.join(filter(None, [str(directory), env.get("PYTHONPATH")]))}


def at(env, moment):
    """The environment shop-knol runs in when the history is to say it ran at `moment` (ISO, UTC)."""
    return {**_on_path(env, CLOCK), "TEST_NOW": moment}


def answering(env, tmp_path, *answers):
    """The environment shop-knol runs in when kb is to be in a state no contract call can produce: the stand-in
    (tests/stand_in) answers each call an answer describes with the message the step wrote, and every other call reaches
    the real kb. Each answer is as the stand-in's docstring says; its faults are the step's own words."""
    path = tmp_path / "kb-answers.yaml"
    path.write_text(dumps(list(answers)))
    return {**_on_path(env, STAND_IN), "KB_STAND_IN": str(path)}
