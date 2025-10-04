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
def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio

# Strategy for generating aspect ratios
def ratio_strategy():
    return st.tuples(
        st.integers(min_value=1, max_value=100),
        st.integers(min_value=1, max_value=100)
    )

# Strategy for generating target ratios
def target_ratios_strategy():
    return st.lists(ratio_strategy(), min_size=1, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    aspect_ratio=st.floats(min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False),
    target_ratios=target_ratios_strategy(),
    width=st.integers(min_value=1, max_value=1000),
    height=st.integers(min_value=1, max_value=1000),
    image_size=st.integers(min_value=1, max_value=1000)
)
@example(aspect_ratio=1.0, target_ratios=[(1, 1)], width=100, height=100, image_size=100)
@example(aspect_ratio=1.5, target_ratios=[(3, 2), (4, 3)], width=200, height=150, image_size=200)
@example(aspect_ratio=0.75, target_ratios=[(3, 4), (1, 1)], width=150, height=200, image_size=200)
@example(aspect_ratio=2.0, target_ratios=[(2, 1), (4, 3)], width=400, height=200, image_size=400)
@example(aspect_ratio=1.333, target_ratios=[(4, 3), (16, 9)], width=800, height=600, image_size=800)
def test_find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    global stop_collecting
    if stop_collecting:
        return
    
    target_ratios_copy = copy.deepcopy(target_ratios)
    try:
        expected = find_closest_aspect_ratio(aspect_ratio, target_ratios_copy, width, height, image_size)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {
            "aspect_ratio": aspect_ratio,
            "target_ratios": target_ratios,
            "width": width,
            "height": height,
            "image_size": image_size
        },
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