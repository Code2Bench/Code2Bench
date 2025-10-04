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
def match_size(image_size, h, w):
    ratio_ = 9999
    size_ = 9999
    select_size = None
    for image_s in image_size:
        ratio_tmp = abs(image_s[0] / image_s[1] - h / w)
        size_tmp = abs(max(image_s) - max(w, h))
        if ratio_tmp < ratio_:
            ratio_ = ratio_tmp
            size_ = size_tmp
            select_size = image_s
        if ratio_ == ratio_tmp:
            if size_ == size_tmp:
                select_size = image_s
    return select_size

# Strategy for generating image sizes
def image_size_strategy():
    return st.lists(
        st.tuples(
            st.integers(min_value=1, max_value=1000),
            st.integers(min_value=1, max_value=1000)
        ),
        min_size=1, max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    image_size=image_size_strategy(),
    h=st.integers(min_value=1, max_value=1000),
    w=st.integers(min_value=1, max_value=1000)
)
@example(image_size=[(100, 100)], h=100, w=100)
@example(image_size=[(200, 100), (100, 200)], h=100, w=100)
@example(image_size=[(50, 50), (100, 100)], h=75, w=75)
@example(image_size=[(300, 200), (200, 300)], h=250, w=250)
@example(image_size=[(400, 400), (500, 500)], h=450, w=450)
def test_match_size(image_size, h, w):
    global stop_collecting
    if stop_collecting:
        return
    
    image_size_copy = copy.deepcopy(image_size)
    try:
        expected = match_size(image_size_copy, h, w)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"image_size": image_size, "h": h, "w": w},
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