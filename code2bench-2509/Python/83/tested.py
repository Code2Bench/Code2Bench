def is_properly_closed(text: str) -> bool:
    import re

    # Check for even number of single quotes
    quote_count = text.count("'")
    if quote_count % 2 != 0:
        return False

    # Check for properly nested square brackets using a stack
    bracket_stack = []
    for char in text:
        if char == '[':
            bracket_stack.append(char)
        elif char == ']':
            if bracket_stack and bracket_stack[-1] == '[':
                bracket_stack.pop()
            else:
                return False
    return len(bracket_stack) == 0