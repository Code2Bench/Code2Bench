from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def convert_url(url: str) -> str:
    if url.endswith("/mcp") or url.endswith("/mcp/"):
        if url.endswith("/mcp"):
            return url + "/"
        return url
    if url.endswith("/sse"):
        return url.replace("/sse", "/mcp/")
    return url + "/mcp/"

# Strategy for generating URLs
def url_strategy():
    base_url = st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=1,
        max_size=50
    ).map(lambda s: f"http://{s}")
    return st.one_of([
        base_url,
        base_url.map(lambda s: s + "/sse"),
        base_url.map(lambda s: s + "/mcp"),
        base_url.map(lambda s: s + "/mcp/")
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(url=url_strategy())
@example(url="http://localhost:4444/servers/uuid")
@example(url="http://localhost:4444/servers/uuid/sse")
@example(url="http://localhost:4444/servers/uuid/mcp")
@example(url="http://localhost:4444/servers/uuid/mcp/")
def test_convert_url(url: str):
    global stop_collecting
    if stop_collecting:
        return
    
    try:
        expected = convert_url(url)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"url": url},
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