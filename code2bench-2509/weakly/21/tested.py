from urllib.parse import urlparse

def extract_domain(url_or_domain: str) -> str:
    try:
        parsed = urlparse(url_or_domain)
        domain = parsed.netloc
        if not domain:
            domain = parsed.path.split('/')[0] if parsed.path else url_or_domain
        return domain.lower()
    except Exception:
        return url_or_domain.lower()