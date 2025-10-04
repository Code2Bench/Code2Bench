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
def chunk_sentences(
    sentences: List[str], max_chunk_size: int, overlap_sentences: int
) -> List[str]:
    """
    Helper to group sentences into chunks with overlap.
    """
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sep = " " if current_chunk else ""
        new_length = current_length + len(sep) + len(sentence)
        if new_length > max_chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            overlap = current_chunk[-overlap_sentences:] if overlap_sentences else []
            current_chunk = overlap + [sentence]
            current_length = sum(len(s) for s in current_chunk) + len(current_chunk) - 1
        else:
            current_chunk.append(sentence)
            current_length = new_length
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

# Strategy for generating sentences
def sentence_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    sentences=st.lists(sentence_strategy(), min_size=1, max_size=20),
    max_chunk_size=st.integers(min_value=1, max_value=1000),
    overlap_sentences=st.integers(min_value=0, max_value=10)
)
@example(sentences=["a"], max_chunk_size=1, overlap_sentences=0)
@example(sentences=["a", "b"], max_chunk_size=1, overlap_sentences=1)
@example(sentences=["a", "b", "c"], max_chunk_size=10, overlap_sentences=2)
@example(sentences=["a" * 100], max_chunk_size=50, overlap_sentences=0)
@example(sentences=["a", "b", "c"], max_chunk_size=100, overlap_sentences=0)
@example(sentences=["a", "b", "c"], max_chunk_size=100, overlap_sentences=3)
def test_chunk_sentences(sentences: List[str], max_chunk_size: int, overlap_sentences: int):
    global stop_collecting
    if stop_collecting:
        return
    
    sentences_copy = copy.deepcopy(sentences)
    try:
        expected = chunk_sentences(sentences_copy, max_chunk_size, overlap_sentences)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if len(sentences) > 1 or max_chunk_size < sum(len(s) for s in sentences) or overlap_sentences > 0:
        generated_cases.append({
            "Inputs": {"sentences": sentences, "max_chunk_size": max_chunk_size, "overlap_sentences": overlap_sentences},
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