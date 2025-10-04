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
def clean_if_name(code: str) -> str:
    try:
        astree = ast.parse(code)
        last_block = astree.body[-1]
        if isinstance(last_block, ast.If):
            condition = last_block.test
            if ast.unparse(condition).strip() == "__name__ == '__main__'":
                code = ast.unparse(astree.body[:-1]) + "\n" + ast.unparse(last_block.body)  # type: ignore
    except Exception:
        pass

    return code

# Strategy for generating Python code strings
def code_strategy():
    # Generate valid Python code snippets
    return st.one_of(
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=100),
        st.from_regex(r'[a-zA-Z0-9_\s\n=+\-*/%()\[\]{}.,;:<>!@#$%^&|`~"\']+', fullmatch=True),
        st.builds(
            lambda x: f"if __name__ == '__main__':\n    {x}",
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=50)
        ),
        st.builds(
            lambda x: f"if __name__ == '__main__':\n    {x}\nelse:\n    pass",
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=50)
        ),
        st.builds(
            lambda x: f"{x}\nif __name__ == '__main__':\n    pass",
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=50)
        )
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(code=code_strategy())
@example(code="")
@example(code="if __name__ == '__main__':\n    pass")
@example(code="print('Hello, World!')")
@example(code="if __name__ == '__main__':\n    print('Hello, World!')")
@example(code="print('Hello, World!')\nif __name__ == '__main__':\n    print('Hello, World!')")
@example(code="if __name__ == '__main__':\n    print('Hello, World!')\nelse:\n    pass")
def test_clean_if_name(code: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    code_copy = copy.deepcopy(code)

    # Call func0 to verify input validity
    try:
        expected = clean_if_name(code_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "code": code_copy
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