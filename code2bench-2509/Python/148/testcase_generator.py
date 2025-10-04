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
def time_to_24hrtime(hhmmss):
    ''' (h)h:mm:ssa or (h)h:mm:ssp --> hh:mm:ss '''

    hhmm_colon = hhmmss.find(':')
    if hhmm_colon == -1: return hhmmss

    ap = hhmmss[-1].lower()                # Get last character of time (#, a, p).lower()
    if ap not in ['a', 'p']:
        return hhmmss

    hh = int(hhmmss[:hhmm_colon])
    if hh == 12 and ap == 'a':
        hh = 0
    elif hh <= 11 and ap == 'p':
        hh += 12

    hhmmss24 = f"{hh:0>2}{hhmmss[hhmm_colon:-1]}"

    return hhmmss24

# Strategy for generating time strings
def time_strategy():
    return st.one_of([
        # Valid 12-hour format with 'a' or 'p'
        st.tuples(
            st.integers(min_value=1, max_value=12),
            st.just(":"),
            st.integers(min_value=0, max_value=59),
            st.just(":"),
            st.integers(min_value=0, max_value=59),
            st.one_of([st.just("a"), st.just("p")])
        ).map(lambda x: f"{x[0]}{x[1]}{x[2]:02}{x[3]}{x[4]:02}{x[5]}"),
        # Invalid format (missing colon)
        st.text(st.characters(min_codepoint=48, max_codepoint=122), min_size=1, max_size=8),
        # Invalid format (missing 'a' or 'p')
        st.tuples(
            st.integers(min_value=1, max_value=12),
            st.just(":"),
            st.integers(min_value=0, max_value=59),
            st.just(":"),
            st.integers(min_value=0, max_value=59),
            st.text(st.characters(min_codepoint=48, max_codepoint=122), min_size=1, max_size=1)
        ).map(lambda x: f"{x[0]}{x[1]}{x[2]:02}{x[3]}{x[4]:02}{x[5]}")
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(hhmmss=time_strategy())
@example(hhmmss="12:00:00a")
@example(hhmmss="12:00:00p")
@example(hhmmss="11:59:59a")
@example(hhmmss="11:59:59p")
@example(hhmmss="1:00:00a")
@example(hhmmss="1:00:00p")
@example(hhmmss="invalid")
@example(hhmmss="12345678")
def test_time_to_24hrtime(hhmmss):
    global stop_collecting
    if stop_collecting:
        return
    
    hhmmss_copy = copy.deepcopy(hhmmss)
    try:
        expected = time_to_24hrtime(hhmmss_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if ":" in hhmmss and hhmmss[-1].lower() in ['a', 'p']:
        generated_cases.append({
            "Inputs": {"hhmmss": hhmmss},
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