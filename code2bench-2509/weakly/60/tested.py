import ast
import re

def extract_first_section_name_from_code(source_code: str) -> str | None:
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print':
            for arg in node.args:
                if isinstance(arg, ast.Str):
                    match = re.match(r'Section:\s*(.+)', arg.s)
                    if match:
                        return match.group(1)
    return None