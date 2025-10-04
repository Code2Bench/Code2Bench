

def split_continuous_references(text: str) -> str:
    """
    Split continuous reference tags into individual reference tags.

    Converts patterns like [1:92ff35fb, 4:bfe6f044] to [1:92ff35fb] [4:bfe6f044]

    Only processes text if:
    1. '[' appears exactly once
    2. ']' appears exactly once
    3. Contains commas between '[' and ']'

    Args:
        text (str): Text containing reference tags

    Returns:
        str: Text with split reference tags, or original text if conditions not met
    """
    # Early return if text is empty
    if not text:
        return text
    # Check if '[' appears exactly once
    if text.count("[") != 1:
        return text
    # Check if ']' appears exactly once
    if text.count("]") != 1:
        return text
    # Find positions of brackets
    open_bracket_pos = text.find("[")
    close_bracket_pos = text.find("]")

    # Check if brackets are in correct order
    if open_bracket_pos >= close_bracket_pos:
        return text
    # Extract content between brackets
    content_between_brackets = text[open_bracket_pos + 1 : close_bracket_pos]
    # Check if there's a comma between brackets
    if "," not in content_between_brackets:
        return text
    text = text.replace(content_between_brackets, content_between_brackets.replace(", ", "]["))
    text = text.replace(content_between_brackets, content_between_brackets.replace(",", "]["))

    return text