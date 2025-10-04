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
def quat2axisangle(quat):
    """
    Converts quaternion to axis-angle format.
    Returns a unit vector direction scaled by its angle in radians.

    Args:
        quat (np.array): (x,y,z,w) vec4 float angles

    Returns:
        np.array: (ax,ay,az) axis-angle exponential coordinates
    """
    return R.from_quat(quat).as_rotvec()

# Strategy for generating quaternions
def quat_strategy():
    return hnp.arrays(
        dtype=np.float32,
        shape=(4,),
        elements=st.floats(min_value=-1.0, max_value=1.0, allow_nan=False, allow_infinity=False)
    ).filter(lambda x: np.linalg.norm(x) > 0)  # Ensure non-zero quaternion

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(quat=quat_strategy())
@example(quat=np.array([0.0, 0.0, 0.0, 1.0]))  # Identity quaternion
@example(quat=np.array([1.0, 0.0, 0.0, 0.0]))  # 180-degree rotation around x-axis
@example(quat=np.array([0.0, 1.0, 0.0, 0.0]))  # 180-degree rotation around y-axis
@example(quat=np.array([0.0, 0.0, 1.0, 0.0]))  # 180-degree rotation around z-axis
@example(quat=np.array([0.5, 0.5, 0.5, 0.5]))  # Arbitrary quaternion
def test_quat2axisangle(quat):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    quat_copy = copy.deepcopy(quat)

    # Call func0 to verify input validity
    try:
        expected = quat2axisangle(quat_copy)
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