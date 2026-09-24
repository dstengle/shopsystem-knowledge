"""Drive shop-knol the way a user does: a subprocess per command, YAML in files and on stdout."""
import subprocess
import sys

import yaml


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
    path.write_text(yaml.safe_dump(content, sort_keys=False, allow_unicode=True))
    result = knol(env, "create", type_name, "--from", str(path), "-m", message)
    assert result.returncode == 0, result.stderr
    return yaml.safe_load(result.stdout)["id"]
