from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import Dict  # Import Dict from typing

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def convert_str_cookie_to_dict(cookie_str: str) -> Dict:
    cookie_dict: Dict[str, str] = dict()
    if not cookie_str:
        return cookie_dict
    for cookie in cookie_str.split(";"):
        cookie = cookie.strip()
        if not cookie:
            continue
        cookie_list = cookie.split("=")
        if len(cookie_list) != 2:
            continue
        cookie_value = cookie_list[1]
        if isinstance(cookie_value, list):
            cookie_value = "".join(cookie_value)
        cookie_dict[cookie_list[0]] = cookie_value
    return cookie_dict

# Strategy for generating cookie strings
def cookie_str_strategy():
    # Generate valid cookie key-value pairs
    key = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='-_'),
        min_size=1, max_size=10
    )
    value = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='-_'),
        min_size=0, max_size=10
    )
    cookie_pair = st.builds(lambda k, v: f"{k}={v}", key, value)
    
    # Generate a list of cookie pairs separated by semicolons
    return st.lists(cookie_pair, min_size=0, max_size=5).map(lambda x: ";".join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(cookie_str=cookie_str_strategy())
@example(cookie_str="")
@example(cookie_str="key1=value1")
@example(cookie_str="key1=value1;key2=value2")
@example(cookie_str="key1=value1;key2=value2;key3=value3")
@example(cookie_str="key1=value1;key2=value2;key3=value3;key4=value4")
@example(cookie_str="key1=value1;key2=value2;key3=value3;key4=value4;key5=value5")
def test_convert_str_cookie_to_dict(cookie_str: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    cookie_str_copy = copy.deepcopy(cookie_str)

    # Call func0 to verify input validity
    try:
        expected = convert_str_cookie_to_dict(cookie_str_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "cookie_str": cookie_str_copy
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