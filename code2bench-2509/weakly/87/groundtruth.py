
from urllib.parse import urlunsplit
from urllib.parse import urlsplit

def metadata_url_for_resource(resource_url: str) -> str:
    """
    RFC 9728: insert '/.well-known/oauth-protected-resource' between host and path.
    If the resource has a path (e.g., '/mcp'), append it after the well-known suffix.
    """
    u = urlsplit(resource_url)
    path = u.path.lstrip("/")
    suffix = "/.well-known/oauth-protected-resource"
    if path:
        suffix += f"/{path}"
    return urlunsplit((u.scheme, u.netloc, suffix, "", ""))