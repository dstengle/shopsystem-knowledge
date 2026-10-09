"""kb's own answers, asked as the oracle a Then compares shop-knol's printed refusals with, and the words a Then needs
to show a fault the way the user is shown it. Not a step module: imported plainly, never star-imported (adrs/0035)."""
import os
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

import driver
from kb import NotStarted, init
from kb.client import connect
from kb.content import NotCanonical, dumps, loads
from kb.contract import kb_pb2


NO_STORE = "store"
"""The `rule` kb's contract publishes (kb adrs/0018) for the fault it gives when a call finds no store."""


def signature(env, message: str = "") -> kb_pb2.Signature:
    """The signature a command run with `env` makes its change under: KB_ACTOR's role, the piece of work after a colon,
    and the message given."""
    role, _, execution = env.get("KB_ACTOR", "").partition(":")
    return kb_pb2.Signature(role=role, execution=execution, message=message)


def kb_answer(env, call, request, cwd=None):
    """kb's own answer to `request`, through its published in-process client (kb adrs/0018), made from where shop-knol
    ran (`cwd`, or the suite's default) under exactly `env` - never the ambient environment of the process running
    the suite, so a shell GIT_DIR or a shell HOME's global git config never reaches this call either (adrs/0047) -
    so it goes to the scenario's own store and no other: what a Then compares shop-knol's printed refusal with, so
    no step spells kb's wording, which is kb's to change. Always the real kb, never the stand-in (which loads only in
    shop-knol's own process): a Then over an answer the stand-in gave compares with what the stand-in gave, never
    with this (Review Focus 4). Asked after shop-knol's own call was refused, so of the same state; a refused call
    changes nothing. Refused, as `knol` is, with no `cwd` and no default set, or either outside the test's own
    directory (`_isolated`). The suite's own directory and environment are restored after. From a `Removed`
    directory, which this process cannot enter, kb is asked the way shop-knol was run instead:
    `_kb_answer_from_gone`."""
    directory = cwd if cwd is not None else driver._default_cwd
    if directory is None:
        raise RuntimeError("kb was asked with no working directory, and the suite set no default")
    driver._isolated(directory, env)
    if isinstance(directory, driver.Removed):
        return _kb_answer_from_gone(env, call, request, directory)
    with _as_run(directory, env):
        return getattr(connect(), call)(request)


def kb_refuses_to_start(env, root: Path, cwd: Path) -> list:
    """kb's own refusal to start a store at `root`, asked as shop-knol starts one, through `kb.init` in this process,
    from `cwd` under exactly `env`, as `kb_answer` asks: the faults of the `NotStarted` it raises, none if it starts
    one. Refused, as `knol` is, with `cwd` outside the test's own directory (`_isolated`)."""
    driver._isolated(cwd, env)
    role, _, execution = env.get("KB_ACTOR", "").partition(":")
    with _as_run(cwd, env):
        try:
            init(str(root), role, execution=execution)
        except NotStarted as refusal:
            return refusal.faults
    return []


OPERATOR = "operator"
"""The role a store kb's operator starts is started under, in a step: a role of the step's own, never the one
shop-knol is run as."""


def operator_started(env, root: Path) -> None:
    """A store started empty at `root` the way kb's operator starts one, through `kb.init` (published) in this
    process, from `root` under exactly `env`, as `kb_answer` asks: never by writing a file. Refused, as `knol` is,
    with `root` outside the test's own directory (`_isolated`)."""
    driver._isolated(root, env)
    with _as_run(root, env):
        init(str(root), OPERATOR)


def operator_created(env, root: Path, kind: str, title: str, content: dict) -> str:
    """An artifact created in the store at `root` the way kb's operator records one, through kb's published client in
    this process, from `root` under exactly `env`, signed by the operator's role: never by writing a file, and never
    through shop-knol. Gives back the id kb named it with; refused, as `knol` is, outside the test's own directory."""
    driver._isolated(root, env)
    asked = kb_pb2.CreateRequest(
        kind=kind, title=title, content=dumps(content), signature=kb_pb2.Signature(role=OPERATOR, message=f"Add {title}"),
    )
    with _as_run(root, env):
        answer = connect(root).Create(asked)
    assert answer.WhichOneof("outcome") == "result", answer
    return answer.result.id


@contextmanager
def _as_run(directory, env):
    """In `directory`, under exactly `env`, as shop-knol was run; the suite's own directory and environment restored
    after."""
    here, kept = Path.cwd(), dict(os.environ)
    try:
        os.chdir(directory)
        os.environ.clear()
        os.environ.update(env)
        yield
    finally:
        os.chdir(here)
        os.environ.clear()
        os.environ.update(kept)


_ASK_KB = (
    "import sys\n"
    "from kb.client import connect\n"
    "from kb.contract import kb_pb2\n"
    "asked = getattr(kb_pb2, sys.argv[2]).FromString(sys.stdin.buffer.read())\n"
    "sys.stdout.buffer.write(getattr(connect(), sys.argv[1])(asked).SerializeToString())\n"
)
"""kb's published client asked one call, the request read from stdin and the answer written to stdout, both as the
contract's messages serialized."""


def _kb_answer_from_gone(env, call, request, gone: driver.Removed):
    """kb's own answer to `request` from a working directory that no longer exists: `gone` made again, entered by a
    subprocess under exactly `env`, and removed before kb is asked, as `knol` runs shop-knol there. The answer's
    message is the one the contract's service publishes for `call`. `_isolated` is asserted again, of `gone.path`."""
    driver._isolated(gone.path, env)
    gone.path.mkdir()
    asked = subprocess.run(
        [sys.executable, "-c", _ASK_KB, call, type(request).__name__],
        env=env, capture_output=True, cwd=gone, input=request.SerializeToString(), preexec_fn=gone.remove,
    )
    assert asked.returncode == 0, asked.stderr.decode()
    answer = kb_pb2.DESCRIPTOR.services_by_name["Kb"].methods_by_name[call].output_type.name
    return getattr(kb_pb2, answer).FromString(asked.stdout)


def printed(fault) -> str:
    """A fault as the one line the shop's spec says the user is shown: the artifact and the place in it, the rule,
    then the message as kb returned it, its lines joined."""
    message = " ".join(line.strip() for line in fault.message.splitlines())
    where = f"{fault.artifact} at {fault.place}" if fault.place else fault.artifact
    said = f"{fault.rule}: {message}" if fault.rule else message
    return f"{where}: {said}" if where else said


def refused_as_kb_refuses(env, result, workdir, called):
    """kb's own answer to the call the scenario's own When made, from the same directory and KB_ROOT, refuses the
    store rule it publishes (kb adrs/0018); the user is shown that one fault, in kb's words, and nothing else. Shared
    by store_not_found.py and read_back_from_elsewhere.py, each importing it plainly, never one from the other
    (no step module imports another)."""
    faults = kb_answer(env, called["call"], called["request"], cwd=workdir).refusal.faults
    assert [fault.rule for fault in faults] == [NO_STORE], faults
    assert result.stderr.splitlines() == [printed(faults[0])], result.stderr
    assert result.stdout == ""


UNKEPT = "Keep prices in step with costs. \nAnd with what the shelves hold.\n"
"""Prose the shop cannot keep as written: a line before its last ends in a space. Written into a file as a quoted
scalar, since kb's own writing of content refuses it."""


def refused_as_unkept(result, path: Path, place: str) -> None:
    """The one line shop-knol prints for prose in the file at `path` that kb cannot keep, at `place` in that file:
    kb's own refusal to write the same file's content (`kb.content.dumps`, kb adrs/0018), never spelled here, as the
    fault `printed` shows the user."""
    try:
        dumps(loads(path.read_text()))
    except NotCanonical as refusal:
        assert result.returncode == 1
        fault = kb_pb2.Fault(artifact=str(path), place=place, rule="content", message=str(refusal))
        assert result.stderr.splitlines() == [printed(fault)], result.stderr
        return
    raise AssertionError(f"kb keeps {path} as written")
