from typing import Any, Optional
import json
import re

def extract_json_from_string(s: str) -> Optional[Any]:
    """
    Searches for a JSON object within the string and returns the loaded JSON if found, otherwise returns None.
    """
    # Regex to find JSON objects (greedy, matches first { to last })
    match = re.search(r"\{.*\}", s, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    return None