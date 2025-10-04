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
def remove_main_block(source_code: str) -> str:
    """
    Remove the if __name__ == "__main__": block from the source code.
    """
    tree = ast.parse(source_code)
    lines = source_code.splitlines()

    # Find the main block and note its line numbers
    for node in tree.body:
        if isinstance(node, ast.If):
            test = node.test
            if (
                isinstance(test, ast.Compare)
                and isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
                and len(test.ops) == 1
                and isinstance(test.ops[0], ast.Eq)
                and len(test.comparators) == 1
                and isinstance(test.comparators[0], ast.Constant)
                and test.comparators[0].value == "__main__"
            ):

                # Remove lines corresponding to this block
                start_lineno = node.lineno - 1
                end_lineno = node.end_lineno
                return "\n".join(lines[:start_lineno] + lines[end_lineno:])

    return source_code

# Strategy for generating source code with potential main block
def source_code_strategy():
    # Generate random Python code with or without a main block
    code_without_main = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), whitelist_characters='\n'),
        min_size=0, max_size=100
    )
    code_with_main = st.builds(
        lambda code: f"{code}\nif __name__ == '__main__':\n    pass",
        code_without_main
    )
    return st.one_of(code_without_main, code_with_main)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(source_code=source_code_strategy())
@example(source_code="")
@example(source_code="print('Hello, World!')")
@example(source_code="if __name__ == '__main__':\n    print('Hello, World!')")
@example(source_code="def foo():\n    pass\nif __name__ == '__main__':\n    foo()")
@example(source_code="import os\nif __name__ == '__main__':\n    os.system('ls')")
def test_remove_main_block(source_code: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    source_code_copy = copy.deepcopy(source_code)

    # Call func0 to verify input validity
    try:
        expected = remove_main_block(source_code_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "source_code": source_code_copy
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