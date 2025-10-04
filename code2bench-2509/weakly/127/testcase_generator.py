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
def quat2euler(quat):
    """
    Converts extrinsic euler angles into quaternion form

    Args:
        quat (np.array): (x,y,z,w) float quaternion angles

    Returns:
        np.array: (r,p,y) angles

    Raises:
        AssertionError: [Invalid input shape]
    """
    return R.from_quat(quat).as_euler("xyz")

# Strategy for generating quaternion inputs
def quat_strategy():
    return hnp.arrays(
        dtype=np.float32,
        shape=(4,),
        elements=st.floats(min_value=-1.0, max_value=1.0, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(quat=quat_strategy())
@example(quat=np.array([0.0, 0.0, 0.0, 1.0]))
@example(quat=np.array([1.0, 0.0, 0.0, 0.0]))
@example(quat=np.array([0.0, 1.0, 0.0, 0.0]))
@example(quat=np.array([0.0, 0.0, 1.0, 0.0]))
@example(quat=np.array([0.5, 0.5, 0.5, 0.5]))
def test_quat2euler(quat):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    quat_copy = copy.deepcopy(quat)

    # Call func0 to verify input validity
    try:
        expected = quat2euler(quat_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "quat": quat_copy.tolist()
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