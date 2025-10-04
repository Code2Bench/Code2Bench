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
def preprocess_operands(operand):
    """
    Interprets a string operand as an appropriate type.

    Args:
        operand (str): the string operand to interpret.

    Returns:
        The interpreted operand as an appropriate type.
    """
    if isinstance(operand, str):
        if operand.isdigit():
            operand = int(operand)
        elif operand.replace(".", "").isnumeric():
            operand = float(operand)
    return operand

# Strategy for generating operands
def operand_strategy():
    return st.one_of([
        st.integers(min_value=-2147483648, max_value=2147483647),
        st.floats(allow_nan=False, allow_infinity=False, width=32),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10).filter(
            lambda x: x.isdigit() or x.replace(".", "").isnumeric()
        ),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10).filter(
            lambda x: not x.isdigit() and not x.replace(".", "").isnumeric()
        )
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(operand=operand_strategy())
@example(operand="123")
@example(operand="123.456")
@example(operand="abc")
@example(operand="123abc")
@example(operand="")
def test_preprocess_operands(operand):
    global stop_collecting
    if stop_collecting:
        return
    
    operand_copy = copy.deepcopy(operand)
    try:
        expected = preprocess_operands(operand_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"operand": operand},
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