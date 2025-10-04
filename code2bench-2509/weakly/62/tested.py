import ast

def remove_main_block(source_code: str) -> str:
    tree = ast.parse(source_code)
    main_block = None
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            if isinstance(node.test, ast.Compare):
                left = node.test.left
                if isinstance(left, ast.Name) and left.id == "__name__":
                    ops = node.test.ops
                    if len(ops) == 1 and isinstance(ops[0], ast.Eq):
                        right = ops[0].right
                        if isinstance(right, ast.Str) and right.s == "__main__":
                            main_block = node
                            break
    if main_block:
        new_tree = ast.Module(body=[n for n in tree.body if n is not main_block])
        return ast.unparse(new_tree)
    return source_code