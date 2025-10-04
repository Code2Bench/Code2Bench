from typing import List
import urllib

import urllib.parse
from typing import List

def modify_url(url: str, remove: List[str]) -> str:
    scheme, netloc, path, query, fragment = urllib.parse.urlsplit(url)
    params = urllib.parse.parse_qs(query)
    for param_key in remove:
        if param_key in params:
            del params[param_key]
    query = urllib.parse.urlencode(params, doseq=True)
    return urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))