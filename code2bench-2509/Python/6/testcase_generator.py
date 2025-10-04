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
def extract_boxed(text):
    results, i = [], 0
    prefix = r'\boxed{'
    plen = len(prefix)

    while True:
        start = text.find(prefix, i)
        if start == -1:
            break   # no more \boxed{…}

        j = start + plen
        depth = 1
        while j < len(text) and depth:
            if text[j] == '{':
                depth += 1
            elif text[j] == '}':
                depth -= 1
            j += 1

        results.append(text[start + plen : j - 1])
        i = j

    return results

# Strategy for generating text with \boxed{...} patterns
def boxed_text_strategy():
    return st.one_of([
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
        st.lists(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
            min_size=1, max_size=5
        ).map(lambda lst: r'\boxed{' + '}{'.join(lst) + '}'),
        st.recursive(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
            lambda children: st.one_of([
                st.tuples(st.just(r'\boxed{'), children, st.just('}')).map(lambda x: ''.join(x)),
                st.tuples(st.just(r'\boxed{'), children, st.just('}'), children).map(lambda x: ''.join(x))
            ]),
            max_leaves=5
        )
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=boxed_text_strategy())
@example(text=r'\boxed{1}')
@example(text=r'\boxed{1}\boxed{2}')
@example(text=r'\boxed{\boxed{1}}')
@example(text=r'\boxed{1} \boxed{2}')
@example(text=r'\boxed{1} \boxed{2} \boxed{3}')
@example(text=r'\boxed{1} \boxed{2} \boxed{3} \boxed{4}')
@example(text=r'\boxed{1} \boxed{2} \boxed{3} \boxed{4} \boxed{5}')
@example(text=r'\boxed{1} \boxed{2} \boxed{3} \boxed{4} \boxed{5} \boxed{6}')
@example(text=r'\boxed{1} \boxed{2} \boxed{3} \boxed{4} \boxed{5} \boxed{6} \boxed{7}')
@example(text=r'\boxed{1} \boxed{2} \boxed{3} \boxed{4} \boxed{5} \boxed{6} \boxed{7} \boxed{8}')
@example(text=r'\boxed{1} \boxed{2} \boxed{3} \boxed{4} \boxed{5} \boxed{6} \boxed{7} \boxed{8} \boxed{9}')
@example(text=r'\boxed{1} \boxed{2} \boxed{3} \boxed{4} \boxed{5} \boxed{6} \boxed{7} \boxed{8} \boxed{9} \boxed{10}')
def test_extract_boxed(text):
    global stop_collecting
    if stop_collecting:
        return
    
    text_copy = copy.deepcopy(text)
    try:
        expected = extract_boxed(text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if r'\boxed{' in text:
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