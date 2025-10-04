import urllib.parse
from typing import Dict

def extract_url_params_to_dict(url: str) -> Dict:
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    return {k: v[0] for k, v in query_params.items()}