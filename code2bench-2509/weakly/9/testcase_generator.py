from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import difflib
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
def closest_name(input_str, options):
    input_str = input_str.lower()

    closest_match = difflib.get_close_matches(
        input_str, list(options.keys()), n=1, cutoff=0.5
    )
    assert isinstance(closest_match, list) and len(closest_match) > 0, (
        f"The value [{input_str}] is not valid!"
    )
    result = closest_match[0]

    if result != input_str:
        print(f"Automatically corrected [{input_str}] -> [{result}].")

    return result

# Strategies for generating inputs
def input_str_strategy():
    return st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')))

def options_strategy():
    return st.dictionaries(
        keys=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'))),
        values=st.integers(min_value=0, max_value=100),
        min_size=1, max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    input_str=input_str_strategy(),
    options=options_strategy()
)
@example(
    input_str="hello",
    options={"hello": 1, "world": 2}
)
@example(
    input_str="helo",
    options={"hello": 1, "world": 2}
)
@example(
    input_str="hllo",
    options={"hello": 1, "world": 2}
)
@example(
    input_str="hell",
    options={"hello": 1, "world": 2}
)
@example(
    input_str="heaven",
    options={"hello": 1, "world": 2}
)
def test_closest_name(input_str: str, options: dict):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    input_str_copy = copy.deepcopy(input_str)
    options_copy = copy.deepcopy(options)

    # Call func0 to verify input validity
    try:
        result = closest_name(input_str_copy, options_copy)
    except AssertionError:
        return  # Skip inputs that cause assertions
    except Exception:
        return  # Skip inputs that cause other exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "input_str": input_str_copy,
            "options": options_copy
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