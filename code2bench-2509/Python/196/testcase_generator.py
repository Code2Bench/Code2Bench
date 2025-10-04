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
def _heuristic_transition(previous_text: str, current_heading: str) -> str:
    tail = previous_text[-240:]
    if any(word in tail.lower() for word in ["problem", "issue", "challenge"]):
        return f"Now that we've identified the challenges, let's explore {current_heading.lower()} to find solutions."
    elif any(word in tail.lower() for word in ["solution", "approach", "method"]):
        return f"Building on this approach, {current_heading.lower()} provides the next step in our analysis."
    elif any(word in tail.lower() for word in ["important", "crucial", "essential"]):
        return f"Given this importance, {current_heading.lower()} becomes our next focus area."
    else:
        return (
            f"Building on the discussion above, this leads us into {current_heading.lower()}, "
            f"where we focus on practical implications and what to do next."
        )

# Strategy for generating previous_text
def previous_text_strategy():
    keywords = ["problem", "issue", "challenge", "solution", "approach", "method", "important", "crucial", "essential"]
    return st.one_of([
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=500).filter(
            lambda x: any(word in x.lower() for word in keywords)
        ),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=500).filter(
            lambda x: not any(word in x.lower() for word in keywords)
        )
    ])

# Strategy for generating current_heading
def current_heading_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(previous_text=previous_text_strategy(), current_heading=current_heading_strategy())
@example(previous_text="This is a problem we need to solve.", current_heading="Solutions")
@example(previous_text="Our approach is innovative.", current_heading="Next Steps")
@example(previous_text="This is crucial for success.", current_heading="Implementation")
@example(previous_text="This is a generic discussion.", current_heading="Conclusion")
def test_heuristic_transition(previous_text: str, current_heading: str):
    global stop_collecting
    if stop_collecting:
        return
    
    previous_text_copy = copy.deepcopy(previous_text)
    current_heading_copy = copy.deepcopy(current_heading)
    try:
        expected = _heuristic_transition(previous_text_copy, current_heading_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"previous_text": previous_text, "current_heading": current_heading},
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