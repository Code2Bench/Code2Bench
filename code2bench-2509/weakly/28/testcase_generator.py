from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import re
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
def extract_answer_obj(s: str):
    if "<|begin_of_box|>" not in s or "<|end_of_box|>" not in s:
        return None
    try:
        res = s.split("<|begin_of_box|>")[1].split("<|end_of_box|>")[0].strip()

        # Processing leading zeros if any
        ptn = r"\[\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]\]"
        m = re.search(ptn, res)
        if m:
            old_str = m.group(0)
            v1 = int(m.group(1))
            v2 = int(m.group(2))
            v3 = int(m.group(3))
            v4 = int(m.group(4))
            new_str = f"[[{v1},{v2},{v3},{v4}]]"
            res = res.replace(old_str, new_str)
        try:
            return json.loads(res)
        except:
            return eval(res, {"true": True, "false": False, "null": None})
    except:
        return None

# Strategy for generating strings with potential JSON-like content
def json_like_strategy():
    return st.one_of(
        st.just("true"),
        st.just("false"),
        st.just("null"),
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.lists(st.one_of(st.integers(), st.floats(allow_nan=False, allow_infinity=False)), max_size=5),
        st.dictionaries(st.text(min_size=1, max_size=5), st.one_of(st.integers(), st.floats(allow_nan=False, allow_infinity=False)), max_size=5)
    )

# Strategy for generating strings with the required markers and JSON-like content
def s_strategy():
    return st.builds(
        lambda x: f"<|begin_of_box|>{x}<|end_of_box|>",
        json_like_strategy()
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(s=s_strategy())
@example(s="<|begin_of_box|>[[1, 2, 3, 4]]<|end_of_box|>")
@example(s="<|begin_of_box|>[[ 1, 2, 3, 4 ]]<|end_of_box|>")
@example(s="<|begin_of_box|>true<|end_of_box|>")
@example(s="<|begin_of_box|>false<|end_of_box|>")
@example(s="<|begin_of_box|>null<|end_of_box|>")
@example(s="<|begin_of_box|>123<|end_of_box|>")
@example(s="<|begin_of_box|>1.23<|end_of_box|>")
@example(s="<|begin_of_box|>[1, 2, 3]<|end_of_box|>")
@example(s="<|begin_of_box|>{\"a\": 1}<|end_of_box|>")
@example(s="<|begin_of_box|><|end_of_box|>")
@example(s="invalid string")
def test_extract_answer_obj(s: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    s_copy = copy.deepcopy(s)

    # Call func0 to verify input validity
    try:
        expected = extract_answer_obj(s_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "s": s_copy
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