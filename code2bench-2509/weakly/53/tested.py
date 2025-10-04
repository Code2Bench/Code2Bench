import re
import unicodedata

def _normalize_name(name: str) -> str:
    name = name.strip()
    name = name.lower()
    name = unicodedata.normalize('NFKC', name)
    name = re.sub(r'[-]+', ' ', name)
    name = re.sub(r'\s+', ' ', name)
    return name