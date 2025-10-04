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
def get_c2w(w2cs, transform_matrix, relative_c2w=True):
    if relative_c2w:
        target_cam_c2w = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        abs2rel = target_cam_c2w @ w2cs[0]
        ret_poses = [target_cam_c2w, ] + [abs2rel @ np.linalg.inv(w2c) for w2c in w2cs[1:]]
    else:
        ret_poses = [np.linalg.inv(w2c) for w2c in w2cs]
    ret_poses = [transform_matrix @ x for x in ret_poses]
    return np.array(ret_poses, dtype=np.float32)

# Strategies for generating inputs
def w2cs_strategy():
    return hnp.arrays(
        dtype=np.float32,
        shape=st.tuples(
            st.integers(min_value=1, max_value=5),  # Number of w2c matrices
            st.just(4),  # 4x4 matrices
            st.just(4)
        ),
        elements=st.floats(min_value=-10.0, max_value=10.0, allow_nan=False, allow_infinity=False)
    )

def transform_matrix_strategy():
    return hnp.arrays(
        dtype=np.float32,
        shape=(4, 4),
        elements=st.floats(min_value=-10.0, max_value=10.0, allow_nan=False, allow_infinity=False)
    )

def relative_c2w_strategy():
    return st.booleans()

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    w2cs=w2cs_strategy(),
    transform_matrix=transform_matrix_strategy(),
    relative_c2w=relative_c2w_strategy()
)
@example(
    w2cs=np.array([[[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]], dtype=np.float32),
    transform_matrix=np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.float32),
    relative_c2w=True
)
@example(
    w2cs=np.array([[[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]], dtype=np.float32),
    transform_matrix=np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.float32),
    relative_c2w=False
)
@example(
    w2cs=np.array([[[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]], dtype=np.float32),
    transform_matrix=np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.float32),
    relative_c2w=True
)
def test_get_c2w(w2cs, transform_matrix, relative_c2w):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    w2cs_copy = copy.deepcopy(w2cs)
    transform_matrix_copy = copy.deepcopy(transform_matrix)
    relative_c2w_copy = copy.deepcopy(relative_c2w)

    # Call func0 to verify input validity
    try:
        expected = get_c2w(w2cs_copy, transform_matrix_copy, relative_c2w_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "w2cs": w2cs_copy.tolist(),
            "transform_matrix": transform_matrix_copy.tolist(),
            "relative_c2w": relative_c2w_copy
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