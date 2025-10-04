
import ast

def remove_main_block(source_code: str) -> str:
    """
    Remove the if __name__ == "__main__": block from the source code.
    """
    tree = ast.parse(source_code)
    lines = source_code.splitlines()

    # Find the main block and note its line numbers
    for node in tree.body:
        if isinstance(node, ast.If):
            test = node.test
            if (
                isinstance(test, ast.Compare)
                and isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
                and len(test.ops) == 1
                and isinstance(test.ops[0], ast.Eq)
                and len(test.comparators) == 1
                and isinstance(test.comparators[0], ast.Constant)
                and test.comparators[0].value == "__main__"
            ):

                # Remove lines corresponding to this block
                start_lineno = node.lineno - 1
                end_lineno = node.end_lineno
                return "\n".join(lines[:start_lineno] + lines[end_lineno:])

    return source_code