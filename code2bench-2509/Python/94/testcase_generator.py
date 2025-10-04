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
def align_first_line_to_second(code_string: str) -> str:
    lines = code_string.splitlines()

    first_line_info = None
    second_line_info = None

    for index, line_content in enumerate(lines):
        if line_content.strip():
            if first_line_info is None:
                first_line_info = {"index": index, "content": line_content}
            elif second_line_info is None:
                second_line_info = {"index": index, "content": line_content}
                break

    if not first_line_info or not second_line_info:
        return code_string

    first_line_content = first_line_info["content"]
    second_line_content = second_line_info["content"]

    first_line_indent = " " * (
        len(first_line_content) - len(first_line_content.lstrip(" "))
    )
    second_line_indent = " " * (
        len(second_line_content) - len(second_line_content.lstrip(" "))
    )

    if first_line_indent != second_line_indent:
        original_index = first_line_info["index"]
        stripped_content = first_line_content.lstrip(" ")
        lines[original_index] = second_line_indent + stripped_content

    return "\n".join(lines)

# Strategy for generating code-like lines
def line_strategy():
    return st.one_of([
        # Lines with varying indentation
        st.tuples(
            st.text(st.characters(whitelist_categories=('Zs',)), min_size=0, max_size=8),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
        ).map(lambda x: "".join(x)),
        # Empty lines
        st.just(""),
        # Lines with no indentation
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(code_string=st.lists(line_strategy(), min_size=2, max_size=10).map(lambda x: "\n".join(x)))
@example(code_string="  first line\nsecond line")
@example(code_string="first line\n  second line")
@example(code_string="\n\nfirst line\nsecond line")
@example(code_string="first line\n\nsecond line")
@example(code_string="  first line\n  second line")
@example(code_string="first line\nsecond line\nthird line")
@example(code_string="  first line\nsecond line\n  third line")
def test_align_first_line_to_second(code_string: str):
    global stop_collecting
    if stop_collecting:
        return
    
    code_string_copy = copy.deepcopy(code_string)
    try:
        expected = align_first_line_to_second(code_string_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    lines = code_string.splitlines()
    if len(lines) >= 2 and any(line.strip() for line in lines):
        generated_cases.append({
            "Inputs": {"code_string": code_string},
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