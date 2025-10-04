from typing import List

def _collapse_repeated_lines(lines: List[str]) -> List[str]:
    result = []
    i = 0
    while i < len(lines):
        current_line = lines[i]
        j = i + 1
        while j < len(lines) and lines[j] == current_line:
            j += 1
        # Calculate the number of repetitions
        repetition = j - i
        # Add the line with repetition count annotation
        result.append(f"{current_line} (Repeated {repetition} times)")
        i = j
    return result