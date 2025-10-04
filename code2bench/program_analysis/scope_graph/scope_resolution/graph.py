from networkx import DiGraph, dfs_postorder_nodes
from typing import Dict, Optional, Iterator, List, NewType, Tuple
from enum import Enum
from collections import defaultdict

from code2bench.program_analysis.scope_graph.graph import Node
from code2bench.program_analysis.scope_graph.utils import TextRange

from .imports import LocalImportStmt
from .definition import LocalDef
from .reference import Reference
from .scope import LocalScope, ScopeStack
from .graph_types import NodeKind, EdgeKind, ScopeNode, ScopeID


class ScopeGraph:
    def __init__(self, range: TextRange, src_bytes: bytearray = None):
        # TODO: put all this logic into a separate Graph class
        self._graph = DiGraph()
        self._node_counter = 0

        self.scope2range: Dict[ScopeID, TextRange] = {}

        root_scope = ScopeNode(range=range, type=NodeKind.SCOPE)
        self.root_idx = self.add_node(root_scope)
        self.scope2range[self.root_idx] = range
        self.src_bytes = src_bytes        
        self.unresolved_refs: List[Reference] = []

    def insert_local_scope(self, new: LocalScope):
        """
        Insert local scope to smallest enclosing parent scope
        """
        parent_scope = self.scope_by_range(new.range, self.root_idx)
        if parent_scope is not None:
            new_node = ScopeNode(range=new.range, type=NodeKind.SCOPE)
            new_id = self.add_node(new_node)
            self._graph.add_edge(new_id, parent_scope, type=EdgeKind.ScopeToScope)

            self.scope2range[new_id] = new.range

    def insert_local_import(self, new: LocalImportStmt):
        """
        Insert import into smallest enclosing parent scope
        """
        parent_scope = self.scope_by_range(new.range, self.root_idx)
        if parent_scope is not None:
            new_node = ScopeNode(
                range=new.range,
                type=NodeKind.IMPORT,
                data={
                    "from_name": new.from_name,
                    "aliases": new.aliases,
                    "names": new.names,
                },
            )

            new_id = self.add_node(new_node)
            self._graph.add_edge(new_id, parent_scope, type=EdgeKind.ImportToScope)

    def insert_local_def(self, new: LocalDef) -> None:
        """
        Insert a def into the scope-graph
        """
        defining_scope = self.scope_by_range(new.range, self.root_idx)
        if defining_scope is not None:
            new_def = ScopeNode(
                range=new.range,
                name=new.name,
                type=NodeKind.DEFINITION,
                data={"def_type": new.symbol},
            )
            new_idx = self.add_node(new_def)
            self._graph.add_edge(new_idx, defining_scope, type=EdgeKind.DefToScope)

    def insert_hoisted_def(self, new: LocalDef) -> None:
        """
        Insert a def into the scope-graph, at the parent scope of the defining scope
        """
        defining_scope = self.scope_by_range(new.range, self.root_idx)
        if defining_scope is not None:
            def_type = new.symbol
            new_def = ScopeNode(
                range=new.range,
                name=new.name,
                type=NodeKind.DEFINITION,
            )
            new_idx = self.add_node(new_def)

            # if the parent scope exists, insert this def there, if not,
            # insert into the defining scope
            parent_scope = self.parent_scope(defining_scope)
            target_scope = parent_scope if parent_scope is not None else defining_scope

            self._graph.add_edge(new_idx, target_scope, type=EdgeKind.DefToScope)

    def insert_global_def(self, new: LocalDef) -> None:
        """
        Insert a def into the scope-graph, at the root scope
        """
        new_def = ScopeNode(
            range=new.range,
            name=new.name,
            type=NodeKind.DEFINITION,
        )
        new_idx = self.add_node(new_def)
        self._graph.add_edge(new_idx, self.root_idx, type=EdgeKind.DefToScope)

    def insert_ref(self, new: Reference) -> None:
        possible_defs = []
        possible_imports = []

        local_scope_idx = self.scope_by_range(new.range, self.root_idx)
        if local_scope_idx is not None:
            # traverse the scopes from the current-scope to the root-scope
            for scope in self.parent_scope_stack(local_scope_idx):
                # # find candidate definitions in each scope
                # for local_def in [
                #     src
                #     for src, dst, attrs in self._graph.in_edges(scope, data=True)
                #     if attrs["type"] == EdgeKind.DefToScope
                # ]:
                for src, dst, attrs in self._graph.in_edges(scope, data=True):
                    if attrs["type"] == EdgeKind.DefToScope:
                        local_def = src
                        def_node = self.get_node(local_def)
                        if def_node.type == NodeKind.DEFINITION:
                            if new.name == def_node.name:
                                possible_defs.append((local_def, def_node.name))
                                break  # ensure that we add the first definition in the nearest ancestor scope

                # find candidate imports in each scope
                # TODO: fix this for new import names format
                for local_import in [
                    src
                    for src, dst, attrs in self._graph.in_edges(scope, data=True)
                    if attrs["type"] == EdgeKind.ImportToScope
                ]:
                    import_node = self.get_node(local_import)
                    if import_node.type == NodeKind.IMPORT:
                        if new.name in import_node.data["names"]:
                            possible_imports.append((local_import, import_node.name))

        # 如果没有找到可能的def或者import，这里就不会进来，所以这里可以修改一下方法。
        if possible_defs or possible_imports:
            # 最终在这里创建引用节点
            new_ref = ScopeNode(range=new.range, name=new.name, type=NodeKind.REFERENCE)
            ref_idx = self.add_node(new_ref)

            for def_idx, _ in possible_defs:
                self._graph.add_edge(ref_idx, def_idx, type=EdgeKind.RefToDef)

            for imp_idx, _ in possible_imports:
                self._graph.add_edge(ref_idx, imp_idx, type=EdgeKind.RefToImport)

            # add an edge back to the originating scope of the reference
            self._graph.add_edge(ref_idx, local_scope_idx, type=EdgeKind.RefToOrigin)
        # 不行，这样好像有问题
        else:
            self.unresolved_refs.append(new)

    # TODO: maybe we want to think about another class for sticking all these utility access methods
    def scopes(self) -> List[ScopeID]:
        """
        Return all scopes in the graph
        """
        return [
            u
            for u, attrs in self._graph.nodes(data=True)
            if attrs["type"] == NodeKind.SCOPE
        ]

    def imports(self, start: int) -> List[int]:
        """
        Get all imports in the scope
        """
        return [
            u
            for u, v, attrs in self._graph.in_edges(start, data=True)
            if attrs["type"] == EdgeKind.ImportToScope
        ]

    def get_all_imports(self) -> List[ScopeNode]:
        all_imports = []

        scopes = self.scopes()
        for scope in scopes:
            all_imports.extend([self.get_node(i) for i in self.imports(scope)])

        return all_imports

    def definitions(self, start: int) -> List[ScopeNode]:
        """
        Get all definitions in the scope and child scope
        """
        return [
            self.get_node(u)
            for u, v, attrs in self._graph.in_edges(start, data=True)
            if attrs["type"] == EdgeKind.DefToScope
        ]

    def get_all_definitions(self) -> List[ScopeNode]:
        all_defs = []

        scopes = self.scopes()
        for scope in scopes:
            all_defs.extend(self.definitions(scope))

        return all_defs

    def references_by_origin(self, start: int) -> List[int]:
        """
        Get all references in the scope and child scope
        """
        return [
            u
            for u, v, attrs in self._graph.in_edges(start, data=True)
            if attrs["type"] == EdgeKind.RefToOrigin
        ]

    def child_scopes(self, start: ScopeID) -> List[ScopeID]:
        """
        Get all child scopes of the given scope
        """
        return [
            u
            for u, v, attrs in self._graph.edges(data=True)
            if attrs["type"] == EdgeKind.ScopeToScope and v == start
        ]

    def parent_scope(self, start: ScopeID) -> Optional[ScopeID]:
        """
        Produce the parent scope of a given scope
        """
        if self.get_node(start).type == NodeKind.SCOPE:
            for src, dst, attrs in self._graph.out_edges(start, data=True):
                if attrs["type"] == EdgeKind.ScopeToScope:
                    return dst
        return None

    def scope_by_range(self, range: TextRange, start: ScopeID = None) -> ScopeID:
        """
        Returns the smallest child
        """
        # print(f"Finding scope by range: {range.line_range()}")
        node = self.get_node(start)
        # if node.range.contains_line(range):
        if node.range.contains(range):
            # print(f"Scope {node.range.line_range()} contains {range.line_range()}")
            for child_id, attrs in [
                (src, attrs)
                for src, dst, attrs in self._graph.in_edges(start, data=True)
                if attrs["type"] == EdgeKind.ScopeToScope
            ]:
                if child := self.scope_by_range(range, child_id):
                    return child
            return start

        return None

    def range_by_scope(self, scope: ScopeID) -> Optional[TextRange]:
        """
        Returns the range of a scope
        """
        return self.scope2range.get(scope, None)

    def child_scope_stack(self, start: ScopeID) -> List[ScopeID]:
        stack = self.child_scopes(start)

        for child in self.child_scopes(start):
            stack += self.child_scope_stack(child)

        return stack

    def get_leaf_children(self, start: ScopeID) -> Iterator[ScopeID]:
        """
        Finds all the leaf children reachable from the given scope
        """
        # Use DFS to find all reachable nodes
        for node in dfs_postorder_nodes(self._graph, start):
            if self._graph.out_degree(node) == 0:  # for directed graphs
                yield node

    def parent_scope_stack(self, start: ScopeID):
        """
        Returns stack of parent scope traversed
        """
        return ScopeStack(self._graph, start)

    def add_node(self, node: ScopeNode) -> int:
        """
        Adds node and increments node_counter for its id
        """
        id = self._node_counter
        self._graph.add_node(id, **node.dict())

        self._node_counter += 1

        return id

    def get_node(self, idx: int) -> ScopeNode:
        return ScopeNode(**self._graph.nodes(data=True)[idx])
    
    def find_definition(self, reference: Reference) -> Optional[ScopeNode]:
        possible_defs = []
        possible_imports = []

        local_scope_idx = self.scope_by_range(reference.range, self.root_idx)
        if local_scope_idx is not None:
            # 遍历从当前作用域到根作用域的所有父作用域
            for scope in self.parent_scope_stack(local_scope_idx):
                # 查找每个作用域中的候选定义
                for local_def in [
                    src
                    for src, dst, attrs in self._graph.in_edges(scope, data=True)
                    if attrs["type"] == EdgeKind.DefToScope
                ]:
                    def_node = self.get_node(local_def)
                    if def_node.type == NodeKind.DEFINITION and def_node.name == reference.name:
                        possible_defs.append(def_node)
                        break  # 在最近的祖先作用域找到第一个定义时停止

                # 查找每个作用域中的候选导入
                for local_import in [
                    src
                    for src, dst, attrs in self._graph.in_edges(scope, data=True)
                    if attrs["type"] == EdgeKind.ImportToScope
                ]:
                    import_node = self.get_node(local_import)
                    if import_node.type == NodeKind.IMPORT and reference.name in import_node.data["names"]:
                        possible_imports.append(import_node)

        # 如果找到了定义或导入，则返回第一个找到的定义
        if possible_defs:
            return possible_defs[0]
        elif possible_imports:
            return possible_imports[0]

        return None
    
    def find_all_external_references(scope_graph: "ScopeGraph") -> List[ScopeNode]:
        """
        Find all references in the graph that refer to external imports.
        """
        external_references = []
        
        # Step 1: Get all import nodes
        all_imports = scope_graph.get_all_imports()

        # Step 2: For each import, find references to it
        for import_node in all_imports:
            import_index = import_node.id  # Assuming ScopeNode has an `id` attribute
            
            # Find all references that point to this import
            references_to_import = [
                src for src, dst, attrs in scope_graph._graph.in_edges(import_index, data=True)
                if attrs["type"] == EdgeKind.RefToImport
            ]
            
            # Get the actual reference nodes
            for ref_index in references_to_import:
                ref_node = scope_graph.get_node(ref_index)
                external_references.append(ref_node)
        
        return external_references
    
    def unresolved_refs_name(self) -> List[str]:
        return [ref.name for ref in self.unresolved_refs]
    
    def find_unresolved_refs(self):
        for ref in self.unresolved_refs:
            name = ref.name
            print(f"name: {name}, text range: {ref.range.start_point, ref.range.end_point}")
        
    def span_select(self, *ranges: List[TextRange], indent=False):
        """
        Select the part of the file_content corresponding
        to the span of nodes. Warning: if you give this non-consecutive
        nodes, it will return the file contents spanning between the nodes

        Parameters
        ----------
        nodes : TreeSitter.Node
            arbitrary number of nodes to use to extract file_contents
        (optional)
        indent : True/False
            If true, adds spaces to indent beginning of node contents
            to match true file position. Useful for maintaining relative
            indentation in class methods, for example.

        Returns
        -------
        selection : str
            selection of self.file_contents spanning all the input nodes
        """
        if not ranges or not all(ranges):
            return ""

        start, end = ranges[0].start_byte, ranges[-1].end_byte
        select = self.src_bytes[start:end].decode("utf-8")
        if indent:
            return " " * ranges[0].start_point[1] + select
        return select

    def to_str(self):
        """
        A str representation of the graph
        """
        repr = "\n"

        for u, v, attrs in self._graph.edges(data=True):
            edge_type = attrs["type"]
            u_data = ""
            v_data = ""

            # if (
            #     edge_type == EdgeKind.RefToDef
            #     or edge_type == EdgeKind.RefToImport
            #     or EdgeKind.DefToScope
            # ):
            u_data = self.get_node(u)
            v_data = self.get_node(v)

            repr += f"Edge: {u}:{u_data.name}({self.span_select(u_data.range)})({u_data.range.start_point}, {u_data.range.end_point}) \
                \n--{edge_type}-> \n{v}:{v_data.name}({self.span_select(v_data.range)})({u_data.range.start_point}, {u_data.range.end_point})\n\n"

        return repr
