from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import difflib
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
def suggest_similar_models(invalid_model: str, available_models: list[str]) -> list[str]:
    """Use difflib to find similar model names"""
    if not available_models:
        return []

    # Get close matches using fuzzy matching
    suggestions = difflib.get_close_matches(invalid_model, available_models, n=3, cutoff=0.3)
    return suggestions

# Strategies for generating inputs
def invalid_model_strategy():
    return st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=1, max_size=20)

def available_models_strategy():
    return st.lists(
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=1, max_size=20),
        min_size=0, max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    invalid_model=invalid_model_strategy(),
    available_models=available_models_strategy()
)
@example(invalid_model="", available_models=[])
@example(invalid_model="model1", available_models=["model1", "model2", "model3"])
@example(invalid_model="modelX", available_models=["modelA", "modelB", "modelC"])
@example(invalid_model="abc", available_models=["abcd", "abce", "abcf"])
@example(invalid_model="xyz", available_models=["xyzw", "xyzv", "xyzu"])
def test_suggest_similar_models(invalid_model: str, available_models: list[str]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    invalid_model_copy = copy.deepcopy(invalid_model)
    available_models_copy = copy.deepcopy(available_models)

    # Call func0 to verify input validity
    try:
        expected = suggest_similar_models(invalid_model_copy, available_models_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "invalid_model": invalid_model_copy,
            "available_models": available_models_copy
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