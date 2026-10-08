"""The steps of publish-a-shops-spec for the files a publish deletes: those it published earlier and no longer writes.
Star-imported by the feature's test module alone (adrs/0035). A published file left from earlier is put in the
directory as the publisher wrote it, its published-from line naming the artifact it came from, since kb gives an
artifact no new title: its old file is what a publish under its old title left."""
from pathlib import Path

from pytest_bdd import given, parsers, then

import spec_shop
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
