
from urllib.parse import urlparse, urlsplit, urlunsplit

def check_resource_allowed(requested_resource: str, configured_resource: str) -> bool:
    """Check if a requested resource URL matches a configured resource URL.

    A requested resource matches if it has the same scheme, domain, port,
    and its path starts with the configured resource's path. This allows
    hierarchical matching where a token for a parent resource can be used
    for child resources.

    Args:
        requested_resource: The resource URL being requested
        configured_resource: The resource URL that has been configured

    Returns:
        True if the requested resource matches the configured resource
    """
    # Parse both URLs
    requested = urlparse(requested_resource)
    configured = urlparse(configured_resource)

    # Compare scheme, host, and port (origin)
    if requested.scheme.lower() != configured.scheme.lower() or requested.netloc.lower() != configured.netloc.lower():
        return False

    # Handle cases like requested=/foo and configured=/foo/
    requested_path = requested.path
    configured_path = configured.path

    # If requested path is shorter, it cannot be a child
    if len(requested_path) < len(configured_path):
        return False

    # Check if the requested path starts with the configured path
    # Ensure both paths end with / for proper comparison
    # This ensures that paths like "/api123" don't incorrectly match "/api"
    if not requested_path.endswith("/"):
        requested_path += "/"
    if not configured_path.endswith("/"):
        configured_path += "/"

    return requested_path.startswith(configured_path)