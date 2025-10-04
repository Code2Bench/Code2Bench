
from base64 import urlsafe_b64decode

from base64 import urlsafe_b64decode

def str_from_base64url(base64url: str) -> str:
    base64url_with_padding = base64url + "=" * (-len(base64url) % 4)
    return urlsafe_b64decode(base64url_with_padding).decode("utf-8")