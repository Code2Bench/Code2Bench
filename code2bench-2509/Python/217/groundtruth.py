from typing import List

from typing import List

def _split_respecting_brackets(content: str) -> List[str]:
    parts = []
    current_part = ""
    bracket_count = 0
    comma_count = 0

    for i, char in enumerate(content):
        if char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
        elif char == ',' and bracket_count == 0:
            parts.append(current_part.strip())
            current_part = ""
            comma_count += 1
            if comma_count == 2:  # After finding 2 commas, rest is tail
                remaining = content[i+1:].strip()
                if remaining:
                    parts.append(remaining)
                break
            continue
        current_part += char

    # Add final part if we haven't reached 3 parts yet
    if len(parts) < 3 and current_part.strip():
        parts.append(current_part.strip())

    return parts