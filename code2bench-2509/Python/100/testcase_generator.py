from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
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
def extract_weave_refs_from_value(value):
    """Extract all strings that start with 'weave:///' from a value."""
    refs = []
    if isinstance(value, str) and value.startswith("weave:///"):
        refs.append(value)
    elif isinstance(value, dict):
        for v in value.values():
            refs.extend(extract_weave_refs_from_value(v))
    elif isinstance(value, list):
        for v in value:
            refs.extend(extract_weave_refs_from_value(v))
    return refs

# Strategy for generating values that may contain weave refs
def value_strategy():
    return st.recursive(
        st.one_of([
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1),
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.booleans()
        ]),
        lambda children: st.one_of(
            st.lists(children, max_size=5),
            st.dictionaries(st.text(st.characters(whitelist_categories=('L', 'N')), max_size=5), children, max_size=5)
        ),
        max_leaves=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(value=value_strategy())
@example(value="weave:///example")
@example(value={"key": "weave:///example"})
@example(value=["weave:///example"])
@example(value={"key": {"nested_key": "weave:///example"}})
@example(value=[{"key": "weave:///example"}])
@example(value={"key": "not_a_weave_ref"})
@example(value=["not_a_weave_ref"])
@example(value={"key": {"nested_key": "not_a_weave_ref"}})
@example(value=[{"key": "not_a_weave_ref"}])
def test_extract_weave_refs_from_value(value):
    global stop_collecting
    if stop_collecting:
        return
    
    value_copy = copy.deepcopy(value)
    try:
        expected = extract_weave_refs_from_value(value_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if isinstance(value, (str, dict, list)):
        generated_cases.append({
            "Inputs": {"value": value},
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