from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from urllib.parse import urlparse
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
def extract_domain(url_or_domain):
    try:
        parsed_url = urlparse(url_or_domain)
        domain = parsed_url.netloc
        if not domain:
            domain = parsed_url.path

        domain = domain.split(':')[0]
        domain = domain.split('/')[0].split('?')[0].split('#')[0]

        return domain.lower().strip()
    except Exception:
        return url_or_domain.lower().strip()

# Strategy for generating URLs or domains
def url_or_domain_strategy():
    # Generate valid domains
    domain = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-'),
        min_size=1, max_size=20
    ).map(lambda s: s.lower())

    # Generate valid URLs
    scheme = st.sampled_from(['http', 'https', 'ftp', ''])
    netloc = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-'),
        min_size=1, max_size=20
    ).map(lambda s: s.lower())
    path = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=0, max_size=20
    ).map(lambda s: s.lower())
    query = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=0, max_size=20
    ).map(lambda s: s.lower())
    fragment = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=0, max_size=20
    ).map(lambda s: s.lower())

    url = st.builds(
        lambda s, n, p, q, f: f"{s}://{n}{p}?{q}#{f}" if s else f"{n}{p}?{q}#{f}",
        scheme, netloc, path, query, fragment
    )

    return st.one_of(domain, url)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(url_or_domain=url_or_domain_strategy())
@example(url_or_domain="example.com")
@example(url_or_domain="http://example.com")
@example(url_or_domain="https://example.com/path?query=value#fragment")
@example(url_or_domain="ftp://example.com:8080")
@example(url_or_domain="invalid url")
@example(url_or_domain="")
def test_extract_domain(url_or_domain):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    url_or_domain_copy = copy.deepcopy(url_or_domain)

    # Call func0 to verify input validity
    try:
        expected = extract_domain(url_or_domain_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "url_or_domain": url_or_domain_copy
        }
    })

    # Stop collecting after 500 cases
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)