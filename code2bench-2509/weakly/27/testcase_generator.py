from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import inspect
import json
import os
import atexit
import copy
from typing import Dict, Optional

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def get_docstring_description_input(func) -> Dict[str, Optional[str]]:
    """Extract parameter descriptions from function docstring.

    Parses the function's docstring to extract descriptions for each parameter.
    Looks for lines that start with parameter names followed by descriptions.

    Args:
        func: The function to extract parameter descriptions from.

    Returns:
        Dictionary mapping parameter names to their descriptions.
        Parameters without descriptions are omitted.

    Example:
        For a function with docstring containing "param1: Description of param1",
        returns {"param1": "Description of param1"}.
    """
    doc = func.__doc__
    if not doc:
        return {}
    descriptions = {}
    for line in map(str.strip, doc.splitlines()):
        for param in inspect.signature(func).parameters:
            if param == "self":
                continue
            if line.startswith(param):
                descriptions[param] = line.split(param, 1)[1].strip()
    return descriptions

# Strategy for generating functions with docstrings
def func_strategy():
    # Generate a simple function with a docstring containing parameter descriptions
    param_names = st.lists(
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10),
        min_size=1, max_size=5
    )
    param_descriptions = st.lists(
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
        min_size=1, max_size=5
    )
    return st.builds(
        lambda names, descs: create_function_with_docstring(names, descs),
        param_names, param_descriptions
    )

def create_function_with_docstring(param_names, param_descriptions):
    # Create a function with a docstring containing parameter descriptions
    docstring = "\n".join([f"{name}: {desc}" for name, desc in zip(param_names, param_descriptions)])
    def func(*args, **kwargs):
        pass
    func.__doc__ = docstring
    return func

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(func=func_strategy())
@example(func=lambda x: x)
@example(func=lambda x, y: x + y)
@example(func=lambda x, y, z: x + y + z)
def test_get_docstring_description_input(func):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    func_copy = copy.deepcopy(func)

    # Call func0 to verify input validity
    try:
        expected = get_docstring_description_input(func_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "func": func_copy.__name__ if hasattr(func_copy, '__name__') else "lambda"
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