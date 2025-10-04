import unicodedata

def normalize_unicode_homographs(text: str) -> str:
    normalized_text = unicodedata.normalize("NFKD", text)
    result = []
    for char in normalized_text:
        if ord(char) < 128:
            result.append(char)
    return ''.join(result)