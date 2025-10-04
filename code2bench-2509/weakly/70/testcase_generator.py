from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Dict
from collections import Counter
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
def calculate_aggregated_metrics(metrics_data: Dict[str, list]) -> Dict[str, Dict]:
    """Calculate aggregated scores for metrics (numeric average or categorical frequency)."""
    agg_metrics = {}
    for metric_name, scores in metrics_data.items():
        # Remove None values
        scores = [score for score in scores if score is not None]
        if not scores:
            avg_score = 0
        elif isinstance(scores[0], (int, float)):
            # Numeric metric - calculate average
            avg_score = sum(scores) / len(scores)
        else:
            # Categorical metric - create frequency distribution
            avg_score = dict(Counter(scores))
        agg_metrics[metric_name] = {"score": avg_score}
    return agg_metrics

# Strategies for generating inputs
def metric_name_strategy():
    return st.text(min_size=1, max_size=10, alphabet=st.characters(whitelist_categories=('L', 'N')))

def numeric_scores_strategy():
    return st.lists(st.one_of(st.integers(), st.floats(allow_nan=False, allow_infinity=False)), min_size=0, max_size=10)

def categorical_scores_strategy():
    return st.lists(st.text(min_size=1, max_size=5, alphabet=st.characters(whitelist_categories=('L', 'N'))), min_size=0, max_size=10)

def metrics_data_strategy():
    return st.dictionaries(
        keys=metric_name_strategy(),
        values=st.one_of(
            numeric_scores_strategy(),
            categorical_scores_strategy(),
            st.lists(st.one_of(st.none(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.text(min_size=1, max_size=5)), min_size=0, max_size=10)
        ),
        min_size=1, max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(metrics_data=metrics_data_strategy())
@example(metrics_data={})
@example(metrics_data={"metric1": []})
@example(metrics_data={"metric1": [1, 2, 3]})
@example(metrics_data={"metric1": [1.0, 2.0, 3.0]})
@example(metrics_data={"metric1": ["a", "b", "c"]})
@example(metrics_data={"metric1": [None, 1, 2]})
@example(metrics_data={"metric1": [None, "a", "b"]})
@example(metrics_data={"metric1": [1, 2, 3], "metric2": ["a", "b", "c"]})
def test_calculate_aggregated_metrics(metrics_data: Dict[str, list]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    metrics_data_copy = copy.deepcopy(metrics_data)

    # Call func0 to verify input validity
    try:
        expected = calculate_aggregated_metrics(metrics_data_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "metrics_data": {k: v for k, v in metrics_data_copy.items()}
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