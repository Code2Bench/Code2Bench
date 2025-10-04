from urllib.parse import urlparse

def url_to_provider_name(url: str) -> str:
    parsed = urlparse(url)
    host_path = parsed.hostname + parsed.path if parsed.hostname else parsed.path
    sanitized = ''.join('_' if c in ('.', '/', '-') else c for c in host_path)
    return sanitized