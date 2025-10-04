from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import Dict, Tuple

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def validate_script(script: Dict) -> Tuple[bool, str]:
    """Validate the generated script."""
    required_sections = ['hook', 'introduction', 'showcase', 'value_proposition', 'call_to_action']

    # Check for missing sections
    for section in required_sections:
        if section not in script:
            return False, f"Missing required section: {section}"

    # Validate section content
    for section, content in script.items():
        if not content.get('text'):
            return False, f"Missing text in section: {section}"
        if not content.get('duration'):
            return False, f"Missing duration in section: {section}"

    # Validate total duration
    total_duration = sum(float(content['duration'].split()[0]) for content in script.values())
    if total_duration > 90:  # 90 seconds max
        return False, f"Total duration ({total_duration}s) exceeds maximum allowed (90s)"

    return True, ""

# Strategies for generating inputs
def text_strategy():
    return st.text(min_size=1, max_size=100)

def duration_strategy():
    return st.floats(min_value=0.1, max_value=90.0).map(lambda x: f"{x:.1f}s")

def section_strategy():
    return st.fixed_dictionaries({
        'text': text_strategy(),
        'duration': duration_strategy()
    })

def script_strategy():
    return st.dictionaries(
        keys=st.sampled_from(['hook', 'introduction', 'showcase', 'value_proposition', 'call_to_action']),
        values=section_strategy(),
        min_size=5,
        max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(script=script_strategy())
@example(script={
    'hook': {'text': 'Welcome!', 'duration': '10.0s'},
    'introduction': {'text': 'This is an introduction.', 'duration': '20.0s'},
    'showcase': {'text': 'Here is our showcase.', 'duration': '30.0s'},
    'value_proposition': {'text': 'Our value proposition.', 'duration': '20.0s'},
    'call_to_action': {'text': 'Call to action!', 'duration': '10.0s'}
})
@example(script={
    'hook': {'text': 'Hi!', 'duration': '5.0s'},
    'introduction': {'text': 'Intro.', 'duration': '10.0s'},
    'showcase': {'text': 'Showcase.', 'duration': '15.0s'},
    'value_proposition': {'text': 'Value.', 'duration': '10.0s'},
    'call_to_action': {'text': 'Action!', 'duration': '5.0s'}
})
@example(script={
    'hook': {'text': 'Hello!', 'duration': '1.0s'},
    'introduction': {'text': 'Introduction.', 'duration': '1.0s'},
    'showcase': {'text': 'Showcase.', 'duration': '1.0s'},
    'value_proposition': {'text': 'Value.', 'duration': '1.0s'},
    'call_to_action': {'text': 'Action!', 'duration': '1.0s'}
})
def test_validate_script(script: Dict):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    script_copy = copy.deepcopy(script)

    # Call func0 to verify input validity
    try:
        expected = validate_script(script_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "script": script_copy
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