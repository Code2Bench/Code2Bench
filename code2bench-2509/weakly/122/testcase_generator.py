from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import urllib.parse
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
def parse_specific_attributes(specific_attributes):
    assert isinstance(specific_attributes, str), "Specific attributes must be a string"
    parsed_specific_attributes = urllib.parse.parse_qsl(specific_attributes)
    return (
        {key: value for (key, value) in parsed_specific_attributes}
        if parsed_specific_attributes
        else dict()
    )

# Strategy for generating specific_attributes
def specific_attributes_strategy():
    key = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_-'),
        min_size=1, max_size=10
    )
    value = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_-'),
        min_size=1, max_size=10
    )
    return st.lists(
        st.tuples(key, value),
        min_size=0, max_size=5
    ).map(lambda x: urllib.parse.urlencode(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(specific_attributes=specific_attributes_strategy())
@example(specific_attributes="")
@example(specific_attributes="key1=value1")
@example(specific_attributes="key1=value1&key2=value2")
@example(specific_attributes="key1=value1&key2=value2&key3=value3")
def test_parse_specific_attributes(specific_attributes: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    specific_attributes_copy = copy.deepcopy(specific_attributes)

    # Call func0 to verify input validity
    try:
        expected = parse_specific_attributes(specific_attributes_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "specific_attributes": specific_attributes_copy
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