import re
import json

def parse_mobile_response(response: str) -> dict:
    pattern = r'<\|Memory\|>(.*?)<\|Reason\|>(.*?)<\|Action\|>(.*?)<\|end_of_box\|>'
    match = re.search(pattern, response, re.DOTALL)
    if not match:
        return None
    memory, reason, action = match.groups()
    action = action.replace('<|begin_of_box|>', '').replace('<|end_of_box|>', '')
    parsed_action = None
    if action.startswith('{'):
        try:
            parsed_action = json.loads(action)
        except json.JSONDecodeError:
            pass
    return {
        'memory': memory,
        'reason': reason,
        'action': action,
        'parsed_action': parsed_action
    }