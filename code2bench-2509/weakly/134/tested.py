import base64
from typing import Union

def _deserialize_bytes_base64(attr: Union[bytes, bytearray, str]) -> bytes:
    if isinstance(attr, (bytes, bytearray)):
        return bytes(attr)
    elif isinstance(attr, str):
        # Replace URL-safe characters with standard base64 characters
        attr = attr.replace('-', '+').replace('_', '/')
        # Ensure proper padding
        padding = len(attr) % 4
        if padding != 0:
            attr += '=' * (4 - padding)
        return base64.b64decode(attr)
    else:
        raise TypeError("Input must be a bytes-like object or a base64 encoded string")