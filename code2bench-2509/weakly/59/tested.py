import ast
from typing import Optional

def extract_function_body(source_code: str, function_name: str) -> Optional[str]:
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            body_lines = []
            for stmt in node.body:
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Str):
                    body_lines.append(stmt.value.s)
            return '\n'.join(body_lines)
    return None