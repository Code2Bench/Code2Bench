from typing import List

def _apply_stops(text: str, stop: List[str]) -> str:
    if not text:
        return ""
    
    for word in stop:
        if word in text:
            return text[:text.index(word)].strip()
    
    return text.strip()