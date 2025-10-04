from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Dict, List
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
def collect_all_selected_models(llm_configs: List[Dict]) -> List[str]:
    """Collect all models from all configured providers, remove duplicates and maintain order."""
    seen = set()
    ordered_models: List[str] = []
    for conf in llm_configs or []:
        models_str = (conf.get("models") or "").strip()
        if not models_str:
            continue
        for m in models_str.split(","):
            model = m.strip()
            if model and model not in seen:
                seen.add(model)
                ordered_models.append(model)
    return ordered_models

# Strategy for generating LLM configs
def llm_config_strategy():
    return st.lists(
        st.dictionaries(
            keys=st.just("models"),
            values=st.text(
                st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
                min_size=1
            ).map(lambda s: ",".join([m.strip() for m in s.split(",") if m.strip()])),
            min_size=0,
            max_size=5
        ),
        min_size=0,
        max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(llm_configs=llm_config_strategy())
@example(llm_configs=[])
@example(llm_configs=[{"models": "model1"}])
@example(llm_configs=[{"models": "model1,model2"}])
@example(llm_configs=[{"models": "model1,model2"}, {"models": "model2,model3"}])
@example(llm_configs=[{"models": "model1,model2"}, {"models": ""}])
@example(llm_configs=[{"models": "model1,model2"}, {"models": "model3,model4"}])
@example(llm_configs=[{"models": "model1,model2"}, {"models": "model2,model3"}, {"models": "model3,model4"}])
def test_collect_all_selected_models(llm_configs: List[Dict]):
    global stop_collecting
    if stop_collecting:
        return
    
    llm_configs_copy = copy.deepcopy(llm_configs)
    try:
        expected = collect_all_selected_models(llm_configs_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(conf.get("models", "").strip() for conf in llm_configs):
        generated_cases.append({
            "Inputs": {"llm_configs": llm_configs},
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