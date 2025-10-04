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
def parse_assert_statement(statement):
    """Parse a Python assert statement and extract the expected output from the
    right side of the '==' operator as a string.

    :param statement: A string containing the assert statement.
    :return: The expected output from the assert statement as a string.
    """
    try:
        parsed = ast.parse(statement, mode="exec")
    except SyntaxError:
        return "Invalid syntax"

    if len(parsed.body) == 0:
        return "Empty statement"

    if not isinstance(parsed.body[0], ast.Assert):
        return "Not an assert statement"

    comparison = parsed.body[0].test

    if not isinstance(comparison, ast.Compare) or not isinstance(comparison.ops[0], ast.Eq):
        return "Not an equality assertion"

    # Extract and return the right side of the '==' operator as a string
    return ast.get_source_segment(statement, comparison.comparators[0])

# Strategy for generating assert statements
def assert_statement_strategy():
    # Generate valid Python expressions for the left and right sides of the assertion
    left_side = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
    right_side = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
    
    # Combine into an assert statement
    return st.builds(
        lambda l, r: f"assert {l} == {r}",
        left_side, right_side
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(statement=assert_statement_strategy())
@example(statement="assert 1 == 1")
@example(statement="assert 'a' == 'a'")
@example(statement="assert [1, 2] == [1, 2]")
@example(statement="assert {'a': 1} == {'a': 1}")
@example(statement="invalid statement")
@example(statement="")
def test_parse_assert_statement(statement: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    statement_copy = copy.deepcopy(statement)

    # Call func0 to verify input validity
    try:
        expected = parse_assert_statement(statement_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "statement": statement_copy
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