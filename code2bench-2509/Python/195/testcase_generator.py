from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import Dict

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _rule_based_analysis(previous_text: str, current_text: str) -> Dict[str, float]:
    flow = 0.6
    consistency = 0.6
    progression = 0.6

    if previous_text and previous_text[-1] in ".!?":
        flow += 0.1
    if any(k in current_text.lower() for k in ["therefore", "next", "building on", "as a result", "furthermore", "additionally"]):
        progression += 0.2
    if len(current_text.split()) > 120:
        consistency += 0.1
    if any(k in current_text.lower() for k in ["however", "but", "although", "despite"]):
        flow += 0.1

    return {
        "flow": min(flow, 1.0),
        "consistency": min(consistency, 1.0),
        "progression": min(progression, 1.0),
    }

# Strategy for generating text inputs
def text_strategy():
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=1,
        max_size=200
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(previous_text=text_strategy(), current_text=text_strategy())
@example(previous_text="This is a sentence.", current_text="Therefore, we can conclude.")
@example(previous_text="", current_text="Building on this idea, we proceed.")
@example(previous_text="Previous text.", current_text="However, there are exceptions.")
@example(previous_text="Short.", current_text="A very long text " * 30)
@example(previous_text="Ends with question?", current_text="Next, we discuss the results.")
def test_rule_based_analysis(previous_text: str, current_text: str):
    global stop_collecting
    if stop_collecting:
        return

    previous_text_copy = copy.deepcopy(previous_text)
    current_text_copy = copy.deepcopy(current_text)
    try:
        expected = _rule_based_analysis(previous_text_copy, current_text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Filter to prioritize meaningful cases
    if (
        previous_text and previous_text[-1] in ".!?" or
        any(k in current_text.lower() for k in ["therefore", "next", "building on", "as a result", "furthermore", "additionally"]) or
        len(current_text.split()) > 120 or
        any(k in current_text.lower() for k in ["however", "but", "although", "despite"])
    ):
        generated_cases.append({
            "Inputs": {"previous_text": previous_text, "current_text": current_text},
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