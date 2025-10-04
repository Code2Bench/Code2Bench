from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import ast
import json
import os
import atexit
import copy
from typing import List

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _parse_options_string(options_string: str) -> List[str]:
    try:
        parsed_list = ast.literal_eval(options_string.strip())
        return [str(option).strip() for option in parsed_list]
    except (ValueError, SyntaxError):
        return []

# Strategy for generating options_string
def options_string_strategy():
    # Generate valid list representations
    valid_list = st.lists(
        st.one_of(
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False)
        ),
        min_size=0, max_size=10
    ).map(lambda x: str(x))
    
    # Generate invalid strings
    invalid_string = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=1, max_size=20
    )
    
    return st.one_of(valid_list, invalid_string)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(options_string=options_string_strategy())
@example(options_string="['option1', 'option2', 'option3']")
@example(options_string="[1, 2, 3]")
@example(options_string="[1.0, 2.0, 3.0]")
@example(options_string="['  option1  ', '  option2  ', '  option3  ']")
@example(options_string="invalid_string")
@example(options_string="")
def test_parse_options_string(options_string: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    options_string_copy = copy.deepcopy(options_string)

    # Call func0 to verify input validity
    try:
        expected = _parse_options_string(options_string_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "options_string": options_string_copy
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