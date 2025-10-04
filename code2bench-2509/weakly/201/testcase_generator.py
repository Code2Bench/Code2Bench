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
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

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
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(list_of_dict=list_of_flat_dict_strategy())
@example(list_of_dict=[])
@example(list_of_dict=[{"a": 1}])
@example(list_of_dict=[{"a": 1}, {"a": 2}])
@example(list_of_dict=[{"a": 1}, {"b": 2}])
@example(list_of_dict=[{"a": 1}, {"a": 2}, {"b": 3}])
def test_list_of_flat_dict_to_dict_of_list(list_of_dict):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    list_of_dict_copy = copy.deepcopy(list_of_dict)

    # Call func0 to verify input validity
    try:
        expected = list_of_flat_dict_to_dict_of_list(list_of_dict_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "list_of_dict": list_of_dict_copy
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