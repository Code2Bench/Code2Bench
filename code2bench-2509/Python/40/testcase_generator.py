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
def list_of_dict_to_dict_of_list(list_of_dict: list[dict]):
    if len(list_of_dict) == 0:
        return {}
    keys = list_of_dict[0].keys()
    output = {key: [] for key in keys}
    for data in list_of_dict:
        for key, item in data.items():
            assert key in output
            output[key].append(item)
    return output

# Strategy for generating dictionaries
def dict_strategy():
    return st.dictionaries(
        keys=st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=5),
        values=st.one_of([
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=5),
            st.booleans()
        ]),
        min_size=1, max_size=5
    )

# Strategy for generating lists of dictionaries
def list_of_dict_strategy():
    return st.lists(
        dict_strategy(),
        min_size=0, max_size=5
    ).filter(lambda lst: all(set(lst[0].keys()) == set(d.keys()) for d in lst) if len(lst) > 0 else True)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(list_of_dict=list_of_dict_strategy())
@example(list_of_dict=[])
@example(list_of_dict=[{"a": 1}])
@example(list_of_dict=[{"a": 1}, {"a": 2}])
@example(list_of_dict=[{"a": 1, "b": "x"}, {"a": 2, "b": "y"}])
@example(list_of_dict=[{"a": 1}, {"a": 2}, {"a": 3}])
def test_list_of_dict_to_dict_of_list(list_of_dict):
    global stop_collecting
    if stop_collecting:
        return
    
    list_of_dict_copy = copy.deepcopy(list_of_dict)
    try:
        expected = list_of_dict_to_dict_of_list(list_of_dict_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if len(list_of_dict) > 0 or len(list_of_dict) == 0:
        generated_cases.append({
            "Inputs": {"list_of_dict": list_of_dict},
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