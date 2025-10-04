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
def format_improvement_safe(parent_metrics: Dict[str, Any], child_metrics: Dict[str, Any]) -> str:
    if not parent_metrics or not child_metrics:
        return ""

    improvement_parts = []
    for metric, child_value in child_metrics.items():
        if metric in parent_metrics:
            parent_value = parent_metrics[metric]
            # Only calculate improvement for numeric values
            if isinstance(child_value, (int, float)) and isinstance(parent_value, (int, float)):
                try:
                    diff = child_value - parent_value
                    improvement_parts.append(f"{metric}={diff:+.4f}")
                except (ValueError, TypeError):
                    # Skip non-numeric comparisons
                    continue

    return ", ".join(improvement_parts)

# Strategy for generating metrics dictionaries
def metrics_strategy():
    return st.dictionaries(
        keys=st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
        values=st.one_of([
            st.integers(min_value=-2147483648, max_value=2147483647),
            st.floats(allow_nan=False, allow_infinity=False, width=32),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.booleans(),
            st.lists(st.integers(), max_size=3)
        ]),
        min_size=1, max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(parent_metrics=metrics_strategy(), child_metrics=metrics_strategy())
@example(parent_metrics={}, child_metrics={})
@example(parent_metrics={"a": 1}, child_metrics={"a": 2})
@example(parent_metrics={"a": 1.5}, child_metrics={"a": 2.5})
@example(parent_metrics={"a": "string"}, child_metrics={"a": "another"})
@example(parent_metrics={"a": [1, 2]}, child_metrics={"a": [3, 4]})
@example(parent_metrics={"a": True}, child_metrics={"a": False})
def test_format_improvement_safe(parent_metrics: Dict[str, Any], child_metrics: Dict[str, Any]):
    global stop_collecting
    if stop_collecting:
        return
    
    parent_metrics_copy = copy.deepcopy(parent_metrics)
    child_metrics_copy = copy.deepcopy(child_metrics)
    try:
        expected = format_improvement_safe(parent_metrics_copy, child_metrics_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter cases to prioritize those with numeric comparisons
    if any(
        isinstance(parent_metrics.get(metric), (int, float)) and isinstance(child_metrics.get(metric), (int, float))
        for metric in child_metrics
    ):
        generated_cases.append({
            "Inputs": {"parent_metrics": parent_metrics, "child_metrics": child_metrics},
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