from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from collections.abc import MutableMapping
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
def flatten_dict(dictionary, prefix="", sep="_"):
    results = []
    for k, v in dictionary.items():
        new_key = str(prefix) + sep + str(k) if prefix else k
        if isinstance(v, MutableMapping):
            results.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            results.append((new_key, v))
    return dict(results)

# Strategies for generating inputs
def key_strategy():
    return st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10)

def value_strategy():
    return st.one_of(
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10)
    )

def dict_strategy():
    return st.recursive(
        st.dictionaries(key_strategy(), value_strategy(), min_size=1, max_size=5),
        lambda children: st.dictionaries(key_strategy(), children, min_size=1, max_size=3),
        max_leaves=5  # Restrict recursive depth
    )

def sep_strategy():
    return st.text(alphabet=st.characters(whitelist_categories=('P', 'S')), min_size=1, max_size=1)

def prefix_strategy():
    return st.one_of(
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10),
        st.just("")
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    dictionary=dict_strategy(),
    prefix=prefix_strategy(),
    sep=sep_strategy()
)
@example(
    dictionary={},
    prefix="",
    sep="_"
)
@example(
    dictionary={"a": 1},
    prefix="",
    sep="_"
)
@example(
    dictionary={"a": {"b": 2}},
    prefix="",
    sep="_"
)
@example(
    dictionary={"a": {"b": {"c": 3}}},
    prefix="",
    sep="_"
)
@example(
    dictionary={"a": {"b": 2}, "c": 3},
    prefix="pre",
    sep="."
)
def test_flatten_dict(dictionary, prefix, sep):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    dictionary_copy = copy.deepcopy(dictionary)
    prefix_copy = copy.deepcopy(prefix)
    sep_copy = copy.deepcopy(sep)

    # Call func0 to verify input validity
    try:
        expected = flatten_dict(dictionary_copy, prefix_copy, sep_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "dictionary": dictionary_copy,
            "prefix": prefix_copy,
            "sep": sep_copy
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