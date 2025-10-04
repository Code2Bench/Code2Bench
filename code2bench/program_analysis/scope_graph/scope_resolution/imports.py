from dataclasses import dataclass, asdict
from typing import Optional, List

from code2bench.program_analysis.scope_graph.utils import TextRange

from .graph_types import NodeKind


def parse_from(buffer: bytearray, range: TextRange) -> str:
    return buffer[range.start_byte : range.end_byte].decode("utf-8")


def parse_alias(buffer: bytearray, range: TextRange):
    return buffer[range.start_byte : range.end_byte].decode("utf-8")


def parse_name(buffer: bytearray, range: TextRange):
    return buffer[range.start_byte : range.end_byte].decode("utf-8")


class LocalImportStmt:
    """
    Represents a local import statement of the form:

    from <from_names> import <names> as <alias>
    from module import name1, name2, name3 as alias
    """

    def __init__(
        self,
        range: TextRange,
        names: List[str],
        from_name: Optional[str] = "",
        aliases: Optional[List[str]] = [],
    ):
        self.range = range
        self.names = names
        self.from_name = from_name
        self.aliases = aliases

    # Technically, this is the only python specific method
    def __str__(self):
        from_name = f"from {self.from_name} " if self.from_name else ""
        # TODO: fix this
        alias_str = f" as {self.aliases}" if self.aliases else ""

        names = ", ".join(self.names)

        return f"{from_name}import {names}{alias_str}"
