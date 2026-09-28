"""The layout of a content model's `sections`, shared by the renderers that publish prose: each section a heading and its
body, with the sections inside it a level down."""


def laid_out(sections: list[dict], level: int) -> list[str]:
    """Each section as its heading and its body, then the sections inside it a level down; the blocks are for the
    caller to join."""
    blocks = []
    for section in sections:
        blocks += [heading(level, section["title"]), section.get("body", "").rstrip()]
        blocks += laid_out(section.get("sections", []), level + 1)
    return blocks


def heading(level: int, title: str) -> str:
    """A heading at `level`, the title's trailing space not shown, so the line ends where its words end."""
    return f"{'#' * level} {title.rstrip(' ')}"
