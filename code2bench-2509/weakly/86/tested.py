from urllib.parse import urlparse

def _split_url(url: str) -> tuple[str, str]:
    parsed = urlparse(url)
    
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include both a protocol and a host name")
    
    return parsed.scheme.lower(), parsed.netloc.lower()