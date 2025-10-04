
import unicodedata

import unicodedata

def safe_truncate(text: str, max_length: int) -> str:
    if max_length <= 0:
        raise ValueError("max_length must be greater than 0")
    text = unicodedata.normalize("NFC", text)
    if len(text) <= max_length:
        return text
    end_pos = max_length - 1
    if unicodedata.combining(text[end_pos + 1]):
        while unicodedata.combining(text[end_pos]):
            end_pos -= 1
        end_pos -= 1
    return text[:end_pos] + "…"