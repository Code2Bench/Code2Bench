from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
import scipy.ndimage
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
def smooth_depth(depth):
    MAX_DEPTH_VAL = 1e5
    KERNEL_SIZE = 11
    depth = depth.copy()
    depth[depth == 0] = MAX_DEPTH_VAL
    smoothed_depth = scipy.ndimage.minimum_filter(depth, KERNEL_SIZE)
    smoothed_depth[smoothed_depth == MAX_DEPTH_VAL] = 0
    return smoothed_depth

# Strategy for generating depth arrays
def depth_strategy():
    return hnp.arrays(
        dtype=np.float32,
        shape=hnp.array_shapes(min_dims=2, max_dims=2, min_side=11, max_side=100),
        elements=st.floats(min_value=0.0, max_value=1e5, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(depth=depth_strategy())
@example(depth=np.zeros((11, 11), dtype=np.float32))
@example(depth=np.full((11, 11), 1e5, dtype=np.float32))
@example(depth=np.random.uniform(0, 1e5, (11, 11)).astype(np.float32))
def test_smooth_depth(depth):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    depth_copy = copy.deepcopy(depth)

    # Call func0 to verify input validity
    try:
        expected = smooth_depth(depth_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "depth": depth_copy.tolist()
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