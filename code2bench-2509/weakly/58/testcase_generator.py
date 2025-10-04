from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import json
import os
import atexit
import copy
from typing import Optional

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _parsing_score(grade_stdout: str) -> Optional[float]:
    for line in grade_stdout.splitlines():
        line = line.strip()
        if "score" not in line:
            continue
        m = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", line)
        if not m:
            continue
        json_str = m.group(0)
        try:
            # Priority 1: JSON parsing
            return float(json.loads(json_str)["score"])
        except:
            pass
        try:
            # Priority 2: Eval dict
            return float(eval(json_str)["score"])
        except:
            pass
        try:
            # Priority 3: Regex for the last number in the string
            return float(re.findall(r"[-+]?\d*\.\d+|\d+", json_str)[-1])
        except:
            pass
    return None

# Strategy for generating grade_stdout
def grade_stdout_strategy():
    # Generate lines with potential JSON-like structures
    json_like = st.one_of(
        st.builds(
            lambda score: f'{{"score": {score}}}',
            st.floats(allow_nan=False, allow_infinity=False)
        ),
        st.builds(
            lambda score: f'{{"score": "{score}"}}',
            st.floats(allow_nan=False, allow_infinity=False)
        ),
        st.builds(
            lambda score: f'{{"score": {score}, "other": "value"}}',
            st.floats(allow_nan=False, allow_infinity=False)
        ),
        st.builds(
            lambda score: f'{{"score": {score}}} other text',
            st.floats(allow_nan=False, allow_infinity=False)
        ),
        st.builds(
            lambda score: f'other text {{"score": {score}}}',
            st.floats(allow_nan=False, allow_infinity=False)
        ),
        st.builds(
            lambda score: f'other text {{"score": {score}}} other text',
            st.floats(allow_nan=False, allow_infinity=False)
        ),
        st.builds(
            lambda score: f'{{"score": {score}}} {{"other": "value"}}',
            st.floats(allow_nan=False, allow_infinity=False)
        ),
        st.builds(
            lambda score: f'{{"score": {score}}} {{"other": "value"}} other text',
            st.floats(allow_nan=False, allow_infinity=False)
        ),
        st.builds(
            lambda score: f'other text {{"score": {score}}} {{"other": "value"}}',
            st.floats(allow_nan=False, allow_infinity=False)
        ),
        st.builds(
            lambda score: f'other text {{"score": {score}}} {{"other": "value"}} other text',
            st.floats(allow_nan=False, allow_infinity=False)
        )
    )
    
    # Generate lines without JSON-like structures
    non_json_like = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=0, max_size=50
    )
    
    # Combine lines into a multi-line string
    return st.lists(
        st.one_of(
            json_like,
            non_json_like
        ),
        min_size=0, max_size=10
    ).map(lambda x: '\n'.join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(grade_stdout=grade_stdout_strategy())
@example(grade_stdout="")
@example(grade_stdout="score: 100")
@example(grade_stdout="score: 100\nother text")
@example(grade_stdout='{"score": 100}')
@example(grade_stdout='{"score": 100}\nother text')
@example(grade_stdout='other text\n{"score": 100}')
@example(grade_stdout='other text\n{"score": 100}\nother text')
@example(grade_stdout='{"score": 100}\n{"other": "value"}')
@example(grade_stdout='{"score": 100}\n{"other": "value"}\nother text')
@example(grade_stdout='other text\n{"score": 100}\n{"other": "value"}')
@example(grade_stdout='other text\n{"score": 100}\n{"other": "value"}\nother text')
def test_parsing_score(grade_stdout: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    grade_stdout_copy = copy.deepcopy(grade_stdout)

    # Call func0 to verify input validity
    try:
        expected = _parsing_score(grade_stdout_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "grade_stdout": grade_stdout_copy
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