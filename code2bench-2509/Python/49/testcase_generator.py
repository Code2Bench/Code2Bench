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
def get_minimum_num_micro_batch_size(total_lengths, max_tokens_per_gpu):
    batches = []
    for l in total_lengths:
        for i in range(len(batches)):
            if batches[i] + l <= max_tokens_per_gpu:
                batches[i] += l
                break
        else:
            batches.append(l)

    return len(batches)

# Strategy for generating total_lengths and max_tokens_per_gpu
def generate_inputs():
    return st.tuples(
        st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=1, max_value=1000)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(inputs=generate_inputs())
@example(inputs=([1, 2, 3], 3))
@example(inputs=([10, 20, 30], 50))
@example(inputs=([5, 5, 5, 5], 10))
@example(inputs=([100], 100))
@example(inputs=([1, 1, 1, 1, 1], 1))
def test_get_minimum_num_micro_batch_size(inputs):
    global stop_collecting
    if stop_collecting:
        return
    
    total_lengths, max_tokens_per_gpu = inputs
    total_lengths_copy = copy.deepcopy(total_lengths)
    max_tokens_per_gpu_copy = copy.deepcopy(max_tokens_per_gpu)
    try:
        expected = get_minimum_num_micro_batch_size(total_lengths_copy, max_tokens_per_gpu_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"total_lengths": total_lengths, "max_tokens_per_gpu": max_tokens_per_gpu},
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