"""The one exception every refusal travels in, kb's or shop-knol's own, before `cli`'s one printer shows it
(CLAUDE.md rule 4). Its own module so a concern that raises it never has to import `cli` to do so."""


class Refused(Exception):
    """A refusal on its way to the one printer: the faults to print, one line each."""

    def __init__(self, faults):
        super().__init__(faults)
        self.faults = list(faults)
