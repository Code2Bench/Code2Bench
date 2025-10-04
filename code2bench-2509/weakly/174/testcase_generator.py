from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import ast
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
def parse_nested_str_list(input_string):
    # Add quotation marks around the words in the string
    quoted_string = re.sub(r"(\w+)", r'"\1"', input_string)

    # Safely evaluate the string as a Python object
    try:
        python_object = ast.literal_eval(quoted_string)
        return python_object
    except (ValueError, SyntaxError) as e:
        print(f"Failed to convert string to Python object: {e}")
        return input_string

# Strategy for generating input strings
def input_string_strategy():
    # Generate nested lists of words
    word = st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10)
    nested_list = st.recursive(
        word,
        lambda children: st.lists(children, min_size=1, max_size=3),
        max_leaves=5
    )
    return st.builds(
        lambda x: str(x).replace("'", "").replace('"', ''),
        nested_list
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(input_string=input_string_strategy())
@example(input_string="")
@example(input_string="a")
@example(input_string="a b")
@example(input_string="[a b]")
@example(input_string="[a [b c]]")
@example(input_string="[[a b] [c d]]")
def test_parse_nested_str_list(input_string: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    input_string_copy = copy.deepcopy(input_string)

    # Call func0 to verify input validity
    try:
        expected = parse_nested_str_list(input_string_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "input_string": input_string_copy
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