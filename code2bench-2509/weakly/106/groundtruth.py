
import unicodedata

def detect_unicode_homographs(text: str) -> tuple[bool, str]:
    """
    Detect and normalize Unicode homograph characters used to bypass security checks.
    Returns (has_homographs, normalized_text)
    """
    # Common homograph replacements
    homograph_map = {
        # Cyrillic to Latin mappings
        '\u0430': 'a',  # Cyrillic а
        '\u0435': 'e',  # Cyrillic е  
        '\u043e': 'o',  # Cyrillic о
        '\u0440': 'p',  # Cyrillic р
        '\u0441': 'c',  # Cyrillic с
        '\u0443': 'y',  # Cyrillic у
        '\u0445': 'x',  # Cyrillic х
        '\u0410': 'A',  # Cyrillic А
        '\u0415': 'E',  # Cyrillic Е
        '\u041e': 'O',  # Cyrillic О
        '\u0420': 'P',  # Cyrillic Р
        '\u0421': 'C',  # Cyrillic С
        '\u0425': 'X',  # Cyrillic Х
        # Greek to Latin mappings
        '\u03b1': 'a',  # Greek α
        '\u03bf': 'o',  # Greek ο
        '\u03c1': 'p',  # Greek ρ
        '\u03c5': 'u',  # Greek υ
        '\u03c7': 'x',  # Greek χ
        '\u0391': 'A',  # Greek Α
        '\u039f': 'O',  # Greek Ο
        '\u03a1': 'P',  # Greek Ρ
    }

    # Check if text contains any homographs
    has_homographs = any(char in text for char in homograph_map)

    # Normalize the text
    normalized = text
    for homograph, replacement in homograph_map.items():
        normalized = normalized.replace(homograph, replacement)

    # Also normalize using Unicode NFKD
    normalized = unicodedata.normalize('NFKD', normalized)

    return (has_homographs, normalized)