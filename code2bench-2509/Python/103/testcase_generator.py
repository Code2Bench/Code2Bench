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
def _optimize_prompt_for_imagen(prompt: str) -> str:
    """
    Optimize prompt for Imagen API by removing Gemini-specific formatting
    and enhancing it with Imagen best practices.

    Based on Imagen prompt guide: https://ai.google.dev/gemini-api/docs/imagen
    """
    # Remove Gemini-specific formatting
    prompt = prompt.replace('\n\nEnhanced prompt:', '')
    prompt = prompt.replace('\n\nAspect ratio:', '')

    # Clean up extra whitespace
    prompt = ' '.join(prompt.split())

    # Add Imagen-specific enhancements if not present
    if 'professional' in prompt.lower() and 'linkedin' in prompt.lower():
        # Enhance for LinkedIn professional content
        prompt += ", high quality, professional photography, business appropriate"

    if 'digital transformation' in prompt.lower() or 'technology' in prompt.lower():
        # Enhance for tech content
        prompt += ", modern, innovative, clean design, corporate aesthetic"

    # Ensure prompt doesn't exceed Imagen's 480 token limit
    if len(prompt) > 400:  # Leave some buffer
        prompt = prompt[:400] + "..."

    return prompt

# Strategy for generating prompts
def prompt_strategy():
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=1,
        max_size=500
    ).map(lambda s: s.replace('\x00', ''))  # Remove null characters

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(prompt=prompt_strategy())
@example(prompt="")
@example(prompt="professional linkedin profile")
@example(prompt="digital transformation in technology")
@example(prompt="\n\nEnhanced prompt: test\n\nAspect ratio: 16:9")
@example(prompt="a" * 500)
def test_optimize_prompt_for_imagen(prompt: str):
    global stop_collecting
    if stop_collecting:
        return
    
    prompt_copy = copy.deepcopy(prompt)
    try:
        expected = _optimize_prompt_for_imagen(prompt_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter to prioritize meaningful cases
    if (
        '\n\nEnhanced prompt:' in prompt or
        '\n\nAspect ratio:' in prompt or
        'professional' in prompt.lower() and 'linkedin' in prompt.lower() or
        'digital transformation' in prompt.lower() or 'technology' in prompt.lower() or
        len(prompt) > 400
    ):
        generated_cases.append({
            "Inputs": {"prompt": prompt},
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