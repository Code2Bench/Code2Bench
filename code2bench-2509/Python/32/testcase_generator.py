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
def rename_keys(data, key_mapping):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            new_key = key_mapping.get(key, key)
            new_data[new_key] = rename_keys(value, key_mapping)
        return new_data
    elif isinstance(data, list):
        return [rename_keys(item, key_mapping) for item in data]
    else:
        return data

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

# Strategy for key mappings
key_mapping_strategy = st.dictionaries(
    st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=5),
    st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=5),
    min_size=1, max_size=5
)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(data=json_strategy, key_mapping=key_mapping_strategy)
@example(data={}, key_mapping={})
@example(data={"a": 1}, key_mapping={"a": "b"})
@example(data=[1, 2], key_mapping={"a": "b"})
@example(data={"a": {"b": 1}}, key_mapping={"a": "c", "b": "d"})
@example(data="string", key_mapping={"a": "b"})
@example(data={"a": [1]}, key_mapping={"a": "b"})
def test_rename_keys(data, key_mapping):
    global stop_collecting
    if stop_collecting:
        return
    
    data_copy = copy.deepcopy(data)
    key_mapping_copy = copy.deepcopy(key_mapping)
    try:
        expected = rename_keys(data_copy, key_mapping_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if isinstance(data, (dict, list)) or key_mapping:
        generated_cases.append({
            "Inputs": {"data": data, "key_mapping": key_mapping},
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