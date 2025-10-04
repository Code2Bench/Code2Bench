from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import re
import os
import atexit
import copy
from typing import Any, Optional

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def extract_json_from_string(s: str) -> Optional[Any]:
    """
    Searches for a JSON object within the string and returns the loaded JSON if found, otherwise returns None.
    """
    # Regex to find JSON objects (greedy, matches first { to last })
    match = re.search(r"\{.*\}", s, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    return None

# Strategy for generating strings with potential JSON objects
def json_string_strategy():
    # Generate valid JSON objects
    json_obj = st.recursive(
        st.one_of(
            st.none(),
            st.booleans(),
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.text(min_size=0, max_size=10),
        ),
        lambda children: st.lists(children, min_size=0, max_size=3) | st.dictionaries(st.text(min_size=1, max_size=5), children, min_size=0, max_size=3),
        max_leaves=5  # Restrict recursion depth
    )
    
    # Wrap JSON objects in random text
    return st.builds(
        lambda j, prefix, suffix: f"{prefix}{json.dumps(j)}{suffix}",
        json_obj,
        st.text(min_size=0, max_size=10),
        st.text(min_size=0, max_size=10)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(s=json_string_strategy())
@example(s="")
@example(s="no json here")
@example(s='{"key": "value"}')
@example(s='prefix{"key": "value"}suffix')
@example(s='{"invalid": json}')
@example(s='{"nested": {"key": "value"}}')
def test_extract_json_from_string(s: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    s_copy = copy.deepcopy(s)

    # Call func0 to verify input validity
    try:
        expected = extract_json_from_string(s_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "s": s_copy
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