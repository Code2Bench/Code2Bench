import json
import re
from typing import Dict, Any

def parse_llm_response(response: str) -> Dict[str, Any]:
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw_response": response}
    else:
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw_response": response}