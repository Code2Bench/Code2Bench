import string
import re

def canonicalize(text: str, keep_punctuation_exact_string: str = None) -> str:
    # Replace underscores with spaces
    text = text.replace('_', ' ')
    
    # Normalize whitespace to a single space
    text = re.sub(r'\s+', ' ', text)
    
    # If keep_punctuation_exact_string is provided, preserve it and remove all other punctuation
    if keep_punctuation_exact_string:
        # Remove all punctuation except the exact string
        text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
        text = text.replace(keep_punctuation_exact_string, keep_punctuation_exact_string)
    else:
        # Remove all punctuation
        text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Strip leading and trailing whitespace
    return text.strip()