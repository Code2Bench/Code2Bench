
from urllib.parse import urlparse

def _split_url(url: str) -> tuple[str, str]:
    """
    Splits the URL into scheme and netloc.

    Args:
        url (str): The URL to split.

    Returns:
        tuple[str, str]: The scheme and netloc of the URL.

    Raises:
        ValueError: If the URL does not include protocol and host name.
    """
    parsed_url = urlparse(url)
    if not (parsed_url.scheme and parsed_url.netloc):
        raise ValueError(f"URL must include protocol and host name: {url}")
    return parsed_url.scheme.lower(), parsed_url.netloc.lower()