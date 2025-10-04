from typing import List

def _apply_stops(text: str, stop: List[str]) -> str:
    if not text:
        return ""
    for s in stop or []:
        if s and s in text:
            return text.split(s, 1)[0].strip()
    return text.strip()