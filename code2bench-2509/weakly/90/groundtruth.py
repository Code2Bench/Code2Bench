from typing import Any
import codecs

def _clean_text_value(value: Any) -> Any:
    """Fix common text encoding issues and decode escaped sequences.

    - Fix UTF-8 displayed as Windows-1252/latin-1 (e.g., â -> ’)
    - Decode backslash-escaped unicode sequences when present
    - Leave non-strings unchanged
    """
    if not isinstance(value, str):
        return value

    text = value

    # Attempt to fix mojibake: bytes intended as UTF-8 shown as latin-1
    # Trigger only if typical mojibake markers present
    if any(mark in text for mark in ("â€", "Ã", "Â")):
        try:
            text = text.encode("latin-1", errors="ignore").decode(
                "utf-8", errors="ignore"
            )
        except Exception:
            pass

    # Decode literal escape sequences like \u2019 -> ’ if present
    if "\\u" in text or "\\x" in text:
        try:
            text = codecs.decode(text.encode("utf-8"), "unicode_escape")
        except Exception:
            pass

    return text