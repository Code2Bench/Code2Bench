import difflib
from typing import List

def format_diff_message(optim_text: str, incr_text: str) -> str:
    optim_lines = optim_text.splitlines()
    incr_lines = incr_text.splitlines()
    
    diff = difflib.ndiff(optim_lines, incr_lines)
    
    optim_only = [line for line in diff if line.startswith(' - ')]
    incr_only = [line for line in diff if line.startswith(' + ')]
    
    optim_only_str = '\n'.join(['    ' + line[2:] for line in optim_only])
    incr_only_str = '\n'.join(['    ' + line[2:] for line in incr_only])
    
    message = (
        "Only in optimized prompt:\n"
        f"{optim_only_str}\n\n"
        "Only in incremental prompt:\n"
        f"{incr_only_str}"
    )
    
    return message