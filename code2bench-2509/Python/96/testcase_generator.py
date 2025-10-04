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
def _compute_duration(metrics: Dict[str, Any]) -> float:
    """
    Prefer a single wall-clock measurement if present; otherwise sum only per-step durations.
    Avoid double counting and ignore non-numeric / boolean values.
    """
    wall = metrics.get("total_duration_wall_clock")
    if isinstance(wall, (int, float)):
        return float(wall)

    # Fallback: sum per-step durations only (keys ending with "_duration")
    total = 0.0
    for k, v in metrics.items():
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            continue
        if k.endswith("_duration"):
            total += float(v)
    return total

# Strategy for generating metrics dictionaries
def metrics_strategy():
    return st.dictionaries(
        keys=st.one_of(
            st.just("total_duration_wall_clock"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1).filter(lambda x: x.endswith("_duration")),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1)
        ),
        values=st.one_of(
            st.integers(min_value=0, max_value=1000),
            st.floats(allow_nan=False, allow_infinity=False, min_value=0.0, max_value=1000.0),
            st.booleans(),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1)
        ),
        min_size=1,
        max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(metrics=metrics_strategy())
@example(metrics={"total_duration_wall_clock": 10.5})
@example(metrics={"step1_duration": 5.0, "step2_duration": 3.0})
@example(metrics={"step1_duration": 5.0, "step2_duration": 3.0, "total_duration_wall_clock": 10.5})
@example(metrics={"step1_duration": 5.0, "step2_duration": "invalid"})
@example(metrics={"step1_duration": True, "step2_duration": 3.0})
@example(metrics={"step1_duration": 5.0, "step2_duration": 3.0, "other_key": "value"})
def test_compute_duration(metrics: Dict[str, Any]):
    global stop_collecting
    if stop_collecting:
        return
    
    metrics_copy = copy.deepcopy(metrics)
    try:
        expected = _compute_duration(metrics_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "total_duration_wall_clock" in metrics or any(k.endswith("_duration") for k in metrics):
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