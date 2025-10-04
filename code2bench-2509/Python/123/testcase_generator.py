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
def _find_unclosed(json_str):
    """
    Identifies the unclosed braces and brackets in the JSON string.

    Args:
        json_str (str): The JSON string to analyze.

    Returns:
        list: A list of unclosed elements in the order they were opened.
    """
    unclosed = []
    inside_string = False
    escape_next = False

    for char in json_str:
        if inside_string:
            if escape_next:
                escape_next = False
            elif char == "\\":
                escape_next = True
            elif char == '"':
                inside_string = False
        else:
            if char == '"':
                inside_string = True
            elif char in "{[":
                unclosed.append(char)
            elif char in "}]":
                if unclosed and ((char == "}" and unclosed[-1] == "{") or (char == "]" and unclosed[-1] == "[")):
                    unclosed.pop()

    return unclosed

# Strategy for generating JSON-like strings
def json_like_strategy():
    return st.recursive(
        st.one_of([
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=10),
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.booleans()
        ]),
        lambda children: st.one_of(
            st.lists(children, max_size=5),
            st.dictionaries(st.text(st.characters(whitelist_categories=('L', 'N')), max_size=5), children, max_size=5)
        ),
        max_leaves=5
    ).map(lambda x: json.dumps(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(json_str=json_like_strategy())
@example(json_str='{"key": "value"}')
@example(json_str='{"key": [1, 2, 3]}')
@example(json_str='{"key": {"nested": "value"}}')
@example(json_str='{"key": "value"')
@example(json_str='{"key": [1, 2, 3')
@example(json_str='{"key": {"nested": "value"')
@example(json_str='{"key": "value"} }')
@example(json_str='{"key": [1, 2, 3]} ]')
@example(json_str='{"key": {"nested": "value"}} }')
def test_find_unclosed(json_str):
    global stop_collecting
    if stop_collecting:
        return
    
    json_str_copy = copy.deepcopy(json_str)
    try:
        expected = _find_unclosed(json_str_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(char in json_str for char in "{}[]"):
        generated_cases.append({
            "Inputs": {"json_str": json_str},
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