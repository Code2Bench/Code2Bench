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
def logmap_so3(R):
    R11 = R[0, 0]
    R12 = R[0, 1]
    R13 = R[0, 2]
    R21 = R[1, 0]
    R22 = R[1, 1]
    R23 = R[1, 2]
    R31 = R[2, 0]
    R32 = R[2, 1]
    R33 = R[2, 2]
    tr = np.trace(R)
    omega = np.empty((3,), dtype=np.float64)

    if(np.abs(tr + 1.0) < 1e-10):
        if(np.abs(R33 + 1.0) > 1e-10):
            omega = (np.pi / np.sqrt(2.0 + 2.0 * R33)) * np.array([R13, R23, 1.0+R33])
        elif(np.abs(R22 + 1.0) > 1e-10):
            omega = (np.pi / np.sqrt(2.0 + 2.0 * R22)) * np.array([R12, 1.0+R22, R32])
        else:
            omega = (np.pi / np.sqrt(2.0 + 2.0 * R11)) * np.array([1.0+R11, R21, R31])
    else:
        magnitude = 1.0
        tr_3 = tr - 3.0
        if tr_3 < -1e-7:
            theta = np.arccos((tr - 1.0) / 2.0)
            magnitude = theta / (2.0 * np.sin(theta))
        else:
            magnitude = 0.5 - tr_3 * tr_3 / 12.0

        omega = magnitude * np.array([R32 - R23, R13 - R31, R21 - R12])

    return omega

# Strategies for generating inputs
def rotation_matrix_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=(3, 3),
        elements=st.floats(min_value=-1.0, max_value=1.0, allow_nan=False, allow_infinity=False)
    ).filter(lambda x: np.linalg.det(x) > 0)  # Ensure valid rotation matrix

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(R=rotation_matrix_strategy())
@example(R=np.eye(3))
@example(R=np.array([[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]]))
@example(R=np.array([[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, -1.0]]))
@example(R=np.array([[-1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0]]))
def test_logmap_so3(R):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    R_copy = copy.deepcopy(R)

    # Call func0 to verify input validity
    try:
        expected = logmap_so3(R_copy)
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