
import html
import re

def sanitize_html(text: str) -> str:
    """
    Sanitize HTML content by removing HTML tags and decoding HTML entities.
    Also escapes problematic characters that might break MDX parsing.

    Args:
        text: The text to sanitize

    Returns:
        Sanitized text safe for MDX
    """
    if not text:
        return ""

    # Convert text to string if it's not already
    text = str(text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Handle comparison operators that break MDX
    # These are the specific patterns we saw in the error output
    text = re.sub(r"<(\d+)", r"less than \1", text)  # <4mb -> less than 4mb
    text = re.sub(r">(\d+)", r"greater than \1", text)  # >10 -> greater than 10
    text = re.sub(r"<=(\d+)", r"less than or equal to \1", text)
    text = re.sub(r">=(\d+)", r"greater than or equal to \1", text)

    # For standalone < and > characters, replace with safer alternatives
    text = re.sub(r"(?<!\w)<(?!\w)", "&lt;", text)
    text = re.sub(r"(?<!\w)>(?!\w)", "&gt;", text)

    # Replace quote types that can break MDX

    # Escape pipe characters that can break tables
    text = text.replace("|", "\\|")
    text = re.sub(r"\{([^}]*)\s+([^}]*)\}", r"{\1_\2}", text)

    # Handle JSON examples with quotes
    if "{" in text and "}" in text:
        # Replace single and double quotes in JSON with backticks
        text = re.sub(
            r"(\{[^{}]*\})", lambda m: m.group(0).replace("'", "`").replace('"', "`"), text
        )

        # If we still have curly braces, wrap them in code tags
        text = re.sub(r"(\{[^{}]+\})", r"`\1`", text)

    # Handle special characters that might trigger MDX parsing
    text = text.replace("$", "\\$")
    text = text.replace("%", "\\%")

    # Some special HTML entities need to be preserved during unescaping
    text = html.unescape(text.replace("&lt;", "_LT_").replace("&gt;", "_GT_"))
    text = text.replace("_LT_", "&lt;").replace("_GT_", "&gt;")

    # Remove any trailing/leading whitespace
    text = text.strip()

    return text