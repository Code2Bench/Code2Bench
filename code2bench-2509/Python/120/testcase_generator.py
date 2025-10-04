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
def get_optimal_patched_size_with_sp(patched_h, patched_w, sp_size):
    assert sp_size > 0 and (sp_size & (sp_size - 1)) == 0, "sp_size must be a power of 2"

    h_ratio, w_ratio = 1, 1
    while sp_size != 1:
        sp_size //= 2
        if patched_h % 2 == 0:
            patched_h //= 2
            h_ratio *= 2
        elif patched_w % 2 == 0:
            patched_w //= 2
            w_ratio *= 2
        else:
            if patched_h > patched_w:
                patched_h //= 2
                h_ratio *= 2
            else:
                patched_w //= 2
                w_ratio *= 2
    return patched_h * h_ratio, patched_w * w_ratio

# Strategy for generating power of 2 values
def power_of_two_strategy():
    return st.integers(min_value=0, max_value=10).map(lambda x: 2 ** x)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    patched_h=st.integers(min_value=1, max_value=1024),
    patched_w=st.integers(min_value=1, max_value=1024),
    sp_size=power_of_two_strategy()
)
@example(patched_h=1, patched_w=1, sp_size=1)
@example(patched_h=2, patched_w=2, sp_size=2)
@example(patched_h=3, patched_w=3, sp_size=4)
@example(patched_h=4, patched_w=4, sp_size=8)
@example(patched_h=5, patched_w=5, sp_size=16)
@example(patched_h=6, patched_w=6, sp_size=32)
@example(patched_h=7, patched_w=7, sp_size=64)
@example(patched_h=8, patched_w=8, sp_size=128)
@example(patched_h=9, patched_w=9, sp_size=256)
@example(patched_h=10, patched_w=10, sp_size=512)
def test_get_optimal_patched_size_with_sp(patched_h, patched_w, sp_size):
    global stop_collecting
    if stop_collecting:
        return
    
    patched_h_copy = copy.deepcopy(patched_h)
    patched_w_copy = copy.deepcopy(patched_w)
    sp_size_copy = copy.deepcopy(sp_size)
    try:
        expected = get_optimal_patched_size_with_sp(patched_h_copy, patched_w_copy, sp_size_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"patched_h": patched_h, "patched_w": patched_w, "sp_size": sp_size},
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