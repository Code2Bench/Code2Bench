import re
import ast

def parse_nested_str_list(input_string: str) -> object:
    try:
        # Add quotes around each word to ensure proper parsing
        quoted_string = re.sub(r'(\b\w+\b)', r'"\1"', input_string)
        return ast.literal_eval(quoted_string)
    except (ValueError, SyntaxError):
        return input_string