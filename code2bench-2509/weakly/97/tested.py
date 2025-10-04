import math
from collections import Counter

def calculate_information_content(text: str) -> float:
    if not text:
        return 0.0
    counts = Counter(text)
    total_chars = len(text)
    entropy = 0.0
    for char, count in counts.items():
        probability = count / total_chars
        entropy -= probability * math.log2(probability)
    return entropy