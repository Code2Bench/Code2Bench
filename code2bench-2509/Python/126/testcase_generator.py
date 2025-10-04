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
def combine_nums(a, b):
    a = int(a)
    b = int(b)
    possible = [[a + b, f"{a}+{b}={a+b}"], [a * b, f"{a}*{b}={a*b}"]]
    if a <= b:
        possible.append([b - a, f"{b}-{a}={b-a}"])
        if a != 0 and b % a == 0:
            possible.append([b // a, f"{b}/{a}={round(b//a,0)}"])
    else:
        possible.append([a - b, f"{a}-{b}={a-b}"])
        if b != 0 and a % b == 0:
            possible.append([a // b, f"{a}/{b}={round(a//b,0)}"])
    return possible

# Strategy for generating integers
int_strategy = st.integers(min_value=-2147483648, max_value=2147483647)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(a=int_strategy, b=int_strategy)
@example(a=0, b=0)
@example(a=1, b=1)
@example(a=2, b=4)
@example(a=4, b=2)
@example(a=-1, b=1)
@example(a=1, b=-1)
@example(a=0, b=1)
@example(a=1, b=0)
def test_combine_nums(a, b):
    global stop_collecting
    if stop_collecting:
        return
    
    a_copy = copy.deepcopy(a)
    b_copy = copy.deepcopy(b)
    try:
        expected = combine_nums(a_copy, b_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter to ensure meaningful cases
    if (a != 0 or b != 0) and (a != b):
        generated_cases.append({
            "Inputs": {"a": a, "b": b},
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