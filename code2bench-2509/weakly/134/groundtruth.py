
import base64

def _deserialize_bytes_base64(attr):
    if isinstance(attr, (bytes, bytearray)):
        return attr
    padding = "=" * (3 - (len(attr) + 3) % 4)  # type: ignore
    attr = attr + padding  # type: ignore
    encoded = attr.replace("-", "+").replace("_", "/")
    return bytes(base64.b64decode(encoded))