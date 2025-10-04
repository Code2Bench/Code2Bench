import unicodedata

def _normalize_text(s: str) -> str:
    return unicodedata.normalize('NFKC', s.strip())