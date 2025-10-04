from typing import Dict, List, Tuple
from tree_sitter_languages import get_language, get_parser

from code2bench.program_analysis.scope_graph.scope_resolution import LocalScope, LocalDef, Reference, Scoping
from code2bench.program_analysis.scope_graph.scope_resolution.imports import (
    LocalImportStmt,
    parse_from,
    parse_alias,
    parse_name,
)
from code2bench.program_analysis.scope_graph.utils import TextRange
from code2bench.program_analysis.scope_graph.languages import LANG_PARSER
from code2bench.program_analysis.scope_graph.scope_resolution.graph import ScopeGraph

from code2bench.program_analysis.scope_graph.ts.capture_types import (
    LocalDefCapture,
    LocalRefCapture,
    LocalImportPartCapture,
    ImportPartType,
)

from code2bench.program_analysis.scope_graph._config import PYTHON_SCM, JAVA_SCM

# 可扩展的命名空间定义
NAMESPACES = {
    "python": ["class", "function", "parameter", "variable"],
    "java": ["class", "method", "parameter", "variable"]  # Java支持
}

# 获取语言查询文件
def get_language_query_file(language: str) -> str:
    if language == "python":
        return PYTHON_SCM
    elif language == "java":
        return JAVA_SCM
    else:
        raise ValueError(f"Unsupported language: {language}")

# 构建查询
def build_query(file_content: bytearray, language: str) -> Tuple:
    try:
        language_sitter = get_language(language)
        parser = get_parser(language)
        query_file_path = get_language_query_file(language)
        query_file_content = open(query_file_path, "rb").read()
        
        root = parser.parse(file_content).root_node
        query = language_sitter.query(query_file_content)
        return query, root
    except Exception as e:
        raise RuntimeError(f"Failed to build query for language {language}: {e}")

# 构建作用域图
def build_scope_graph(src_bytes: bytearray, language: str = "python") -> ScopeGraph:
    query, root_node = build_query(src_bytes, language)
    
    local_def_captures: List[LocalDefCapture] = []
    local_ref_captures: List[LocalRefCapture] = []
    local_scope_capture_indices: List[int] = []
    local_import_stmt_capture_indices: List[int] = []
    local_import_part_captures: List[LocalImportPartCapture] = []

    capture_map: Dict[int, TextRange] = {}
    
    # 遍历查询的结果捕获
    for i, (node, capture_name) in enumerate(query.captures(root_node)):
        capture_map[i] = TextRange(
            start_byte=node.start_byte,
            end_byte=node.end_byte,
            start_point=node.start_point,
            end_point=node.end_point,
        )
        parts = capture_name.split(".")
        match parts:
            case [scoping, "definition", sym]:
                local_def_captures.append(LocalDefCapture(
                    index=i, symbol=sym, scoping=Scoping(scoping)))
            case [scoping, "definition"]:
                local_def_captures.append(LocalDefCapture(
                    index=i, symbol=None, scoping=Scoping(scoping)))
            case ["local", "reference"]:
                local_ref_captures.append(LocalRefCapture(index=i, symbol=None))
            case ["local", "scope"]:
                local_scope_capture_indices.append(i)
            case ["local", "import", "statement"]:
                local_import_stmt_capture_indices.append(i)
            case ["local", "import", part]:
                local_import_part_captures.append(LocalImportPartCapture(index=i, part=part))

    # 构建作用域图
    root_range = TextRange(
        start_byte=root_node.start_byte,
        end_byte=root_node.end_byte,
        start_point=root_node.start_point,
        end_point=root_node.end_point,
    )
    scope_graph = ScopeGraph(root_range, src_bytes=src_bytes)

    # 插入本地作用域
    for i in local_scope_capture_indices:
        scope_graph.insert_local_scope(LocalScope(capture_map[i]))

    # 插入导入语句
    for i in local_import_stmt_capture_indices:
        range = capture_map[i]
        from_name, aliases, names = "", [], []
        for part in local_import_part_captures:
            part_range = capture_map[part.index]
            if range.contains(part_range):
                match part.part:
                    case ImportPartType.MODULE:
                        from_name = parse_from(src_bytes, part_range)
                    case ImportPartType.ALIAS:
                        aliases.append(parse_alias(src_bytes, part_range))
                    case ImportPartType.NAME:
                        names.append(parse_name(src_bytes, part_range))

        import_stmt = LocalImportStmt(
            range, names, from_name=from_name, aliases=aliases
        )
        scope_graph.insert_local_import(import_stmt)

    # 插入定义
    for def_capture in local_def_captures:
        range = capture_map[def_capture.index]
        local_def = LocalDef(range, src_bytes, def_capture.symbol)
        match def_capture.scoping:
            case Scoping.GLOBAL:
                scope_graph.insert_global_def(local_def)
            case Scoping.HOISTED:
                scope_graph.insert_hoisted_def(local_def)
            case Scoping.LOCAL:
                scope_graph.insert_local_def(local_def)

    # 插入引用
    for local_ref_capture in local_ref_captures:
        range = capture_map[local_ref_capture.index]
        symbol_id = local_ref_capture.symbol if local_ref_capture.symbol in NAMESPACES[language] else None
        new_ref = Reference(range, src_bytes, symbol_id=symbol_id)
        scope_graph.insert_ref(new_ref)

    return scope_graph

"""
from typing import Dict, Optional, List
from tree_sitter_languages import get_language, get_parser

from autocodebench.program_analysis.scope_graph.scope_resolution import LocalScope, LocalDef, Reference, Scoping
from autocodebench.program_analysis.scope_graph.scope_resolution.imports import (
    LocalImportStmt,
    parse_from,
    parse_alias,
    parse_name,
)
from autocodebench.program_analysis.scope_graph.utils import TextRange
from autocodebench.program_analysis.scope_graph.languages import LANG_PARSER
from autocodebench.program_analysis.scope_graph.scope_resolution.graph import ScopeGraph

from autocodebench.program_analysis.scope_graph.ts.capture_types import (
    LocalDefCapture,
    LocalRefCapture,
    LocalImportPartCapture,
    ImportPartType,
)

from autocodebench.program_analysis.scope_graph.config import PYTHON_SCM

# TODO: make this a part of TSLangConfig
namespaces = ["class", "function", "parameter", "variable"]

def build_query(file_content: bytearray, query_file: str):
    language = get_language("python")
    parser = get_parser("python")
    
    query_file = open(PYTHON_SCM, "rb").read()
        
    root = parser.parse(file_content).root_node
    # Run the tags queries
    query = language.query(query_file)
    
    return query, root

# TODO: Add support for Java.
def build_scope_graph(src_bytes: bytearray, language: str = "python") -> ScopeGraph:
    # parser = LANG_PARSER[language]
    # query, root_node = parser._build_query(src_bytes, PYTHON_SCM)
    
    query, root_node = build_query(src_bytes, PYTHON_SCM)

    local_def_captures: List[LocalDefCapture] = []
    local_ref_captures: List[LocalRefCapture] = []
    local_scope_capture_indices: List = []
    local_import_stmt_capture_indices: List = []
    local_import_part_capture: List[LocalImportPartCapture] = []
    local_definition_list_comprehension: List[LocalDefCapture] = []

    # capture_id -> range map
    capture_map: Dict[int, TextRange] = {}
    
    # 这里我可以自己定义啊，查询。找到单测，还有 方法。
    for i, (node, capture_name) in enumerate(query.captures(root_node)):
        capture_map[i] = TextRange(
            start_byte=node.start_byte,
            end_byte=node.end_byte,
            start_point=node.start_point,
            end_point=node.end_point,
        )

        parts = capture_name.split(".")
        # print(node, capture_name, parts)
        match parts:
            # case [scoping, "definition", "list", "comprehension"]:
            #     index = i
            #     symbol = sym
            #     scoping_enum = Scoping(Scoping.HOISTED)

            #     l = LocalDefCapture(
            #         index=index,
            #         symbol=symbol,
            #         scoping=scoping_enum,
            #     )
            #     local_def_captures.append(l)
            case [scoping, "definition", sym]:
                index = i
                symbol = sym
                scoping_enum = Scoping(scoping)

                l = LocalDefCapture(
                    index=index,
                    symbol=symbol,
                    scoping=scoping_enum,
                )
                local_def_captures.append(l)
            case [scoping, "definition"]:
                index = i
                symbol = None
                scoping_enum = Scoping(scoping)

                l = LocalDefCapture(
                    index=index,
                    symbol=symbol,
                    scoping=scoping_enum,
                )
                local_def_captures.append(l)
            # TODO: confirm never used and delete
            # case ["local", "reference", sym]:
            #     index = i
            #     symbol = sym

            #     l = LocalRefCapture(index=index, symbol=symbol)
            #     local_ref_captures.append(l)
            case ["local", "reference"]:
                index = i
                symbol = None

                l = LocalRefCapture(index=index, symbol=symbol)
                local_ref_captures.append(l)
            case ["local", "scope"]:
                local_scope_capture_indices.append(i)
            case ["local", "import", "statement"]:
                local_import_stmt_capture_indices.append(i)
            case ["local", "import", part]:
                l = LocalImportPartCapture(index=i, part=part)
                local_import_part_capture.append(l)
            

    root_range = TextRange(
        start_byte=root_node.start_byte,
        end_byte=root_node.end_byte,
        start_point=root_node.start_point,
        end_point=root_node.end_point,
    )
    scope_graph = ScopeGraph(root_range, src_bytes=src_bytes)

    # insert scopes first
    for i in local_scope_capture_indices:
        scope_graph.insert_local_scope(LocalScope(capture_map[i]))

    # insert imports
    for i in local_import_stmt_capture_indices:
        range = capture_map[i]
        from_name, aliases, names = "", [], []
        for part in local_import_part_capture:
            part_range = capture_map[part.index]
            if range.contains(part_range):
                match part.part:
                    case ImportPartType.MODULE:
                        from_name = parse_from(src_bytes, part_range)
                    case ImportPartType.ALIAS:
                        aliases.append(parse_alias(src_bytes, part_range))
                    case ImportPartType.NAME:
                        names.append(parse_name(src_bytes, part_range))

        import_stmt = LocalImportStmt(
            range, names, from_name=from_name, aliases=aliases
        )
        scope_graph.insert_local_import(import_stmt)

    # insert defs
    for def_capture in local_def_captures:
        range = capture_map[def_capture.index]
        local_def = LocalDef(range, src_bytes, def_capture.symbol)
        match def_capture.scoping:
            case Scoping.GLOBAL:
                scope_graph.insert_global_def(local_def)
            case Scoping.HOISTED:
                scope_graph.insert_hoisted_def(local_def)
            case Scoping.LOCAL:
                scope_graph.insert_local_def(local_def)

    # insert refs
    for local_ref_capture in local_ref_captures:
        index = local_ref_capture.index
        symbol = local_ref_capture.symbol

        range = capture_map[index]
        # if the symbol is present, is it one of the supported symbols for this language?
        symbol_id = symbol if symbol in namespaces else None
        new_ref = Reference(range, src_bytes, symbol_id=symbol_id)

        scope_graph.insert_ref(new_ref)

    return scope_graph
"""