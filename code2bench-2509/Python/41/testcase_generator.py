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
def create_chunks(text: str, n: int) -> List[str]:
    r"""Returns successive n-sized chunks from provided text. Split a text
    into smaller chunks of size n".

    Args:
        text (str): The text to be split.
        n (int): The max length of a single chunk.

    Returns:
        List[str]: A list of split texts.
    """

    chunks = []
    i = 0
    while i < len(text):
        # Find the nearest end of sentence within a range of 0.5 * n
        # and 1.5 * n tokens
        j = min(i + int(1.2 * n), len(text))
        while j > i + int(0.8 * n):
            # Decode the tokens and check for full stop or newline
            chunk = text[i:j]
            if chunk.endswith(".") or chunk.endswith("\n"):
                break
            j -= 1
        # If no end of sentence found, use n tokens as the chunk size
        if j == i + int(0.8 * n):
            j = min(i + n, len(text))
        chunks.append(text[i:j])
        i = j
    return chunks

# Strategy for generating text
def text_strategy():
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=1,
        max_size=1000
    )

# Strategy for generating chunk size
def chunk_size_strategy():
    return st.integers(min_value=1, max_value=100)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy(), n=chunk_size_strategy())
@example(text="This is a test.", n=5)
@example(text="This is a test.\nAnother line.", n=10)
@example(text="This is a test. Another sentence.", n=15)
@example(text="This is a test without any punctuation", n=10)
@example(text="", n=5)
def test_create_chunks(text: str, n: int):
    global stop_collecting
    if stop_collecting:
        return
    
    text_copy = copy.deepcopy(text)
    try:
        expected = create_chunks(text_copy, n)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter to prioritize meaningful cases
    if len(text) > 0 and n > 0:
        generated_cases.append({
            "Inputs": {"text": text, "n": n},
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