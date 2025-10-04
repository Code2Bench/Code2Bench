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
def _apply_select_cols(
    current_data: List[Dict], cols_str: str, mime_type: Optional[str], log_id: str
) -> Tuple[Any, Optional[str], Optional[str]]:
    """
    Selects specific columns from data represented as a list of dictionaries.

    Args:
        current_data: The input data (expected List[Dict]).
        cols_str: Comma-separated string of column names to keep.
        mime_type: The original mime type (passed through).
        log_id: Identifier for logging.

    Returns:
        Tuple: (result_data, original_mime_type, error_string)
               result_data is List[Dict] containing only selected columns.
    """
    if not isinstance(current_data, list) or (
        current_data and not isinstance(current_data[0], dict)
    ):
        return (
            current_data,
            mime_type,
            f"Input data for 'select_cols' must be a list of dictionaries, got {type(current_data).__name__}.",
        )

    if not current_data:
        return [], mime_type, None

    try:
        header = list(current_data[0].keys())
        target_cols = [col.strip() for col in cols_str.split(",")]
        output_list = []

        for target_col in target_cols:
            if target_col not in header:
                return (
                    current_data,
                    mime_type,
                    f"Column '{target_col}' not found in data keys: {header}",
                )

        for row_dict in current_data:
            new_row = {col: row_dict.get(col) for col in target_cols}
            output_list.append(new_row)

        return output_list, mime_type, None

    except Exception as e:
        return current_data, mime_type, f"Error selecting columns '{cols_str}': {e}"

# Strategy for generating current_data
def current_data_strategy():
    return st.lists(
        st.dictionaries(
            keys=st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            values=st.one_of([
                st.integers(),
                st.floats(allow_nan=False, allow_infinity=False),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
                st.booleans()
            ]),
            min_size=1, max_size=5
        ),
        min_size=0, max_size=5
    )

# Strategy for generating cols_str
def cols_str_strategy(current_data):
    if not current_data or not isinstance(current_data[0], dict):
        return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
    header = list(current_data[0].keys())
    return st.lists(
        st.sampled_from(header),
        min_size=1, max_size=len(header)
    ).map(lambda cols: ",".join(cols))

# Strategy for generating mime_type
def mime_type_strategy():
    return st.one_of([
        st.just("application/json"),
        st.just("text/csv"),
        st.just(None)
    ])

# Strategy for generating log_id
def log_id_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    current_data=current_data_strategy(),
    cols_str=st.one_of([cols_str_strategy(current_data_strategy().example())]),
    mime_type=mime_type_strategy(),
    log_id=log_id_strategy()
)
@example(current_data=[], cols_str="", mime_type="application/json", log_id="log1")
@example(current_data=[{"a": 1}], cols_str="a", mime_type="text/csv", log_id="log2")
@example(current_data=[{"a": 1, "b": 2}], cols_str="a,b", mime_type=None, log_id="log3")
@example(current_data=[{"a": 1}], cols_str="b", mime_type="application/json", log_id="log4")
@example(current_data="not a list", cols_str="a", mime_type="text/csv", log_id="log5")
@example(current_data=[{"a": 1}, {"b": 2}], cols_str="a", mime_type="application/json", log_id="log6")
def test_apply_select_cols(current_data, cols_str, mime_type, log_id):
    global stop_collecting
    if stop_collecting:
        return
    
    current_data_copy = copy.deepcopy(current_data)
    cols_str_copy = copy.deepcopy(cols_str)
    mime_type_copy = copy.deepcopy(mime_type)
    log_id_copy = copy.deepcopy(log_id)
    
    try:
        expected = _apply_select_cols(current_data_copy, cols_str_copy, mime_type_copy, log_id_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {
            "current_data": current_data,
            "cols_str": cols_str,
            "mime_type": mime_type,
            "log_id": log_id
        },
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