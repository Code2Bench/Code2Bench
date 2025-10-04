from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from collections import OrderedDict
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
def strip_module(state_dict):
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = k[7:] if k.startswith("module.") else k
        new_state_dict[name] = v
    return new_state_dict

# Strategy for generating state_dict
def state_dict_strategy():
    keys = st.one_of(
        st.text(min_size=1, max_size=20).map(lambda s: "module." + s),
        st.text(min_size=1, max_size=20)
    )
    values = st.one_of(
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(min_size=1, max_size=20)
    )
    return st.dictionaries(keys, values, min_size=1, max_size=10).map(lambda d: OrderedDict(d))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(state_dict=state_dict_strategy())
@example(state_dict=OrderedDict({"module.key1": 1, "key2": 2}))
@example(state_dict=OrderedDict({"key1": 1, "key2": 2}))
@example(state_dict=OrderedDict({"module.key1": 1, "module.key2": 2}))
@example(state_dict=OrderedDict({"key1": 1}))
@example(state_dict=OrderedDict({"module.key1": 1}))
def test_strip_module(state_dict):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    state_dict_copy = copy.deepcopy(state_dict)

    # Call func0 to verify input validity
    try:
        expected = strip_module(state_dict_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "state_dict": dict(state_dict_copy)
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