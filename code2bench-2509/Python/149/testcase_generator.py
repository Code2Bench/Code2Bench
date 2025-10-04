from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def format_timer(secs):
    ''' secs --> 4.5 days/hrs/mins/secs '''

    try:
        if secs < 1:
            return '0 secs'

        if secs >= 86400:
            time_str = f"{secs/86400:.1f} days"
        elif secs < 60:
            time_str = f"{secs:.0f} secs"
        elif secs < 3600:
            time_str = f"{secs/60:.0f} mins"
        elif secs == 3600:
            time_str = "1 hr"
        else:
            time_str = f"{secs/3600:.1f} hrs"

        # change xx.0 min/hr --> xx min/hr
        time_str = time_str.replace('.0 ', ' ')
        if time_str == '1 mins': time_str = '1 min'

    except Exception as err:
        #_LOGGER.exception(err)
        time_str = ''

    return time_str

# Strategy for generating seconds
seconds_strategy = st.one_of([
    st.floats(min_value=0, max_value=86400 * 2, allow_nan=False, allow_infinity=False),
    st.integers(min_value=0, max_value=86400 * 2)
])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(secs=seconds_strategy)
@example(secs=0)
@example(secs=0.5)
@example(secs=1)
@example(secs=59)
@example(secs=60)
@example(secs=61)
@example(secs=3599)
@example(secs=3600)
@example(secs=3601)
@example(secs=86399)
@example(secs=86400)
@example(secs=86401)
def test_format_timer(secs):
    global stop_collecting
    if stop_collecting:
        return
    
    try:
        expected = format_timer(secs)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"secs": secs},
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