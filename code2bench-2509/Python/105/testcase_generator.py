from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _int_to_text(num):
    """Helper function to convert an integer to text"""

    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
            "seventeen", "eighteen", "nineteen"]

    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    if num < 20:
        return ones[num]

    if num < 100:
        return tens[num // 10] + (" " + ones[num % 10] if num % 10 != 0 else "")

    if num < 1000:
        return ones[num // 100] + " hundred" + (" " + _int_to_text(num % 100) if num % 100 != 0 else "")

    if num < 1000000:
        return _int_to_text(num // 1000) + " thousand" + (" " + _int_to_text(num % 1000) if num % 1000 != 0 else "")

    if num < 1000000000:
        return _int_to_text(num // 1000000) + " million" + (" " + _int_to_text(num % 1000000) if num % 1000000 != 0 else "")

    return _int_to_text(num // 1000000000) + " billion" + (" " + _int_to_text(num % 1000000000) if num % 1000000000 != 0 else "")

# Strategy for generating integers
num_strategy = st.integers(min_value=0, max_value=2147483647)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(num=num_strategy)
@example(num=0)
@example(num=1)
@example(num=19)
@example(num=20)
@example(num=21)
@example(num=99)
@example(num=100)
@example(num=101)
@example(num=999)
@example(num=1000)
@example(num=1001)
@example(num=999999)
@example(num=1000000)
@example(num=1000001)
@example(num=999999999)
@example(num=1000000000)
@example(num=1000000001)
def test_int_to_text(num):
    global stop_collecting
    if stop_collecting:
        return

    try:
        expected = _int_to_text(num)
    except Exception:
        return  # Skip inputs that cause exceptions

    generated_cases.append({
        "Inputs": {"num": num},
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