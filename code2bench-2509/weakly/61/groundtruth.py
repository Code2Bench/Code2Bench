
import ast

def remove_function(source_code: str, function_name: str) -> str:
    """
    Remove a function definition from the source code.
    """
    tree = ast.parse(source_code)
    lines = source_code.splitlines()

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            start_lineno = node.lineno - 1
            end_lineno = node.end_lineno
            return "\n".join(lines[:start_lineno] + lines[end_lineno:])

    return source_code