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
def post_process_sampled_indices(*, sampled_inds_list, attn_map, image_size):
    inds = np.array(sampled_inds_list).flatten()
    inds = np.array(np.unravel_index(inds, attn_map.shape)).T

    inds_normalised = np.zeros(inds.shape)
    inds_normalised[:, 0] = inds[:, 1] / image_size
    inds_normalised[:, 1] = inds[:, 0] / image_size
    inds_normalised = inds_normalised.tolist()

    return inds, inds_normalised

# Strategies for generating inputs
def sampled_inds_list_strategy(attn_map_shape):
    max_index = np.prod(attn_map_shape) - 1
    return st.lists(
        st.integers(min_value=0, max_value=max_index),
        min_size=1, max_size=10
    )

def attn_map_strategy():
    return hnp.arrays(
        dtype=np.float32,
        shape=st.tuples(
            st.integers(min_value=1, max_value=10),  # height
            st.integers(min_value=1, max_value=10)  # width
        ),
        elements=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)
    )

def image_size_strategy():
    return st.integers(min_value=1, max_value=1000)

# Hypothesis test configuration
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(
    sampled_inds_list=st.lists(
        st.integers(min_value=0, max_value=99),  # max_index is 99 for 10x10 attn_map
        min_size=1, max_size=10
    ),
    attn_map=attn_map_strategy(),
    image_size=image_size_strategy()
)
@example(
    sampled_inds_list=[0],
    attn_map=np.array([[1.0]]),
    image_size=1
)
@example(
    sampled_inds_list=[0, 1, 2],
    attn_map=np.array([[1.0, 0.5], [0.5, 1.0]]),
    image_size=2
)
@example(
    sampled_inds_list=[3, 4],
    attn_map=np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]]),
    image_size=3
)
def test_post_process_sampled_indices(sampled_inds_list, attn_map, image_size):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return

    # Validate input constraints
    max_index = np.prod(attn_map.shape) - 1
    if any(idx > max_index for idx in sampled_inds_list):
        return

    # Deep copy inputs to avoid modification
    sampled_inds_list_copy = copy.deepcopy(sampled_inds_list)
    attn_map_copy = copy.deepcopy(attn_map)
    image_size_copy = copy.deepcopy(image_size)

    # Call func0 to verify input validity
    try:
        expected_inds, expected_inds_normalised = post_process_sampled_indices(
            sampled_inds_list=sampled_inds_list_copy,
            attn_map=attn_map_copy,
            image_size=image_size_copy
        )
    except Exception:
        return  # Skip inputs that cause exceptions

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Single index with minimal attention map"
        elif case_count == 1:
            desc = "Multiple indices with small attention map"
        else:
            desc = "Multiple indices with medium attention map"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Single index with large image size"
        elif case_count == 4:
            desc = "Multiple indices with large attention map"
        elif case_count == 5:
            desc = "Single index with small image size"
        elif case_count == 6:
            desc = "Multiple indices with varying image sizes"
        else:
            desc = "Multiple indices with large image size"

    # Generate usage code
    usage = f"""import numpy as np

# Construct inputs
sampled_inds_list = {sampled_inds_list_copy}
attn_map = np.array({attn_map_copy.tolist()})
image_size = {image_size_copy}

# Call function
inds, inds_normalised = post_process_sampled_indices(
    sampled_inds_list=sampled_inds_list,
    attn_map=attn_map,
    image_size=image_size
)
"""

    # Store case
    # We don't include the expected output for lib-specific types
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "sampled_inds_list": sampled_inds_list_copy,
            "attn_map": attn_map_copy.tolist(),
            "image_size": image_size_copy
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