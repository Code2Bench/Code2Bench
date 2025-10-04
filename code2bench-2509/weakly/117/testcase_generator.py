from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from urllib.parse import urlparse

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def parse_database_uri(uri):
    """Parse database URI and return connection parameters"""
    parsed = urlparse(uri)

    # Remove the driver part (postgresql+pg8000 -> postgresql)
    scheme = parsed.scheme.split('+')[0]

    return {
        'host': parsed.hostname,
        'port': parsed.port or 5432,
        'database': parsed.path.lstrip('/'),
        'user': parsed.username,
        'password': parsed.password
    }

# Strategy for generating database URIs
def database_uri_strategy():
    # Generate valid database URIs with optional components
    scheme = st.sampled_from(['postgresql', 'mysql', 'sqlite', 'mongodb'])
    driver = st.one_of(st.just(''), st.sampled_from(['pg8000', 'psycopg2', 'pymysql']))
    user = st.one_of(st.just(''), st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10))
    password = st.one_of(st.just(''), st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=1, max_size=10))
    host = st.one_of(st.just(''), st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10))
    port = st.one_of(st.just(''), st.integers(min_value=1, max_value=65535))
    database = st.one_of(st.just(''), st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10))

    return st.builds(
        lambda s, d, u, p, h, pt, db: f"{s}+{d}://{u}:{p}@{h}:{pt}/{db}" if d else f"{s}://{u}:{p}@{h}:{pt}/{db}",
        scheme, driver, user, password, host, port, database
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(uri=database_uri_strategy())
@example(uri="postgresql://user:password@localhost:5432/mydb")
@example(uri="mysql://user@localhost/mydb")
@example(uri="sqlite:///path/to/db.sqlite")
@example(uri="mongodb://localhost:27017/mydb")
@example(uri="postgresql+pg8000://user:password@localhost/mydb")
@example(uri="postgresql://localhost:5432")
@example(uri="postgresql://user@localhost")
@example(uri="postgresql://localhost/mydb")
@example(uri="postgresql://user:password@localhost")
@example(uri="postgresql://user:password@localhost:5432")
def test_parse_database_uri(uri):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    uri_copy = copy.deepcopy(uri)

    # Call func0 to verify input validity
    try:
        expected = parse_database_uri(uri_copy)
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