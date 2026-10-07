"""The layout of a feature as Gherkin: its fields and its `scenarios` parts as the text of a `.feature` file, in two-space
indentation. A scenario's `formulates` and `uses` are links the file has no place for, so they are not written."""


def feature_file(name: str, title: str, narrator: str, content: dict) -> str:
    """The feature as a file formulated from the capability's page `name`: its Background where it has steps, then each
    scenario in the order it is held."""
    blocks = [f"# formulated from spec/capabilities/{name}.md\nFeature: {title}\n  Narrator: {narrator}"]
    if content.get("background"):
        blocks.append("\n".join(["  Background:", *_steps(content["background"])]))
    blocks += [_scenario(each) for each in content.get("scenarios", [])]
    return "\n\n".join(blocks) + "\n"


def _scenario(scenario: dict) -> str:
    keyword = "Scenario Outline" if scenario.get("examples") else "Scenario"
    lines = []
    if scenario.get("labels"):
        lines.append("  " + " ".join(scenario["labels"]))
    lines.append(f"  {keyword}: {scenario['title']}")
    lines += _indented(scenario.get("description", ""), 4)
    lines += _steps(scenario["steps"])
    if scenario.get("examples"):
        lines += ["", "    Examples:", *_table(scenario["examples"], 6)]
    return "\n".join(lines)


def _steps(steps: list[dict]) -> list[str]:
    lines = []
    for step in steps:
        lines.append(f"    {step['keyword']} {step['text']}")
        if step.get("table"):
            lines += _table(step["table"], 6)
        if "docstring" in step:
            lines += [" " * 6 + '"""', *_indented(step["docstring"], 6), " " * 6 + '"""']
    return lines


def _indented(text: str, width: int) -> list[str]:
    """The text's lines each indented, a blank line left empty."""
    return [" " * width + line if line else "" for line in text.rstrip("\n").split("\n")] if text else []


def _table(rows: list[list[str]], width: int) -> list[str]:
    """The rows with each column padded to its widest cell."""
    widest = [max(len(row[at]) for row in rows) for at in range(len(rows[0]))]
    return [" " * width + "| " + " | ".join(cell.ljust(widest[at]) for at, cell in enumerate(row)) + " |" for row in rows]
