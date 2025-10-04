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
def compute_method_ranks(data, selected_models=None, selected_data=None):
    """
    Compute, for each metric, the rank of each model (1 = best accuracy).

    Args:
        data (List[Dict]): your JSON‐like list of dicts.
        selected_models (List[str], optional):
            List of clean model names (with "_temp0_n1_seed2" already stripped)
            whose ranks you care about.  If None, returns ranks for _all_ models.
        selected_data (List[str], optional):
            List of metric names _without_ the "_acc" suffix.  If None,
            defaults to all keys ending in "_acc" except "avg_acc".

    Returns:
        Dict[str, Dict[str,int]]:  
            Outer: metric →  
            Inner: model_name → rank (1 = highest accuracy)
    """
    # 1. Determine which metrics to rank
    if selected_data is None:
        selected_data = sorted(
            k[:-4] for k in data[0].keys()
            if k.endswith("_acc") and k != "avg_acc"
        )

    # 2. Prepare clean model names + parsed accuracies
    models = []
    for item in data:
        clean_name = item["model"].replace("_temp0_n1_seed2", "")
        models.append((clean_name, item))

    # 3. For each metric, sort and assign ranks
    all_ranks = {}
    for metric in selected_data:
        key = f"{metric}_acc"
        # build list of (model, float(acc))
        vals = [
            (name, float(item.get(key, 0.0)))
            for name, item in models
        ]
        # sort desc by accuracy
        vals.sort(key=lambda x: x[1], reverse=True)
        # assign ranks (1-based). Ties get the same rank.
        ranks = {}
        prev_score = None
        prev_rank = 0
        for idx, (name, score) in enumerate(vals, start=1):
            if score == prev_score:
                rank = prev_rank
            else:
                rank = idx
            ranks[name] = rank
            prev_score, prev_rank = score, rank

        # if user only wants a subset, filter
        if selected_models is not None:
            ranks = {m: ranks[m] for m in selected_models if m in ranks}

        all_ranks[metric] = ranks

    return all_ranks

# Strategy for generating JSON-like data
def data_strategy():
    return st.lists(
        st.dictionaries(
            keys=st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            values=st.one_of(
                st.floats(allow_nan=False, allow_infinity=False),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
            ),
            min_size=1,
            max_size=5
        ),
        min_size=1,
        max_size=5
    )

# Strategy for generating model names
def model_name_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)

# Strategy for generating selected models
def selected_models_strategy():
    return st.lists(model_name_strategy(), min_size=1, max_size=5)

# Strategy for generating selected data
def selected_data_strategy():
    return st.lists(st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10), min_size=1, max_size=5)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    data=data_strategy(),
    selected_models=st.one_of([st.none(), selected_models_strategy()]),
    selected_data=st.one_of([st.none(), selected_data_strategy()])
)
@example(data=[{"model": "model1", "metric1_acc": 0.5, "metric2_acc": 0.6}], selected_models=None, selected_data=None)
@example(data=[{"model": "model1", "metric1_acc": 0.5, "metric2_acc": 0.6}], selected_models=["model1"], selected_data=["metric1"])
@example(data=[{"model": "model1", "metric1_acc": 0.5, "metric2_acc": 0.6}, {"model": "model2", "metric1_acc": 0.5, "metric2_acc": 0.6}], selected_models=None, selected_data=None)
@example(data=[{"model": "model1", "metric1_acc": 0.5, "metric2_acc": 0.6}, {"model": "model2", "metric1_acc": 0.5, "metric2_acc": 0.6}], selected_models=["model1", "model2"], selected_data=["metric1", "metric2"])
def test_compute_method_ranks(data, selected_models, selected_data):
    global stop_collecting
    if stop_collecting:
        return
    
    data_copy = copy.deepcopy(data)
    selected_models_copy = copy.deepcopy(selected_models)
    selected_data_copy = copy.deepcopy(selected_data)
    try:
        expected = compute_method_ranks(data_copy, selected_models_copy, selected_data_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"data": data, "selected_models": selected_models, "selected_data": selected_data},
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