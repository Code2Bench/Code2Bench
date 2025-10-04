from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import urllib.parse
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
def egg_info_for_url(url):
    parts = urllib.parse.urlparse(url)
    scheme, server, path, parameters, query, fragment = parts
    base = urllib.parse.unquote(path.split('/')[-1])
    if server == 'sourceforge.net' and base == 'download':  # XXX Yuck
        base = urllib.parse.unquote(path.split('/')[-2])
    if '#' in base:
        base, fragment = base.split('#', 1)
    return base, fragment

# Strategy for generating URLs
def url_strategy():
    schemes = st.sampled_from(["http", "https", "ftp"])
    servers = st.one_of(
        st.just("sourceforge.net"),
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-'), min_size=1, max_size=20)
    )
    paths = st.lists(
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='._-'), min_size=1, max_size=10),
        min_size=1, max_size=5
    ).map(lambda x: '/' + '/'.join(x))
    fragments = st.one_of(
        st.just(""),
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='._-'), min_size=1, max_size=10)
    )
    return st.builds(
        lambda s, sv, p, f: f"{s}://{sv}{p}#{f}" if f else f"{s}://{sv}{p}",
        schemes, servers, paths, fragments
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(url=url_strategy())
@example(url="http://sourceforge.net/project/download")
@example(url="http://example.com/path/to/file#fragment")
@example(url="https://sourceforge.net/project/download#fragment")
@example(url="ftp://example.com/file")
@example(url="http://example.com/path/to/file")
def test_egg_info_for_url(url: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    url_copy = copy.deepcopy(url)

    # Call func0 to verify input validity
    try:
        expected_base, expected_fragment = egg_info_for_url(url_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "url": url_copy
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