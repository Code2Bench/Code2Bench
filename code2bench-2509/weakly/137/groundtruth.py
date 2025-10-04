from typing import Optional
import base64

import base64
import typing

def _serialize_bytes(o, format: typing.Optional[str] = None) -> str:
    encoded = base64.b64encode(o).decode()
    if format == "base64url":
        return encoded.strip("=").replace("+", "-").replace("/", "_")
    return encoded