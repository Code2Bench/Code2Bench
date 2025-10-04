import unicodedata

def remove_control_characters(text: str) -> str:
    return ''.join(char for char in text if not unicodedata.category(char).startswith('C'))