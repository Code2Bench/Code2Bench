import re
from typing import Dict, List

def parse_grounding(response: str, special_token_list: List[str] = None, action_sep: str = ',', max_actions: int = 3) -> Dict:
    format_correct = False
    pattern = r'<observation>(.*?)</observation><reasoning>(.*?)</reasoning></think><answer>(.*?)</answer>'
    match = re.search(pattern, response, re.DOTALL)
    
    if match:
        observation_content = match.group(1).strip()
        reasoning_content = match.group(2).strip()
        action_content = match.group(3).strip()
        
        # Clean content by removing special tokens
        if special_token_list:
            for token in special_token_list:
                observation_content = observation_content.replace(token, '')
                reasoning_content = reasoning_content.replace(token, '')
                action_content = action_content.replace(token, '')
        
        # Extract actions from answer content
        actions = [action.strip() for action in action_content.split(action_sep)][:max_actions]
        
        # Reconstruct the response with tags
        llm_response = f"<observation>{observation_content}</observation><reasoning>{reasoning_content}</reasoning>