import codecs
from typing import Any

def _clean_text_value(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        # Attempt to decode using UTF-8 first
        decoded = value.encode('utf-8').decode('utf-8')
    except UnicodeDecodeError:
        # If UTF-8 decoding fails, try Windows-1252/latin-1
        try:
            decoded = value.encode('utf-8').decode('windows-1252')
        except UnicodeDecodeError:
            # If both fail, return original
            return value
    # Check for mojibake markers
    if any(marker in decoded for marker in ['â€', 'Ã', 'Â']):
        # Attempt to fix mojibake by re-encoding to UTF-8
        try:
            fixed = decoded.encode('utf-8').decode('utf-8')
        except UnicodeDecodeError:
            fixed = decoded
    else:
        fixed = decoded
    # Decode backslash-escaped unicode sequences
    try:
        fixed = codecs.decode(fixed, 'unicode_escape')
    except UnicodeError:
        pass
    return fixed