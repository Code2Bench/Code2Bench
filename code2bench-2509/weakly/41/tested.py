import unicodedata

def find_special_unicode(s: str) -> dict:
    result = {}
    for char in s:
        if ord(char) > 127:
            code_point = f"U+{ord(char):04X}"
            category = unicodedata.category(char)
            result[char] = f"{code_point} ({category})"
    return result