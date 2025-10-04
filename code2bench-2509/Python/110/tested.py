from typing import Dict, List, Any

def get_termination_value(item: Dict[str, Any]) -> str:
    termination = item.get('termination')
    
    if termination:
        return termination
    
    if 'messages' in item:
        last_message = item['messages'][-1]
        if 'max_turns_reached' in last_message:
            return 'max_turns_reached'
        if 'max_tokens_reached' in last_message:
            return 'max_tokens_reached'
        if '<answer>' in last_message.get('content') and '</answer>' in last_message.get('content'):
            return 'answered'
    
    return 'unknown'