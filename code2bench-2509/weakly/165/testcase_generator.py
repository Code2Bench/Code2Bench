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
def unskew(R):
    return np.array([R[2, 1], R[0, 2], R[1, 0]], dtype=np.float64)

# Strategy for generating 3x3 matrices
def matrix_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=(3, 3),
        elements=st.floats(allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(R=matrix_strategy())
@example(R=np.zeros((3, 3)))
@example(R=np.ones((3, 3)))
@example(R=np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]]))
@example(R=np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]))
def test_unskew(R):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    R_copy = copy.deepcopy(R)

    # Call func0 to verify input validity
    try:
        expected = unskew(R_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "R": R_copy.tolist()
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