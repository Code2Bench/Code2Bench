from typing import Union

def replace_symbols(text: str, lang: str = "en") -> str:
    replacements = {
        "en": {
            ";": ";",
            "-": "–",
            ":": ":",
            "&": "and",
            "'": "'"
        },
        "fr": {
            ";": ";",
            "-": "–",
            ":": ":",
            "&": "et",
            "'": "'"
        },
        "pt": {
            ";": ";",
            "-": "–",
            ":": ":",
            "&": "e",
            "'": "'"
        },
        "ca": {
            ";": ";",
            "-": "–",
            ":": ":",
            "&": "i",
            "'": "'"
        },
        "es": {
            ";": ";",
            "-": "–",
            ":": ":",
            "&": "y",
            "'": "'"
        }
    }
    
    if lang not in replacements:
        raise ValueError(f"Unsupported language: {lang}")
    
    result = []
    i = 0
    while i < len(text):
        if text[i] in replacements[lang]:
            # Replace the symbol
            result.append(replacements[lang][text[i]])
            i += 1
        else:
            # Keep the character as is
            result.append(text[i])
            i += 1
    
    return "".join(result)