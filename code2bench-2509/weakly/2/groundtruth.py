
from collections import Counter
from itertools import product

def kmer_encode(sequence, k=3):
    sequence = sequence.upper()
    kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
    kmer_counts = Counter(kmers)
    return {kmer: kmer_counts.get(kmer, 0) / len(kmers) for kmer in [''.join(p) for p in product('ACGT', repeat=k)]}