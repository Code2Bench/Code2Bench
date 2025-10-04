from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import bisect
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
def find_chunk_index(chunks, idx):
    """
    Find the 0-based chunk index that contains the given index idx.
    chunks: List of (begin_idx, end_idx).
    idx: The index to search for.
    Returns the 0-based chunk index.
    """
    starts = [chunk[0] for chunk in chunks]
    pos = bisect.bisect_right(starts, idx) - 1  # Find position of idx in starts
    if pos < 0 or pos >= len(chunks):
        raise ValueError(f"Index {idx} not found in any chunk")
    chunk_begin, chunk_end = chunks[pos]
    if idx < chunk_begin or idx > chunk_end:
        raise ValueError(f"Index {idx} not found in any chunk")
    return pos

# Strategies for generating inputs
def chunks_strategy():
    # Generate a list of non-overlapping, sorted chunks
    return st.lists(
        st.tuples(
            st.integers(min_value=0, max_value=100),
            st.integers(min_value=0, max_value=100)
        ).filter(lambda x: x[0] <= x[1]),
        min_size=1,
        max_size=10
    ).map(lambda chunks: sorted(chunks, key=lambda x: x[0]))

def idx_strategy(chunks):
    # Generate an index that is within the range of the chunks
    if not chunks:
        return st.integers(min_value=0, max_value=100)
    min_idx = chunks[0][0]
    max_idx = chunks[-1][1]
    return st.integers(min_value=min_idx, max_value=max_idx)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    chunks=chunks_strategy(),
    idx=st.integers(min_value=0, max_value=100)
)
@example(chunks=[(0, 10)], idx=5)
@example(chunks=[(0, 10), (20, 30)], idx=25)
@example(chunks=[(0, 10), (20, 30)], idx=15)
@example(chunks=[(0, 10), (20, 30)], idx=0)
@example(chunks=[(0, 10), (20, 30)], idx=30)
def test_find_chunk_index(chunks, idx):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    chunks_copy = copy.deepcopy(chunks)
    idx_copy = copy.deepcopy(idx)

    # Call func0 to verify input validity
    try:
        expected = find_chunk_index(chunks_copy, idx_copy)
    except ValueError:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "chunks": chunks_copy,
            "idx": idx_copy
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