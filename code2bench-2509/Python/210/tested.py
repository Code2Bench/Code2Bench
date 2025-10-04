def extract_block_content(text: str, start_idx: int) -> str:
    import re
    # Find the first occurrence of '{' starting from start_idx
    open_brace = text.find('{', start_idx)
    if open_brace == -1:
        return ""
    
    # Find the corresponding '}' after the opening brace
    close_brace = text.find('}', open_brace + 1)
    if close_brace == -1:
        return ""
    
    # Extract the block content between the braces
    block_content = text[open_brace:close_brace + 1]
    
    # Handle nested blocks by counting the number of braces
    count = 1
    i = open_brace + 1
    while count > 0:
        i += 1
        if text[i] == '{':
            count += 1
        elif text[i] == '}':
            count -= 1
    
    # Extract the block content up to the matching '}' and include the braces
    return block_content