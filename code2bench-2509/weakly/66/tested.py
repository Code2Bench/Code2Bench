import re
from typing import Dict, List

def parse_worldmodeling(response: str, special_token_list: List[str] = None, action_sep: str = ',', max_actions: int = 3) -> Dict:
    format_correct = False
    llm_raw_response = response
    llm_response = response
    
    # Check if the response follows the expected format
    pattern = r'<think>(.*?)</think><reasoning>(.*?)</reasoning><prediction>(.*?)</prediction><answer>(.*?)</answer>'
    match = re.search(pattern, llm_raw_response, re.DOTALL)
    
    if match:
        think_content = match.group(1).strip()
        reasoning_content = match.group(2).strip()
        prediction_content = match.group(3).strip()
        action_content = match.group(4).strip()
        format_correct = True
    else:
        think_content = ""
        reasoning_content = ""
        prediction_content = ""
        action_content = ""
    
    # Remove special tokens from action_content
    if special_token_list:
        for token in special_token_list:
            action_content = action_content.replace(token, "")
    
    # Split action_content into individual actions
    actions = []
    if action_content:
        action_list = action_content.split(action_sep)
        for action in action_list:
            action = action.strip()
            if action:
                actions.append(action)
    
    # Truncate actions to max_actions
    if len(actions) > max_actions:
        actions = actions[:max_actions]
    
    # Reconstruct the response with tags
    reconstructed_response = f"<think>{think_content}</think><reasoning>{reasoning_content}</reasoning><prediction>{prediction_content}</prediction><answer>{action_content}</answer>"
    
    return {
        "llm_raw_response": llm_raw_response,
        "llm_response": reconstructed_response,
        "think_content": think_content,
        "reasoning_content": reasoning_content,
        "prediction_content": prediction_content,
        "action_content": action_content,
        "actions": actions,
        "format_correct": format_correct
    }