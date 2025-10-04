from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List
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
def _format_models(models: List[str]) -> str:
    if not models:
        return "No models"

    if len(models) == 1:
        return models[0]
    elif len(models) <= 3:
        return "\n".join([f"• {model}" for model in models])
    else:
        first_two = models[:2]
        remaining_count = len(models) - 2
        formatted = "\n".join([f"• {model}" for model in first_two])
        formatted += f"\n• ...and {remaining_count} more"
        return formatted

# Strategy for generating model names
def model_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(models=st.lists(model_strategy(), max_size=10))
@example(models=[])
@example(models=["Model1"])
@example(models=["Model1", "Model2"])
@example(models=["Model1", "Model2", "Model3"])
@example(models=["Model1", "Model2", "Model3", "Model4"])
def test_format_models(models: List[str]):
    global stop_collecting
    if stop_collecting:
        return
    
    models_copy = copy.deepcopy(models)
    try:
        expected = _format_models(models_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if not models or len(models) >= 1:
        generated_cases.append({
            "Inputs": {"models": models},
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