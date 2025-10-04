from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import ast
import os
import atexit
import copy
from typing import Any

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def parse_json_string_recursively(data: Any) -> Any:
    if isinstance(data, dict):
        return {k: parse_json_string_recursively(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [parse_json_string_recursively(item) for item in data]
    elif isinstance(data, tuple):
        return [parse_json_string_recursively(item) for item in data]
    elif isinstance(data, str):
        data = data.strip()
        if (data.startswith('{') and data.endswith('}')) or (data.startswith('[') and data.endswith(']')):
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                try:
                    return ast.literal_eval(data)
                except (SyntaxError, ValueError):
                    try:
                        fixed_str = data.replace("'", '"')
                        return json.loads(fixed_str)
                    except json.JSONDecodeError:
                        if data.count('}, {') > 0:
                            try:
                                wrapped_data = '[' + data + ']'
                                return json.loads(wrapped_data)
                            except json.JSONDecodeError:
                                return data
                        return data
        return data
    else:
        return data

# Strategies for generating inputs
def json_like_strategy():
    return st.recursive(
        st.one_of(
            st.none(),
            st.booleans(),
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.text(min_size=0, max_size=20),
        ),
        lambda children: st.one_of(
            st.lists(children, min_size=0, max_size=5),
            st.dictionaries(st.text(min_size=1, max_size=10), children, min_size=0, max_size=5),
        ),
        max_leaves=5
    )

def json_string_strategy():
    return st.one_of(
        st.text(min_size=0, max_size=20),
        st.from_regex(r'\{.*\}', fullmatch=True),
        st.from_regex(r'\[.*\]', fullmatch=True),
        st.from_regex(r'\{.*\}, \{.*\}', fullmatch=True),
    )

def data_strategy():
    return st.one_of(
        json_like_strategy(),
        json_string_strategy(),
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(data=data_strategy())
@example(data=None)
@example(data=True)
@example(data=42)
@example(data=3.14)
@example(data="plain text")
@example(data="{}")
@example(data="[]")
@example(data='{"key": "value"}')
@example(data='[1, 2, 3]')
@example(data='{"key": "value"}, {"key2": "value2"}')
def test_parse_json_string_recursively(data: Any):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    data_copy = copy.deepcopy(data)

    # Call func0 to verify input validity
    try:
        expected = parse_json_string_recursively(data_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "data": data_copy
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