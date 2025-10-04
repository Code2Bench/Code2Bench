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
def build_buckets(mantissa_lst: list[int], max_value: int) -> list[int]:
    exponent = 0
    buckets: list[int] = []
    while True:
        for m in mantissa_lst:
            value = m * 10**exponent
            if value <= max_value:
                buckets.append(value)
            else:
                return buckets
        exponent += 1

# Strategy for generating mantissa_lst
def mantissa_lst_strategy():
    return st.lists(
        st.integers(min_value=1, max_value=9),  # Mantissa values between 1 and 9
        min_size=1, max_size=5, unique=True  # Ensure unique mantissa values
    )

# Strategy for generating max_value
def max_value_strategy():
    return st.integers(min_value=1, max_value=10**6)  # Max value up to 1 million

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(mantissa_lst=mantissa_lst_strategy(), max_value=max_value_strategy())
@example(mantissa_lst=[1], max_value=1)
@example(mantissa_lst=[1, 2], max_value=100)
@example(mantissa_lst=[1, 3, 5], max_value=1000)
@example(mantissa_lst=[9], max_value=10)
@example(mantissa_lst=[1, 2, 3, 4, 5], max_value=10000)
def test_build_buckets(mantissa_lst: list[int], max_value: int):
    global stop_collecting
    if stop_collecting:
        return
    
    mantissa_lst_copy = copy.deepcopy(mantissa_lst)
    max_value_copy = copy.deepcopy(max_value)
    try:
        expected = build_buckets(mantissa_lst_copy, max_value_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"mantissa_lst": mantissa_lst, "max_value": max_value},
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