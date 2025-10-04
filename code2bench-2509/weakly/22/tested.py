from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    if not url or len(url) >= 2048:
        return False
    result = urlparse(url)
    return all([
        result.scheme in ('http', 'https'),
        result.netloc,
        result.scheme and result.netloc
    ])