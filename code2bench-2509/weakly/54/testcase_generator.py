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
def validate_channel_info(channel_info: Dict) -> Tuple[bool, str]:
    """Validate channel information before processing."""
    required_fields = ['channel_name', 'channel_niche', 'target_audience', 'key_topics', 'unique_points']

    # Check for missing required fields
    for field in required_fields:
        if not channel_info.get(field):
            return False, f"Missing required field: {field}"

    # Validate field lengths
    if len(channel_info['channel_name']) < 3:
        return False, "Channel name must be at least 3 characters long"

    if len(channel_info['target_audience']) < 10:
        return False, "Target audience description must be at least 10 characters long"

    if len(channel_info['key_topics']) < 10:
        return False, "Key topics must be at least 10 characters long"

    if len(channel_info['unique_points']) < 10:
        return False, "Unique selling points must be at least 10 characters long"

    return True, ""

# Strategies for generating inputs
def channel_info_strategy():
    return st.fixed_dictionaries({
        'channel_name': st.text(min_size=0, max_size=20),
        'channel_niche': st.text(min_size=0, max_size=20),
        'target_audience': st.text(min_size=0, max_size=20),
        'key_topics': st.text(min_size=0, max_size=20),
        'unique_points': st.text(min_size=0, max_size=20)
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(channel_info=channel_info_strategy())
@example(channel_info={'channel_name': '', 'channel_niche': '', 'target_audience': '', 'key_topics': '', 'unique_points': ''})
@example(channel_info={'channel_name': 'ab', 'channel_niche': 'tech', 'target_audience': 'tech enthusiasts', 'key_topics': 'AI, ML, Data Science', 'unique_points': 'In-depth analysis'})
@example(channel_info={'channel_name': 'TechChannel', 'channel_niche': 'tech', 'target_audience': 'tech enthusiasts', 'key_topics': 'AI, ML, Data Science', 'unique_points': 'In-depth analysis'})
@example(channel_info={'channel_name': 'TechChannel', 'channel_niche': 'tech', 'target_audience': 'tech enthusiasts', 'key_topics': 'AI, ML, Data Science', 'unique_points': 'In-depth analysis'})
@example(channel_info={'channel_name': 'TechChannel', 'channel_niche': 'tech', 'target_audience': 'tech enthusiasts', 'key_topics': 'AI, ML, Data Science', 'unique_points': 'In-depth analysis'})
def test_validate_channel_info(channel_info: Dict):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    channel_info_copy = copy.deepcopy(channel_info)

    # Call func0 to verify input validity
    try:
        result, message = validate_channel_info(channel_info_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": channel_info_copy
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