from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Any, Dict, List, Optional, Tuple
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
def _apply_filter_rows_eq(
    current_data: List[Dict], filter_spec: str, mime_type: Optional[str], log_id: str
) -> Tuple[Any, Optional[str], Optional[str]]:
    """
    Filters a list of dictionaries based on a column's value equality.

    Args:
        current_data: The input data (expected List[Dict]).
        filter_spec: String in the format 'column_name:value'.
        mime_type: The original mime type (passed through).
        log_id: Identifier for logging.

    Returns:
        Tuple: (result_data, original_mime_type, error_string)
               result_data is List[Dict] containing only filtered rows.
    """
    if not isinstance(current_data, list) or (
        current_data and not isinstance(current_data[0], dict)
    ):
        return (
            current_data,
            mime_type,
            f"Input data for 'filter_rows_eq' must be a list of dictionaries, got {type(current_data).__name__}.",
        )

    if not current_data:
        return [], mime_type, None

    try:
        parts = filter_spec.split(":", 1)
        if len(parts) != 2:
            return (
                current_data,
                mime_type,
                f"Invalid filter format '{filter_spec}'. Expected 'column_name:value'.",
            )
        col_name, filter_value = parts[0].strip(), parts[1].strip()

        header = list(current_data[0].keys())
        if col_name not in header:
            return (
                current_data,
                mime_type,
                f"Filter column '{col_name}' not found in data keys: {header}",
            )

        output_list = [
            row for row in current_data if str(row.get(col_name)) == filter_value
        ]

        return output_list, mime_type, None

    except Exception as e:
        return current_data, mime_type, f"Error filtering rows by '{filter_spec}': {e}"

# Strategy for generating dictionaries
def dict_strategy():
    return st.dictionaries(
        keys=st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10),
        values=st.one_of([
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.booleans()
        ]),
        min_size=1, max_size=5
    )

# Strategy for generating lists of dictionaries
def list_of_dicts_strategy():
    return st.lists(dict_strategy(), min_size=0, max_size=5)

# Strategy for generating filter_spec
def filter_spec_strategy():
    return st.tuples(
        st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
    ).map(lambda x: f"{x[0]}:{x[1]}")

# Strategy for generating mime_type
def mime_type_strategy():
    return st.one_of([
        st.just("application/json"),
        st.just("text/csv"),
        st.just(None)
    ])

# Strategy for generating log_id
def log_id_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    current_data=list_of_dicts_strategy(),
    filter_spec=filter_spec_strategy(),
    mime_type=mime_type_strategy(),
    log_id=log_id_strategy()
)
@example(current_data=[], filter_spec="key:value", mime_type="application/json", log_id="test")
@example(current_data=[{"key": "value"}], filter_spec="key:value", mime_type="text/csv", log_id="test")
@example(current_data=[{"key": "value"}], filter_spec="invalid:format", mime_type=None, log_id="test")
@example(current_data=[{"key": "value"}], filter_spec="nonexistent:value", mime_type="application/json", log_id="test")
@example(current_data=[{"key": "value"}, {"key": "other"}], filter_spec="key:value", mime_type="text/csv", log_id="test")
def test_apply_filter_rows_eq(current_data, filter_spec, mime_type, log_id):
    global stop_collecting
    if stop_collecting:
        return
    
    current_data_copy = copy.deepcopy(current_data)
    filter_spec_copy = copy.deepcopy(filter_spec)
    mime_type_copy = copy.deepcopy(mime_type)
    log_id_copy = copy.deepcopy(log_id)
    
    try:
        expected = _apply_filter_rows_eq(current_data_copy, filter_spec_copy, mime_type_copy, log_id_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if not isinstance(current_data, list) or (current_data and not isinstance(current_data[0], dict)):
        generated_cases.append({
            "Inputs": {"current_data": current_data, "filter_spec": filter_spec, "mime_type": mime_type, "log_id": log_id},
            "Expected": expected
        })
    elif not current_data:
        generated_cases.append({
            "Inputs": {"current_data": current_data, "filter_spec": filter_spec, "mime_type": mime_type, "log_id": log_id},
            "Expected": expected
        })
    else:
        parts = filter_spec.split(":", 1)
        if len(parts) != 2:
            generated_cases.append({
                "Inputs": {"current_data": current_data, "filter_spec": filter_spec, "mime_type": mime_type, "log_id": log_id},
                "Expected": expected
            })
        else:
            col_name, filter_value = parts[0].strip(), parts[1].strip()
            header = list(current_data[0].keys())
            if col_name not in header:
                generated_cases.append({
                    "Inputs": {"current_data": current_data, "filter_spec": filter_spec, "mime_type": mime_type, "log_id": log_id},
                    "Expected": expected
                })
            else:
                generated_cases.append({
                    "Inputs": {"current_data": current_data, "filter_spec": filter_spec, "mime_type": mime_type, "log_id": log_id},
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