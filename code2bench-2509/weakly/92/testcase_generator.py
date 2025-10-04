from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import textwrap
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
def _jupyterize(src: str) -> str:
    src = textwrap.dedent(src)
    tree = ast.parse(src, mode="exec")

    if tree.body and isinstance(tree.body[-1], ast.Expr):
        # Extract the last expression
        last = tree.body.pop()
        body_code = ast.unparse(ast.Module(tree.body, []))
        expr_code = ast.unparse(last.value)  # type: ignore
        # Display the last expression value like Jupyter does
        return f"{body_code}\n_ = {expr_code}\nif _ is not None: print(_)"
    else:
        return src

# Strategy for generating Python source code
def src_strategy():
    # Generate valid Python code snippets
    return st.one_of(
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=100),
        st.from_regex(r'[a-zA-Z0-9_]+ = [a-zA-Z0-9_]+', fullmatch=True),
        st.from_regex(r'print\([a-zA-Z0-9_]+\)', fullmatch=True),
        st.from_regex(r'[a-zA-Z0-9_]+\([a-zA-Z0-9_]*\)', fullmatch=True)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(src=src_strategy())
@example(src="")
@example(src="x = 10")
@example(src="print('Hello, World!')")
@example(src="def foo(): pass")
@example(src="x = 10\ny = 20\nx + y")
def test_jupyterize(src: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    src_copy = copy.deepcopy(src)

    # Call func0 to verify input validity
    try:
        expected = _jupyterize(src_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "src": src_copy
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