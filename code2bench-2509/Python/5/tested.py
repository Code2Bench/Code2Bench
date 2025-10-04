def last_boxed_only_string(string: str) -> str | None:
    import re
    
    # Find all occurrences of \\boxed or \\fbox
    matches = re.findall(r'\\boxed\s*([^\$]+)\s*$', string)
    matches_fbox = re.findall(r'\\fbox\s*([^\$]+)\s*$', string)
    
    # Combine matches and find the last one
    all_matches = matches + matches_fbox
    if all_matches:
        return all_matches[-1]
    else:
        return None