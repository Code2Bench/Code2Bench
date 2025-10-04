from dataclasses import dataclass
from typing import Optional

from code2bench.program_analysis.scope_graph.utils import TextRange

from .graph_types import NodeKind


@dataclass
class LocalDef:
    range: TextRange
    symbol: str
    name: str

    def __init__(
        self, range: TextRange, buffer: bytearray, symbol: Optional[str]
    ) -> "LocalDef":
        self.range = range
        self.symbol = symbol
        self.name = buffer[self.range.start_byte : self.range.end_byte].decode("utf-8")

    def to_node(self):
        return {
            "name": self.name,
            "range": self.range.dict(),
            "type": NodeKind.DEFINITION,
            "data": {"def_type": self.symbol},
        }
