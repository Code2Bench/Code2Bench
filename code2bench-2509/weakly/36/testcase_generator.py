from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import Dict
from urllib.parse import urlparse

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def parse_pg_uri(uri: str) -> Dict[str, str]:
    """Parse PostgreSQL URI and extract connection details."""
    parsed = urlparse(uri)
    return {
        'host': parsed.hostname or 'localhost',
        'port': str(parsed.port or 5432),
        'user': parsed.username or 'mirix',
        'database': parsed.path.lstrip('/') or 'mirix'
    }

# Strategy for generating PostgreSQL URIs
def pg_uri_strategy():
    # Generate valid components for a PostgreSQL URI
    scheme = st.just("postgresql")
    user = st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_'), min_size=1, max_size=10)
    password = st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_'), min_size=1, max_size=10)
    host = st.one_of(st.just("localhost"), st.ip_addresses(v=4), st.ip_addresses(v=6))
    port = st.integers(min_value=1, max_value=65535)
    database = st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_'), min_size=1, max_size=10)
    
    # Combine components into a URI
    return st.builds(
        lambda s, u, p, h, pt, d: f"{s}://{u}:{p}@{h}:{pt}/{d}",
        scheme, user, password, host, port, database
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(uri=pg_uri_strategy())
@example(uri="postgresql://user:password@localhost:5432/database")
@example(uri="postgresql://localhost:5432/database")
@example(uri="postgresql://user@localhost/database")
@example(uri="postgresql://localhost/database")
@example(uri="postgresql://user:password@127.0.0.1:5432/database")
@example(uri="postgresql://user:password@[::1]:5432/database")
def test_parse_pg_uri(uri: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    uri_copy = copy.deepcopy(uri)

    # Call func0 to verify input validity
    try:
        expected = parse_pg_uri(uri_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "uri": uri_copy
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