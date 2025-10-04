

def _extract_balanced_json(text: str) -> str:
    """Extract a complete JSON object by counting balanced braces."""
    start_idx = text.find('{')
    if start_idx == -1:
        return text

    brace_count = 0
    in_string = False
    escape_next = False

    for i, char in enumerate(text[start_idx:], start_idx):
        if escape_next:
            escape_next = False
            continue

        if char == '\\':
            escape_next = True
            continue

        if char == '"' and not escape_next:
            in_string = not in_string
            continue

        if not in_string:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    return text[start_idx:i+1]

    # If we get here, braces weren't balanced - return original text
    return text