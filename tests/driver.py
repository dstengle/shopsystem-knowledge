"""Drive shop-knol the way a user does: a subprocess per command, YAML in files and on stdout."""
import os
import socket
import subprocess
import sys
import time
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


def _isolated(directory, env: dict) -> None:
    """Refuses, with a clear error, when `directory` - or `env`'s own KB_ROOT, if it names one - lies outside the
    test's own temporary directory: `_default_cwd`'s root, once a test has set it (adrs/0047). Makes isolation an
    assertion, where it was until now only ever a matter of construction. Skipped before any test sets
    `_default_cwd`: the session guard's own throwaway probes are deliberately pointed outside it, first."""
    if _default_cwd is None:
        return
    root = Path(os.fspath(_default_cwd)).resolve()
    named = {"the working directory": os.fspath(directory), "KB_ROOT": env.get("KB_ROOT")}
    for what, given in named.items():
        if given is None:
            continue
        outside = Path(given).resolve()
        if outside != root and root not in outside.parents:
            raise RuntimeError(f"{what} {outside} lies outside the test's own temporary directory {root}")


def knol(env, *args, cwd=None, piped=None):
    """Run one shop-knol command, from `cwd` when the user works somewhere other than the suite's default for this
    test, with `piped` on its standard input when another command's output is piped in; a `Removed` cwd is gone by
    the time shop-knol starts. Refused with no `cwd` and no default set, or either outside the test's own directory
    (`_isolated`)."""
    global _runs
    directory = cwd if cwd is not None else _default_cwd
    if directory is None:
        raise RuntimeError("shop-knol was run with no working directory, and the suite set no default")
    _isolated(directory, env)
    _runs += 1
    return subprocess.run(
        [sys.executable, "-m", "shop_knowledge", *args],
        env=env, capture_output=True, text=True, cwd=directory, input=piped,
        preexec_fn=directory.remove if isinstance(directory, Removed) else None,
    )


def unnamed(env) -> dict:
    """`env` with no KB_ROOT: what a run is given where nothing is to name a knowledge base. The suite's `env` names the
    shop's directory before any store is there, and init refuses a KB_ROOT naming a directory holding none."""
    return {name: value for name, value in env.items() if name != "KB_ROOT"}


def start(env, shop):
    """Start a knowledge base the way the user now does: run init from the shop's directory, naming none, with nothing
    naming a knowledge base, so it starts one there."""
    result = knol(unnamed(env), "init", cwd=shop)
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
    """Where kb keeps the store it starts in `root`: the subdirectory kb/, which kb publishes (`kb.init`).
    The one place a step names it; what kb keeps inside it is kb's own."""
    return root / "kb"


def connection_in(directory: Path, address: str) -> None:
    """Write, in `directory`, the connection to the server at `address`: `kb/server.yaml` holding its `address`, the
    form kb publishes. The one place a step writes it; kb never does."""
    store_in(directory).mkdir()
    (store_in(directory) / "server.yaml").write_text(dumps({"address": address}))


def _free_port() -> int:
    """A port on 127.0.0.1 no one is listening on, as the system hands one out."""
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


_SERVE_WITHIN = 5.0
"""How long, in seconds, `serve` waits for kb serve to take connections before failing the step."""


def _answering(server: subprocess.Popen, port: int, said: Path) -> bool:
    """Whether the server takes a connection on `port`; refused, with what it wrote to `said`, once it has exited."""
    if server.poll() is not None:
        raise RuntimeError(f"kb serve exited {server.returncode}: {said.read_text()}")
    with socket.socket() as probe:
        return probe.connect_ex(("127.0.0.1", port)) == 0


def serve(env, root: Path) -> tuple[subprocess.Popen, str]:
    """Start `kb serve` on the store in `root`, on 127.0.0.1 and a port of its own, from `root` itself, and return it
    with its address once it takes connections; failed, with what it wrote, if it does not within `_SERVE_WITHIN`.
    What it writes goes to a file beside `root`, in the test's own directory. The caller stops it (`stop`)."""
    _isolated(root, env)
    port = _free_port()
    address = f"127.0.0.1:{port}"
    kb = Path(sys.executable).parent / "kb"
    said = root.parent / "kb-serve.stderr"
    with said.open("w") as stderr:
        server = subprocess.Popen(
            [str(kb), "serve", str(root), "--listen", address],
            env=env, cwd=root, stdout=subprocess.DEVNULL, stderr=stderr,
        )
    deadline = time.monotonic() + _SERVE_WITHIN
    while not _answering(server, port, said):
        if time.monotonic() > deadline:
            stop(server)
            raise RuntimeError(f"kb serve took no connection within {_SERVE_WITHIN}s: {said.read_text()}")
        time.sleep(0.05)
    return server, address


def stop(server: subprocess.Popen) -> None:
    """Stop a server `serve` started, and wait until it has gone."""
    if server.poll() is None:
        server.terminate()
    server.communicate()


CLOCK = Path(__file__).parent / "clock"
STAND_IN = Path(__file__).parent / "stand_in"


def _on_path(env, directory: Path) -> dict:
    """`env` with `directory` first on shop-knol's PYTHONPATH, so its sitecustomize loads when shop-knol starts."""
    return {**env, "PYTHONPATH": os.pathsep.join(filter(None, [str(directory), env.get("PYTHONPATH")]))}


def _refuse_if_combined(env, other: Path, this_name: str, other_name: str) -> None:
    """`at` and `answering` are both loaded as `sitecustomize`, so a process loads only the first of them a caller
    combines on its PYTHONPATH; the other never loads, silently. Refused while both are `sitecustomize`, so no
    scenario can carry both without knowing it."""
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
