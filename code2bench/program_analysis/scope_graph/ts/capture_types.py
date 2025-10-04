from pydantic import BaseModel
from typing import Optional
from enum import Enum

from code2bench.program_analysis.scope_graph.scope_resolution import Scoping


class LocalDefCapture(BaseModel):
    index: int
    symbol: Optional[str]
    scoping: Scoping


class LocalRefCapture(BaseModel):
    index: int
    symbol: Optional[str]


class ImportPartType(str, Enum):
    MODULE = "module"
    ALIAS = "alias"
    NAME = "name"


class LocalImportPartCapture(BaseModel):
    index: int
    part: str
