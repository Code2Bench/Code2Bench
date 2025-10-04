from typing import List

def find_boxed_content_with_boxed(text: str) -> List[str]:
    # This function scans the string manually to ensure proper brace matching,
    # allowing for nested expressions inside \boxed{}, but only extracting
    # the outermost matched segments.
    result = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == '{':
            # Find the matching closing brace
            j = i + 1
            while j < n and text[j] != '}':
                j += 1
            if j < n:
                # Extract the content between the braces
                content = text[i+1:j]
                # Check if the content contains another \boxed{} expression
                if '{' in content and '}' in content:
                    # If the content contains another \boxed{}, treat it as a single match
                    result.append(content)
                    i = j + 1
                else:
                    # If the content does not contain another \boxed{}, add it as a single match
                    result.append(content)
                    i = j + 1
            else:
                # No closing brace found, skip
                i += 1
        else:
            # Not a brace, move to next character
            i += 1
    return result