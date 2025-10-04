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
def scrape_python_blocks(source_code, file_path_for_logging):
    """
    Parses Python source code from a string and extracts top-level classes,
    functions, and try/if blocks. It ignores methods inside classes and
    any blocks nested within functions.

    Args:
        source_code (str): The Python source code as a string.
        file_path_for_logging (str): The path of the file being scraped, for logging purposes.

    Returns:
        list: A list of strings, where each string is a source code block.
    """
    blocks = []
    try:
        # Parse the source code into an Abstract Syntax Tree (AST)
        tree = ast.parse(source_code, filename=file_path_for_logging)
    except (SyntaxError, ValueError) as e:
        print(f"Error parsing {file_path_for_logging}: {e}")
        return []

    # Iterate over only the top-level nodes in the module's body
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # Extracts top-level functions and full classes
            blocks.append(ast.get_source_segment(source_code, node))
        elif isinstance(node, ast.Try):
            # Extracts top-level try...except...finally blocks
            blocks.append(ast.get_source_segment(source_code, node))
        elif isinstance(node, ast.If):
            # Extracts top-level if blocks, as requested
            blocks.append(ast.get_source_segment(source_code, node))

    return blocks

# Strategies for generating inputs
def source_code_strategy():
    # Generate valid Python code blocks
    return st.one_of(
        st.text(min_size=1, max_size=100),  # Random text
        st.from_regex(r'def \w+\(.*\):\n\s+pass'),  # Simple function
        st.from_regex(r'class \w+:\n\s+pass'),  # Simple class
        st.from_regex(r'try:\n\s+pass\nexcept:\n\s+pass'),  # Simple try block
        st.from_regex(r'if \w+:\n\s+pass'),  # Simple if block
    )

def file_path_strategy():
    # Generate file paths
    return st.one_of(
        st.just("example.py"),
        st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('L', 'N', 'P')))
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    source_code=source_code_strategy(),
    file_path_for_logging=file_path_strategy()
)
@example(
    source_code="def foo():\n    pass",
    file_path_for_logging="example.py"
)
@example(
    source_code="class Bar:\n    pass",
    file_path_for_logging="example.py"
)
@example(
    source_code="try:\n    pass\nexcept:\n    pass",
    file_path_for_logging="example.py"
)
@example(
    source_code="if True:\n    pass",
    file_path_for_logging="example.py"
)
@example(
    source_code="invalid code",
    file_path_for_logging="example.py"
)
def test_scrape_python_blocks(source_code: str, file_path_for_logging: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    source_code_copy = copy.deepcopy(source_code)
    file_path_for_logging_copy = copy.deepcopy(file_path_for_logging)

    # Call func0 to verify input validity
    try:
        expected = scrape_python_blocks(source_code_copy, file_path_for_logging_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "source_code": source_code_copy,
            "file_path_for_logging": file_path_for_logging_copy
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