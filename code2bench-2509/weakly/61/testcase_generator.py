from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import ast
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
def remove_function(source_code: str, function_name: str) -> str:
    """
    Remove a function definition from the source code.
    """
    tree = ast.parse(source_code)
    lines = source_code.splitlines()

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            start_lineno = node.lineno - 1
            end_lineno = node.end_lineno
            return "\n".join(lines[:start_lineno] + lines[end_lineno:])

    return source_code

# Strategies for generating inputs
def source_code_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), min_codepoint=32, max_codepoint=126),
        min_size=1, max_size=1000
    )

def function_name_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), min_codepoint=97, max_codepoint=122),
        min_size=1, max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    source_code=source_code_strategy(),
    function_name=function_name_strategy()
)
@example(
    source_code="def foo():\n    pass\ndef bar():\n    pass",
    function_name="foo"
)
@example(
    source_code="def foo():\n    pass",
    function_name="bar"
)
@example(
    source_code="",
    function_name="foo"
)
@example(
    source_code="def foo():\n    pass",
    function_name="foo"
)
def test_remove_function(source_code: str, function_name: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    source_code_copy = copy.deepcopy(source_code)
    function_name_copy = copy.deepcopy(function_name)

    # Call func0 to verify input validity
    try:
        expected = remove_function(source_code_copy, function_name_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "source_code": source_code_copy,
            "function_name": function_name_copy
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