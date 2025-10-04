
import unicodedata
import re

def _normalize_name(name: str):
    name = name.strip()
    name = name.lower().replace("-", " ")
    name = re.sub(" +", " ", name)
    return unicodedata.normalize("NFKD", name).lower()