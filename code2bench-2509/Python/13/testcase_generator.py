from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Any, Dict
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
def _format_product_context_md(data: Dict[str, Any]) -> str:
    lines = ["# Product Context\n"]
    for key, value in data.items():
        heading = key.replace("_", " ").title()
        lines.append(f"## {heading}\n")
        if isinstance(value, str):
            lines.append(value.strip() + "\n")
        elif isinstance(value, list):
            for item in value:
                lines.append(f"*   {item}\n")
        else: # Fallback for other types
            lines.append(str(value) + "\n")
        lines.append("\n")
    return "".join(lines)

# Strategy for generating JSON-like dictionaries
def dict_strategy():
    return st.dictionaries(
        keys=st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
        values=st.one_of([
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
            st.lists(st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20), min_size=1, max_size=5),
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.booleans()
        ]),
        min_size=1, max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(data=dict_strategy())
@example(data={"key": "value"})
@example(data={"key": ["item1", "item2"]})
@example(data={"key": 42})
@example(data={"key": 3.14})
@example(data={"key": True})
@example(data={"key_with_underscores": "value"})
def test_format_product_context_md(data: Dict[str, Any]):
    global stop_collecting
    if stop_collecting:
        return
    
    data_copy = copy.deepcopy(data)
    try:
        expected = _format_product_context_md(data_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"data": data},
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