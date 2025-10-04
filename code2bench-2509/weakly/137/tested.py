import base64
import typing

def _serialize_bytes(o: bytes, format: typing.Optional[str] = None) -> str:
    if format == "base64url":
        encoded = base64.urlsafe_b64encode(o).decode("utf-8")
    else:
        encoded = base64.b64encode(o).decode("utf-8")
    return encoded.replace("=", "")