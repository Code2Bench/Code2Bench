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
def factorization(dimension: int, factor: int = -1) -> tuple[int, int]:
    if factor > 0 and (dimension % factor) == 0 and dimension >= factor**2:
        m = factor
        n = dimension // factor
        if m > n:
            n, m = m, n
        return m, n
    if factor < 0:
        factor = dimension
    m, n = 1, dimension
    length = m + n
    while m < n:
        new_m = m + 1
        while dimension % new_m != 0:
            new_m += 1
        new_n = dimension // new_m
        if new_m + new_n > length or new_m > factor:
            break
        else:
            m, n = new_m, new_n
    if m > n:
        n, m = m, n
    return m, n

# Strategy for generating dimensions and factors
dimension_strategy = st.integers(min_value=1, max_value=1000)
factor_strategy = st.integers(min_value=-1, max_value=100)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(dimension=dimension_strategy, factor=factor_strategy)
@example(dimension=127, factor=-1)
@example(dimension=128, factor=2)
@example(dimension=250, factor=4)
@example(dimension=360, factor=8)
@example(dimension=512, factor=16)
@example(dimension=1024, factor=32)
def test_factorization(dimension: int, factor: int):
    global stop_collecting
    if stop_collecting:
        return
    
    dimension_copy = copy.deepcopy(dimension)
    factor_copy = copy.deepcopy(factor)
    try:
        expected = factorization(dimension_copy, factor_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if dimension > 0 and factor >= -1:
        generated_cases.append({
            "Inputs": {"dimension": dimension, "factor": factor},
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