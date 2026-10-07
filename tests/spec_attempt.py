"""A record the shop is expected to refuse, and the comparison of what the user is shown with kb's own refusal of the
same record (kb adrs/0018), so no step spells kb's wording. Imported plainly by the step modules of
use-the-shops-types.feature that need it, never star-imported."""
from kb.content import dumps
from kb.contract import kb_pb2

from driver import knol
from kb_oracle import kb_answer, printed, signature

MESSAGE = "Record it"


def create(env, tmp_path, attempted, kind, content):
    """Give `create` the content as the user does, saying why, and remember what was given in `attempted`."""
    attempted.update(kind=kind, content=content)
    path = tmp_path / "attempt.yaml"
    path.write_text(dumps(content))
    return knol(env, "create", kind, "--from", str(path), "-m", MESSAGE)


def refused_as_unfit(env, result, attempted):
    """The user is shown kb's own refusal of the record `create` was given, one line to each fault kb found."""
    assert result.returncode == 1 and result.stdout == "", result.stdout
    content = dict(attempted["content"])
    request = kb_pb2.CreateRequest(
        kind=attempted["kind"], title=content.pop("title"), content=dumps(content), signature=signature(env, MESSAGE),
    )
    faults = kb_answer(env, "Create", request).refusal.faults
    assert faults, "kb kept the record"
    assert sorted(result.stderr.splitlines()) == sorted(printed(fault) for fault in faults), result.stderr
