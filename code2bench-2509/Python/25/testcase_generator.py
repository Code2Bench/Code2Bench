from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
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
def split_token_counts_and_frame_ids(T, token_frame, world_size, rank):
    S = T * token_frame
    split_sizes = [S // world_size + (1 if i < S % world_size else 0) for i in range(world_size)]
    start = sum(split_sizes[:rank])
    end = start + split_sizes[rank]
    counts = [0] * T
    for idx in range(start, end):
        t = idx // token_frame
        counts[t] += 1

    counts_filtered = []
    frame_ids = []
    for t, c in enumerate(counts):
        if c > 0:
            counts_filtered.append(c)
            frame_ids.append(t)
    return counts_filtered, frame_ids

# Strategy for generating inputs
def input_strategy():
    T = st.integers(min_value=1, max_value=100)
    token_frame = st.integers(min_value=1, max_value=100)
    world_size = st.integers(min_value=1, max_value=100)
    rank = st.integers(min_value=0, max_value=99)
    return st.tuples(T, token_frame, world_size, rank).filter(lambda x: x[3] < x[2])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(inputs=input_strategy())
@example((1, 1, 1, 0))
@example((10, 5, 2, 0))
@example((10, 5, 2, 1))
@example((100, 10, 10, 5))
@example((50, 20, 5, 4))
def test_split_token_counts_and_frame_ids(inputs):
    global stop_collecting
    if stop_collecting:
        return

    T, token_frame, world_size, rank = inputs
    try:
        expected = split_token_counts_and_frame_ids(T, token_frame, world_size, rank)
    except Exception:
        return  # Skip inputs that cause exceptions

    generated_cases.append({
        "Inputs": {"T": T, "token_frame": token_frame, "world_size": world_size, "rank": rank},
        "Expected": expected
    })
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)