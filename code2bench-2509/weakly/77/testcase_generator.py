from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import string
import json
import os
import atexit
import copy
from typing import Optional

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def encode_base_n(num: int, n: int, table: Optional[str] = None) -> str:
    """
    Encode a number in base-n representation.

    Args:
        num: The number to encode
        n: The base to use for encoding
        table: Custom character table (optional)

    Returns:
        String representation of the number in base-n

    Examples:
        >>> encode_base_n(255, 16)
        'ff'
        >>> encode_base_n(42, 36)
        '16'
    """
    if table is None:
        # Default table: 0-9, a-z
        table = string.digits + string.ascii_lowercase

    if not 2 <= n <= len(table):
        raise ValueError(f"Base must be between 2 and {len(table)}")

    if num == 0:
        return table[0]

    result = []
    is_negative = num < 0
    num = abs(num)

    while num > 0:
        result.append(table[num % n])
        num //= n

    if is_negative:
        result.append("-")

    return "".join(reversed(result))

# Strategies for generating inputs
def num_strategy():
    return st.integers(min_value=-1000, max_value=1000)

def base_strategy():
    return st.integers(min_value=2, max_value=36)

def table_strategy():
    return st.text(
        alphabet=st.characters(min_codepoint=33, max_codepoint=126),
        min_size=2,
        max_size=36
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    num=num_strategy(),
    n=base_strategy(),
    table=st.one_of(st.none(), table_strategy())
)
@example(num=0, n=2, table=None)
@example(num=255, n=16, table=None)
@example(num=42, n=36, table=None)
@example(num=-123, n=10, table=None)
@example(num=123, n=10, table="01")
@example(num=123, n=2, table="01")
@example(num=123, n=36, table="0123456789abcdefghijklmnopqrstuvwxyz")
def test_encode_base_n(num: int, n: int, table: Optional[str]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    num_copy = copy.deepcopy(num)
    n_copy = copy.deepcopy(n)
    table_copy = copy.deepcopy(table)

    # Call func0 to verify input validity
    try:
        expected = encode_base_n(num_copy, n_copy, table_copy)
    except ValueError:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "num": num_copy,
            "n": n_copy,
            "table": table_copy
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