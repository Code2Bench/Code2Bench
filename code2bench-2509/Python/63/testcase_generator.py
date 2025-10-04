from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Any, Dict
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
def format_metrics_safe(metrics: Dict[str, Any]) -> str:
    if not metrics:
        return ""

    formatted_parts = []
    for name, value in metrics.items():
        if isinstance(value, (int, float)):
            try:
                formatted_parts.append(f"{name}={value:.4f}")
            except (ValueError, TypeError):
                formatted_parts.append(f"{name}={value}")
        else:
            formatted_parts.append(f"{name}={value}")

    return ", ".join(formatted_parts)

# Strategy for generating metrics dictionary
def metrics_strategy():
    return st.dictionaries(
        keys=st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
        values=st.one_of([
            st.integers(min_value=-2147483648, max_value=2147483647),
            st.floats(allow_nan=False, allow_infinity=False, width=32),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.booleans(),
            st.none()
        ]),
        min_size=0, max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(metrics=metrics_strategy())
@example(metrics={})
@example(metrics={"a": 1})
@example(metrics={"a": 1.23456789})
@example(metrics={"a": "string"})
@example(metrics={"a": True})
@example(metrics={"a": None})
@example(metrics={"a": 1, "b": 2.345, "c": "string", "d": True, "e": None})
def test_format_metrics_safe(metrics: Dict[str, Any]):
    global stop_collecting
    if stop_collecting:
        return
    
    metrics_copy = copy.deepcopy(metrics)
    try:
        expected = format_metrics_safe(metrics_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"metrics": metrics},
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