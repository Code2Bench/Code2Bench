from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Any, List, Dict
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
def _convert_dicts_to_rows(
    data: List[Dict[str, Any]], headers: List[str]
) -> List[List[str]]:
    """Convert list of dictionaries to list of rows using the specified header order.

    Args:
        data: List of dictionaries to convert
        headers: List of column headers to use for ordering

    Returns:
        List of rows where each row is a list of string values in header order
    """
    if not data:
        return []

    if not headers:
        raise ValueError("Headers are required when using list[dict] format")

    rows = []
    for item in data:
        row = []
        for header in headers:
            value = item.get(header, "")
            row.append(str(value) if value is not None else "")
        rows.append(row)

    return rows

# Strategy for generating dictionaries
def dict_strategy():
    return st.dictionaries(
        keys=st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
        values=st.one_of([
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.booleans(),
            st.none()
        ]),
        min_size=1,
        max_size=5
    )

# Strategy for generating headers
def headers_strategy():
    return st.lists(
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
        min_size=1,
        max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(data=st.lists(dict_strategy(), min_size=0, max_size=5), headers=headers_strategy())
@example(data=[], headers=["col1", "col2"])
@example(data=[{"col1": 1, "col2": "value"}], headers=["col1", "col2"])
@example(data=[{"col1": None, "col2": 3.14}], headers=["col1", "col2"])
@example(data=[{"col1": True, "col2": False}], headers=["col1", "col2"])
@example(data=[{"col1": "value1"}, {"col1": "value2"}], headers=["col1"])
def test_convert_dicts_to_rows(data: List[Dict[str, Any]], headers: List[str]):
    global stop_collecting
    if stop_collecting:
        return
    
    data_copy = copy.deepcopy(data)
    headers_copy = copy.deepcopy(headers)
    try:
        expected = _convert_dicts_to_rows(data_copy, headers_copy)
    except ValueError:
        return  # Skip inputs that cause ValueError
    
    if data or headers:
        generated_cases.append({
            "Inputs": {"data": data, "headers": headers},
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