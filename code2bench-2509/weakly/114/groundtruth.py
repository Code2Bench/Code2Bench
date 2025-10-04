
import binascii
import urllib
import base64

def clean_pot(po_token: str):
    # Clean and validate the PO Token. This will strip invalid characters off
    # (e.g. additional url params the user may accidentally include)
    try:
        return base64.urlsafe_b64encode(
            base64.urlsafe_b64decode(urllib.parse.unquote(po_token))).decode()
    except (binascii.Error, ValueError):
        raise ValueError('Invalid PO Token')