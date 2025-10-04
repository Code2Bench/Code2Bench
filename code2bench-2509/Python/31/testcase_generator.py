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
def extract_boxed_content(ans: str):
    idx = ans.rfind(r'\boxed{')
    if idx == -1:
        return ans

    idx += len(r'\boxed{')
    brace_level = 1
    content_start = idx
    i = idx

    while i < len(ans):
        if ans[i] == '{':
            brace_level += 1
        elif ans[i] == '}':
            brace_level -= 1
            if brace_level == 0:
                break
        i += 1

    if brace_level != 0:
        # Unbalanced braces
        return ans

    content = ans[content_start:i]
    return content

# Strategy for generating strings with \boxed{...} content
def boxed_string_strategy():
    return st.one_of([
        # Strings with balanced \boxed{...}
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50),
            st.just(r'\boxed{'),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50),
            st.just('}')
        ).map(lambda x: ''.join(x)),
        # Strings with unbalanced \boxed{...}
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50),
            st.just(r'\boxed{'),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50)
        ).map(lambda x: ''.join(x)),
        # Strings without \boxed{...}
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=100),
        # Strings with nested \boxed{...}
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50),
            st.just(r'\boxed{'),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50),
            st.just(r'\boxed{'),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50),
            st.just('}'),
            st.just('}')
        ).map(lambda x: ''.join(x))
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(ans=boxed_string_strategy())
@example(ans=r'\boxed{content}')
@example(ans=r'\boxed{content')
@example(ans='no boxed content')
@example(ans=r'\boxed{\boxed{nested}}')
@example(ans=r'\boxed{unbalanced')
def test_extract_boxed_content(ans: str):
    global stop_collecting
    if stop_collecting:
        return
    
    ans_copy = copy.deepcopy(ans)
    try:
        expected = extract_boxed_content(ans_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if r'\boxed{' in ans or '}' in ans:
        generated_cases.append({
            "Inputs": {"ans": ans},
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