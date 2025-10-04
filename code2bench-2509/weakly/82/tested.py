import re
import json
from typing import Tuple

def _parse_tool_call(action: str) -> Tuple[str, bool]:
    tool_call_pattern = r"<tool_call>(.*?)</tool_call>"
    match = re.search(tool_call_pattern, action, re.DOTALL)
    if not match:
        return action, False
    
    tool_content = match.group(1).strip()
    try:
        tool_name, params = tool_content.split("(", 1)
        params = params.rstrip(")")
        params = json.loads(params)
        parsed_action = json.dumps({"tool": tool_name, "params": params})
        return parsed_action, True
    except (ValueError, json.JSONDecodeError):
        return action, False