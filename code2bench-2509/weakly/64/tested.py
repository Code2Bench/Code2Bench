import re
from typing import Dict, List

def parse_no_think(response: str, special_token_list: List[str] = None, action_sep: str = ',', max_actions: int = 3) -> Dict:
    format_correct = False
    llm_raw_response = response
    llm_response = ""
    think_content = ""
    action_content = ""
    actions = []

    # Check if the response strictly follows the expected format
    match = re.search(r'<answer>(.*?)</answer>', response, re.DOTALL)
    if match:
        action_content = match.group(1).strip()
        llm_response = f"<answer>{action_content}</answer>"
        format_correct = True
    else:
        return {
            "llm_raw_response": llm_raw_response,
            "llm_response": llm_response,
            "think_content": think_content,
            "action_content": action_content,
            "actions": actions,
            "format_correct": format_correct
        }

    # Remove special tokens if provided
    if special_token_list:
        for token in special_token_list:
            action_content = action_content.replace(token, "")

    # Split the action content into individual actions
    action_list = action_content.split(action_sep)
    actions = [action.strip() for action in action_list[:max_actions]]

    return {
        "llm_raw_response": llm_raw_response,
        "llm_response": llm_response,
        "think_content": think_content,
        "action_content": action_content,
        "actions": actions,
        "format_correct": format_correct
    }