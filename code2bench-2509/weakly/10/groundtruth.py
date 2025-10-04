
import string

def normalize_text(text: str) -> str:
    text = text.lower()
    text = ''.join(ch for ch in text if ch not in set(string.punctuation))
    text = ' '.join(text.split())
    return text