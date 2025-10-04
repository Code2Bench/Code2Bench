from typing import Optional

def _truncate(value: str, max_chars: Optional[int], ellipsis: str) -> str:
    if max_chars is None:
        return value
    
    if max_chars <= 0:
        return ""
    
    if len(value) <= max_chars:
        return value
    
    return value[:max_chars - len(ellipsis)] + ellipsis