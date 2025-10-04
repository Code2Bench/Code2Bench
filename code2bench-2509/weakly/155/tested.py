import re
import unicodedata

def normalize_name(tag_name: str) -> str:
    # Normalize Unicode characters
    normalized = unicodedata.normalize('NFKD', tag_name)
    # Remove diacritical marks
    stripped = ''.join(char for char in normalized if not unicodedata.combining(char))
    # Convert to lowercase
    lowercased = stripped.lower()
    # Replace spaces with underscores
    underscored = lowercased.replace(' ', '_')
    # Filter out non-alphanumeric, non-underscore, non-period, non-colon, non-hyphen characters
    cleaned = re.sub(r'[^\w.:_-]', '', underscored)
    return cleaned