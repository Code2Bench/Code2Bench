from collections import Counter
from itertools import product

def kmer_encode(sequence: str, k: int = 3) -> dict:
    sequence = sequence.upper()
    n = len(sequence)
    if n < k:
        return {}
    kmers = [sequence[i:i+k] for i in range(n - k + 1)]
    counts = Counter(kmers)
    total = n - k + 1
    alphabet = ['A', 'C', 'G', 'T']
    all_kmers = [''.join(p) for p in product(alphabet, repeat=k)]
    frequencies = {kmer: counts.get(kmer, 0) / total for kmer in all_kmers}
    return frequencies