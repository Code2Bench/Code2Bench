from typing import List, Dict

def _validate_messages(messages: List[Dict[str, str]]) -> bool:
    if not messages:
        return False
    
    for message in messages:
        if 'role' not in message or message['role'] not in ['system', 'user', 'assistant']:
            return False
        
        if not isinstance(message['content'], str):
            return False
    
    if not messages or messages[0]['role'] != 'system':
        return False
    
    return True