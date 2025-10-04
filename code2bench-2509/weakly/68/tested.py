from urllib.parse import urlparse

def _ext_from_uri(uri: str) -> str:
    parsed = urlparse(uri)
    path = parsed.path
    if '.' in path:
        return '.' + path.split('.')[-1].lower()
    return ''