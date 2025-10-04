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
def extract_boxed_answer(text: str):
    """Extract the last boxed{…} string from a LaTeX-like answer."""
    answers = []
    for piece in text.split("boxed{")[1:]:
        n = 0
        for i, ch in enumerate(piece):
            if ch == "{":
                n += 1
            elif ch == "}":
                n -= 1
                if n < 0:
                    answers.append(piece[: i] if (i + 1 == len(piece) or piece[i + 1] != "%") else piece[: i + 1])
                    break
    return answers[-1] if answers else None

# Strategy for generating LaTeX-like text with boxed answers
def text_strategy():
    return st.one_of([
        # Text with multiple boxed answers
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.just("boxed{"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.just("}"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.just("boxed{"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.just("}")
        ).map(lambda x: "".join(x)),
        # Text with a single boxed answer
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.just("boxed{"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.just("}")
        ).map(lambda x: "".join(x)),
        # Text with nested braces in boxed answer
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.just("boxed{"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.just("{"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.just("}"),
            st.just("}")
        ).map(lambda x: "".join(x)),
        # Text with no boxed answer
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
        # Text with boxed answer followed by a comment
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.just("boxed{"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.just("}%"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
        ).map(lambda x: "".join(x))
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy())
@example(text="boxed{answer}")
@example(text="boxed{answer}% comment")
@example(text="boxed{answer} more text boxed{another answer}")
@example(text="boxed{answer{with{nested}braces}}")
@example(text="text with no boxed answer")
def test_extract_boxed_answer(text: str):
    global stop_collecting
    if stop_collecting:
        return
    
    text_copy = copy.deepcopy(text)
    try:
        expected = extract_boxed_answer(text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "boxed{" in text:
        generated_cases.append({
            "Inputs": {"text": text},
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