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
def diff_dicts(dict1, dict2):
    diff = {}
    for key, value in dict1.items():
        if key not in dict2:
            diff[key] = value
            continue

        try:
            if value != dict2[key]:
                diff[key] = value
        except Exception:
            pass
    return diff

# Strategy for generating dictionaries
def dict_strategy():
    return st.dictionaries(
        keys=st.text(st.characters(whitelist_categories=('L', 'N'), max_codepoint=127), min_size=1, max_size=5),
        values=st.one_of([
            st.integers(min_value=-2147483648, max_value=2147483647),
            st.floats(allow_nan=False, allow_infinity=False, width=32),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.booleans(),
            st.lists(st.integers(min_value=-2147483648, max_value=2147483647), max_size=5),
            st.dictionaries(
                keys=st.text(st.characters(whitelist_categories=('L', 'N'), max_codepoint=127), min_size=1, max_size=5),
                values=st.integers(min_value=-2147483648, max_value=2147483647),
                max_size=5
            )
        ]),
        min_size=0, max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(dict1=dict_strategy(), dict2=dict_strategy())
@example(dict1={}, dict2={})
@example(dict1={"a": 1}, dict2={"a": 2})
@example(dict1={"a": 1}, dict2={"b": 2})
@example(dict1={"a": [1, 2]}, dict2={"a": [3, 4]})
@example(dict1={"a": {"b": 1}}, dict2={"a": {"b": 2}})
@example(dict1={"a": "string"}, dict2={"a": "different"})
@example(dict1={"a": True}, dict2={"a": False})
def test_diff_dicts(dict1, dict2):
    global stop_collecting
    if stop_collecting:
        return
    
    dict1_copy = copy.deepcopy(dict1)
    dict2_copy = copy.deepcopy(dict2)
    try:
        expected = diff_dicts(dict1_copy, dict2_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if dict1 or dict2:
        generated_cases.append({
            "Inputs": {"dict1": dict1, "dict2": dict2},
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