from typing import List

def _split_respecting_brackets(content: str) -> List[str]:
    parts = []
    i = 0
    while i < len(content):
        if content[i] == ',':
            # Check if we are inside brackets
            if '[' in content[i:]:
                # Find the matching closing bracket
                j = content.find(']', i)
                if j != -1:
                    # Skip the content inside brackets
                    i = j + 1
                else:
                    # No matching closing bracket, split here
                    parts.append(content[i])
                    i += 1
            else:
                # Not inside brackets, split here
                parts.append(content[i])
                i += 1
        else:
            i += 1
    # Limit to three parts
    return parts[:3]