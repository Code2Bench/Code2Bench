from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import collections
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
def list_of_flat_dict_to_dict_of_list(list_of_dict):
    """
    Helper function to go from a list of flat dictionaries to a dictionary of lists.
    By "flat" we mean that none of the values are dictionaries, but are numpy arrays,
    floats, etc.

    Args:
        list_of_dict (list): list of flat dictionaries

    Returns:
        dict_of_list (dict): dictionary of lists
    """
    assert isinstance(list_of_dict, list)
    dic = collections.OrderedDict()
    for i in range(len(list_of_dict)):
        for k in list_of_dict[i]:
            if k not in dic:
                dic[k] = []
            dic[k].append(list_of_dict[i][k])
    return dic

# Strategies for generating inputs
def flat_value_strategy():
    return st.one_of(
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(min_size=0, max_size=10),
        st.booleans()
    )

def flat_dict_strategy():
    return st.dictionaries(
        keys=st.text(min_size=1, max_size=10),
        values=flat_value_strategy(),
        min_size=1, max_size=5
    )

def list_of_flat_dict_strategy():
    return st.lists(
        flat_dict_strategy(),
        min_size=1, max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(list_of_dict=list_of_flat_dict_strategy())
@example(list_of_dict=[])
@example(list_of_dict=[{"a": 1}])
@example(list_of_dict=[{"a": 1}, {"a": 2}])
@example(list_of_dict=[{"a": 1}, {"b": 2}])
@example(list_of_dict=[{"a": 1}, {"a": 2}, {"b": 3}])
def test_list_of_flat_dict_to_dict_of_list(list_of_dict):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return

    # Deep copy input to avoid modification
    list_of_dict_copy = copy.deepcopy(list_of_dict)

    # Call func0 to verify input validity
    try:
        expected = list_of_flat_dict_to_dict_of_list(list_of_dict_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Multiple dictionaries with overlapping keys"
        elif case_count == 1:
            desc = "Single dictionary"
        else:
            desc = "Multiple dictionaries with unique keys"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Empty list"
        elif case_count == 4:
            desc = "Single key in all dictionaries"
        elif case_count == 5:
            desc = "Mixed keys in dictionaries"
        elif case_count == 6:
            desc = "Large number of dictionaries"
        else:
            desc = "Mixed types in dictionary values"

    # Store case
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "list_of_dict": list_of_dict_copy
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