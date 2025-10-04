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
def flatten_nested_dict_list(d, parent_key="", sep="_", item_key=""):
    items = []
    if isinstance(d, (tuple, list)):
        new_key = parent_key + sep + item_key if len(parent_key) > 0 else item_key
        for i, v in enumerate(d):
            items.extend(flatten_nested_dict_list(v, new_key, sep=sep, item_key=str(i)))
        return items
    elif isinstance(d, dict):
        new_key = parent_key + sep + item_key if len(parent_key) > 0 else item_key
        for k, v in d.items():
            assert isinstance(k, str)
            items.extend(flatten_nested_dict_list(v, new_key, sep=sep, item_key=k))
        return items
    else:
        new_key = parent_key + sep + item_key if len(parent_key) > 0 else item_key
        return [(new_key, d)]

# Strategy for generating nested dictionaries and lists
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
@given(d=json_strategy, parent_key=st.text(st.characters(whitelist_categories=('L', 'N')), max_size=5), sep=st.text(st.characters(whitelist_categories=('P', 'S')), max_size=1), item_key=st.text(st.characters(whitelist_categories=('L', 'N')), max_size=5))
@example(d={}, parent_key="", sep="_", item_key="")
@example(d=[], parent_key="", sep="_", item_key="")
@example(d={"a": 1}, parent_key="", sep="_", item_key="")
@example(d=[1, 2], parent_key="", sep="_", item_key="")
@example(d={"a": {"b": 1}}, parent_key="", sep="_", item_key="")
@example(d={"a": [1, 2]}, parent_key="", sep="_", item_key="")
@example(d={"a": {"b": {"c": 1}}}, parent_key="", sep="_", item_key="")
def test_flatten_nested_dict_list(d, parent_key, sep, item_key):
    global stop_collecting
    if stop_collecting:
        return
    
    d_copy = copy.deepcopy(d)
    try:
        expected = flatten_nested_dict_list(d_copy, parent_key, sep, item_key)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if isinstance(d, (dict, list)):
        generated_cases.append({
            "Inputs": {"d": d, "parent_key": parent_key, "sep": sep, "item_key": item_key},
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