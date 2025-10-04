from urllib.parse import urlparse

def is_url(path: str) -> bool:
    result = urlparse(path)
    return bool(result.scheme and result.netloc)