import re
from typing import Dict, List

def parse_freethink(response: str, special_token_list: List[str] = None, action_sep: str = ',', max_actions: int = 3) -> Dict:
    # Remove <image> tags
    response = re.sub(r'<image>.*?</image>', '', response, flags=re.DOTALL)
    
    # Check if the response strictly follows the expected format
    format_correct = False
    pattern = r'</think><answer>(.*?)</answer>'
    match = re.search(pattern, response, re.DOTALL)
    
    if match:
        format_correct = True
        answer_content = match.group(1)
        think_content = response[:match.start()].strip()
        
        # Process answer content
        if special_token_list:
            for token in special_token_list:
                answer_content = answer_content.replace(token, '')
        
        # Split actions and limit to max_actions
        actions = [action.strip() for action in answer_content.split(action_sep) if action.strip()]
        actions = actions[:max_actions]
        
        # Prepare the result
        result = {
            "llm_raw_response": response,
            "llm_response": response,
            "think_content": think_content,
            "action_content": answer_content,
            "actions": actions,
            "format_correct": format_correct
        }
    else:
        result = {
            "llm_raw_response": response,
            "llm_response": response,
            "think_content": "",
            "action_content": "",
            "actions": [],
            "format_correct": False
        }
    
    return result