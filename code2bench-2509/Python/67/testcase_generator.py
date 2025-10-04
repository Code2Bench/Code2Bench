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
def group_metrics_with_subprefixes(metrics: list[str]) -> dict:
    result = {}

    for metric in metrics:
        if "/" not in metric:
            if "charts" not in result:
                result["charts"] = {"direct_metrics": [], "subgroups": {}}
            result["charts"]["direct_metrics"].append(metric)
        else:
            parts = metric.split("/")
            main_prefix = parts[0]

            if main_prefix not in result:
                result[main_prefix] = {"direct_metrics": [], "subgroups": {}}

            if len(parts) == 2:
                result[main_prefix]["direct_metrics"].append(metric)
            else:
                subprefix = parts[1]
                if subprefix not in result[main_prefix]["subgroups"]:
                    result[main_prefix]["subgroups"][subprefix] = []
                result[main_prefix]["subgroups"][subprefix].append(metric)

    for group_data in result.values():
        group_data["direct_metrics"].sort()
        for subgroup_metrics in group_data["subgroups"].values():
            subgroup_metrics.sort()

    if "charts" in result and not result["charts"]["direct_metrics"]:
        del result["charts"]

    return result

# Strategy for generating metric names
def metric_strategy():
    return st.one_of([
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
        ).map(lambda x: f"{x[0]}/{x[1]}"),
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
        ).map(lambda x: f"{x[0]}/{x[1]}/{x[2]}")
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(metrics=st.lists(metric_strategy(), min_size=1, max_size=20, unique=True))
@example(metrics=["loss", "train/acc", "train/loss/normalized", "train/loss/unnormalized", "val/loss"])
@example(metrics=["train/acc", "train/loss/normalized", "train/loss/unnormalized"])
@example(metrics=["loss"])
@example(metrics=["train/acc"])
@example(metrics=["train/loss/normalized"])
@example(metrics=["train/loss/unnormalized"])
@example(metrics=["val/loss"])
@example(metrics=["train/acc", "train/loss/normalized", "train/loss/unnormalized", "val/loss"])
@example(metrics=["train/acc", "train/loss/normalized", "train/loss/unnormalized", "val/loss", "charts"])
def test_group_metrics_with_subprefixes(metrics: list[str]):
    global stop_collecting
    if stop_collecting:
        return
    
    metrics_copy = copy.deepcopy(metrics)
    try:
        expected = group_metrics_with_subprefixes(metrics_copy)
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