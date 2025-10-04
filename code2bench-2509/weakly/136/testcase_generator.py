from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import List

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _parse_api_keys(api_keys: str) -> List[str]:
    if not api_keys:
        return []
    return [key.strip() for key in api_keys.split(",")]

# Strategy for generating api_keys
def api_keys_strategy():
    return st.one_of(
        st.just(""),  # Empty string
        st.lists(
            st.text(
                alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S'), min_codepoint=32, max_codepoint=126),
                min_size=1,
                max_size=10
            ),
            min_size=0,
            max_size=10
        ).map(lambda x: ",".join(x))  # Join list into a comma-separated string
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(api_keys=api_keys_strategy())
@example(api_keys="")
@example(api_keys="key1")
@example(api_keys="key1,key2")
@example(api_keys="key1, key2, key3")
@example(api_keys="  key1  ,  key2  ")
def test_parse_api_keys(api_keys: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    api_keys_copy = copy.deepcopy(api_keys)

    # Call func0 to verify input validity
    try:
        expected = _parse_api_keys(api_keys_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "api_keys": api_keys_copy
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