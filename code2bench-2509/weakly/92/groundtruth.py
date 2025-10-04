
import textwrap
import ast

def _jupyterize(src: str) -> str:
    src = textwrap.dedent(src)
    tree = ast.parse(src, mode="exec")

    if tree.body and isinstance(tree.body[-1], ast.Expr):
        # Extract the last expression
        last = tree.body.pop()
        body_code = ast.unparse(ast.Module(tree.body, []))
        expr_code = ast.unparse(last.value)  # type: ignore
        # Display the last expression value like Jupyter does
        return f"{body_code}\n_ = {expr_code}\nif _ is not None: print(_)"
    else:
        return src