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
def _clean_content(content: str) -> str:
    # Remove excessive whitespace
    lines = content.split('\n')
    cleaned_lines = []

    for line in lines:
        # Remove trailing whitespace
        line = line.rstrip()
        cleaned_lines.append(line)

    # Remove empty lines at the beginning and end
    while cleaned_lines and not cleaned_lines[0].strip():
        cleaned_lines.pop(0)

    while cleaned_lines and not cleaned_lines[-1].strip():
        cleaned_lines.pop()

    return '\n'.join(cleaned_lines)

# Strategy for generating content strings
def content_strategy():
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z', 'Zs')),
        min_size=0,
        max_size=100
    ).map(lambda s: s.replace('\r', ''))  # Ensure no carriage returns

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(content=content_strategy())
@example(content="")
@example(content="   ")
@example(content="\n\n\n")
@example(content="  line1  \n  line2  \n  line3  ")
@example(content="  line1  \n\n  line2  \n\n  line3  ")
@example(content="\n  line1  \n  line2  \n  line3  \n")
@example(content="  line1  \n  line2  \n  line3  \n\n")
def test_clean_content(content: str):
    global stop_collecting
    if stop_collecting:
        return
    
    content_copy = copy.deepcopy(content)
    try:
        expected = _clean_content(content_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter to prioritize meaningful cases
    if any(line.strip() for line in content.split('\n')) or not content.strip():
        generated_cases.append({
            "Inputs": {"content": content},
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