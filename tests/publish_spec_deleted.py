"""The steps of publish-a-shops-spec for the files a publish deletes: those it published earlier and no longer writes.
Star-imported by the feature's test module alone (adrs/0035). A published file left from earlier is put in the
directory as the publisher wrote it, its published-from line naming the artifact it came from, since kb gives an
artifact no new title: its old file is what a publish under its old title left."""
from pathlib import Path

from pytest_bdd import given, parsers, then

import spec_shop
from driver import knol
from publish_refusals import UNREADABLE, lines_naming
from published_from import gherkin, markdown


def _path(target, file):
    return target / file.strip("`")


def _put(target, kept, file, text):
    path = _path(target, file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    kept[path] = text


def _left(env, name, file, title):
    """What a publish wrote at `file` for the artifact `name`, then titled `title`: its published-from line, where the
    publisher puts it, and its heading."""
    if file.endswith(".feature`"):
        return f"{gherkin(env, name)}\n# formulated from spec/capabilities/{Path(file.strip('`')).stem}.md\nFeature: {title}\n"
    if file.startswith("`spec/"):
        return f"---\nid: {name}\ntitle: {title}\n---\n{markdown(env, name)}\n\n# {title}\n"
    return f"{markdown(env, name)}\n\n# {title}\n"


@given(parsers.parse("{artifact} was published earlier as {old}, and its title has since changed so that it is now "
                     "published as {new}"), target_fixture="renamed")
def _published_earlier(env, tmp_path, built, target, kept, artifact, old, new):
    if artifact == "one of the shop's decisions, numbered 7":
        name = spec_shop.numbered_decision(env, tmp_path, built.shop, 7, "Keep every log")
        title = "0007 Keep the log"
    else:
        capability, feature = spec_shop.ordered_capability(env, tmp_path, built.shop, "Tail the log")
        name = feature if artifact.startswith("the feature formulating") else capability
        title = "Read the log"
    _put(target, kept, old, _left(env, name, old, title))
    return {"old": old, "new": new}


@given(parsers.parse("the directory also holds {stale}, published earlier from {artifact}"), target_fixture="stale")
def _stale_file(env, tmp_path, built, target, kept, stale, artifact):
    if artifact == "a decision linking to another shop of the same product":
        _, name = spec_shop.other_shop_decision(env, tmp_path, built.product, 99, "Old rule")
    else:
        capability, feature = spec_shop.retired_capability(env, tmp_path, built.shop, "Old cache")
        name = feature if artifact.startswith("the feature formulating") else capability
    _put(target, kept, stale, _left(env, name, stale, "Old"))
    return {"file": stale, "name": name}


@given(parsers.parse("the directory holds `notes/old.md`, whose published-from line names {artifact}"))
def _notes_elsewhere(env, target, kept, stale, artifact):
    _put(target, kept, "notes/old.md", f"{markdown(env, stale['name'])}\n\n# Old\n")


@then(parsers.re(r"(?P<old>`[^`]+`) is deleted"))
def _deleted(result, target, kept, old):
    assert result.returncode == 0, result.stderr
    assert _path(target, old) in kept and not _path(target, old).exists(), (old, result.stdout)


@then(parsers.re(r"that directory holds (?P<new>`[^`]+`)"))
def _holds(target, new):
    assert _path(target, new).is_file(), new


@then("`notes/old.md` is still in that directory, as it was")
def _notes_kept(target, kept):
    path = _path(target, "notes/old.md")
    assert path.read_text() == kept[path]


@given(parsers.re(r"a directory holding (?P<file>`[^`]+`), which has no published-from line"), target_fixture="by_hand")
def _written_by_hand(target, kept, file):
    _put(target, kept, file, "# Notes\n\nWritten by hand beside the published files.\n")
    return file


@given("no artifact is published under that name")
def _nothing_published_there(env, tmp_path, built, by_hand):
    """A publish of the shop's spec elsewhere writes no file under that name."""
    elsewhere = tmp_path / "elsewhere"
    published = knol(env, "render", "spec", built.shop, "--to", str(elsewhere))
    assert published.returncode == 0, published.stderr
    assert not (elsewhere / by_hand.strip("`")).exists() and by_hand.strip("`") not in published.stdout, published.stdout


@then(parsers.re(r"(?P<file>`[^`]+`) is left as it was"))
def _left_as_it_was(result, target, kept, file):
    assert result.returncode == 0, result.stderr
    assert _path(target, file).read_text() == kept[_path(target, file)], file


@given(parsers.re(r"a directory holding (?P<file>`[^`]+`), which cannot be read"), target_fixture="by_hand")
def _which_cannot_be_read(env, built, target, kept, request, file):
    """A file that carries the published-from line, so it would be deleted were it readable, its read permission taken
    away and given back when the scenario ends, so the temporary directory can be cleaned."""
    _put(target, kept, file, f"{markdown(env, built.decisions[0])}\n\n# Old\n")
    path = _path(target, file)
    path.chmod(0o000)
    request.addfinalizer(lambda: path.chmod(0o644))
    kept[path] = UNREADABLE
    return file


@then(parsers.re(r"publishing is rejected because that file cannot be read, naming (?P<file>`[^`]+`)"))
def _rejected_unreadable(result, file):
    lines_naming(result, "cannot be read", [file.strip("`")])


@then(parsers.re(r"(?P<file>`[^`]+`) is still in that directory"))
def _still_there(target, kept, file):
    assert _path(target, file).is_file() and _path(target, file) in kept
