from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Optional
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
def parse_provider_and_model(model_str: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    """
    Parse a model string like 'openai/gpt-4', 'text-completion-openai/gpt-3.5-turbo-instruct/', etc.
    Returns (provider, model_name), both lowercased and stripped of trailing slashes.
    """
    if not isinstance(model_str, str) or not model_str:
        return None, None
    model_str = model_str.strip().rstrip("/")
    if "/" in model_str:
        provider, model_name = model_str.split("/", 1)
        provider = provider.strip().lower()
        model_name = model_name.strip()
        # Handle cases like 'text-completion-openai' -> 'openai'
        if "-" in provider:
            provider = provider.split("-")[-1]
        return provider, model_name
    return None, model_str.strip() if model_str else None

# Strategy for generating model strings
def model_strategy():
    return st.one_of([
        st.just(None),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
        ).map(lambda x: f"{x[0]}/{x[1]}"),
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
        ).map(lambda x: f"{x[0]}-{x[1]}/{x[2]}")
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(model_str=model_strategy())
@example(model_str=None)
@example(model_str="")
@example(model_str="openai/gpt-4")
@example(model_str="text-completion-openai/gpt-3.5-turbo-instruct/")
@example(model_str="gpt-4")
@example(model_str="text-completion-openai/")
@example(model_str="/gpt-4")
def test_parse_provider_and_model(model_str: Optional[str]):
    global stop_collecting
    if stop_collecting:
        return
    
    model_str_copy = copy.deepcopy(model_str)
    try:
        expected = parse_provider_and_model(model_str_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if model_str is None or isinstance(model_str, str):
        generated_cases.append({
            "Inputs": {"model_str": model_str},
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