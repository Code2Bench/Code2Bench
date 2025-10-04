from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path

from code2bench.program_analysis.scope_graph.scope_resolution.graph import ScopeGraph
from code2bench.program_analysis.scope_graph.scope_resolution.imports import LocalImportStmt
from code2bench.program_analysis.scope_graph.repo_resolution.namespace import NameSpace
from code2bench.program_analysis.scope_graph.fs import RepoFs
from code2bench.program_analysis.scope_graph.utils import SysModules, ThirdPartyModules

import logging

logger = logging.getLogger(__name__)


class ModuleType(str, Enum):
    # a local package
    LOCAL = "local"
    # system/core lib
    SYS = "sys"
    # third party lib
    THIRD_PARTY = "third_party"
    UNKNOWN = "unknown"


@dataclass
class LocalImport:
    """
    This represents a single Import that is the result of joining
    from_name and names in LocalImportStmt
    """

    namespace: NameSpace
    module_type: ModuleType
    filepath: Path
    # only for ModuleType.LOCAL
    import_path: Optional[Path] = None
    # if this import is defined in a scope
    ref_scopes: Optional[int] = field(default_factory=list)

    def __str__(self):
        return f"{self.namespace} {self.module_type} {self.import_path}"


def import_stmt_to_import(
    import_stmt: LocalImportStmt,
    filepath: Path,
    g: ScopeGraph,
    fs: RepoFs,
    sys_modules: SysModules,
    third_party_modules: ThirdPartyModules,
) -> List[LocalImport]:
    """
    Convert an import statement, which may hold multiple imports
    """
    imports = []
    namespaces = []

    logger.debug(f"Finding imports for file: {filepath}")
    # from foo.bar import baz
    # root_ns = foo.bar
    # name = baz
    # namespaces = [foo.bar.baz]

    if import_stmt.from_name:
        root = import_stmt.from_name
        for name in import_stmt.names:
            namespaces += [NameSpace(root, child=name)]

    else:
        namespaces = [NameSpace(n) for n in import_stmt.names]

    # resolve module type
    import_path = None
    for ns in namespaces:
        if ns.root in sys_modules:
            module_type = ModuleType.SYS
        elif ns.root in third_party_modules:
            module_type = ModuleType.THIRD_PARTY
        elif import_path := fs.match_file(ns.to_path()):
            module_type = ModuleType.LOCAL
        else:
            module_type = ModuleType.UNKNOWN

        # resolve refs to this import
        ref_scopes = []
        for scope in g.scopes():
            for ref in g.references_by_origin(scope):
                ref_node = g.get_node(ref)
                if ref_node.name == ns.child:
                    ref_scopes.append(scope)

        imports.append(
            LocalImport(
                ns,
                module_type,
                filepath,
                import_path=import_path,
                ref_scopes=ref_scopes,
            )
        )

    return imports
