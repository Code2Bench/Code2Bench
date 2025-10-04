from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import ast
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
def parse_arguments(json_value):
    try:
        try:
            parsed_value = json.loads(json_value)
        except:
            parsed_value = ast.literal_eval(json_value)
        return parsed_value, True
    except:
        return json_value, False

# Strategy for generating JSON-like strings
def json_value_strategy():
    return st.one_of(
        st.none(),
        st.booleans(),
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(),
        st.lists(st.one_of(st.none(), st.booleans(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.text()), max_size=5),
        st.dictionaries(st.text(), st.one_of(st.none(), st.booleans(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.text()), max_size=5)
    ).map(lambda x: json.dumps(x))

# Strategy for generating Python literal-like strings
def literal_value_strategy():
    return st.one_of(
        st.none(),
        st.booleans(),
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(),
        st.lists(st.one_of(st.none(), st.booleans(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.text()), max_size=5),
        st.tuples(st.one_of(st.none(), st.booleans(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.text())),
        st.dictionaries(st.text(), st.one_of(st.none(), st.booleans(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.text()), max_size=5)
    ).map(lambda x: str(x))

# Combined strategy for generating test cases
def combined_strategy():
    return st.one_of(
        json_value_strategy(),
        literal_value_strategy(),
        st.text()  # Random text that may not be valid JSON or Python literal
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(json_value=combined_strategy())
@example(json_value='{"key": "value"}')
@example(json_value='[1, 2, 3]')
@example(json_value='{"key": [1, 2, 3]}')
@example(json_value='invalid_json')
@example(json_value='None')
@example(json_value='True')
@example(json_value='123')
@example(json_value='123.456')
@example(json_value='"string"')
@example(json_value='[1, 2, 3, 4, 5]')
@example(json_value='{"a": 1, "b": 2}')
@example(json_value='(1, 2, 3)')
@example(json_value='{"a": [1, 2, 3], "b": {"c": 4}}')
def test_parse_arguments(json_value: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    json_value_copy = copy.deepcopy(json_value)

    # Call func0 to verify input validity
    try:
        parsed_value, success = parse_arguments(json_value_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "json_value": json_value_copy
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