from typing import Any, Dict
from typing import Any, Callable, Dict, List, Optional, Union
import json

def _parse_json_fields(field: Any) -> Dict[str, Any]:
    """Parse a JSON field from the database, handling potential errors.

    Args:
        field: The field to parse, can be a string or dict

    Returns:
        Parsed dictionary or error dictionary if parsing fails
    """
    if isinstance(field, dict):
        return field
    if isinstance(field, str):
        try:
            return json.loads(field)
        except Exception as e:
            return {"error": f"Unable to parse {field}: {e}"}
    return {"error": f"Invalid {field} format"}