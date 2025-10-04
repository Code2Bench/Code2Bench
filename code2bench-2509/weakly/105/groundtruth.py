
import unicodedata

def normalize_unicode_homographs(text: str) -> str:
    """
    Normalize Unicode homograph characters to their ASCII equivalents.
    This prevents bypass attempts using visually similar characters from different scripts.

    For example:
    - Cyrillic 'с' (U+0441) -> Latin 'c' 
    - Cyrillic 'а' (U+0430) -> Latin 'a'
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
        # Other confusables
        '\u2010': '-',  # Hyphen
        '\u2011': '-',  # Non-breaking hyphen
        '\u2212': '-',  # Minus sign
        '\uff0d': '-',  # Fullwidth hyphen-minus
    }

    # Apply direct homograph replacements
    normalized = text
    for homograph, replacement in homograph_map.items():
        normalized = normalized.replace(homograph, replacement)

    # Also normalize using Unicode NFKD (compatibility decomposition)
    # This handles many other Unicode tricks
    normalized = unicodedata.normalize('NFKD', normalized)

    return normalized