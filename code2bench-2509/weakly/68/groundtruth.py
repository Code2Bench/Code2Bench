
from urllib.parse import urlparse

def _ext_from_uri(uri: str) -> str:
    path = urlparse(uri).path
    if "." in path:
        return "." + path.split(".")[-1].lower()
    return ""