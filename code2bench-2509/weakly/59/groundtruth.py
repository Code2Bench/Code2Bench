from typing import Optional
import ast

def extract_function_body(source_code: str, function_name: str) -> Optional[str]:
    """
    Extracts the body of a function from the source code.
    Returns None if the function is not found.

    Assumption: The function is multiline and defined at the top level.
    """
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            lines = source_code.splitlines()
            start = node.body[0].lineno
            end = node.body[-1].end_lineno
            body_lines = lines[start - 1 : end]
            indent_level = len(body_lines[0]) - len(body_lines[0].lstrip())
            return "\n".join(line[indent_level:] for line in body_lines)
    return None