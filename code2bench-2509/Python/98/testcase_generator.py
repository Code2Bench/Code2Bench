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
def format_dict_to_string(data: dict, indent_level=0, use_colon=True):
    if not isinstance(data, dict):
        return str(data)

    lines = []
    indent = "  " * indent_level  # 2 spaces per indentation level
    separator = ": " if use_colon else " "

    for key, value in data.items():
        if isinstance(value, dict):
            # Recursive case: nested dictionary
            lines.append(f"{indent}{key}:")
            nested_string = format_dict_to_string(
                value, indent_level + 1, use_colon
            )
            lines.append(nested_string)
        else:
            # Base case: simple key-value pair
            lines.append(f"{indent}{key}{separator}{value}")

    return "\n".join(lines)

# Strategy for generating dictionaries
def dict_strategy():
    return st.recursive(
        st.dictionaries(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=10),
            st.one_of([
                st.integers(),
                st.floats(allow_nan=False, allow_infinity=False),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=10),
                st.booleans()
            ]),
            max_size=5
        ),
        lambda children: st.dictionaries(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=10),
            children,
            max_size=5
        ),
        max_leaves=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    data=dict_strategy(),
    indent_level=st.integers(min_value=0, max_value=5),
    use_colon=st.booleans()
)
@example(data={}, indent_level=0, use_colon=True)
@example(data={"key": "value"}, indent_level=0, use_colon=True)
@example(data={"key": "value"}, indent_level=1, use_colon=False)
@example(data={"nested": {"key": "value"}}, indent_level=0, use_colon=True)
@example(data={"nested": {"key": "value"}}, indent_level=1, use_colon=False)
@example(data={"key": 42}, indent_level=0, use_colon=True)
@example(data={"key": True}, indent_level=0, use_colon=True)
def test_format_dict_to_string(data, indent_level, use_colon):
    global stop_collecting
    if stop_collecting:
        return
    
    data_copy = copy.deepcopy(data)
    try:
        expected = format_dict_to_string(data_copy, indent_level, use_colon)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"data": data, "indent_level": indent_level, "use_colon": use_colon},
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