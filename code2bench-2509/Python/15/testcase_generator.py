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
def _truncate(value: str, max_chars: int, ellipsis: str) -> str:
    if max_chars is None:
        return value
    if max_chars <= 0:
        return ""
    if len(value) <= max_chars:
        return value
    # Ensure final length <= max_chars considering ellipsis
    ell = ellipsis or ""
    if len(ell) >= max_chars:
        # Ellipsis doesn't fit; hard cut
        return value[:max_chars]
    cut = max_chars - len(ell)
    return value[:cut] + ell

# Strategy for generating test cases
def truncate_strategy():
    return st.tuples(
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=100),
        st.one_of([st.integers(min_value=-10, max_value=100), st.none()]),
        st.one_of([st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=10), st.none()])
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(value_max_ell=truncate_strategy())
@example(value_max_ell=("short", 10, "..."))
@example(value_max_ell=("longer than max", 5, "..."))
@example(value_max_ell=("exact length", 12, "..."))
@example(value_max_ell=("", 5, "..."))
@example(value_max_ell=("long", 0, "..."))
@example(value_max_ell=("long", None, "..."))
@example(value_max_ell=("long", 10, ""))
@example(value_max_ell=("long", 10, None))
@example(value_max_ell=("long", 10, "very long ellipsis"))
def test_truncate(value_max_ell):
    global stop_collecting
    if stop_collecting:
        return
    
    value, max_chars, ellipsis = value_max_ell
    value_copy = copy.deepcopy(value)
    ellipsis_copy = copy.deepcopy(ellipsis)
    try:
        expected = _truncate(value_copy, max_chars, ellipsis_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"value": value, "max_chars": max_chars, "ellipsis": ellipsis},
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