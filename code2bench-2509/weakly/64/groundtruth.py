from typing import Dict
import re
from typing import Dict, List

def parse_no_think(response: str, special_token_list=None, action_sep=',', max_actions=3) -> Dict:
    """
    Parse response in format: <answer>...</answer>

    Returns a dict with keys:
    - llm_raw_response: the original response
    - llm_response: the response with <answer> tag
    - think_content: empty string (no think content in this format)
    - action_content: the content inside <answer> tag
    - actions: a list of actions extracted from action_content
    - format_correct: whether the response strictly follows the expected format
    """
    response = response.replace("<image>", "")
    # Pattern to check for content strictly in the format <answer>...</answer>
    strict_pattern = r'^\s*<answer>(.*?)</answer>\s*$'
    strict_match = re.match(strict_pattern, response.strip(), re.DOTALL)
    format_correct = strict_match is not None

    # Pattern to extract content from answer tag
    extraction_pattern = r'<answer>(.*?)</answer>'
    match = re.search(extraction_pattern, response, re.DOTALL)
    # format_correct = match is not None

    if not strict_match:
        think_content, action_content, actions = "", "", []
    else:
        action_content = match.group(1)
        think_content = ""  # No think content in this format
        if special_token_list is not None:
            for special_token in special_token_list:
                action_content = action_content.replace(special_token, "").strip()
        actions = [action.strip() for action in action_content.split(action_sep) if action.strip()]
        if len(actions) > max_actions:
            actions = actions[:max_actions]
            action_content = (" " + action_sep + " ").join(actions)

    llm_response = "<answer>" + action_content.strip() + "</answer>"
    return {
        "llm_raw_response": response,
        "llm_response": llm_response,
        "think_content": think_content,
        "action_content": action_content,
        "actions": actions,
        "format_correct": format_correct
    }