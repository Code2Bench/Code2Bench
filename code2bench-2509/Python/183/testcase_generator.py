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
def isqrt(n):
    """Integer square root using Newton's method"""
    if n < 0:
        raise ValueError("Square root of negative number")
    if n == 0:
        return 0

    # Initial guess
    x = n
    while True:
        # Newton's method: x_new = (x + n/x) / 2
        x_new = (x + n // x) // 2
        if x_new >= x:
            return x
        x = x_new

# Strategy for generating integers
int_strategy = st.integers(min_value=0, max_value=2147483647)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(n=int_strategy)
@example(n=0)
@example(n=1)
@example(n=2)
@example(n=3)
@example(n=4)
@example(n=9)
@example(n=16)
@example(n=25)
@example(n=2147483647)
def test_isqrt(n):
    global stop_collecting
    if stop_collecting:
        return
    
    try:
        expected = isqrt(n)
    except ValueError:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"n": n},
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