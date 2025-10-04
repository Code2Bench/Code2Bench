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
def normalize_base_url(url: str) -> str:
    """Normalize a base URL by adding http:// if missing and ensuring trailing slash."""
    if not url:
        return url

    # Strip whitespace
    url = url.strip()

    # Add http:// if no protocol is specified
    if not url.startswith(('http://', 'https://')):
        # If it looks like a local IP or localhost, use http, otherwise https
        if any(x in url for x in ['localhost', '127.0.0.1', '192.168.', '10.', '172.']):
            url = f'http://{url}'
        else:
            url = f'https://{url}'

    # Ensure trailing slash for base URLs
    if not url.endswith('/'):
        url = f'{url}/'

    return url

# Strategy for generating URLs
def url_strategy():
    return st.one_of([
        # Empty URL
        st.just(""),
        # URLs without protocol
        st.tuples(
            st.one_of([
                st.just("localhost"),
                st.just("127.0.0.1"),
                st.just("192.168.1.1"),
                st.just("10.0.0.1"),
                st.just("172.16.0.1"),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
            ]),
            st.one_of([
                st.just(""),
                st.just("/"),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
            ])
        ).map(lambda x: f"{x[0]}{x[1]}"),
        # URLs with protocol
        st.tuples(
            st.one_of([st.just("http://"), st.just("https://")]),
            st.one_of([
                st.just("localhost"),
                st.just("127.0.0.1"),
                st.just("192.168.1.1"),
                st.just("10.0.0.1"),
                st.just("172.16.0.1"),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
            ]),
            st.one_of([
                st.just(""),
                st.just("/"),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
            ])
        ).map(lambda x: f"{x[0]}{x[1]}{x[2]}"),
        # URLs with whitespace
        st.tuples(
            st.text(st.characters(whitelist_categories=('Zs',)), min_size=1, max_size=5),
            st.one_of([
                st.just("localhost"),
                st.just("127.0.0.1"),
                st.just("192.168.1.1"),
                st.just("10.0.0.1"),
                st.just("172.16.0.1"),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
            ]),
            st.text(st.characters(whitelist_categories=('Zs',)), min_size=1, max_size=5)
        ).map(lambda x: f"{x[0]}{x[1]}{x[2]}")
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(url=url_strategy())
@example(url="")
@example(url="localhost")
@example(url="127.0.0.1")
@example(url="192.168.1.1")
@example(url="10.0.0.1")
@example(url="172.16.0.1")
@example(url="example.com")
@example(url="http://example.com")
@example(url="https://example.com")
@example(url="http://localhost")
@example(url="https://localhost")
@example(url="http://127.0.0.1")
@example(url="https://127.0.0.1")
@example(url="http://192.168.1.1")
@example(url="https://192.168.1.1")
@example(url="http://10.0.0.1")
@example(url="https://10.0.0.1")
@example(url="http://172.16.0.1")
@example(url="https://172.16.0.1")
@example(url="example.com/path")
@example(url="http://example.com/path")
@example(url="https://example.com/path")
@example(url="http://localhost/path")
@example(url="https://localhost/path")
@example(url="http://127.0.0.1/path")
@example(url="https://127.0.0.1/path")
@example(url="http://192.168.1.1/path")
@example(url="https://192.168.1.1/path")
@example(url="http://10.0.0.1/path")
@example(url="https://10.0.0.1/path")
@example(url="http://172.16.0.1/path")
@example(url="https://172.16.0.1/path")
@example(url="  example.com  ")
@example(url="  http://example.com  ")
@example(url="  https://example.com  ")
@example(url="  http://localhost  ")
@example(url="  https://localhost  ")
@example(url="  http://127.0.0.1  ")
@example(url="  https://127.0.0.1  ")
@example(url="  http://192.168.1.1  ")
@example(url="  https://192.168.1.1  ")
@example(url="  http://10.0.0.1  ")
@example(url="  https://10.0.0.1  ")
@example(url="  http://172.16.0.1  ")
@example(url="  https://172.16.0.1  ")
def test_normalize_base_url(url: str):
    global stop_collecting
    if stop_collecting:
        return
    
    url_copy = copy.deepcopy(url)
    try:
        expected = normalize_base_url(url_copy)
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