from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import math
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

# Ground truth function
def _prime_factors(x: int) -> list[int]:
    factors = []
    while x % 2 == 0:
        factors.append(2)
        x //= 2
    for i in range(3, int(math.sqrt(x)) + 1, 2):
        while x % i == 0:
            factors.append(i)
            x //= i
    if x > 1:
        factors.append(x)
    return sorted(factors)

# Strategy for generating integers
def integer_strategy():
    return st.integers(min_value=2, max_value=1000)

# Hypothesis test configuration
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(x=integer_strategy())
@example(x=2)
@example(x=3)
@example(x=4)
@example(x=5)
@example(x=6)
@example(x=7)
@example(x=8)
@example(x=9)
@example(x=10)
@example(x=11)
@example(x=12)
@example(x=13)
@example(x=14)
@example(x=15)
@example(x=16)
@example(x=17)
@example(x=18)
@example(x=19)
@example(x=20)
@example(x=21)
@example(x=22)
@example(x=23)
@example(x=24)
@example(x=25)
@example(x=26)
@example(x=27)
@example(x=28)
@example(x=29)
@example(x=30)
@example(x=31)
@example(x=32)
@example(x=33)
@example(x=34)
@example(x=35)
@example(x=36)
@example(x=37)
@example(x=38)
@example(x=39)
@example(x=40)
@example(x=41)
@example(x=42)
@example(x=43)
@example(x=44)
@example(x=45)
@example(x=46)
@example(x=47)
@example(x=48)
@example(x=49)
@example(x=50)
@example(x=51)
@example(x=52)
@example(x=53)
@example(x=54)
@example(x=55)
@example(x=56)
@example(x=57)
@example(x=58)
@example(x=59)
@example(x=60)
@example(x=61)
@example(x=62)
@example(x=63)
@example(x=64)
@example(x=65)
@example(x=66)
@example(x=67)
@example(x=68)
@example(x=69)
@example(x=70)
@example(x=71)
@example(x=72)
@example(x=73)
@example(x=74)
@example(x=75)
@example(x=76)
@example(x=77)
@example(x=78)
@example(x=79)
@example(x=80)
@example(x=81)
@example(x=82)
@example(x=83)
@example(x=84)
@example(x=85)
@example(x=86)
@example(x=87)
@example(x=88)
@example(x=89)
@example(x=90)
@example(x=91)
@example(x=92)
@example(x=93)
@example(x=94)
@example(x=95)
@example(x=96)
@example(x=97)
@example(x=98)
@example(x=99)
@example(x=100)
def test_prime_factors(x: int):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return

    # Deep copy input to avoid modification
    x_copy = copy.deepcopy(x)

    # Call func0 to verify input validity
    try:
        expected = _prime_factors(x_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Small prime number"
        elif case_count == 1:
            desc = "Composite number with multiple factors"
        else:
            desc = "Large composite number"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Smallest prime number"
        elif case_count == 4:
            desc = "Number with repeated prime factors"
        elif case_count == 5:
            desc = "Number with a single prime factor"
        elif case_count == 6:
            desc = "Number with multiple distinct prime factors"
        else:
            desc = "Large prime number"

    # Store case
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "x": x_copy
        },
        "Expected": expected,
        "Usage": None
    })
    case_count += 1
    if case_count >= MAX_CASES:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {sum(len(cases) for cases in generated_cases.values())} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)