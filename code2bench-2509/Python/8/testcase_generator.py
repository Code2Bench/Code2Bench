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
def fuzzy_match(prediction: str, reference: str) -> bool:
    """Fuzzy match function for BigBench Extra Hard."""
    if prediction == reference:
        return True

    # (a) vs a
    if len(prediction) == 3 and prediction[0] == "(" and prediction[-1] == ")":
        return prediction[1] == reference
    if len(reference) == 3 and reference[0] == "(" and reference[-1] == ")":
        return reference[1] == prediction

    # Numbers
    try:
        if float(prediction) == float(reference):
            return True
    except ValueError:
        pass

    # quote issues
    if prediction.replace("'", "") == reference.replace("'", ""):
        return True

    # Bracket issues
    if f"[{reference}]" == prediction or f"[{prediction}]" == reference:
        return True

    # Question mark issues
    if prediction.endswith("?") and prediction[:-1] == reference:
        return True

    return False

# Strategy for generating strings with specific patterns
def string_strategy():
    return st.one_of([
        # Exact matches
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
        # Strings with parentheses
        st.tuples(st.just("("), st.characters(whitelist_categories=('L', 'N')), st.just(")")).map(lambda x: "".join(x)),
        # Numeric strings
        st.from_regex(r"-?\d+(\.\d+)?"),
        # Strings with quotes
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20).map(lambda s: s.replace("a", "'")),
        # Strings with brackets
        st.tuples(st.just("["), st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20), st.just("]")).map(lambda x: "".join(x)),
        # Strings with question marks
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20).map(lambda s: s + "?")
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(prediction=string_strategy(), reference=string_strategy())
@example(prediction="(a)", reference="a")
@example(prediction="a", reference="(a)")
@example(prediction="1.0", reference="1")
@example(prediction="'a'", reference="a")
@example(prediction="[a]", reference="a")
@example(prediction="a?", reference="a")
def test_fuzzy_match(prediction: str, reference: str):
    global stop_collecting
    if stop_collecting:
        return
    
    prediction_copy = copy.deepcopy(prediction)
    reference_copy = copy.deepcopy(reference)
    try:
        expected = fuzzy_match(prediction_copy, reference_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if prediction != reference:  # Skip exact matches to focus on fuzzy cases
        generated_cases.append({
            "Inputs": {"prediction": prediction, "reference": reference},
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