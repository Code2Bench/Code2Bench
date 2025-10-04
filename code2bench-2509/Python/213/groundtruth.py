from typing import List

from typing import List

def _collapse_repeated_lines(lines: List[str]) -> List[str]:
    if not lines:
        return []
    collapsed_lines = []
    prev_line = lines[0]
    count = 1
    for line in lines[1:]:
        if line == prev_line:
            count += 1
        else:
            if count > 1:
                collapsed_lines.append(f"{prev_line} (Repeated {count} times)")
            else:
                collapsed_lines.append(prev_line)
            prev_line = line
            count = 1
    if count > 1:
        collapsed_lines.append(f"{prev_line} (Repeated {count} times)")
    else:
        collapsed_lines.append(prev_line)
    return collapsed_lines