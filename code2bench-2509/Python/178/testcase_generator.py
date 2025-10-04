from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Any, Optional, Tuple
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
def _apply_tail(
    current_data: str, n_str: str, mime_type: Optional[str], log_id: str
) -> Tuple[Any, Optional[str], Optional[str]]:
    if not isinstance(current_data, str):
        return (
            current_data,
            mime_type,
            f"Input data for 'tail' must be a string, got {type(current_data).__name__}.",
        )

    try:
        n = int(n_str.strip())
        if n < 0:
            return current_data, mime_type, "Tail count N cannot be negative."
        if n == 0:
            return "", mime_type, None

        lines = current_data.splitlines(keepends=True)
        tail_lines = lines[-n:]
        return "".join(tail_lines), mime_type, None
    except (ValueError, TypeError) as e:
        return current_data, mime_type, f"Invalid tail count N '{n_str}': {e}"
    except Exception as e:
        return current_data, mime_type, f"Error applying tail '{n_str}': {e}"

# Strategy for generating test inputs
def current_data_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=100)

def n_str_strategy():
    return st.one_of([
        st.integers(min_value=-100, max_value=100).map(str),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
    ])

def mime_type_strategy():
    return st.one_of([
        st.just(None),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
    ])

def log_id_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    current_data=current_data_strategy(),
    n_str=n_str_strategy(),
    mime_type=mime_type_strategy(),
    log_id=log_id_strategy()
)
@example(current_data="line1\nline2\nline3", n_str="2", mime_type="text/plain", log_id="test1")
@example(current_data="line1\nline2\nline3", n_str="0", mime_type="text/plain", log_id="test2")
@example(current_data="line1\nline2\nline3", n_str="-1", mime_type="text/plain", log_id="test3")
@example(current_data="line1\nline2\nline3", n_str="invalid", mime_type="text/plain", log_id="test4")
@example(current_data="", n_str="1", mime_type="text/plain", log_id="test5")
@example(current_data="line1\nline2\nline3", n_str="100", mime_type="text/plain", log_id="test6")
def test_apply_tail(current_data: str, n_str: str, mime_type: Optional[str], log_id: str):
    global stop_collecting
    if stop_collecting:
        return
    
    current_data_copy = copy.deepcopy(current_data)
    n_str_copy = copy.deepcopy(n_str)
    mime_type_copy = copy.deepcopy(mime_type)
    log_id_copy = copy.deepcopy(log_id)
    
    try:
        expected = _apply_tail(current_data_copy, n_str_copy, mime_type_copy, log_id_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {
            "current_data": current_data,
            "n_str": n_str,
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