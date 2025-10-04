from typing import Optional
from dataclasses import dataclass

from code2bench.program_analysis.scope_graph.utils import SymbolId, TextRange


@dataclass
class Reference:
    range: TextRange
    symbol_id: Optional[SymbolId]

    def __init__(
        self, range: TextRange, buffer: bytearray, symbol_id: Optional[SymbolId] = None
    ) -> "Reference":
        self.range = range
        self.symbol_id = symbol_id
        self.name = buffer[self.range.start_byte : self.range.end_byte].decode("utf-8")
