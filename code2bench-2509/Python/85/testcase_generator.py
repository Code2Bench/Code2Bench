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
def find_boxed_content_with_boxed(text: str) -> list[str]:
    results = []
    i = 0
    while i < len(text):
        if text[i : i + 7] == "\\boxed{":
            i += 7  # Move past "\boxed{"
            content = ""
            brace_count = 1
            while i < len(text) and brace_count > 0:
                if text[i] == "{":
                    brace_count += 1
                elif text[i] == "}":
                    brace_count -= 1

                if brace_count > 0:
                    content += text[i]
                i += 1

            results.append(content)
        else:
            i += 1
    return results

# Strategy for generating text with boxed content
def boxed_text_strategy():
    return st.one_of([
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{\\boxed{{{s}}}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{\\boxed{{\\boxed{{{s}}}}}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} and \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} or \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} but \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} then \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} else \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} if \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} while \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} for \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} with \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} without \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} plus \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} minus \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} times \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} divided by \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} modulo \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} power \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} root \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} log \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} sin \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} cos \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} tan \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} cot \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} sec \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} csc \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} arcsin \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} arccos \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} arctan \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} arccot \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} arcsec \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} arccsc \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} sinh \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} cosh \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} tanh \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} coth \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} sech \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} csch \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} arcsinh \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} arccosh \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} arctanh \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} arccoth \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} arcsech \\boxed{{{s}}}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda s: f"\\boxed{{{s}}} arccsch \\boxed{{{s}}}"),
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=boxed_text_strategy())
@example(text="\\boxed{42}")
@example(text="\\boxed{\\boxed{42}}")
@example(text="\\boxed{\\boxed{\\boxed{42}}}")
@example(text="\\boxed{42} and \\boxed{42}")
@example(text="\\boxed{42} or \\boxed{42}")
@example(text="\\boxed{42} but \\boxed{42}")
@example(text="\\boxed{42} then \\boxed{42}")
@example(text="\\boxed{42} else \\boxed{42}")
@example(text="\\boxed{42} if \\boxed{42}")
@example(text="\\boxed{42} while \\boxed{42}")
@example(text="\\boxed{42} for \\boxed{42}")
@example(text="\\boxed{42} with \\boxed{42}")
@example(text="\\boxed{42} without \\boxed{42}")
@example(text="\\boxed{42} plus \\boxed{42}")
@example(text="\\boxed{42} minus \\boxed{42}")
@example(text="\\boxed{42} times \\boxed{42}")
@example(text="\\boxed{42} divided by \\boxed{42}")
@example(text="\\boxed{42} modulo \\boxed{42}")
@example(text="\\boxed{42} power \\boxed{42}")
@example(text="\\boxed{42} root \\boxed{42}")
@example(text="\\boxed{42} log \\boxed{42}")
@example(text="\\boxed{42} sin \\boxed{42}")
@example(text="\\boxed{42} cos \\boxed{42}")
@example(text="\\boxed{42} tan \\boxed{42}")
@example(text="\\boxed{42} cot \\boxed{42}")
@example(text="\\boxed{42} sec \\boxed{42}")
@example(text="\\boxed{42} csc \\boxed{42}")
@example(text="\\boxed{42} arcsin \\boxed{42}")
@example(text="\\boxed{42} arccos \\boxed{42}")
@example(text="\\boxed{42} arctan \\boxed{42}")
@example(text="\\boxed{42} arccot \\boxed{42}")
@example(text="\\boxed{42} arcsec \\boxed{42}")
@example(text="\\boxed{42} arccsc \\boxed{42}")
@example(text="\\boxed{42} sinh \\boxed{42}")
@example(text="\\boxed{42} cosh \\boxed{42}")
@example(text="\\boxed{42} tanh \\boxed{42}")
@example(text="\\boxed{42} coth \\boxed{42}")
@example(text="\\boxed{42} sech \\boxed{42}")
@example(text="\\boxed{42} csch \\boxed{42}")
@example(text="\\boxed{42} arcsinh \\boxed{42}")
@example(text="\\boxed{42} arccosh \\boxed{42}")
@example(text="\\boxed{42} arctanh \\boxed{42}")
@example(text="\\boxed{42} arccoth \\boxed{42}")
@example(text="\\boxed{42} arcsech \\boxed{42}")
@example(text="\\boxed{42} arccsch \\boxed{42}")
def test_find_boxed_content_with_boxed(text: str):
    global stop_collecting
    if stop_collecting:
        return
    
    text_copy = copy.deepcopy(text)
    try:
        expected = find_boxed_content_with_boxed(text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "\\boxed{" in text:
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