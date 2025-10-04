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
def parse_generator(string: str):
    cmds = []
    quotes = []
    current = ""
    q_string = ""
    inquote = False
    for cha in string:
        if not inquote and cha == " ":
            if current:
                cmds.append(current)
                quotes.append(q_string)
            q_string = ""
            current = ""
            continue
        if cha == "\"":
            inquote ^= True

        current += cha

        if inquote and cha != "\"":
            q_string += cha

    if current:
        cmds.append(current)
        quotes.append(q_string)

    return cmds, quotes, inquote

# Strategy for generating strings with quotes and spaces
def string_strategy():
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), blacklist_characters="\""),
        min_size=0,
        max_size=50
    ).map(lambda s: s.replace(" ", "_"))  # Replace spaces to avoid premature splitting

def quoted_string_strategy():
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), blacklist_characters="\""),
        min_size=1,
        max_size=20
    ).map(lambda s: f"\"{s}\"")

def mixed_string_strategy():
    return st.one_of([
        string_strategy(),
        quoted_string_strategy(),
        st.lists(st.one_of([string_strategy(), quoted_string_strategy()]), min_size=1, max_size=5).map(" ".join)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(string=mixed_string_strategy())
@example(string="")
@example(string=" ")
@example(string="\"\"")
@example(string="\"a\"")
@example(string="a b c")
@example(string="\"a\" \"b\" \"c\"")
@example(string="a \"b\" c")
@example(string="\"a b\" c")
@example(string="a \"b c\"")
@example(string="\"a b c\"")
@example(string="\"a\"\"b\"\"c\"")
@example(string="\"a\" \"b\" \"c\"")
@example(string="\"a\"\"b\"\"c\"")
@example(string="\"a\"\"b\"\"c\"")
def test_parse_generator(string: str):
    global stop_collecting
    if stop_collecting:
        return
    
    string_copy = copy.deepcopy(string)
    try:
        expected = parse_generator(string_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "\"" in string or " " in string:
        generated_cases.append({
            "Inputs": {"string": string},
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