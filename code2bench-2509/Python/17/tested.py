from typing import List

def merge_short_sentences_latin(sens: List[str]) -> List[str]:
    result = []
    i = 0
    while i < len(sens):
        if len(sens[i]) <= 2:
            # If current sentence is too short, check next sentence
            if i + 1 < len(sens):
                result.append(sens[i])
                i += 1
            else:
                # If it's the last sentence and too short, merge with previous
                if len(result) > 0:
                    result[-1] += sens[i]
                else:
                    # If list is empty or only one sentence, leave as is
                    pass
        else:
            result.append(sens[i])
            i += 1
    return result