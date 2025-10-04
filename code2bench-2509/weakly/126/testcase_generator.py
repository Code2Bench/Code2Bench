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
def euler2quat(euler):
    """
    Converts extrinsic euler angles into quaternion form

    Args:
        euler (np.array): (r,p,y) angles

    Returns:
        np.array: (x,y,z,w) float quaternion angles

    Raises:
        AssertionError: [Invalid input shape]
    """
    return R.from_euler("xyz", euler).as_quat()

# Strategy for generating euler angles
def euler_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=(3,),
        elements=st.floats(min_value=-np.pi, max_value=np.pi, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(euler=euler_strategy())
@example(euler=np.array([0.0, 0.0, 0.0]))
@example(euler=np.array([np.pi, 0.0, 0.0]))
@example(euler=np.array([0.0, np.pi, 0.0]))
@example(euler=np.array([0.0, 0.0, np.pi]))
@example(euler=np.array([np.pi, np.pi, np.pi]))
def test_euler2quat(euler):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    euler_copy = copy.deepcopy(euler)

    # Call func0 to verify input validity
    try:
        expected = euler2quat(euler_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "euler": euler_copy.tolist()
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