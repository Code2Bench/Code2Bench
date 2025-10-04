import textwrap
import ast

def _jupyterize(src: str) -> str:
    tree = ast.parse(src)
    last_node = tree.body[-1]
    if isinstance(last_node, ast.Expr):
        last_expr = last_node
        new_last_expr = ast.Expr(value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='print', ctx=ast.Load()),
                attr='flush',
                ctx=ast.Load()
            ),
            args=[last_expr.value],
            keywords=[]
        ))
        new_tree = ast.copy_location(ast.Module(body=tree.body[:-1] + [new_last_expr], type_ignores=tree.type_ignores), tree)
        return compile(new_tree, '<string>', 'exec')
    return src