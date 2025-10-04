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
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

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
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(results=recursive_dict_strategy())
@example(results={})
@example(results={"key1": "value1"})
@example(results={"key1": {"key2": "value2"}})
@example(results={"key1": {"key2": {"key3": "value3"}}})
@example(results={"key1": 123, "key2": 456.789})
def test_flatten_results_dict(results):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    results_copy = copy.deepcopy(results)

    # Call func0 to verify input validity
    try:
        expected = flatten_results_dict(results_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "results": results_copy
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