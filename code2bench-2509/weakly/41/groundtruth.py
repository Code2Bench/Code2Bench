
import unicodedata

def find_special_unicode(s):
    special_chars = {}
    for char in s:
        if ord(char) > 127:  # Non-ASCII characters
            # unicode_name = unicodedata.name(char, None)
            unicode_name = unicodedata.category(char)
            special_chars[char] = f'U+{ord(char):04X} ({unicode_name})'
    return special_chars