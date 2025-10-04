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
def trim_schema(schema: dict) -> dict:
    if "title" in schema:
        del schema["title"]
    if "default" in schema and schema["default"] is None:
        del schema["default"]
    if "anyOf" in schema:
        types = [
            type_dict["type"] for type_dict in schema["anyOf"]
            if type_dict["type"] != 'null'
        ]
        schema["type"] = types
        del schema["anyOf"]
    if "properties" in schema:
        schema["properties"] = {
            k: trim_schema(v)
            for k, v in schema["properties"].items()
        }
    return schema

# Strategy for generating JSON schema-like dictionaries
def schema_strategy():
    return st.recursive(
        st.one_of([
            st.dictionaries(
                st.text(st.characters(whitelist_categories=('L', 'N')), max_size=10),
                st.one_of([
                    st.text(st.characters(whitelist_categories=('L', 'N')), max_size=10),
                    st.booleans(),
                    st.none(),
                    st.integers(),
                    st.floats(allow_nan=False, allow_infinity=False)
                ]),
                max_size=5
            ),
            st.lists(
                st.one_of([
                    st.text(st.characters(whitelist_categories=('L', 'N')), max_size=10),
                    st.booleans(),
                    st.none(),
                    st.integers(),
                    st.floats(allow_nan=False, allow_infinity=False)
                ]),
                max_size=5
            )
        ]),
        lambda children: st.dictionaries(
            st.text(st.characters(whitelist_categories=('L', 'N')), max_size=10),
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
@example(schema={"title": "Example", "default": None})
@example(schema={"anyOf": [{"type": "string"}, {"type": "null"}]})
@example(schema={"anyOf": [{"type": "integer"}, {"type": "boolean"}]})
@example(schema={"properties": {"key": {"title": "Nested", "default": None}}})
@example(schema={"properties": {"key": {"anyOf": [{"type": "string"}, {"type": "null"}]}}})
def test_trim_schema(schema):
    global stop_collecting
    if stop_collecting:
        return
    
    schema_copy = copy.deepcopy(schema)
    try:
        expected = trim_schema(schema_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "title" in schema or "default" in schema or "anyOf" in schema or "properties" in schema:
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