

def is_properly_closed(text):
    quote_count = 0
    bracket_stack = []
    i = 0
    while i < len(text):
        char = text[i]
        if char == "'":
            if i > 0 and text[i - 1] == "\\":
                i += 1
                continue
            quote_count += 1
        elif char == "[":
            bracket_stack.append("[")
        elif char == "]":
            if not bracket_stack or bracket_stack[-1] != "[":
                return False
            bracket_stack.pop()
        i += 1
    return quote_count % 2 == 0 and len(bracket_stack) == 0