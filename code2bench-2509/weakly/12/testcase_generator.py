from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import Dict, Any

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _deep_merge_dicts(source: Dict, destination: Dict) -> Dict:
    """
    Recursively merges the 'source' dictionary into the 'destination' dictionary.
    Keys from 'source' will overwrite existing keys in 'destination'.
    If a key in 'source' corresponds to a dictionary, a recursive merge is performed.
    The 'destination' dictionary is modified in place.
    """
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            if isinstance(
                node, dict
            ):  # Ensure the destination node is a dict for merging
                _deep_merge_dicts(value, node)
            else:  # If destination's node is not a dict, overwrite it entirely
                destination[key] = copy.deepcopy(value)
        else:
            destination[key] = value
    return destination

# Strategies for generating dictionaries
def dict_strategy(max_depth: int = 3) -> st.SearchStrategy[Dict]:
    """
    Recursively generates dictionaries with a maximum depth to avoid infinite recursion.
    """
    base_strategy = st.one_of(
        st.none(),
        st.booleans(),
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(min_size=0, max_size=10)
    )
    return st.recursive(
        base_strategy,
        lambda children: st.dictionaries(
            keys=st.text(min_size=1, max_size=5),
            values=children,
            min_size=0, max_size=5
        ),
        max_leaves=max_depth
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    source=dict_strategy(),
    destination=dict_strategy()
)
@example(source={}, destination={})
@example(source={"a": 1}, destination={"b": 2})
@example(source={"a": {"b": 1}}, destination={"a": {"c": 2}})
@example(source={"a": 1}, destination={"a": {"b": 2}})
@example(source={"a": {"b": 1}}, destination={"a": 2})
def test_deep_merge_dicts(source: Dict, destination: Dict):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    source_copy = copy.deepcopy(source)
    destination_copy = copy.deepcopy(destination)

    # Call func0 to verify input validity
    try:
        result = _deep_merge_dicts(source_copy, destination_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "source": source_copy,
            "destination": destination_copy
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