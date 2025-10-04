from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import operator
from functools import reduce
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
def get_in(keys, coll, default=None, no_default=False):
    try:
        return reduce(operator.getitem, keys, coll)
    except (KeyError, IndexError, TypeError):
        if no_default:
            raise
        return default

# Strategies for generating inputs
def keys_strategy():
    return st.lists(
        st.one_of(
            st.integers(min_value=0, max_value=10),  # For list indexing
            st.text(min_size=1, max_size=5)        # For dict keys
        ),
        min_size=0, max_size=5
    )

def coll_strategy(keys):
    if not keys:
        return st.one_of(
            st.lists(st.integers(), min_size=0, max_size=10),
            st.dictionaries(st.text(min_size=1, max_size=5), st.integers(), min_size=0, max_size=10)
        )
    
    # Build a collection that matches the keys
    coll = {}
    for key in keys:
        if isinstance(key, int):
            coll = st.lists(st.integers(), min_size=key + 1, max_size=key + 1)
        elif isinstance(key, str):
            coll = st.dictionaries(st.just(key), st.integers(), min_size=1, max_size=1)
    return coll

def default_strategy():
    return st.one_of(st.none(), st.integers(), st.text())

def no_default_strategy():
    return st.booleans()

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    keys=keys_strategy(),
    coll=st.builds(
        lambda k: coll_strategy(k),
        keys_strategy()
    ),
    default=default_strategy(),
    no_default=no_default_strategy()
)
@example(keys=[], coll=[1, 2, 3], default=None, no_default=False)
@example(keys=[0], coll=[1, 2, 3], default=None, no_default=True)
@example(keys=["a"], coll={"a": 1}, default=None, no_default=False)
@example(keys=[0, 1], coll=[[1, 2], [3, 4]], default=None, no_default=True)
@example(keys=["a", "b"], coll={"a": {"b": 1}}, default=None, no_default=False)
@example(keys=[0, "a"], coll=[{"a": 1}], default=None, no_default=True)
def test_get_in(keys, coll, default, no_default):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    keys_copy = copy.deepcopy(keys)
    coll_copy = copy.deepcopy(coll)
    default_copy = copy.deepcopy(default)
    no_default_copy = copy.deepcopy(no_default)

    # Call func0 to verify input validity
    try:
        result = get_in(keys_copy, coll_copy, default_copy, no_default_copy)
    except Exception:
        if not no_default_copy:
            return  # Skip unexpected exceptions when no_default is False

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "keys": keys_copy,
            "coll": coll_copy,
            "default": default_copy,
            "no_default": no_default_copy
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