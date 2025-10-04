
from urllib.parse import urlparse

def extract_domain(url_or_domain):
    try:
        parsed_url = urlparse(url_or_domain)
        domain = parsed_url.netloc
        if not domain:
            domain = parsed_url.path

        domain = domain.split(':')[0]
        domain = domain.split('/')[0].split('?')[0].split('#')[0]

        return domain.lower().strip()
    except Exception:
        return url_or_domain.lower().strip()