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
def find_box(pred_str: str):
    ans = pred_str.split("boxed")[-1]
    if not ans:
        return ""
    if ans[0] == "{":
        stack = 1
        a = ""
        for c in ans[1:]:
            if c == "{":
                stack += 1
                a += c
            elif c == "}":
                stack -= 1
                if stack == 0:
                    break
                a += c
            else:
                a += c
    else:
        a = ans.split("$")[0].strip()
    return a

# Strategy for generating pred_str
def pred_str_strategy():
    return st.one_of([
        # Case 1: Empty string
        st.just(""),
        # Case 2: String with "boxed" followed by a JSON-like object
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=20),
            st.just("boxed"),
            st.recursive(
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=10),
                lambda children: st.dictionaries(
                    st.text(st.characters(whitelist_categories=('L', 'N')), max_size=5),
                    children,
                    max_size=3
                ),
                max_leaves=3
            ).map(lambda x: "{" + json.dumps(x) + "}")
        ).map(lambda x: "".join(x)),
        # Case 3: String with "boxed" followed by a non-JSON-like object
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=20),
            st.just("boxed"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.just("$"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=20)
        ).map(lambda x: "".join(x)),
        # Case 4: String without "boxed"
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(pred_str=pred_str_strategy())
@example(pred_str="")
@example(pred_str="boxed{key: value}")
@example(pred_str="boxed$value")
@example(pred_str="boxed{key: {nested: value}}")
@example(pred_str="boxed value$")
@example(pred_str="boxed value")
def test_find_box(pred_str: str):
    global stop_collecting
    if stop_collecting:
        return
    
    pred_str_copy = copy.deepcopy(pred_str)
    try:
        expected = find_box(pred_str_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "boxed" in pred_str or not pred_str:
        generated_cases.append({
            "Inputs": {"pred_str": pred_str},
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