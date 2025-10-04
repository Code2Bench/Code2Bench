import ast

def parse_function_arguments(source_code: str, tool_name: str) -> list:
    tree = ast.parse(source_code)
    arguments = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == tool_name:
            for arg in node.args.args:
                arguments.append(arg.arg)
            break
    return arguments