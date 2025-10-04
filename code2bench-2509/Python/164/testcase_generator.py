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
def _build_command_line_options(test_options: Dict[str, Any]) -> list:
    """Helper function to build command-line options from the test options dictionary."""
    additional_options = []

    for key, value in test_options.items():
        if isinstance(value, bool):
            # Default behavior expecting argparse.BooleanOptionalAction support
            additional_options.append(f"--{'no-' if not value else ''}{key.replace('_', '-')}")
        elif isinstance(value, list):
            additional_options.extend([f"--{key.replace('_', '-')}"] + [str(v) for v in value])
        else:
            # Just add --key value
            additional_options.extend(["--" + key.replace("_", "-"), str(value)])

    return additional_options

# Strategy for generating test options
def test_options_strategy():
    key_strategy = st.text(st.characters(whitelist_categories=('L', 'N', 'P')), min_size=1, max_size=10)
    value_strategy = st.one_of([
        st.booleans(),
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
        st.lists(st.one_of([st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)]), min_size=1, max_size=3)
    ])
    return st.dictionaries(key_strategy, value_strategy, min_size=1, max_size=5)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(test_options=test_options_strategy())
@example(test_options={"flag": True})
@example(test_options={"flag": False})
@example(test_options={"value": 42})
@example(test_options={"list": [1, 2, 3]})
@example(test_options={"nested": {"key": "value"}})
@example(test_options={"flag": True, "value": 42, "list": [1, 2, 3]})
def test_build_command_line_options(test_options: Dict[str, Any]):
    global stop_collecting
    if stop_collecting:
        return
    
    test_options_copy = copy.deepcopy(test_options)
    try:
        expected = _build_command_line_options(test_options_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"test_options": test_options},
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