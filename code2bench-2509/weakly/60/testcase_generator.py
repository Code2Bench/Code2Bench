from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import ast
import re
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
def extract_first_section_name_from_code(source_code):
    """
    Extract the first section name from the source code.
    """
    parsed = ast.parse(source_code)
    for node in ast.walk(parsed):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value
            if getattr(call.func, "id", None) == "print" and call.args:
                arg0 = call.args[0]
                if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                    # Match "Section: ..." pattern
                    m = re.match(r"Section:\s*(.+)", arg0.value)
                    if m:
                        return m.group(1).strip()
    return None

# Strategy for generating source code with potential section names
def source_code_strategy():
    # Generate section names
    section_name = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), min_codepoint=32, max_codepoint=126),
        min_size=1, max_size=20
    )
    
    # Generate print statements with section names
    print_statement = st.builds(
        lambda s: f'print("Section: {s}")',
        section_name
    )
    
    # Generate random code snippets
    random_code = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), min_codepoint=32, max_codepoint=126),
        min_size=0, max_size=100
    )
    
    # Combine print statements with random code
    return st.lists(
        st.one_of(
            print_statement,
            random_code
        ),
        min_size=1, max_size=10
    ).map(lambda x: '\n'.join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(source_code=source_code_strategy())
@example(source_code='print("Section: Introduction")')
@example(source_code='print("Section: Results")')
@example(source_code='print("Section: ")')
@example(source_code='print("Section: 123")')
@example(source_code='print("Section: !@#")')
@example(source_code='print("No section here")')
@example(source_code='x = 1\ny = 2\nprint("Section: Methods")')
@example(source_code='print("Section: A")\nprint("Section: B")')
@example(source_code='print("Not a section")')
def test_extract_first_section_name_from_code(source_code: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    source_code_copy = copy.deepcopy(source_code)

    # Call func0 to verify input validity
    try:
        expected = extract_first_section_name_from_code(source_code_copy)
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