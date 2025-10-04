
from urllib.parse import urlparse

def url_to_provider_name(url: str) -> str:
    """Create a sanitized provider name from a URL."""
    parsed_url = urlparse(url)
    # Combine host and path, remove leading slash from path
    name = parsed_url.netloc + parsed_url.path
    # Replace characters that are invalid for identifiers
    return name.replace('.', '_').replace('/', '_').replace('-', '_')