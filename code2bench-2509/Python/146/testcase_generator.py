from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Any, Dict, Tuple
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
def validate_operation(operation: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate a batch operation dictionary.

    Args:
        operation: Operation dictionary to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    op_type = operation.get('type')
    if not op_type:
        return False, "Missing 'type' field"

    # Validate required fields for each operation type
    required_fields = {
        'insert_text': ['index', 'text'],
        'delete_text': ['start_index', 'end_index'],
        'replace_text': ['start_index', 'end_index', 'text'],
        'format_text': ['start_index', 'end_index'],
        'insert_table': ['index', 'rows', 'columns'],
        'insert_page_break': ['index'],
        'find_replace': ['find_text', 'replace_text']
    }

    if op_type not in required_fields:
        return False, f"Unsupported operation type: {op_type or 'None'}"

    for field in required_fields[op_type]:
        if field not in operation:
            return False, f"Missing required field: {field}"

    return True, ""

# Strategy for generating operation dictionaries
def operation_strategy():
    return st.one_of([
        st.fixed_dictionaries({
            'type': st.just('insert_text'),
            'index': st.integers(min_value=0, max_value=100),
            'text': st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50)
        }),
        st.fixed_dictionaries({
            'type': st.just('delete_text'),
            'start_index': st.integers(min_value=0, max_value=100),
            'end_index': st.integers(min_value=0, max_value=100)
        }),
        st.fixed_dictionaries({
            'type': st.just('replace_text'),
            'start_index': st.integers(min_value=0, max_value=100),
            'end_index': st.integers(min_value=0, max_value=100),
            'text': st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50)
        }),
        st.fixed_dictionaries({
            'type': st.just('format_text'),
            'start_index': st.integers(min_value=0, max_value=100),
            'end_index': st.integers(min_value=0, max_value=100)
        }),
        st.fixed_dictionaries({
            'type': st.just('insert_table'),
            'index': st.integers(min_value=0, max_value=100),
            'rows': st.integers(min_value=1, max_value=10),
            'columns': st.integers(min_value=1, max_value=10)
        }),
        st.fixed_dictionaries({
            'type': st.just('insert_page_break'),
            'index': st.integers(min_value=0, max_value=100)
        }),
        st.fixed_dictionaries({
            'type': st.just('find_replace'),
            'find_text': st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50),
            'replace_text': st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50)
        }),
        st.dictionaries(
            keys=st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10),
            values=st.one_of([
                st.integers(),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50),
                st.booleans()
            ]),
            min_size=1, max_size=5
        )
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(operation=operation_strategy())
@example(operation={'type': 'insert_text', 'index': 0, 'text': 'Hello'})
@example(operation={'type': 'delete_text', 'start_index': 0, 'end_index': 5})
@example(operation={'type': 'replace_text', 'start_index': 0, 'end_index': 5, 'text': 'World'})
@example(operation={'type': 'format_text', 'start_index': 0, 'end_index': 5})
@example(operation={'type': 'insert_table', 'index': 0, 'rows': 2, 'columns': 3})
@example(operation={'type': 'insert_page_break', 'index': 0})
@example(operation={'type': 'find_replace', 'find_text': 'foo', 'replace_text': 'bar'})
@example(operation={'type': 'invalid_type'})
@example(operation={'type': 'insert_text'})
@example(operation={'type': 'delete_text', 'start_index': 0})
def test_validate_operation(operation: Dict[str, Any]):
    global stop_collecting
    if stop_collecting:
        return
    
    operation_copy = copy.deepcopy(operation)
    try:
        expected = validate_operation(operation_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"operation": operation},
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