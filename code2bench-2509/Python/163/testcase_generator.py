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
def _parse_content_type_header(header):
    tokens = header.split(";")
    content_type, params = tokens[0].strip(), tokens[1:]
    params_dict = {}
    items_to_strip = "\"' "

    for param in params:
        param = param.strip()
        if param:
            key, value = param, True
            index_of_equals = param.find("=")
            if index_of_equals != -1:
                key = param[:index_of_equals].strip(items_to_strip)
                value = param[index_of_equals + 1 :].strip(items_to_strip)
            params_dict[key.lower()] = value
    return content_type, params_dict

# Strategy for generating content-type headers
def header_strategy():
    content_type = st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=1,
        max_size=50
    )
    param_key = st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=1,
        max_size=20
    )
    param_value = st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=0,
        max_size=20
    )
    param = st.one_of([
        st.tuples(param_key, param_value),
        st.just(("", ""))
    ])
    params = st.lists(param, max_size=5)
    return st.tuples(content_type, params).map(
        lambda x: f"{x[0]}; " + "; ".join(f"{k}={v}" if v else k for k, v in x[1] if k)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(header=header_strategy())
@example(header="text/plain")
@example(header="text/plain; charset=utf-8")
@example(header="text/plain; charset=utf-8; boundary=abc")
@example(header="text/plain; charset='utf-8'")
@example(header="text/plain; charset=\"utf-8\"")
@example(header="text/plain; charset=utf-8; boundary=\"abc\"")
@example(header="text/plain; charset=utf-8; boundary='abc'")
@example(header="text/plain; charset=utf-8; boundary=abc; foo=bar")
@example(header="text/plain; charset=utf-8; boundary=abc; foo")
@example(header="text/plain; charset=utf-8; boundary=abc; foo=")
def test_parse_content_type_header(header):
    global stop_collecting
    if stop_collecting:
        return
    
    header_copy = copy.deepcopy(header)
    try:
        expected = _parse_content_type_header(header_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if ";" in header or header.strip():
        generated_cases.append({
            "Inputs": {"header": header},
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