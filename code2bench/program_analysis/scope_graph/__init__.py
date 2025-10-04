from code2bench.config import config
from code2bench.program_analysis.scope_graph.scope_resolution.graph import ScopeGraph
from code2bench.utils.json_utils import load_json
from code2bench.program_analysis.scope_graph.build_scopes import build_scope_graph

keyword_and_builtin = load_json(config.KEYWORD_AND_BUILTIN_PATH)

def build_python_scope_graph(code: str):
    return build_scope_graph(bytearray(code, encoding="utf-8"), language="python")

def get_unresolved_refs(code: str) -> list:
    scope_graph = build_python_scope_graph(code)
    unresolved_refs = scope_graph.unresolved_refs_name()
    return list(set(unresolved_refs) - set(keyword_and_builtin["keyword_and_builtin"]))