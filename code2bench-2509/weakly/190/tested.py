import html
import re

def sanitize_html(text: str) -> str:
    # Remove HTML tags using regex
    text = re.sub(r'<[^>]+>', '', text)
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Handle comparison operators
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    text = text.replace('<=', 'less than or equal to').replace('>=', 'greater than or equal to')
    
    # Escape pipe characters
    text = text.replace('|', '&pipe;')
    
    # Modify JSON-like content
    text = text.replace('"', '`').replace("'", '`')
    text = re.sub(r'\{([^{}]+)\}', r'`{\1}`', text)
    
    # Escape special characters
    text = text.replace('$', '&dollar;').replace('%', '&percent;')
    
    # Strip leading and trailing whitespaces
    return text.strip()