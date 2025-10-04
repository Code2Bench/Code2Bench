from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Optional
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
def extract_examples_section(docstring: Optional[str]) -> Optional[str]:
    """Extracts the 'Examples:' section from a Google-style docstring.

    Args:
        docstring (Optional[str]): The full docstring of a function.

    Returns:
        Optional[str]: The extracted examples section, or None if not found.
    """
    if not docstring or "Examples:" not in docstring:
        return None

    lines = docstring.strip().splitlines()
    in_examples = False
    examples_lines = []

    for line in lines:
        stripped = line.strip()

        if not in_examples and stripped.startswith("Examples:"):
            in_examples = True
            examples_lines.append(line)
            continue

        if in_examples:
            if stripped and not line.startswith(" ") and stripped.endswith(":"):
                break
            examples_lines.append(line)

    return "\n".join(examples_lines).strip() if examples_lines else None

# Strategy for generating docstrings
def docstring_strategy():
    return st.one_of([
        st.just(None),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=100),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=100).map(lambda x: f"Examples:\n{x}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=100).map(lambda x: f"Examples:\n    {x}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=100).map(lambda x: f"Examples:\n    {x}\nOtherSection:"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=100).map(lambda x: f"Examples:\n    {x}\n    OtherSection:"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=100).map(lambda x: f"Examples:\n    {x}\nOtherSection:\n    Content"),
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(docstring=docstring_strategy())
@example(docstring=None)
@example(docstring="Examples:\n    Example 1\n    Example 2")
@example(docstring="Examples:\n    Example 1\nOtherSection:")
@example(docstring="Examples:\n    Example 1\n    Example 2\nOtherSection:\n    Content")
@example(docstring="Examples:\n    Example 1\n    Example 2\nOtherSection:")
@example(docstring="Examples:\n    Example 1\n    Example 2\nOtherSection:\n    Content")
def test_extract_examples_section(docstring: Optional[str]):
    global stop_collecting
    if stop_collecting:
        return
    
    docstring_copy = copy.deepcopy(docstring)
    try:
        expected = extract_examples_section(docstring_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if docstring is not None and "Examples:" in docstring:
        generated_cases.append({
            "Inputs": {"docstring": docstring},
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