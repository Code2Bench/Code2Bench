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
def skew(v):
    """Returns the skew-symmetric matrix of a vector
    cfo, 2015/08/13

    """
    return np.array([[0, -v[2], v[1]],
                    [v[2], 0, -v[0]],
                    [-v[1], v[0], 0]], dtype=np.float64)

# Strategy for generating 3D vectors
def vector_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=(3,),
        elements=st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(v=vector_strategy())
@example(v=np.array([0.0, 0.0, 0.0]))
@example(v=np.array([1.0, 0.0, 0.0]))
@example(v=np.array([0.0, 1.0, 0.0]))
@example(v=np.array([0.0, 0.0, 1.0]))
@example(v=np.array([1.0, 1.0, 1.0]))
@example(v=np.array([-1.0, -1.0, -1.0]))
def test_skew(v):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    v_copy = copy.deepcopy(v)

    # Call func0 to verify input validity
    try:
        expected = skew(v_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "v": v_copy.tolist()
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