from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import ast
import json
import os
import atexit
import copy
from typing import List

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def deduplicate(solutions: List[str]) -> List[str]:
    asts = set()
    deduplicated = []
    for solution in solutions:
        solution = re.sub(r"#[^\n]*", "", solution)
        solution = re.sub(r'"""[^"]*"""', "", solution)
        solution = re.sub(r"'''[^']*'''", "", solution)
        try:
            ast_string = ast.dump(ast.parse(solution))
        except SyntaxError:
            continue
        except MemoryError:
            continue
        if ast_string not in asts:
            asts.add(ast_string)
            deduplicated.append(solution)
    return list(deduplicated)

# Strategy for generating Python code strings
def python_code_strategy():
    # Generate valid Python code snippets
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), whitelist_characters='\n\t '),
        min_size=1, max_size=100
    ).filter(lambda x: x.strip() != "")

# Strategy for generating lists of Python code strings
def solutions_strategy():
    return st.lists(
        python_code_strategy(),
        min_size=0, max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(solutions=solutions_strategy())
@example(solutions=[])
@example(solutions=["print('Hello, World!')"])
@example(solutions=["print('Hello, World!')", "print('Hello, World!')"])
@example(solutions=["# Comment", "print('Hello, World!')"])
@example(solutions=["'''Docstring'''", "print('Hello, World!')"])
def test_deduplicate(solutions: List[str]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    solutions_copy = copy.deepcopy(solutions)

    # Call func0 to verify input validity
    try:
        expected = deduplicate(solutions_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "solutions": solutions_copy
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