import ast
from typing import List

def _parse_options_string(options_string: str) -> List[str]:
    try:
        parsed = ast.literal_eval(options_string)
        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed]
        else:
            return []
    except (ValueError, SyntaxError):
        return []