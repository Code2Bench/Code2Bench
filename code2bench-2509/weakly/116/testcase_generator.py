from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from configparser import ConfigParser
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
def entry_points(text: str, text_source="entry-points") -> dict[str, dict]:
    """Given the contents of entry-points file,
    process it into a 2-level dictionary (``dict[str, dict[str, str]]``).
    The first level keys are entry-point groups, the second level keys are
    entry-point names, and the second level values are references to objects
    (that correspond to the entry-point value).
    """
    parser = ConfigParser(default_section=None, delimiters=("=",))  # type: ignore
    parser.optionxform = str  # case sensitive
    parser.read_string(text, text_source)
    groups = {k: dict(v.items()) for k, v in parser.items()}
    groups.pop(parser.default_section, None)
    return groups

# Strategy for generating valid entry-points text
def entry_points_text_strategy():
    # Generate valid section names
    section_name = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S'), whitelist_characters='_-'),
        min_size=1, max_size=10
    ).filter(lambda x: x.strip() and not x.startswith('[') and not x.endswith(']'))
    
    # Generate valid key-value pairs
    key = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S'), whitelist_characters='_-'),
        min_size=1, max_size=10
    ).filter(lambda x: x.strip())
    value = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S'), whitelist_characters='_-'),
        min_size=1, max_size=10
    ).filter(lambda x: x.strip())
    key_value_pair = st.tuples(key, value).map(lambda x: f"{x[0]}={x[1]}")
    
    # Generate sections with key-value pairs
    section = st.lists(
        key_value_pair,
        min_size=1, max_size=5
    ).map(lambda x: '\n'.join(x))
    
    # Combine sections into a valid entry-points text
    return st.lists(
        st.tuples(section_name, section),
        min_size=1, max_size=3
    ).map(lambda x: '\n'.join([f"[{s[0]}]\n{s[1]}" for s in x]))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=entry_points_text_strategy())
@example(text="")
@example(text="[group1]\nkey1=value1")
@example(text="[group1]\nkey1=value1\nkey2=value2\n[group2]\nkey3=value3")
@example(text="[group1]\nkey1=value1\n[group2]\nkey2=value2\n[group3]\nkey3=value3")
def test_entry_points(text: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    text_copy = copy.deepcopy(text)

    # Call func0 to verify input validity
    try:
        expected = entry_points(text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "text": text_copy
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