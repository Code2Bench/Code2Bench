import unicodedata

def remove_symbols(s: str) -> str:
    normalized = unicodedata.normalize("NFKC", s)
    cleaned = ""
    for char in normalized:
        if unicodedata.category(char)[0] not in {"M", "P", "S"}:
            cleaned += char
        else:
            cleaned += " "
    return cleaned