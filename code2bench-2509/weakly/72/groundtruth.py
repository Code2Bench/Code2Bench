
import urllib

def _is_url(policy_string: str) -> bool:
    """Check if the policy string is a URL."""
    try:
        parsed = urllib.parse.urlparse(policy_string)
        return parsed.scheme in ('http', 'https')
    except Exception:  # pylint: disable=broad-except
        return False