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
def sample_indices(N, stride, expand_ratio, c):
    indices = []
    current_start = 0

    while current_start < N:
        bucket_width = int(stride * (expand_ratio**(len(indices) / stride)))

        interval = int(bucket_width / stride * c)
        current_end = min(N, current_start + bucket_width)
        bucket_samples = []
        for i in range(current_end - 1, current_start - 1, -interval):
            for near in range(c):
                bucket_samples.append(i - near)

        indices += bucket_samples[::-1]
        current_start += bucket_width

    return indices

# Strategy for generating inputs
@st.composite
def inputs_strategy(draw):
    N = draw(st.integers(min_value=1, max_value=1000))
    stride = draw(st.integers(min_value=1, max_value=100))
    expand_ratio = draw(st.floats(min_value=1.0, max_value=10.0, allow_nan=False, allow_infinity=False))
    c = draw(st.integers(min_value=1, max_value=10))
    return N, stride, expand_ratio, c

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(inputs=inputs_strategy())
@example(inputs=(10, 2, 2.0, 1))
@example(inputs=(100, 10, 1.5, 3))
@example(inputs=(50, 5, 3.0, 2))
@example(inputs=(1, 1, 1.0, 1))
@example(inputs=(1000, 100, 10.0, 10))
def test_sample_indices(inputs):
    global stop_collecting
    if stop_collecting:
        return
    
    N, stride, expand_ratio, c = inputs
    try:
        expected = sample_indices(N, stride, expand_ratio, c)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"N": N, "stride": stride, "expand_ratio": expand_ratio, "c": c},
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