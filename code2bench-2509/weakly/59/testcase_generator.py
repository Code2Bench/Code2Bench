from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import ast
import json
import os
import atexit
import copy
from typing import Optional

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def extract_function_body(source_code: str, function_name: str) -> Optional[str]:
    """
    Extracts the body of a function from the source code.
    Returns None if the function is not found.

    Assumption: The function is multiline and defined at the top level.
    """
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            lines = source_code.splitlines()
            start = node.body[0].lineno
            end = node.body[-1].end_lineno
            body_lines = lines[start - 1 : end]
            indent_level = len(body_lines[0]) - len(body_lines[0].lstrip())
            return "\n".join(line[indent_level:] for line in body_lines)
    return None

# Strategies for generating inputs
def source_code_strategy():
    # Generate valid Python source code with functions
    function_name = st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10)
    function_body = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    return st.builds(
        lambda name, body: f"def {name}():\n    {body}\n",
        function_name, function_body
    )

def function_name_strategy():
    return st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    source_code=source_code_strategy(),
    function_name=function_name_strategy()
)
@example(
    source_code="def foo():\n    pass\n",
    function_name="foo"
)
@example(
    source_code="def bar():\n    return 42\n",
    function_name="bar"
)
@example(
    source_code="def baz():\n    x = 1\n    y = 2\n    return x + y\n",
    function_name="baz"
)
@example(
    source_code="def qux():\n    pass\n",
    function_name="nonexistent"
)
def test_extract_function_body(source_code: str, function_name: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    source_code_copy = copy.deepcopy(source_code)
    function_name_copy = copy.deepcopy(function_name)

    # Call func0 to verify input validity
    try:
        expected = extract_function_body(source_code_copy, function_name_copy)
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