from typing import List, Tuple

def find_context_core(lines: List[str], context: List[str], start: int) -> Tuple[int, int]:
    if not context:
        return start, 0
    
    # Check exact match
    for i in range(start, len(lines) - len(context) + 1):
        if lines[i:i+len(context)] == context:
            return i, 0
    
    # Check trailing whitespace ignored
    for i in range(start, len(lines) - len(context) + 1):
        if lines[i:i+len(context)].strip() == context.strip():
            return i, 1
    
    # Check leading and trailing whitespace ignored
    for i in range(start, len(lines) - len(context) + 1):
        if lines[i:i+len(context)].strip('\n').strip() == context.strip('\n').strip():
            return i, 100
    
    return -1, 0