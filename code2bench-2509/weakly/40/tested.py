import ast

def clean_if_name(code: str) -> str:
    try:
        tree = ast.parse(code)
        last_node = tree.body[-1]
        if isinstance(last_node, ast.If):
            test = last_node.test
            if isinstance(test, ast.Compare) and isinstance(test.left, ast.Name) and test.left.id == '__name__':
                if len(test.ops) == 1 and isinstance(test.ops[0], ast.Eq) and len(test.comparators) == 1:
                    if isinstance(test.comparators[0], ast.Str) and test.comparators[0].s == '__main__':
                        # Remove the if condition and keep the body
                        new_body = [ast.Expression(body=node) for node in last_node.body]
                        new_tree = ast.Module(body=new_body, type_ignores=tree.type_ignores)
                        return ast.unparse(new_tree)
        return code
    except:
        return code