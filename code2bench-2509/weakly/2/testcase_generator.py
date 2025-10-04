from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from collections import Counter
from itertools import product
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def kmer_encode(sequence, k=3):
    sequence = sequence.upper()
    kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
    kmer_counts = Counter(kmers)
    return {kmer: kmer_counts.get(kmer, 0) / len(kmers) for kmer in [''.join(p) for p in product('ACGT', repeat=k)]}

# Strategy for generating DNA sequences
def sequence_strategy():
    return st.text(alphabet='ACGT', min_size=0, max_size=20)

# Strategy for generating k values
def k_strategy():
    return st.integers(min_value=1, max_value=5)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(sequence=sequence_strategy(), k=k_strategy())
@example(sequence="", k=3)
@example(sequence="ACGT", k=1)
@example(sequence="ACGTACGT", k=2)
@example(sequence="ACGTACGT", k=3)
@example(sequence="ACGTACGT", k=4)
@example(sequence="ACGTACGT", k=5)
def test_kmer_encode(sequence, k):
    global stop_collecting
    if stop_collecting:
        return

    # Validate input constraints
    if k > len(sequence):
        return

    # Deep copy inputs to avoid modification
    sequence_copy = copy.deepcopy(sequence)
    k_copy = copy.deepcopy(k)

    # Call func0 to verify input validity
    try:
        expected = kmer_encode(sequence_copy, k_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "sequence": sequence_copy,
            "k": k_copy
        }
    })

    # Stop collecting after 500 cases
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)