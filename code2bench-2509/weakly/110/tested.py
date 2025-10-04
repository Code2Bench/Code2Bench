import json
import ast

def parse_arguments(json_value: str) -> tuple:
    try:
        parsed = json.loads(json_value)
        return parsed, True
    except json.JSONDecodeError:
        try:
            parsed = ast.literal_eval(json_value)
            return parsed, True
        except (ValueError, SyntaxError):
            return json_value, False