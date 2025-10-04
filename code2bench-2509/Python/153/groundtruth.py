

def sanitize_streamed_message_content(text: str) -> str:
    """Remove trailing JSON delimiters that can leak into assistant text.

    Specifically handles cases where a message string is immediately followed
    by a JSON delimiter in the stream (e.g., '"', '",', '"}', '" ]').
    Internal commas inside the message are preserved.
    """
    if not text:
        return text
    t = text.rstrip()
    # strip trailing quote + delimiter
    if len(t) >= 2 and t[-2] == '"' and t[-1] in ",}]":
        return t[:-2]
    # strip lone trailing quote
    if t.endswith('"'):
        return t[:-1]
    return t