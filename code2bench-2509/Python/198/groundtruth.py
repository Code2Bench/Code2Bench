

def _calculate_phrase_similarity(text1: str, text2: str) -> float:
    if not text1 or not text2:
        return 0.0

    text1_lower = text1.lower()
    text2_lower = text2.lower()

    phrase_boost = 0.0

    words1 = text1_lower.split()
    words2 = text2_lower.split()

    for i in range(len(words1) - 1):
        phrase = f"{words1[i]} {words1[i+1]}"
        if phrase in text2_lower:
            phrase_boost += 0.1

    for i in range(len(words1) - 2):
        phrase = f"{words1[i]} {words1[i+1]} {words1[i+2]}"
        if phrase in text2_lower:
            phrase_boost += 0.15

    return min(0.3, phrase_boost)