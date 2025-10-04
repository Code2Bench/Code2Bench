import ast

def remove_function(source_code: str, function_name: str) -> str:
    tree = ast.parse(source_code)
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    function_to_remove = next((func for func in functions if func.name == function_name), None)
    
    if function_to_remove:
        parent = function_to_remove.parent
        if isinstance(parent, ast.Module):
            parent.body = [node for node in parent.body if node is not function_to_remove]
        elif isinstance(parent, ast.ClassDef):
            parent.body = [node for node in parent.body if node is not function_to_remove]
    
    return ast.unparse(tree)