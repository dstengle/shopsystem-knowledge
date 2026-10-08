"""What the steps of publish-a-shops-spec that publishing refuses share: the Then that finds a refusal by its reason
and names, and the capability and feature a refusal is made for. Imported plainly, never star-imported."""
import spec_shop
from driver import record


def lines_naming(result, reason, names):
    """The refusal is shop-knol's, as one line holding the reason and every one of the names."""
    assert result.returncode == 1 and result.stdout == "", (result.returncode, result.stdout)
    lines = [line for line in result.stderr.splitlines() if reason in line]
    assert any(all(name in line for name in names) for line in lines), result.stderr


def capability(env, tmp_path, shop, title, order=3):
    line = {"title": "Only line", "says": "When asked, it answers."}
    return spec_shop.put(env, tmp_path, "capability", title, shop=shop, gist="A capability.", behaviour=[line], order=str(order))


def feature_of(env, tmp_path, capability, title, scenario):
    return record(env, tmp_path, "feature", {"title": title, "formulates": capability, "scenarios": [{
        "title": f"{title}, as the user does it", "formulates": f"{capability}#behaviour/{spec_shop.line_id(env, capability, 'Only line')}",
        "steps": [{"keyword": "When", "text": "the user acts"}, {"keyword": "Then", "text": "the shelf is in order"}], **scenario}]},
        f"Formulate {title}")
