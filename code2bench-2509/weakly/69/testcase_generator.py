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
def format_diff_message(optim_text: str, incr_text: str) -> str:
    """Creates a detailed diff message between two texts."""
    diff: list[str] = list(difflib.ndiff(optim_text.splitlines(), incr_text.splitlines()))

    # Collect differences
    only_in_optim: list[str] = []
    only_in_incr: list[str] = []

    for line in diff:
        if line.startswith("- "):
            only_in_optim.append(line[2:])
        elif line.startswith("+ "):
            only_in_incr.append(line[2:])

    message: list[str] = []
    if only_in_optim:
        message.append("\nOnly in optimized prompt:")
        message.extend(f"  {line}" for line in only_in_optim)

    if only_in_incr:
        message.append("\nOnly in incremental prompt:")
        message.extend(f"  {line}" for line in only_in_incr)

    return "\n".join(message)

# Strategy for generating text inputs
def text_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), min_codepoint=32, max_codepoint=126),
        min_size=0, max_size=100
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    optim_text=text_strategy(),
    incr_text=text_strategy()
)
@example(optim_text="", incr_text="")
@example(optim_text="line1\nline2", incr_text="line1\nline2")
@example(optim_text="line1\nline2", incr_text="line1\nline3")
@example(optim_text="line1\nline2", incr_text="line3\nline4")
@example(optim_text="line1\nline2\nline3", incr_text="line1\nline3")
def test_format_diff_message(optim_text: str, incr_text: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    optim_text_copy = copy.deepcopy(optim_text)
    incr_text_copy = copy.deepcopy(incr_text)

    # Call func0 to verify input validity
    try:
        expected = format_diff_message(optim_text_copy, incr_text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "optim_text": optim_text_copy,
            "incr_text": incr_text_copy
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