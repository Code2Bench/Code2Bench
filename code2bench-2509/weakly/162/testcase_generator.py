from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
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
def quaternion_multiply(quaternion1, quaternion0):
    w0, x0, y0, z0 = quaternion0
    w1, x1, y1, z1 = quaternion1
    return np.array([
        -x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0, x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
        -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0, x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0
    ],
                       dtype=np.float64)

# Strategies for generating inputs
def quaternion_strategy():
    return st.lists(
        st.floats(min_value=-100.0, max_value=100.0, allow_nan=False, allow_infinity=False),
        min_size=4, max_size=4
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    quaternion1=quaternion_strategy(),
    quaternion0=quaternion_strategy()
)
@example(
    quaternion1=[4, 1, -2, 3],
    quaternion0=[8, -5, 6, 7]
)
@example(
    quaternion1=[0, 0, 0, 0],
    quaternion0=[0, 0, 0, 0]
)
@example(
    quaternion1=[1, 0, 0, 0],
    quaternion0=[0, 1, 0, 0]
)
@example(
    quaternion1=[0, 1, 0, 0],
    quaternion0=[0, 0, 1, 0]
)
@example(
    quaternion1=[0, 0, 1, 0],
    quaternion0=[0, 0, 0, 1]
)
def test_quaternion_multiply(quaternion1, quaternion0):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    quaternion1_copy = copy.deepcopy(quaternion1)
    quaternion0_copy = copy.deepcopy(quaternion0)

    # Call func0 to verify input validity
    try:
        expected = quaternion_multiply(quaternion1_copy, quaternion0_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "quaternion1": quaternion1_copy,
            "quaternion0": quaternion0_copy
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