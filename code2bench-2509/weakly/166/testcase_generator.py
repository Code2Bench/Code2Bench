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
def first_order_rotation(rotvec):
    R = np.zeros((3, 3), dtype=np.float64)
    R[0, 0] = 1.0
    R[1, 0] = rotvec[2]
    R[2, 0] = -rotvec[1]
    R[0, 1] = -rotvec[2]
    R[1, 1] = 1.0
    R[2, 1] = rotvec[0]
    R[0, 2] = rotvec[1]
    R[1, 2] = -rotvec[0]
    R[2, 2] = 1.0
    return R

# Strategy for generating rotation vectors
def rotvec_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=(3,),
        elements=st.floats(min_value=-10.0, max_value=10.0, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(rotvec=rotvec_strategy())
@example(rotvec=np.array([0.0, 0.0, 0.0]))
@example(rotvec=np.array([1.0, 0.0, 0.0]))
@example(rotvec=np.array([0.0, 1.0, 0.0]))
@example(rotvec=np.array([0.0, 0.0, 1.0]))
@example(rotvec=np.array([1.0, 1.0, 1.0]))
@example(rotvec=np.array([-1.0, -1.0, -1.0]))
def test_first_order_rotation(rotvec):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    rotvec_copy = copy.deepcopy(rotvec)

    # Call func0 to verify input validity
    try:
        expected = first_order_rotation(rotvec_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "rotvec": rotvec_copy.tolist()
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