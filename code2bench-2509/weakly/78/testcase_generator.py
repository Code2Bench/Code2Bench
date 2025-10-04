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
def decode_base_n(encoded: str, n: int, table: Optional[str] = None) -> int:
    if table is None:
        table = string.digits + string.ascii_lowercase

    if not 2 <= n <= len(table):
        raise ValueError(f"Base must be between 2 and {len(table)}")

    if not encoded:
        return 0

    is_negative = encoded.startswith("-")
    if is_negative:
        encoded = encoded[1:]

    result = 0
    for i, char in enumerate(reversed(encoded.lower())):
        if char not in table:
            raise ValueError(f"Invalid character '{char}' for base {n}")

        digit_value = table.index(char)
        if digit_value >= n:
            raise ValueError(f"Invalid digit '{char}' for base {n}")

        result += digit_value * (n**i)

    return -result if is_negative else result

# Strategies for generating inputs
def encoded_strategy():
    return st.text(alphabet=string.digits + string.ascii_letters + "-", min_size=0, max_size=10)

def n_strategy():
    return st.integers(min_value=2, max_value=36)

def table_strategy():
    return st.text(alphabet=string.digits + string.ascii_letters, min_size=2, max_size=36)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    encoded=encoded_strategy(),
    n=n_strategy(),
    table=st.one_of(st.none(), table_strategy())
)
@example(encoded="", n=10, table=None)
@example(encoded="ff", n=16, table=None)
@example(encoded="16", n=36, table=None)
@example(encoded="-10", n=10, table=None)
@example(encoded="ZZ", n=36, table=None)
@example(encoded="1010", n=2, table=None)
@example(encoded="invalid", n=10, table=None)
@example(encoded="invalid", n=10, table="0123456789")
def test_decode_base_n(encoded: str, n: int, table: Optional[str]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    encoded_copy = copy.deepcopy(encoded)
    n_copy = copy.deepcopy(n)
    table_copy = copy.deepcopy(table)

    # Call func0 to verify input validity
    try:
        expected = decode_base_n(encoded_copy, n_copy, table_copy)
    except ValueError:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "encoded": encoded_copy,
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