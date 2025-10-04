import ast

def parse_assert_statement(statement: str) -> str:
    try:
        tree = ast.parse(statement, mode='eval')
        if not isinstance(tree.body, ast.Expression):
            return "Invalid assert statement format."
        expr = tree.body
        if not isinstance(expr, ast.Compare):
            return "Assert statement does not contain a comparison."
        if len(expr.ops) != 1 or not isinstance(expr.ops[0], ast.Eq):
            return "Assert statement does not use '==' for comparison."
        left = expr.left
        right = expr.comparators[0]
        if not isinstance(right, ast.Str):
            return "Right side of '==' is not a string."
        return f"'{right.s}'"
    except SyntaxError:
        return "Invalid Python syntax in the assert statement."