from typing import List, Dict

def _clip(messages: List[Dict[str, str]], max_tokens: int) -> List[Dict[str, str]]:
    total_tokens = 0
    clipped_messages = []
    for message in reversed(messages):
        content = message.get("content")
        token_count = len(content) // 3 if content is not None else 0
        if total_tokens + token_count <= max_tokens:
            total_tokens += token_count
            clipped_messages.append(message)
        else:
            break
    return list(reversed(clipped_messages))