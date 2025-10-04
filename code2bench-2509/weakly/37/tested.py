import base64
import re
from typing import Optional

def base64decode(s: str) -> Optional[bytes]:
    if not s:
        return None
    # Check if the string is a valid base64
    if not re.fullmatch(r'[A-Za-z0-9+/=]*', s):
        return None
    try:
        # Handle URL-safe base64 by replacing '-' with '+' and '_' with '/'
        s = s.replace('-', '+').replace('_', '/')
        decoded_bytes = base64.b64decode(s, validate=True)
        return decoded_bytes
    except (base64.binascii.Error, UnicodeDecodeError):
        return None