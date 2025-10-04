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
def _set_all_properties_required(schema: dict) -> dict:
    """Recursively make all properties required in objects."""
    if not isinstance(schema, dict):
        return schema
    if "properties" in schema:
        schema["required"] = list(schema["properties"].keys())
    for value in schema.values():
        if isinstance(value, dict):
            _set_all_properties_required(value)
        elif isinstance(value, list):
            for item in value:
                _set_all_properties_required(item)
    return schema

# Strategy for generating JSON-like schemas
def schema_strategy():
    return st.recursive(
        st.one_of([
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'))),
            st.booleans(),
            st.lists(st.text(st.characters(whitelist_categories=('L', 'N')), max_size=5), max_size=5)
        ]),
        lambda children: st.dictionaries(
            st.text(st.characters(whitelist_categories=('L', 'N')), max_size=5),
            st.one_of([
                children,
                st.lists(children, max_size=5)
            ]),
            max_size=5
        ),
        max_leaves=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(schema=schema_strategy())
@example(schema={})
@example(schema={"properties": {"a": 1}})
@example(schema={"properties": {"a": {"properties": {"b": 2}}}})
@example(schema={"properties": {"a": [{"properties": {"b": 2}}]}})
@example(schema={"properties": {"a": 1}, "required": ["b"]})
def test_set_all_properties_required(schema):
    global stop_collecting
    if stop_collecting:
        return
    
    schema_copy = copy.deepcopy(schema)
    try:
        expected = _set_all_properties_required(schema_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if isinstance(schema, dict) and "properties" in schema:
        generated_cases.append({
            "Inputs": {"schema": schema},
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