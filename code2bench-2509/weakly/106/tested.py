import unicodedata

def detect_unicode_homographs(text: str) -> tuple[bool, str]:
    homograph_chars = {
        'ł': 'l', 'Ł': 'L', 'ø': 'o', 'Ø': 'O', 'þ': 't', 'Þ': 'T',
        'ð': 'd', 'Ð': 'D', 'ß': 'ss', 'ç': 'c', 'Ç': 'C', 'æ': 'ae', 'Æ': 'AE',
        'œ': 'oe', 'Œ': 'OE', 'ĳ': 'ij', 'Ĳ': 'IJ', 'ŋ': 'ng', 'Ŋ': 'NG',
        'ﬃ': 'ffi', 'ﬄ': 'ffl', 'ﬅ': 'ft', 'ﬆ': 'st'
    }
    has_homographs = False
    normalized_text = text
    for char, replacement in homograph_chars.items():
        if char in text:
            has_homographs = True
            normalized_text = normalized_text.replace(char, replacement)
    normalized_text = unicodedata.normalize('NFKD', normalized_text)
    return has_homographs, normalized_text