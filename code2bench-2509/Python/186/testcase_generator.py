from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Any, Dict, List
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
def format_tool_descriptions(schemas: List[Dict[str, Any]]) -> str:
    """Formats tool schemas into a user-friendly description string."""
    descriptions = []
    for schema in schemas:
        desc = [f"{schema['name']}: {schema['description']}"]

        desc.append("\nArguments:")
        for arg_name, arg_info in schema["args"].items():
            default = (
                f" (default: {arg_info['default']})" if "default" in arg_info else ""
            )
            desc.append(f"  - {arg_name}: {arg_info['description']}{default}")

        if schema["examples"]:
            desc.append("\nExamples:")
            for example in schema["examples"]:
                desc.append(f"  {example}")

        if schema["returns"]:
            desc.append(f"\nReturns: {schema['returns']}")

        descriptions.append("\n".join(desc))

    return "\n\n".join(descriptions)

# Strategy for generating tool schemas
def schema_strategy():
    return st.fixed_dictionaries({
        "name": st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
        "description": st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
        "args": st.dictionaries(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.fixed_dictionaries({
                "description": st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=30),
            }, optional={"default": st.one_of([st.none(), st.integers(), st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)])}),
            min_size=1, max_size=3
        ),
        "examples": st.one_of([
            st.lists(st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20), min_size=1, max_size=2),
            st.just([])
        ]),
        "returns": st.one_of([
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=30),
            st.just(None)
        ])
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(schemas=st.lists(schema_strategy(), min_size=1, max_size=3))
@example(schemas=[{
    "name": "tool1",
    "description": "A simple tool",
    "args": {"arg1": {"description": "First argument"}},
    "examples": [],
    "returns": None
}])
@example(schemas=[{
    "name": "tool2",
    "description": "Another tool",
    "args": {"arg1": {"description": "First argument", "default": 42}},
    "examples": ["example1", "example2"],
    "returns": "Some result"
}])
@example(schemas=[{
    "name": "tool3",
    "description": "Complex tool",
    "args": {
        "arg1": {"description": "First argument"},
        "arg2": {"description": "Second argument", "default": "value"}
    },
    "examples": ["example1"],
    "returns": "Complex result"
}])
def test_format_tool_descriptions(schemas: List[Dict[str, Any]]):
    global stop_collecting
    if stop_collecting:
        return
    
    schemas_copy = copy.deepcopy(schemas)
    try:
        expected = format_tool_descriptions(schemas_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"schemas": schemas},
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