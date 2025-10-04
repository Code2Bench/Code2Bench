from dataclasses import dataclass
from pathlib import Path

from code2bench.program_analysis.scope_graph.repo_resolution.namespace import NameSpace
from code2bench.program_analysis.scope_graph.scope_resolution.graph_types import ScopeID


@dataclass
class Export:
    namespace: NameSpace
    scope_id: ScopeID
    file_path: Path
