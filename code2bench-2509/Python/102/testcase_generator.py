from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Any, Dict
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
def display_desc_to_display_path(display_desc: Dict[str, Any]) -> str:
    uri = ""
    path = display_desc.get("path")
    if path:
        uri += path
    display = display_desc.get("display")
    if display:
        if path:
            uri += "#"
        uri += display.lstrip(":")
    options_str = display_desc.get("options_str")
    if options_str:
        uri += f"?{options_str}"
    return uri

# Strategy for generating display_desc dictionaries
def display_desc_strategy():
    return st.fixed_dictionaries({
        "path": st.one_of(st.none(), st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=20)),
        "display": st.one_of(st.none(), st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=20)),
        "options_str": st.one_of(st.none(), st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=20))
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(display_desc=display_desc_strategy())
@example(display_desc={"path": None, "display": None, "options_str": None})
@example(display_desc={"path": "example_path", "display": None, "options_str": None})
@example(display_desc={"path": None, "display": ":example_display", "options_str": None})
@example(display_desc={"path": None, "display": None, "options_str": "example_options"})
@example(display_desc={"path": "example_path", "display": ":example_display", "options_str": None})
@example(display_desc={"path": "example_path", "display": None, "options_str": "example_options"})
@example(display_desc={"path": None, "display": ":example_display", "options_str": "example_options"})
@example(display_desc={"path": "example_path", "display": ":example_display", "options_str": "example_options"})
def test_display_desc_to_display_path(display_desc: Dict[str, Any]):
    global stop_collecting
    if stop_collecting:
        return
    
    display_desc_copy = copy.deepcopy(display_desc)
    try:
        expected = display_desc_to_display_path(display_desc_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(display_desc.values()):  # Only add cases with at least one non-None value
        generated_cases.append({
            "Inputs": {"display_desc": display_desc},
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