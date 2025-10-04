from collections import Counter

def calculate_ngram_repetition(text: str, n: int) -> float:
    words = text.split()
    if n <= 0:
        raise ValueError("n must be greater than 0")
    if len(words) < n:
        return 0.0
    ngrams = [tuple(words[i:i+n]) for i in range(len(words) - n + 1)]
    counter = Counter(ngrams)
    repeated = sum(1 for count in counter.values() if count > 1)
    total = len(ngrams)
    return repeated / total if total > 0 else 0.0