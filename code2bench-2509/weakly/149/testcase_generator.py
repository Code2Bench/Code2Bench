from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from math import isqrt

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def generate_primes(max_num: int) -> list[int]:
    are_primes = [True] * (max_num + 1)
    are_primes[0] = are_primes[1] = False
    for i in range(2, isqrt(max_num) + 1):
        if are_primes[i]:
            for j in range(i * i, max_num + 1, i):
                are_primes[j] = False

    return [prime for prime, is_prime in enumerate(are_primes) if is_prime]

# Strategy for generating max_num
def max_num_strategy():
    return st.integers(min_value=0, max_value=1000)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(max_num=max_num_strategy())
@example(max_num=0)
@example(max_num=1)
@example(max_num=2)
@example(max_num=10)
@example(max_num=100)
def test_generate_primes(max_num: int):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    max_num_copy = copy.deepcopy(max_num)

    # Call func0 to verify input validity
    try:
        expected = generate_primes(max_num_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "max_num": max_num_copy
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