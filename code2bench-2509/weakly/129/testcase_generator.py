from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
import json
import os
import atexit
import copy
from scipy.spatial.transform import Rotation as R

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def axisangle2quat(vec):
    return R.from_rotvec(vec).as_quat()

# Strategy for generating axis-angle vectors
def vec_strategy():
    return hnp.arrays(
        dtype=np.float32,
        shape=(3,),
        elements=st.floats(min_value=-10.0, max_value=10.0, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(vec=vec_strategy())
@example(vec=np.array([0.0, 0.0, 0.0]))
@example(vec=np.array([1.0, 0.0, 0.0]))
@example(vec=np.array([0.0, 1.0, 0.0]))
@example(vec=np.array([0.0, 0.0, 1.0]))
@example(vec=np.array([1.0, 1.0, 1.0]))
@example(vec=np.array([-1.0, -1.0, -1.0]))
def test_axisangle2quat(vec):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    vec_copy = copy.deepcopy(vec)

    # Call func0 to verify input validity
    try:
        expected = axisangle2quat(vec_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "vec": vec_copy.tolist()
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