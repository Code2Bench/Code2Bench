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
def mat2euler_intrinsic(rmat):
    return R.from_matrix(rmat).as_euler("XYZ")

# Strategy for generating valid 3x3 rotation matrices
def rotation_matrix_strategy():
    # Generate random rotation matrices using scipy's Rotation
    return st.builds(
        lambda r: R.from_euler("XYZ", r).as_matrix(),
        hnp.arrays(
            dtype=np.float32,
            shape=(3,),
            elements=st.floats(min_value=-np.pi, max_value=np.pi, allow_nan=False, allow_infinity=False)
        )
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(rmat=rotation_matrix_strategy())
@example(rmat=np.eye(3))  # Identity matrix
@example(rmat=np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]))  # 90-degree rotation around X
@example(rmat=np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]))  # 90-degree rotation around Y
@example(rmat=np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]))  # 90-degree rotation around Z
def test_mat2euler_intrinsic(rmat):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    rmat_copy = copy.deepcopy(rmat)

    # Call func0 to verify input validity
    try:
        expected = mat2euler_intrinsic(rmat_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "rmat": rmat_copy.tolist()
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