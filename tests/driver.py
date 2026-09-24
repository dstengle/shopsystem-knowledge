"""Drive shop-knol the way a user does: a subprocess per command, YAML in files and on stdout."""
import subprocess
import sys

from kb.content import dumps, loads


def knol(env, *args):
    return subprocess.run(
        [sys.executable, "-m", "shop_knowledge", *args],
        env=env, capture_output=True, text=True,
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


def refused_plainly(result):
    """Refused in plain words: something said on stderr, no traceback anywhere, nothing on stdout."""
    assert result.stderr.strip(), "nothing was said"
    assert "Traceback" not in result.stderr + result.stdout, result.stderr
    assert result.stdout == ""


def reported_failure(result):
    assert result.returncode != 0, result.stdout
