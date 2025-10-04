
import unicodedata

def remove_control_characters(text: str) -> str:
    """Remove control characters from text.
    Control characters are non-printable characters in the Unicode standard that control how text is displayed or processed.
    """
    return "".join(i for i in text if unicodedata.category(i)[0] != "C")