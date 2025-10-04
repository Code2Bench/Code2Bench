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
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

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
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
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
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
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

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Single w2c matrix with relative_c2w=True"
        elif case_count == 1:
            desc = "Single w2c matrix with relative_c2w=False"
        else:
            desc = "Multiple w2c matrices with relative_c2w=True"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Identity transform matrix"
        elif case_count == 4:
            desc = "Non-identity transform matrix"
        elif case_count == 5:
            desc = "Multiple w2c matrices with relative_c2w=False"
        elif case_count == 6:
            desc = "Large number of w2c matrices"
        else:
            desc = "Complex transform matrix"

    # Generate usage code
    usage = f"""import numpy as np

# Construct inputs
w2cs = np.array({w2cs_copy.tolist()})
transform_matrix = np.array({transform_matrix_copy.tolist()})
relative_c2w = {relative_c2w_copy}

# Call function
result = get_c2w(w2cs, transform_matrix, relative_c2w)
"""

    # Store case
    # We don't include the expected output for lib-specific types
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "w2cs": w2cs_copy.tolist(),
            "transform_matrix": transform_matrix_copy.tolist(),
            "relative_c2w": relative_c2w_copy
        },
        "Expected": None,
        "Usage": usage
    })
    case_count += 1
    if case_count >= MAX_CASES:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {sum(len(cases) for cases in generated_cases.values())} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)