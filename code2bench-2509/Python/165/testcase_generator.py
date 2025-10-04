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
def build_csp_header(csp_config):
    """
    Build the Content Security Policy header value from the configuration.
    """
    if not csp_config:
        return None

    directives = []
    for directive, value in csp_config.items():
        if value:
            directives.append(f"{directive} {value}")
        else:
            directives.append(directive)

    return "; ".join(directives)

# Strategy for generating CSP configurations
def csp_config_strategy():
    return st.dictionaries(
        keys=st.text(
            st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
            min_size=1,
            max_size=20
        ),
        values=st.one_of([
            st.text(
                st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
                min_size=1,
                max_size=20
            ),
            st.just("")
        ]),
        min_size=0,
        max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(csp_config=csp_config_strategy())
@example(csp_config={})
@example(csp_config={"default-src": "'self'"})
@example(csp_config={"script-src": "'unsafe-inline'", "style-src": ""})
@example(csp_config={"img-src": "https://example.com", "font-src": "https://fonts.gstatic.com"})
def test_build_csp_header(csp_config):
    global stop_collecting
    if stop_collecting:
        return

    csp_config_copy = copy.deepcopy(csp_config)
    try:
        expected = build_csp_header(csp_config_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    if csp_config or expected is None:
        generated_cases.append({
            "Inputs": {"csp_config": csp_config},
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