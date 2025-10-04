from typing import List

def merge_short_sentences_zh(sens: List[str]) -> List[str]:
    # Handle empty list case
    if not sens:
        return []

    # Iterate through the list to merge short sentences
    i = 0
    while i < len(sens) - 1:
        # Check if current sentence is short
        if len(sens[i]) <= 2:
            # Merge with next sentence
            sens[i] += sens[i + 1]
            del sens[i + 1]
            # Continue loop as the next sentence may be short
            i = max(0, i - 1)
        else:
            i += 1

    # If the last sentence is short, merge with the previous one
    if len(sens) > 0 and len(sens[-1]) <= 2:
        sens[-2] += sens[-1]
        del sens[-1]

    return sens