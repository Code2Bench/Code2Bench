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
def normalize_model_name(model: str) -> str:
    """Normalize model name for consistent usage across the application.

    Handles various model name formats and maps them to standard keys.
    (Moved from utils/model_utils.py)

    Args:
        model: Raw model name from usage data

    Returns:
        Normalized model key

    Examples:
        >>> normalize_model_name("claude-3-opus-20240229")
        'claude-3-opus'
        >>> normalize_model_name("Claude 3.5 Sonnet")
        'claude-3-5-sonnet'
    """
    if not model:
        return ""

    model_lower = model.lower()

    if (
        "claude-opus-4-" in model_lower
        or "claude-sonnet-4-" in model_lower
        or "claude-haiku-4-" in model_lower
        or "sonnet-4-" in model_lower
        or "opus-4-" in model_lower
        or "haiku-4-" in model_lower
    ):
        return model_lower

    if "opus" in model_lower:
        if "4-" in model_lower:
            return model_lower
        return "claude-3-opus"
    if "sonnet" in model_lower:
        if "4-" in model_lower:
            return model_lower
        if "3.5" in model_lower or "3-5" in model_lower:
            return "claude-3-5-sonnet"
        return "claude-3-sonnet"
    if "haiku" in model_lower:
        if "3.5" in model_lower or "3-5" in model_lower:
            return "claude-3-5-haiku"
        return "claude-3-haiku"

    return model

# Strategy for generating model names
def model_name_strategy():
    return st.one_of([
        st.just(""),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
        st.tuples(
            st.one_of([st.just("claude-opus-4-"), st.just("claude-sonnet-4-"), st.just("claude-haiku-4-"), st.just("sonnet-4-"), st.just("opus-4-"), st.just("haiku-4-")]),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
        ).map(lambda x: "".join(x)),
        st.tuples(
            st.one_of([st.just("opus"), st.just("sonnet"), st.just("haiku")]),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
        ).map(lambda x: "".join(x)),
        st.tuples(
            st.one_of([st.just("claude-3-opus"), st.just("claude-3-sonnet"), st.just("claude-3-haiku")]),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
        ).map(lambda x: "".join(x)),
        st.tuples(
            st.one_of([st.just("claude-3-5-sonnet"), st.just("claude-3-5-haiku")]),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
        ).map(lambda x: "".join(x))
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(model=model_name_strategy())
@example(model="")
@example(model="claude-3-opus-20240229")
@example(model="Claude 3.5 Sonnet")
@example(model="claude-opus-4-20240229")
@example(model="sonnet-4-20240229")
@example(model="haiku-4-20240229")
@example(model="claude-3-5-sonnet")
@example(model="claude-3-5-haiku")
@example(model="claude-3-opus")
@example(model="claude-3-sonnet")
@example(model="claude-3-haiku")
def test_normalize_model_name(model: str):
    global stop_collecting
    if stop_collecting:
        return
    
    model_copy = copy.deepcopy(model)
    try:
        expected = normalize_model_name(model_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"model": model},
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