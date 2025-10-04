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
def _fix_sqrt(string: str) -> str:
    if "\\sqrt" not in string:
        return string
    splits = string.split("\\sqrt")
    new_string = splits[0]
    for split in splits[1:]:
        if split[0] != "{":
            a = split[0]
            new_substr = "\\sqrt{" + a + "}" + split[1:]
        else:
            new_substr = "\\sqrt" + split
        new_string += new_substr
    return new_string

# Strategy for generating strings with and without \sqrt
def string_strategy():
    return st.one_of([
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.just("\\sqrt"),
            st.one_of([
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=1),
                st.tuples(
                    st.just("{"),
                    st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=5),
                    st.just("}")
                ).map(lambda x: "".join(x))
            ]),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20)
        ).map(lambda x: "".join(x))
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(string=string_strategy())
@example(string="\\sqrt{a}")
@example(string="\\sqrt{a} + b")
@example(string="a + \\sqrt{b}")
@example(string="\\sqrt{a} + \\sqrt{b}")
@example(string="\\sqrt{a} + \\sqrt{b} + c")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c}")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + d")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d}")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + e")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e}")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + f")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f}")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + g")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g}")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + h")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h}")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + i")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i}")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + j")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j}")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j} + k")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j} + \\sqrt{k}")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j} + \\sqrt{k} + l")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j} + \\sqrt{k} + \\sqrt{l}")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j} + \\sqrt{k} + \\sqrt{l} + m")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j} + \\sqrt{k} + \\sqrt{l} + \\sqrt{m}")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j} + \\sqrt{k} + \\sqrt{l} + \\sqrt{m} + n")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j} + \\sqrt{k} + \\sqrt{l} + \\sqrt{m} + \\sqrt{n}")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j} + \\sqrt{k} + \\sqrt{l} + \\sqrt{m} + \\sqrt{n} + o")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j} + \\sqrt{k} + \\sqrt{l} + \\sqrt{m} + \\sqrt{n} + \\sqrt{o}")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j} + \\sqrt{k} + \\sqrt{l} + \\sqrt{m} + \\sqrt{n} + \\sqrt{o} + p")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j} + \\sqrt{k} + \\sqrt{l} + \\sqrt{m} + \\sqrt{n} + \\sqrt{o} + \\sqrt{p}")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j} + \\sqrt{k} + \\sqrt{l} + \\sqrt{m} + \\sqrt{n} + \\sqrt{o} + \\sqrt{p} + q")
@example(string="\\sqrt{a} + \\sqrt{b} + \\sqrt{c} + \\sqrt{d} + \\sqrt{e} + \\sqrt{f} + \\sqrt{g} + \\sqrt{h} + \\sqrt{i} + \\sqrt{j} + \\sqrt{k} + \\sqrt{l} + \\sqrt{m} + \\sqrt{n} + \\sqrt{o} + \\sqrt{p} + \\sqrt{q}")
def test_fix_sqrt(string: str):
    global stop_collecting
    if stop_collecting:
        return
    
    string_copy = copy.deepcopy(string)
    try:
        expected = _fix_sqrt(string_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "\\sqrt" in string:
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