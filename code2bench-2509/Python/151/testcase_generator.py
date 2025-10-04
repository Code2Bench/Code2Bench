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
def time_str_to_secs(time_str=None) -> int:
    ''' 20 sec/min/hrs --> secs '''

    if time_str is None or time_str == "": return 0

    try:
        s1 = str(time_str).replace('_', ' ') + " min"
        time_part = float((s1.split(" ")[0]))
        text_part = s1.split(" ")[1]

        if text_part in ('sec', 'secs'):
            secs = time_part
        elif text_part in ('min', 'mins'):
            secs = time_part * 60
        elif text_part in ('hr', 'hrs'):
            secs = time_part * 3600
        else:
            secs = 0

        if secs < 0: secs = 0

    except:
        secs = 0

    return secs

# Strategy for generating time strings
def time_str_strategy():
    return st.one_of([
        st.just(None),
        st.just(""),
        st.tuples(
            st.floats(allow_nan=False, allow_infinity=False, min_value=-1000, max_value=1000),
            st.one_of([st.just("sec"), st.just("secs"), st.just("min"), st.just("mins"), st.just("hr"), st.just("hrs"), st.just("invalid")])
        ).map(lambda x: f"{x[0]} {x[1]}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(time_str=time_str_strategy())
@example(time_str=None)
@example(time_str="")
@example(time_str="20 sec")
@example(time_str="30 min")
@example(time_str="2 hrs")
@example(time_str="-10 sec")
@example(time_str="invalid")
@example(time_str="20_sec")
def test_time_str_to_secs(time_str):
    global stop_collecting
    if stop_collecting:
        return
    
    time_str_copy = copy.deepcopy(time_str)
    try:
        expected = time_str_to_secs(time_str_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"time_str": time_str},
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