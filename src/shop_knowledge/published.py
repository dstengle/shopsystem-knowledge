"""What a publish leaves in the directory it publishes into: the files a renderer gave back, written, and, for a
shop's spec, the files it published earlier under `spec/capabilities/`, `features/` and `adrs/` that it no longer
writes, deleted. A file there is one it published when it carries the published-from line where the publisher puts
it: its first line, or the line directly after its frontmatter. Nothing else in the directory is ever deleted.

Only the spec renderer deletes: every other renderer's publish only writes, so publishing one artifact into a shop's
repository never takes away the spec published there."""
from pathlib import Path

from kb.contract import kb_pb2

from shop_knowledge import refusal
from shop_knowledge.renderers import published_from

_CLEARED = {"spec": ("spec/capabilities", "features", "adrs")}
"""The renderers whose publish deletes what it no longer writes, and the directories, under the one asked for, whose
files it reads; a renderer not named here deletes nothing."""


def publish(renderer: str, files: dict[str, str], directory: Path) -> None:
    """The files written, then the files `renderer` published earlier and no longer writes deleted, found before
    anything is written so a file that cannot be read stops the publish before it changes the directory."""
    stale = _stale(_CLEARED.get(renderer, ()), files, directory)
    _write(files, directory)
    for path in stale:
        path.unlink()


def _write(files: dict[str, str], directory: Path) -> None:
    """Each file at its path under the directory asked for."""
    for relative, content in files.items():
        path = directory / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def _stale(cleared: tuple[str, ...], files: dict[str, str], directory: Path) -> list[Path]:
    """The regular files directly in each of the `cleared` directories that carry the published-from line and are not
    among `files`; a cleared directory that is a link elsewhere, or sits under one, has none considered."""
    written = {directory / relative for relative in files}
    found = [path for each in cleared if _within(directory, each) for path in sorted((directory / each).glob("*"))]
    return [path for path in found if path.is_file() and not path.is_symlink() and path not in written and _published(path)]


def _within(directory: Path, cleared: str) -> bool:
    """Whether the cleared directory, once its links are followed, is the one at its name under the directory asked
    for, so a link out of the directory never has files elsewhere deleted."""
    return (directory / cleared).resolve() == directory.resolve() / cleared


def _published(path: Path) -> bool:
    """Whether the file carries the published-from line where the publisher puts it; a file that is not UTF-8 text
    does not; a file that cannot be read stops the publish, for it cannot be told whether it was published."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return False
    except OSError as error:
        raise refusal.Refused([kb_pb2.Fault(artifact=str(path), message="cannot be read, so publishing cannot tell whether to delete it")]) from error
    if lines[:1] == ["---"] and "---" in lines[1:]:
        lines = lines[lines.index("---", 1) + 1:]
    return bool(lines) and published_from.is_line(lines[0])
