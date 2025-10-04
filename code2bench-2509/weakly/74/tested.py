from typing import Any, Dict
import json

def _parse_json_fields(field: Any) -> Dict[str, Any]:
    if isinstance(field, dict):
        return field
    elif isinstance(field, str):
        try:
            return json.loads(field)
        except (json.JSONDecodeError, ValueError):
            return {"error": "Failed to parse JSON"}
    else:
        return {"error": "Invalid format"}