
import base64
import re

def base64decode(s: str):
    """
    Decode base64 `str` to original `bytes`.
    If the input is not a valid base64 string, return None.

    Args:
        s(str): A base64 `str` that can be used in text file.

    Returns:
        Optional[bytes]: The original decoded data with type `bytes`.
            If the input is not a valid base64 string, return None.
    """
    # return base64.b64decode(s)
    _base64_regex = re.compile(r'^(?:[A-Za-z\d+/]{4})*(?:[A-Za-z\d+/]{3}=|[A-Za-z\d+/]{2}==)?$')
    s = s.translate(base64._urlsafe_decode_translation)
    if not _base64_regex.fullmatch(s):
        return None
    try:
        return base64.urlsafe_b64decode(s)
    except base64.binascii.Error:
        return None