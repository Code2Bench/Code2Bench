from typing import Any
import ast
import json

import json
import ast
from typing import Any

def parse_json_string_recursively(data: Any) -> Any:
    if isinstance(data, dict):
        return {k: parse_json_string_recursively(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [parse_json_string_recursively(item) for item in data]
    elif isinstance(data, tuple):
        return [parse_json_string_recursively(item) for item in data]
    elif isinstance(data, str):
        data = data.strip()
        if (data.startswith('{') and data.endswith('}')) or (data.startswith('[') and data.endswith(']')):
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                try:
                    return ast.literal_eval(data)
                except (SyntaxError, ValueError):
                    try:
                        fixed_str = data.replace("'", '"')
                        return json.loads(fixed_str)
                    except json.JSONDecodeError:
                        if data.count('}, {') > 0:
                            try:
                                wrapped_data = '[' + data + ']'
                                return json.loads(wrapped_data)
                            except json.JSONDecodeError:
                                return data
                        return data
        return data
    else:
        return data