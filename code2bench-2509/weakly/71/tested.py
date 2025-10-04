from urllib.parse import urlparse

def _parse_url(base_url: str) -> tuple[str, str]:
    parsed = urlparse(base_url)
    host = parsed.hostname or "127.0.0.1"
    port = str(parsed.port) if parsed.port is not None else ""
    return host, port