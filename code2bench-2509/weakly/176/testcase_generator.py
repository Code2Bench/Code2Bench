from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import json
import os
import atexit
import copy
from collections import defaultdict

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def sort_checkpoints(models):
    def get_checkpoint_num(model_name):
        if 'checkpoint-final' in model_name:
            return float('inf')
        # Check for checkpoint pattern
        checkpoint_match = re.search(r'checkpoint-(\d+)', model_name)
        if checkpoint_match:
            return int(checkpoint_match.group(1))
        # Check for global_step pattern
        global_step_match = re.search(r'global_step[_]?(\d+)', model_name)
        if global_step_match:
            return int(global_step_match.group(1))
        return float('inf')

    # Group models by base name (everything before checkpoint- or global_step)
    model_groups = defaultdict(list)
    for model in models:
        # Split on either checkpoint- or global_step
        base_name = re.split(r'(?:checkpoint-|global_step)', model)[0].rstrip('-')
        model_groups[base_name].append(model)

    # Sort each group's checkpoints
    sorted_models = []
    for base_name, checkpoints in model_groups.items():
        sorted_checkpoints = sorted(checkpoints, key=get_checkpoint_num)
        sorted_models.extend(sorted_checkpoints)

    return sorted_models

# Strategy for generating model names
def model_name_strategy():
    base_name = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P'), whitelist_characters='-_'), min_size=1, max_size=10)
    checkpoint_type = st.one_of(
        st.just('checkpoint-'),
        st.just('global_step'),
        st.just('global_step_')
    )
    checkpoint_num = st.integers(min_value=0, max_value=1000)
    return st.one_of(
        st.builds(lambda b, c, n: f"{b}-{c}{n}", base_name, checkpoint_type, checkpoint_num),
        st.builds(lambda b: f"{b}-checkpoint-final", base_name)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(models=st.lists(model_name_strategy(), min_size=1, max_size=10))
@example(models=[])
@example(models=["model-checkpoint-10", "model-checkpoint-5", "model-checkpoint-final"])
@example(models=["model-global_step10", "model-global_step5", "model-global_step_15"])
@example(models=["model-checkpoint-10", "model-global_step5", "model-checkpoint-final"])
@example(models=["model-checkpoint-10", "model-checkpoint-10"])  # Duplicate checkpoints
def test_sort_checkpoints(models):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    models_copy = copy.deepcopy(models)

    # Call func0 to verify input validity
    try:
        expected = sort_checkpoints(models_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "models": models_copy
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