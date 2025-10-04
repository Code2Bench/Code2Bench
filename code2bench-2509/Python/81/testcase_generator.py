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
def group_sentences(corrected_srt, threshold=1.0):
    """按时间间隔分句"""
    if not corrected_srt:
        return []
    sentences = []
    current_sentence = [corrected_srt[0]]
    for i in range(1, len(corrected_srt)):
        prev_end = corrected_srt[i-1]["end"]
        curr_start = corrected_srt[i]["start"]
        if curr_start - prev_end > threshold:
            sentences.append(current_sentence)
            current_sentence = [corrected_srt[i]]
        else:
            current_sentence.append(corrected_srt[i])
    sentences.append(current_sentence)
    return sentences

# Strategy for generating corrected_srt entries
def srt_entry_strategy():
    return st.fixed_dictionaries({
        "start": st.floats(min_value=0.0, allow_nan=False, allow_infinity=False),
        "end": st.floats(min_value=0.0, allow_nan=False, allow_infinity=False)
    }).filter(lambda x: x["end"] >= x["start"])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    corrected_srt=st.lists(srt_entry_strategy(), min_size=0, max_size=20),
    threshold=st.floats(min_value=0.0, allow_nan=False, allow_infinity=False)
)
@example(corrected_srt=[], threshold=1.0)
@example(corrected_srt=[{"start": 0.0, "end": 1.0}], threshold=1.0)
@example(corrected_srt=[{"start": 0.0, "end": 1.0}, {"start": 1.5, "end": 2.5}], threshold=1.0)
@example(corrected_srt=[{"start": 0.0, "end": 1.0}, {"start": 1.1, "end": 2.0}], threshold=1.0)
@example(corrected_srt=[{"start": 0.0, "end": 1.0}, {"start": 1.0, "end": 2.0}], threshold=1.0)
def test_group_sentences(corrected_srt, threshold):
    global stop_collecting
    if stop_collecting:
        return
    
    corrected_srt_copy = copy.deepcopy(corrected_srt)
    try:
        expected = group_sentences(corrected_srt_copy, threshold)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if len(corrected_srt) > 1 or not corrected_srt:
        generated_cases.append({
            "Inputs": {"corrected_srt": corrected_srt, "threshold": threshold},
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