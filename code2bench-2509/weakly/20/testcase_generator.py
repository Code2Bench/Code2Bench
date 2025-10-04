from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from math import ceil

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def get_resize_factor(original_shape, pixels_range, shape_multiplier=14):
    # Original dimensions
    H_ori, W_ori = original_shape
    n_pixels_ori = W_ori * H_ori

    # Determine the closest number of pixels within the range
    min_pixels, max_pixels = pixels_range
    target_pixels = min(max_pixels, max(min_pixels, n_pixels_ori))

    # Calculate the resize factor
    resize_factor = (target_pixels / n_pixels_ori) ** 0.5
    new_width = int(W_ori * resize_factor)
    new_height = int(H_ori * resize_factor)
    new_height = ceil(new_height / shape_multiplier) * shape_multiplier
    new_width = ceil(new_width / shape_multiplier) * shape_multiplier

    return resize_factor, (new_height, new_width)

# Strategies for generating inputs
def original_shape_strategy():
    return st.tuples(
        st.integers(min_value=1, max_value=1000),
        st.integers(min_value=1, max_value=1000)
    )

def pixels_range_strategy():
    return st.tuples(
        st.integers(min_value=1, max_value=1000000),
        st.integers(min_value=1, max_value=1000000)
    ).filter(lambda x: x[0] <= x[1])

def shape_multiplier_strategy():
    return st.integers(min_value=1, max_value=100)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    original_shape=original_shape_strategy(),
    pixels_range=pixels_range_strategy(),
    shape_multiplier=shape_multiplier_strategy()
)
@example(
    original_shape=(100, 100),
    pixels_range=(10000, 20000),
    shape_multiplier=14
)
@example(
    original_shape=(1, 1),
    pixels_range=(1, 1),
    shape_multiplier=1
)
@example(
    original_shape=(1000, 1000),
    pixels_range=(1000000, 1000000),
    shape_multiplier=100
)
@example(
    original_shape=(500, 500),
    pixels_range=(100000, 200000),
    shape_multiplier=10
)
def test_get_resize_factor(original_shape, pixels_range, shape_multiplier):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    original_shape_copy = copy.deepcopy(original_shape)
    pixels_range_copy = copy.deepcopy(pixels_range)
    shape_multiplier_copy = copy.deepcopy(shape_multiplier)

    # Call func0 to verify input validity
    try:
        resize_factor, new_shape = get_resize_factor(original_shape_copy, pixels_range_copy, shape_multiplier_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "original_shape": original_shape_copy,
            "pixels_range": pixels_range_copy,
            "shape_multiplier": shape_multiplier_copy
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