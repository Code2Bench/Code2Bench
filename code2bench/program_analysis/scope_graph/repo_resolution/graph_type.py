from code2bench.program_analysis.scope_graph.scope_resolution.graph import Node
from code2bench.program_analysis.scope_graph.scope_resolution.graph_types import ScopeID

from enum import Enum
from typing import NewType
import os

from pydantic import root_validator


RepoNodeID = NewType("RepoNodeID", str)


class RepoNode(Node):
    repo_id: RepoNodeID
    name: str = None
    file_path: str = None
    scope: ScopeID = None

    @root_validator(pre=True)
    def validate_id(cls, values):
        repo_id = values.get("repo_id")
        parts = repo_id.split("::")

        if len(parts) != 2:
            raise ValueError(f"Invalid repo_id format: {repo_id}")

        filepath = parts[0]
        name = filepath.split(os.sep)[-1]

        values["name"] = name
        values["file_path"] = filepath
        values["scope"] = ScopeID(parts[1])
        return values

    def __str__(self):
        return f"{self.name}"


class EdgeKind(str, Enum):
    ImportToExport = "ImportToExport"
