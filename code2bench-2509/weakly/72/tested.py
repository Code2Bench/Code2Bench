import urllib.parse

def _is_url(policy_string: str) -> bool:
    try:
        result = urllib.parse.urlparse(policy_string)
        return result.scheme in ('http', 'https')
    except:
        return False