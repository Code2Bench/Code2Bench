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
def format_llm_error_message(model_name: str, error_str: str) -> str:
    """Unified LLM error message formatting function"""
    # Handle common error types and provide friendly English error messages
    if "RateLimitError" in error_str or "429" in error_str:
        if "quota" in error_str.lower() or "exceed" in error_str.lower():
            return f"⚠️ {model_name} API quota exceeded. Please check your plan and billing details."
        else:
            return f"⚠️ {model_name} API rate limit hit. Please try again later."
    elif "401" in error_str or "authentication" in error_str.lower():
        return f"🔑 {model_name} API key is invalid. Please check your configuration."
    elif "403" in error_str or "permission" in error_str.lower():
        return f"🚫 {model_name} API access denied. Please check permissions."
    elif "timeout" in error_str.lower():
        return f"⏰ {model_name} API call timed out. Please retry."
    else:
        return f"❌ {model_name} model call failed: {error_str}"

# Strategy for generating model names
def model_name_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=1, max_size=20)

# Strategy for generating error strings
def error_str_strategy():
    return st.one_of([
        st.just("RateLimitError: You have exceeded your quota."),
        st.just("429: Rate limit exceeded."),
        st.just("401: Invalid API key."),
        st.just("403: Permission denied."),
        st.just("Timeout: The request timed out."),
        st.just("Unknown error occurred."),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=1, max_size=50)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(model_name=model_name_strategy(), error_str=error_str_strategy())
@example(model_name="GPT-4", error_str="RateLimitError: You have exceeded your quota.")
@example(model_name="GPT-4", error_str="429: Rate limit exceeded.")
@example(model_name="GPT-4", error_str="401: Invalid API key.")
@example(model_name="GPT-4", error_str="403: Permission denied.")
@example(model_name="GPT-4", error_str="Timeout: The request timed out.")
@example(model_name="GPT-4", error_str="Unknown error occurred.")
def test_format_llm_error_message(model_name: str, error_str: str):
    global stop_collecting
    if stop_collecting:
        return
    
    model_name_copy = copy.deepcopy(model_name)
    error_str_copy = copy.deepcopy(error_str)
    try:
        expected = format_llm_error_message(model_name_copy, error_str_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"model_name": model_name, "error_str": error_str},
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