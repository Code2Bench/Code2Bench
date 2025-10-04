def extract_boxed_answer(text: str) -> str | None:
    import re
    
    # Find all occurrences of boxed{...} patterns
    matches = re.findall(r'boxed{(.*?)}', text)
    
    if not matches:
        return None
    
    # Get the last match
    last_match = matches[-1]
    
    return last_match