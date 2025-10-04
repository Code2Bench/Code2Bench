import unicodedata

def fullwidth_to_halfwidth(s: str) -> str:
    result = []
    for char in s:
        if unicodedata.fullwidth(char):
            # Convert full-width characters to half-width
            half_width_char = unicodedata.normalize('NFKC', char)
            result.append(half_width_char)
        else:
            result.append(char)
    return ''.join(result)