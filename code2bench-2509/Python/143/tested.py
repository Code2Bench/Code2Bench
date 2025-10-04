from typing import List

def merge_short_sentences_en(sens: List[str]) -> List[str]:
    if not sens:
        return []

    result = [sens[0]]
    for i in range(1, len(sens)):
        current = sens[i]
        previous = result[-1]

        # Check if the current sentence is short
        if len(current.split()) <= 2:
            # Merge with the previous sentence
            result[-1] += " " + current
            # If the previous sentence was also short, continue merging
            while len(result[-1].split()) <= 2:
                result[-1] += " " + result[-2]
                result.pop()
        else:
            result.append(current)

    return result