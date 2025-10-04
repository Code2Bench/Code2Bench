
import json
import re

def parse_mobile_response(response):
    pattern = r"Memory:(.*?)Reason:(.*?)Action:(.*)"
    match = re.search(pattern, response, re.DOTALL)
    if not match:
        return None

    memory = match.group(1).strip()
    reason = match.group(2).strip()
    action = match.group(3).strip()

    if "<|begin_of_box|>" in action:
        action = action[
            action.index("<|begin_of_box|>") + len("<|begin_of_box|>") : action.rindex(
                "<|end_of_box|>"
            )
        ]

    parsed_action = None
    if action.startswith("{"):
        parsed_action = json.loads(action)

    return {
        "memory": memory,
        "reason": reason,
        "action": action,
        "parsed_action": parsed_action,
    }