from urllib.parse import urlparse

def get_url_root(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in ('omniverse', 'http', 'https'):
        raise RuntimeError(f"Unsupported protocol: {parsed.scheme}")
    return f"{parsed.scheme}://{parsed.netloc}"