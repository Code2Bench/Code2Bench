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
def remove_binary_diffs(patch_text):
    """
    Remove binary file diffs from a git patch.

    Args:
        patch_text (str): The git patch text

    Returns:
        str: The cleaned patch text with binary diffs removed
    """
    lines = patch_text.splitlines()
    cleaned_lines = []
    block = []
    is_binary_block = False

    for line in lines:
        if line.startswith('diff --git '):
            if block and not is_binary_block:
                cleaned_lines.extend(block)
            block = [line]
            is_binary_block = False
        elif 'Binary files' in line:
            is_binary_block = True
            block.append(line)
        else:
            block.append(line)

    if block and not is_binary_block:
        cleaned_lines.extend(block)
    return '\n'.join(cleaned_lines)

# Strategy for generating git patch text
def patch_text_strategy():
    return st.lists(
        st.one_of([
            st.just("diff --git a/file1 b/file1"),
            st.just("Binary files a/file1 and b/file1 differ"),
            st.just("--- a/file1"),
            st.just("+++ b/file1"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
        ]),
        min_size=1,
        max_size=20
    ).map(lambda lines: '\n'.join(lines))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(patch_text=patch_text_strategy())
@example(patch_text="diff --git a/file1 b/file1\nBinary files a/file1 and b/file1 differ")
@example(patch_text="diff --git a/file1 b/file1\n--- a/file1\n+++ b/file1")
@example(patch_text="diff --git a/file1 b/file1\nBinary files a/file1 and b/file1 differ\ndiff --git a/file2 b/file2\n--- a/file2\n+++ b/file2")
@example(patch_text="diff --git a/file1 b/file1\nSome other line 1\nBinary files a/file1 and b/file1 differ")
def test_remove_binary_diffs(patch_text):
    global stop_collecting
    if stop_collecting:
        return
    
    patch_text_copy = copy.deepcopy(patch_text)
    try:
        expected = remove_binary_diffs(patch_text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if 'Binary files' in patch_text or 'diff --git' in patch_text:
        generated_cases.append({
            "Inputs": {"patch_text": patch_text},
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