import re

def _find_unclosed(json_str: str) -> list:
    # Regular expression to match braces and brackets
    pattern = r'({}|[])(?=(?:\"[^\"]*\"|[^{}[]])*)'
    matches = re.finditer(pattern, json_str)
    
    unclosed = []
    for match in matches:
        # Check if the matched element is an opening brace or bracket
        if match.group(1) in ['{', '[']:
            unclosed.append(match.group(1))
    
    return unclosed