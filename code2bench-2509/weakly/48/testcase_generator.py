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
def parse_function_arguments(source_code: str, tool_name: str):
    """Get arguments of a function from its source code"""
    tree = ast.parse(source_code)
    args = []
    for node in ast.walk(tree):
        # Handle both sync and async functions
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == tool_name:
            for arg in node.args.args:
                args.append(arg.arg)
    return args

# Strategies for generating inputs
def source_code_strategy():
    # Generate valid Python function definitions
    function_name = st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10)
    arg_names = st.lists(st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10), min_size=0, max_size=5)
    return st.builds(
        lambda name, args: f"def {name}({', '.join(args)}):\n    pass",
        function_name, arg_names
    )

def tool_name_strategy():
    return st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    source_code=source_code_strategy(),
    tool_name=tool_name_strategy()
)
@example(
    source_code="def example_func(arg1, arg2):\n    pass",
    tool_name="example_func"
)
@example(
    source_code="async def async_example(arg1):\n    pass",
    tool_name="async_example"
)
@example(
    source_code="def no_args():\n    pass",
    tool_name="no_args"
)
@example(
    source_code="def func_with_kwargs(arg1, arg2, *args, **kwargs):\n    pass",
    tool_name="func_with_kwargs"
)
def test_parse_function_arguments(source_code: str, tool_name: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    source_code_copy = copy.deepcopy(source_code)
    tool_name_copy = copy.deepcopy(tool_name)

    # Call func0 to verify input validity
    try:
        expected = parse_function_arguments(source_code_copy, tool_name_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "source_code": source_code_copy,
            "tool_name": tool_name_copy
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