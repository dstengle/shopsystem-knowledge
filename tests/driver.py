"""Drive shop-knol the way a user does: a subprocess per command, YAML in files and on stdout."""
import os
import subprocess
import sys
from pathlib import Path

from kb.client import connect
from kb.content import dumps, loads
from kb.contract import kb_pb2


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


_default_cwd: Path | None = None
"""The working directory a run is given when a step names none of its own: unset outside a test, so a run made
that way is refused; set to the scenario's own temporary directory by conftest's `_working_directory`, for every
test in the suite (adrs/0047 - no test reaches a knowledge base outside its own temporary directory)."""

_runs = 0
"""How many shop-knol runs `knol` has made in this process, so far: a Then over `before`, a snapshot meant to be
taken ahead of the command under test, can tell it was really taken there and not, resolved lazily, after."""


def runs() -> int:
    """`_runs`, for a Then to compare against a count a `before` fixture took earlier."""
    return _runs


def knol(env, *args, cwd=None, piped=None):
    """Run one shop-knol command, from `cwd` when the user works somewhere other than the suite's default for this
    test, with `piped` on its standard input when another command's output is piped in; a `Removed` cwd is gone by
    the time shop-knol starts. Refused if no `cwd` is given and the suite has set no default."""
    global _runs
    directory = cwd if cwd is not None else _default_cwd
    if directory is None:
        raise RuntimeError("shop-knol was run with no working directory, and the suite set no default")
    _runs += 1
    return subprocess.run(
        [sys.executable, "-m", "shop_knowledge", *args],
        env=env, capture_output=True, text=True, cwd=directory, input=piped,
        preexec_fn=directory.remove if isinstance(directory, Removed) else None,
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


NO_STORE = "store"
"""The `rule` kb's contract publishes (kb adrs/0018) for the fault it gives when a call finds no store."""


def actor(env) -> kb_pb2.Actor:
    """The actor a command run with `env` makes its change as: KB_ACTOR's role, and the piece of work after a colon."""
    role, _, execution = env.get("KB_ACTOR", "").partition(":")
    return kb_pb2.Actor(role=role, execution=execution)


def kb_answer(env, call, request, cwd=None):
    """kb's own answer to `request`, through its published in-process client (kb adrs/0018), made from where shop-knol
    ran (`cwd`, or the suite's default) under exactly `env` - never the ambient environment of the process running
    the suite, so a shell GIT_DIR or a shell HOME's global git config never reaches this call either (adrs/0047) -
    so it goes to the scenario's own store and no other: what a Then compares shop-knol's printed refusal with, so
    no step spells kb's wording, which is kb's to change. Always the real kb, never the stand-in (which loads only in
    shop-knol's own process): a Then over an answer the stand-in gave compares with what the stand-in gave, never
    with this (Review Focus 4). Asked after shop-knol's own call was refused, so of the same state; a refused call
    changes nothing. Refused, as `knol` is, with no `cwd` and no default set. The suite's own directory and
    environment are restored after."""
    directory = cwd if cwd is not None else _default_cwd
    if directory is None:
        raise RuntimeError("kb was asked with no working directory, and the suite set no default")
    here, kept = Path.cwd(), dict(os.environ)
    try:
        os.chdir(directory)
        os.environ.clear()
        os.environ.update(env)
        return getattr(connect(), call)(request)
    finally:
        os.chdir(here)
        os.environ.clear()
        os.environ.update(kept)


def printed(fault) -> str:
    """A fault as the one line the shop's spec says the user is shown: the artifact and the place in it, then kb's
    message as kb returned it, its lines joined."""
    message = " ".join(line.strip() for line in fault.message.splitlines())
    where = f"{fault.artifact} at {fault.path}" if fault.path else fault.artifact
    return f"{where}: {message}" if where else message


def store_in(root: Path) -> Path:
    """Where kb keeps the store it starts in `root`: the subdirectory kb/, which kb's contract names (its Init row).
    The one place a step names it; what kb keeps inside it is kb's own."""
    return root / "kb"


CLOCK = Path(__file__).parent / "clock"
STAND_IN = Path(__file__).parent / "stand_in"


def _on_path(env, directory: Path) -> dict:
    """`env` with `directory` first on shop-knol's PYTHONPATH, so its sitecustomize loads when shop-knol starts."""
    return {**env, "PYTHONPATH": os.pathsep.join(filter(None, [str(directory), env.get("PYTHONPATH")]))}


def _refuse_if_combined(env, other: Path, this_name: str, other_name: str) -> None:
    """`at` and `answering` are both loaded as `sitecustomize`, so a process puts only the first of them a caller
    combines on its PYTHONPATH; the other never loads, silently. Refused until slice 50.23 removes the clock's own
    sitecustomize, so no scenario can carry both without knowing it."""
    if str(other) in env.get("PYTHONPATH", "").split(os.pathsep):
        raise RuntimeError(f"driver.{this_name} refuses: driver.{other_name} is already on this environment's PYTHONPATH")


def at(env, moment):
    """The environment shop-knol runs in when the history is to say it ran at `moment` (ISO, UTC)."""
    _refuse_if_combined(env, STAND_IN, "at", "answering")
    return {**_on_path(env, CLOCK), "TEST_NOW": moment}


def answering(env, tmp_path, *answers):
    """The environment shop-knol runs in when kb is to be in a state no contract call can produce: the stand-in
    (tests/stand_in) answers each call an answer describes with the message the step wrote, and every other call reaches
    the real kb. Each answer is as the stand-in's docstring says; its faults are the step's own words. Refused for a
    second call in one scenario, which would silently replace the first call's answers rather than add to them."""
    _refuse_if_combined(env, CLOCK, "answering", "at")
    path = tmp_path / "kb-answers.yaml"
    if path.exists():
        raise RuntimeError("driver.answering was already called for this scenario; it does not replace answers")
    path.write_text(dumps(list(answers)))
    return {**_on_path(env, STAND_IN), "KB_STAND_IN": str(path)}
