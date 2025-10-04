from typing import Dict, List

from typing import List, Dict

def _validate_messages(messages: List[Dict[str, str]]) -> bool:
    if not messages:
        return False

    for msg in messages:
        if not isinstance(msg, dict):
            return False
        if 'role' not in msg or 'content' not in msg:
            return False
        if msg['role'] not in ['system', 'user', 'assistant']:
            return False
        if not isinstance(msg['content'], str):
            return False

    if messages[0]['role'] != 'system':
        return False

    return True