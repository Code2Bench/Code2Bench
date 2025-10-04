from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import regex
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
def extract_multi_choice_answer(pred_str):
    if "Problem:" in pred_str:
        pred_str = pred_str.split("Problem:", 1)[0]
    pred_str = pred_str.replace("choice is", "answer is")
    patt = regex.search(r"answer is \(?(?P<ans>[abcde])\)?", pred_str.lower())
    if patt is not None:
        return patt.group("ans").upper()
    return "placeholder"

# Strategy for generating pred_str
def pred_str_strategy():
    # Generate strings with potential "Problem:" and "choice is" patterns
    problem_part = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=50)
    choice_part = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=50)
    answer_part = st.sampled_from(["answer is a", "answer is b", "answer is c", "answer is d", "answer is e", "choice is a", "choice is b", "choice is c", "choice is d", "choice is e"])
    return st.one_of(
        st.builds(lambda p, c, a: f"{p}Problem:{c}{a}", problem_part, choice_part, answer_part),
        st.builds(lambda c, a: f"{c}{a}", choice_part, answer_part),
        st.builds(lambda p, a: f"{p}{a}", problem_part, answer_part),
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=100)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(pred_str=pred_str_strategy())
@example(pred_str="Problem: What is the answer? choice is a")
@example(pred_str="answer is b")
@example(pred_str="choice is c")
@example(pred_str="Problem: What is the answer? answer is d")
@example(pred_str="random text without answer")
@example(pred_str="answer is (e)")
def test_extract_multi_choice_answer(pred_str: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    pred_str_copy = copy.deepcopy(pred_str)

    # Call func0 to verify input validity
    try:
        expected = extract_multi_choice_answer(pred_str_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "pred_str": pred_str_copy
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