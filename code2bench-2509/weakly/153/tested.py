import unicodedata

def safe_truncate(text: str, max_length: int) -> str:
    if max_length <= 0:
        raise ValueError("max_length must be greater than 0")
    
    normalized_text = unicodedata.normalize("NFC", text)
    if len(normalized_text) <= max_length:
        return normalized_text
    
    # Find the truncation point ensuring it doesn't break combining characters
    truncation_point = max_length
    while truncation_point > 0 and unicodedata.category(normalized_text[truncation_point - 1])[0] == 'M':
        truncation_point -= 1
    
    truncated_text = normalized_text[:truncation_point] + "..."
    return truncated_text