from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
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
def generate_crop_size_list(base_size=256, patch_size=32, max_ratio=4.0):
    """generate crop size list

    Args:
        base_size (int, optional): the base size for generate bucket. Defaults to 256.
        patch_size (int, optional): the stride to generate bucket. Defaults to 32.
        max_ratio (float, optional): th max ratio for h or w based on base_size . Defaults to 4.0.

    Returns:
        list: generate crop size list
    """
    num_patches = round((base_size / patch_size) ** 2)
    assert max_ratio >= 1.0
    crop_size_list = []
    wp, hp = num_patches, 1
    while wp > 0:
        if max(wp, hp) / min(wp, hp) <= max_ratio:
            crop_size_list.append((wp * patch_size, hp * patch_size))
        if (hp + 1) * wp <= num_patches:
            hp += 1
        else:
            wp -= 1
    return crop_size_list

# Strategy for generating inputs
base_size_strategy = st.integers(min_value=32, max_value=512)
patch_size_strategy = st.integers(min_value=1, max_value=128).filter(lambda x: x != 0)
max_ratio_strategy = st.floats(min_value=1.0, max_value=10.0, allow_nan=False, allow_infinity=False)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True, deadline=None)
@given(base_size=base_size_strategy, patch_size=patch_size_strategy, max_ratio=max_ratio_strategy)
@example(base_size=256, patch_size=32, max_ratio=4.0)
@example(base_size=128, patch_size=16, max_ratio=2.0)
@example(base_size=512, patch_size=64, max_ratio=1.0)
@example(base_size=64, patch_size=8, max_ratio=10.0)
def test_generate_crop_size_list(base_size, patch_size, max_ratio):
    global stop_collecting
    if stop_collecting:
        return
    
    try:
        expected = generate_crop_size_list(base_size, patch_size, max_ratio)
    except (AssertionError, ZeroDivisionError):
        return  # Skip inputs that cause assertion errors or division by zero
    
    generated_cases.append({
        "Inputs": {"base_size": base_size, "patch_size": patch_size, "max_ratio": max_ratio},
        "Expected": expected
    })
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)