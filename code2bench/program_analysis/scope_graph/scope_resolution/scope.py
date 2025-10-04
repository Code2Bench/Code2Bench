from dataclasses import dataclass
from typing import Optional, Iterator
from networkx import DiGraph
from enum import Enum

from code2bench.program_analysis.scope_graph.utils import TextRange

from .graph_types import EdgeKind


@dataclass
class LocalScope:
    range: TextRange

    def __init__(self, range: TextRange):
        self.range = range


class Scoping(str, Enum):
    GLOBAL = "global"
    HOISTED = "hoist"
    LOCAL = "local"


class ScopeStack(Iterator):
    def __init__(self, scope_graph: DiGraph, start: Optional[int]):
        self.scope_graph = scope_graph
        self.start = start

    def __iter__(self) -> "ScopeStack":
        return self

    # 妙啊，这个函数模拟了在程序执行时查找变量定义时的行为，从当前作用域逐层向外查找定义或导入。
    # TODO: fix the start parameter to return the root of the graph if not provided
    def __next__(self) -> int:
        if self.start is not None:
            original = self.start
            parent = None
            for _, target, attrs in self.scope_graph.out_edges(self.start, data=True):
                if (
                    attrs.get("type") == EdgeKind.ScopeToScope
                ):  # Replace with appropriate edge kind check
                    parent = target
                    break
            self.start = parent
            return original
        else:
            raise StopIteration
