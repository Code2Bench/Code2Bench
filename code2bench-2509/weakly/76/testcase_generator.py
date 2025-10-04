from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import base64
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
def voe_decode(ct, luts):
    lut = [''.join([('\\' + x) if x in '.*+?^${}()|[]\\' else x for x in i]) for i in luts[2:-2].split("','")]
    txt = ''
    for i in ct:
        x = ord(i)
        if 64 < x < 91:
            x = (x - 52) % 26 + 65
        elif 96 < x < 123:
            x = (x - 84) % 26 + 97
        txt += chr(x)
    for i in lut:
        txt = re.sub(i, '', txt)
    ct = base64.b64decode(txt)
    txt = ''.join([chr(i - 3) for i in ct])
    txt = base64.b64decode(txt[::-1])
    return json.loads(txt)

# Strategies for generating inputs
def ct_strategy():
    return st.text(
        alphabet=st.characters(min_codepoint=65, max_codepoint=122, whitelist_categories=('L',)),
        min_size=1,
        max_size=100
    )

def luts_strategy():
    return st.lists(
        st.text(
            alphabet=st.characters(min_codepoint=32, max_codepoint=126, whitelist_categories=('L', 'N', 'P', 'S')),
            min_size=1,
            max_size=10
        ),
        min_size=1,
        max_size=10
    ).map(lambda x: "['" + "','".join(x) + "']")

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    ct=ct_strategy(),
    luts=luts_strategy()
)
@example(
    ct="abc",
    luts="['a','b','c']"
)
@example(
    ct="XYZ",
    luts="['X','Y','Z']"
)
@example(
    ct="aBcXyZ",
    luts="['a','B','c','X','y','Z']"
)
def test_voe_decode(ct: str, luts: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    ct_copy = copy.deepcopy(ct)
    luts_copy = copy.deepcopy(luts)

    # Call func0 to verify input validity
    try:
        expected = voe_decode(ct_copy, luts_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "ct": ct_copy,
            "luts": luts_copy
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