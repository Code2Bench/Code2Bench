from typing import List
import ast

def _parse_options_string(options_string: str) -> List[str]:
    """Parse options from string representation of a list."""
    try:
        # Use ast.literal_eval for safe evaluation of string representations
        parsed_list = ast.literal_eval(options_string.strip())
        return [str(option).strip() for option in parsed_list]
    except (ValueError, SyntaxError):
        # If parsing fails, return empty list
        return []