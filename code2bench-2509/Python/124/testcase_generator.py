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
def flatten_state_dict(obj, parent_key="", sep="."):
    items = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
            items.update(flatten_state_dict(v, new_key, sep=sep))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
            items.update(flatten_state_dict(v, new_key, sep=sep))
    else:
        items[parent_key] = obj
    return items

# Strategy for JSON-like objects
json_strategy = st.recursive(
    st.one_of([
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'))),
        st.booleans()
    ]),
    lambda children: st.one_of(
        st.lists(children, max_size=5),
        st.dictionaries(st.text(st.characters(whitelist_categories=('L', 'N')), max_size=5), children, max_size=5)
    ),
    max_leaves=5
)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(obj=json_strategy, sep=st.text(st.characters(whitelist_categories=('P', 'S')), min_size=1, max_size=2))
@example(obj={}, sep=".")
@example(obj={"a": 1}, sep=".")
@example(obj={"a": {"b": 2}}, sep=".")
@example(obj={"a": [1, 2]}, sep=".")
@example(obj=[1, 2], sep=".")
@example(obj={"a": {"b": [1, 2]}}, sep=".")
@example(obj={"a": {"b": {"c": 3}}}, sep=".")
def test_flatten_state_dict(obj, sep):
    global stop_collecting
    if stop_collecting:
        return
    
    obj_copy = copy.deepcopy(obj)
    try:
        expected = flatten_state_dict(obj_copy, sep=sep)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if isinstance(obj, (dict, list)):
        generated_cases.append({
            "Inputs": {"obj": obj, "sep": sep},
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