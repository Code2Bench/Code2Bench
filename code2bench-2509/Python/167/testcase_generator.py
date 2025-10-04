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
def increment_version(old_version, increment):
    new_version_parts = []
    clear = False
    for cur, inc in zip(old_version, increment):
        if clear:
            new_version_parts.append("0")
        else:
            new_version_parts.append(str(int(cur) + inc))
            if inc:
                clear = True
    return new_version_parts

# Strategy for version parts
version_part_strategy = st.text(st.characters(whitelist_categories=('Nd',)), min_size=1, max_size=3).filter(lambda x: x.isdigit())
version_strategy = st.lists(version_part_strategy, min_size=1, max_size=5)

# Strategy for increment values
increment_strategy = st.lists(st.integers(min_value=0, max_value=9), min_size=1, max_size=5).map(tuple)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(old_version=version_strategy, increment=increment_strategy)
@example(old_version=["1", "0", "0"], increment=(1, 0, 0))
@example(old_version=["1", "2", "3"], increment=(0, 1, 0))
@example(old_version=["9", "9", "9"], increment=(0, 0, 1))
@example(old_version=["1", "0", "0"], increment=(0, 0, 0))
@example(old_version=["1", "0", "0"], increment=(1, 1, 1))
@example(old_version=["1", "0", "0"], increment=(0, 0, 1))
@example(old_version=["1", "0", "0"], increment=(1, 0, 1))
def test_increment_version(old_version, increment):
    global stop_collecting
    if stop_collecting:
        return
    
    if len(old_version) != len(increment):
        return  # Skip inputs with mismatched lengths
    
    old_version_copy = copy.deepcopy(old_version)
    increment_copy = copy.deepcopy(increment)
    try:
        expected = increment_version(old_version_copy, increment_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"old_version": old_version, "increment": increment},
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