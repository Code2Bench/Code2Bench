
import unicodedata

import unicodedata

def remove_symbols(s: str) -> str:
    return "".join(
        " " if unicodedata.category(c)[0] in "MSP" else c
        for c in unicodedata.normalize("NFKC", s)
    )