import json
import re
from typing import Any, Optional

def extract_json_from_string(s: str) -> Optional[Any]:
    match = re.search(r'\{(?:[^{}]|(?R))*\}', s)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return None