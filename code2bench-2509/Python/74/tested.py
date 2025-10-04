import re

def normalize_base_url(url: str) -> str:
    if not url:
        return url
    
    # Check if the URL has a protocol
    if re.match(r'^https?://', url):
        return url
    
    # Add protocol if not present
    url = 'http://' + url
    
    # Ensure trailing slash
    url += '/'
    
    return url