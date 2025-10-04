def sanitize_streamed_message_content(text: str) -> str:
    # Remove trailing JSON delimiters
    if text and text[-1] in ',"} ]':
        # Remove the last character if it's a delimiter
        return text[:-1]
    return text