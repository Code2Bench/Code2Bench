from code2bench.program_analysis.scope_graph._config import NAMESPACE_DELIMETERS, LANGUAGE
from pathlib import Path

delimiter = NAMESPACE_DELIMETERS[LANGUAGE]


class NameSpace:
    def __init__(self, parent: str, child: str = ""):
        self.parent = parent.split(delimiter)
        self._child = child.split(delimiter)

    def to_path(self):
        return Path(*self.parent)

    @property
    def root(self):
        return self.parent[0]

    @property
    def child(self):
        return self._child[-1]

    def __hash__(self):
        return hash(tuple(self.parent, self._child))

    def __str__(self):
        return delimiter.join(self.parent + self._child)
