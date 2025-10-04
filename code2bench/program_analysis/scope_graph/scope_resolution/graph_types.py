from typing import Dict, Optional, NewType
from enum import Enum

from code2bench.program_analysis.scope_graph.graph import Node
from code2bench.program_analysis.scope_graph.utils import TextRange


class NodeKind(str, Enum):
    SCOPE = "LocalScope"
    DEFINITION = "LocalDef"
    IMPORT = "Import"
    REFERENCE = "Reference"


class EdgeKind(str, Enum):
    ScopeToScope = "ScopeToScope"
    DefToScope = "DefToScope"
    ImportToScope = "ImportToScope"
    RefToDef = "RefToDef"
    RefToOrigin = "RefToOrigin"
    RefToImport = "RefToImport"


class ScopeNode(Node):
    range: TextRange
    type: NodeKind
    name: Optional[str] = ""
    data: Optional[Dict] = {}


ScopeID = NewType("ScopeID", int)
