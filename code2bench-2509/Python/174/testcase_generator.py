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
def fit_res(w, h, max_w, max_h):
    if w <= max_w and h <= max_h:
        return w, h
    aspect = w / h
    if w > max_w:
        w = max_w
        h = int(w / aspect)
    if h > max_h:
        h = max_h
        w = int(h * aspect)
    return w - (w % 2), h - (h % 2)

# Strategy for generating dimensions
dimension_strategy = st.integers(min_value=1, max_value=10000)
max_dimension_strategy = st.integers(min_value=1, max_value=10000)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    w=dimension_strategy,
    h=dimension_strategy,
    max_w=max_dimension_strategy,
    max_h=max_dimension_strategy
)
@example(w=100, h=100, max_w=100, max_h=100)
@example(w=200, h=100, max_w=100, max_h=100)
@example(w=100, h=200, max_w=100, max_h=100)
@example(w=200, h=200, max_w=100, max_h=100)
@example(w=100, h=100, max_w=200, max_h=200)
@example(w=100, h=100, max_w=50, max_h=50)
@example(w=100, h=100, max_w=50, max_h=200)
@example(w=100, h=100, max_w=200, max_h=50)
def test_fit_res(w, h, max_w, max_h):
    global stop_collecting
    if stop_collecting:
        return
    
    w_copy = copy.deepcopy(w)
    h_copy = copy.deepcopy(h)
    max_w_copy = copy.deepcopy(max_w)
    max_h_copy = copy.deepcopy(max_h)
    try:
        expected = fit_res(w_copy, h_copy, max_w_copy, max_h_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"w": w, "h": h, "max_w": max_w, "max_h": max_h},
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