import json
import ast
from typing import Any

def parse_json_string_recursively(data: Any) -> Any:
    if isinstance(data, (str, bytes)):
        try:
            # Try to parse as JSON
            return json.loads(data)
        except json.JSONDecodeError:
            try:
                # Try to parse using ast.literal_eval
                return ast.literal_eval(data)
            except (ValueError, SyntaxError):
                # Attempt additional fixes
                data = data.replace("'", '"')
                if data.startswith('{') and data.endswith('}'):
                    try:
                        return json.loads(data)
                    except json.JSONDecodeError:
                        try:
                            return ast.literal_eval(data)
                        except (ValueError, SyntaxError):
                            return data
                elif data.startswith('[') and data.endswith(']'):
                    try:
                        return json.loads(data)
                    except json.JSONDecodeError:
                        try:
                            return ast.literal_eval(data)
                        except (ValueError, SyntaxError):
                            return data
                else:
                    return data
    elif isinstance(data, (list, tuple)):
        return type(data)(parse_json_string_recursively(item) for item in data)
    elif isinstance(data, dict):
        return {key: parse_json_string_recursively(value) for key, value in data.items()}
    else:
        return data