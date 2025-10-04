
import ast

import ast

def parse_assert_statement(statement):
    """Parse a Python assert statement and extract the expected output from the
    right side of the '==' operator as a string.

    :param statement: A string containing the assert statement.
    :return: The expected output from the assert statement as a string.
    """
    try:
        parsed = ast.parse(statement, mode="exec")
    except SyntaxError:
        return "Invalid syntax"

    if len(parsed.body) == 0:
        return "Empty statement"

    if not isinstance(parsed.body[0], ast.Assert):
        return "Not an assert statement"

    comparison = parsed.body[0].test

    if not isinstance(comparison, ast.Compare) or not isinstance(comparison.ops[0], ast.Eq):
        return "Not an equality assertion"

    # Extract and return the right side of the '==' operator as a string
    return ast.get_source_segment(statement, comparison.comparators[0])