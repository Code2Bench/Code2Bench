
from urllib.parse import urlparse

from urllib.parse import urlparse

def get_url_root(url: str) -> str:
    supported_list = ["omniverse", "http", "https"]
    protocol = urlparse(url).scheme
    if protocol not in supported_list:
        raise RuntimeError("Unable to find root for {}".format(url))
        return ""
    server = f"{protocol}://{urlparse(url).netloc}"
    return server