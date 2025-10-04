from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from math import comb

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def nth_combination(iterable, r, index):
    pool = tuple(iterable)
    n = len(pool)
    if (r < 0) or (r > n):
        raise ValueError

    c = 1
    k = min(r, n - r)
    for i in range(1, k + 1):
        c = c * (n - k + i) // i

    if index < 0:
        index += c

    if (index < 0) or (index >= c):
        raise IndexError

    result = []
    while r:
        c, n, r = c * r // n, n - 1, r - 1
        while index >= c:
            index -= c
            c, n = c * (n - r) // n, n - 1
        result.append(pool[-1 - n])

    return tuple(result)

# Strategy for generating iterables
def iterable_strategy():
    return st.one_of([
        st.lists(st.integers(min_value=-2147483648, max_value=2147483647), min_size=0, max_size=10),
        st.lists(st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=5), min_size=0, max_size=10),
        st.lists(st.booleans(), min_size=0, max_size=10)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    iterable=iterable_strategy(),
    r=st.integers(min_value=0, max_value=10),
    index=st.integers(min_value=-100, max_value=100)
)
@example(iterable=[], r=0, index=0)
@example(iterable=[1, 2, 3], r=2, index=0)
@example(iterable=[1, 2, 3], r=2, index=2)
@example(iterable=[1, 2, 3], r=2, index=-1)
@example(iterable=[1, 2, 3], r=3, index=0)
@example(iterable=[1, 2, 3], r=0, index=0)
@example(iterable=[1, 2, 3], r=4, index=0)
@example(iterable=[1, 2, 3], r=2, index=3)
def test_nth_combination(iterable, r, index):
    global stop_collecting
    if stop_collecting:
        return
    
    iterable_copy = copy.deepcopy(iterable)
    try:
        expected = nth_combination(iterable_copy, r, index)
    except (ValueError, IndexError):
        return  # Skip inputs that cause exceptions
    
    if len(iterable) >= r and r >= 0 and 0 <= index < comb(len(iterable), r):
        generated_cases.append({
            "Inputs": {"iterable": iterable, "r": r, "index": index},
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