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
def parse_version(version_str: str) -> tuple[int, int, int]:
    """
    Parse version string to tuple of integers for comparison.

    Args:
        version_str: Version string like "5.5.5"

    Returns:
        Tuple of (major, minor, patch) as integers
    """
    try:
        parts = version_str.strip().split(".")
        if len(parts) >= 3:
            return (int(parts[0]), int(parts[1]), int(parts[2]))
        elif len(parts) == 2:
            return (int(parts[0]), int(parts[1]), 0)
        elif len(parts) == 1:
            return (int(parts[0]), 0, 0)
        else:
            return (0, 0, 0)
    except (ValueError, IndexError):
        return (0, 0, 0)

# Strategy for generating version strings
def version_strategy():
    return st.one_of([
        st.tuples(
            st.integers(min_value=0, max_value=2147483647),
            st.integers(min_value=0, max_value=2147483647),
            st.integers(min_value=0, max_value=2147483647)
        ).map(lambda x: f"{x[0]}.{x[1]}.{x[2]}"),
        st.tuples(
            st.integers(min_value=0, max_value=2147483647),
            st.integers(min_value=0, max_value=2147483647)
        ).map(lambda x: f"{x[0]}.{x[1]}"),
        st.integers(min_value=0, max_value=2147483647).map(lambda x: f"{x}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(version_str=version_strategy())
@example(version_str="1.2.3")
@example(version_str="4.5")
@example(version_str="6")
@example(version_str="invalid")
@example(version_str="1.2.3.4")
@example(version_str="")
def test_parse_version(version_str: str):
    global stop_collecting
    if stop_collecting:
        return
    
    try:
        expected = parse_version(version_str)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"version_str": version_str},
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