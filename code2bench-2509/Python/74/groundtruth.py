

def normalize_base_url(url: str) -> str:
    """Normalize a base URL by adding http:// if missing and ensuring trailing slash."""
    if not url:
        return url

    # Strip whitespace
    url = url.strip()

    # Add http:// if no protocol is specified
    if not url.startswith(('http://', 'https://')):
        # If it looks like a local IP or localhost, use http, otherwise https
        if any(x in url for x in ['localhost', '127.0.0.1', '192.168.', '10.', '172.']):
            url = f'http://{url}'
        else:
            url = f'https://{url}'

    # Ensure trailing slash for base URLs
    if not url.endswith('/'):
        url = f'{url}/'

    return url