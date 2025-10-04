from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from collections.abc import Mapping
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

# Ground truth function
def flatten_results_dict(results):
    """
    Expand a hierarchical dict of scalars into a flat dict of scalars.
    If results[k1][k2][k3] = v, the returned dict will have the entry
    {"k1/k2/k3": v}.

    Args:
        results (dict):
    """
    r = {}
    for k, v in results.items():
        if isinstance(v, Mapping):
            v = flatten_results_dict(v)
            for kk, vv in v.items():
                r[k + "/" + kk] = vv
        else:
            r[k] = v
    return r

# Strategies for generating inputs
def key_strategy():
    return st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), min_codepoint=32, max_codepoint=126), min_size=1, max_size=10)

def value_strategy():
    return st.one_of(
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), min_codepoint=32, max_codepoint=126), min_size=1, max_size=10)
    )

def recursive_dict_strategy():
    return st.recursive(
        st.dictionaries(key_strategy(), value_strategy(), min_size=1, max_size=3),
        lambda children: st.dictionaries(key_strategy(), children, min_size=1, max_size=3),
        max_leaves=5  # Restrict recursive depth
    )

# Hypothesis test configuration
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(results=recursive_dict_strategy())
@example(results={})
@example(results={"key1": "value1"})
@example(results={"key1": {"key2": "value2"}})
@example(results={"key1": {"key2": {"key3": "value3"}}})
@example(results={"key1": 123, "key2": 456.789})
def test_flatten_results_dict(results):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return

    # Deep copy input to avoid modification
    results_copy = copy.deepcopy(results)

    # Call func0 to verify input validity
    try:
        expected = flatten_results_dict(results_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Simple flat dictionary"
        elif case_count == 1:
            desc = "Nested dictionary with two levels"
        else:
            desc = "Mixed types in nested dictionary"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Empty dictionary"
        elif case_count == 4:
            desc = "Single key-value pair"
        elif case_count == 5:
            desc = "Deeply nested dictionary"
        elif case_count == 6:
            desc = "Dictionary with mixed scalar types"
        else:
            desc = "Dictionary with multiple nested levels"

    # Store case
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "results": results_copy
        },
        "Expected": expected,
        "Usage": None
    })
    case_count += 1
    if case_count >= MAX_CASES:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {sum(len(cases) for cases in generated_cases.values())} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)