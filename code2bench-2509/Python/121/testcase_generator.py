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
def clean_ddl_for_pglite(ddl):
    """Clean DDL statements for PGlite compatibility"""

    # Remove PostgreSQL-specific extensions and features that PGlite doesn't support
    replacements = [
        # Remove vector column types (PGlite doesn't support pgvector)
        ('vector(1536)', 'TEXT'),  # Replace vector columns with TEXT for now
        ('vector(3072)', 'TEXT'),
        ('vector(4096)', 'TEXT'),

        # Remove GIN indexes (not supported in PGlite)
        ('USING gin', ''),

        # Simplify constraint names
        ('CONSTRAINT ', ''),

        # Remove some PostgreSQL-specific column constraints
        ('::text', ''),

        # Remove timezone from TIMESTAMP
        ('TIMESTAMP WITH TIME ZONE', 'TIMESTAMP'),

        # Simplify SERIAL to INTEGER with autoincrement
        ('BIGSERIAL', 'INTEGER'),
        ('SERIAL', 'INTEGER'),
    ]

    for old, new in replacements:
        ddl = ddl.replace(old, new)

    # Remove any lines that contain unsupported PostgreSQL features
    lines = ddl.split('\n')
    filtered_lines = []

    for line in lines:
        # Skip lines with unsupported features
        if any(unsupported in line.lower() for unsupported in [
            'gin', 'gist', 'tsvector', 'to_tsvector', 'pg_trgm',
            'btree_gin', 'btree_gist'
        ]):
            continue
        filtered_lines.append(line)

    return '\n'.join(filtered_lines)

# Strategy for generating DDL statements
def ddl_strategy():
    # Generate random DDL statements with PostgreSQL-specific features
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=1,
        max_size=1000
    ).map(lambda s: s.replace('\x00', ''))  # Remove null bytes

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(ddl=ddl_strategy())
@example(ddl="CREATE TABLE test (id SERIAL PRIMARY KEY, data TEXT);")
@example(ddl="CREATE TABLE test (id BIGSERIAL PRIMARY KEY, data vector(1536));")
@example(ddl="CREATE TABLE test (id INTEGER PRIMARY KEY, data TIMESTAMP WITH TIME ZONE);")
@example(ddl="CREATE TABLE test (id INTEGER PRIMARY KEY, data TEXT USING gin);")
@example(ddl="CREATE TABLE test (id INTEGER PRIMARY KEY, data TEXT CONSTRAINT test_constraint);")
@example(ddl="CREATE TABLE test (id INTEGER PRIMARY KEY, data TEXT::text);")
@example(ddl="CREATE TABLE test (id INTEGER PRIMARY KEY, data tsvector);")
def test_clean_ddl_for_pglite(ddl):
    global stop_collecting
    if stop_collecting:
        return
    
    ddl_copy = copy.deepcopy(ddl)
    try:
        expected = clean_ddl_for_pglite(ddl_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(
        'vector(' in ddl or
        'USING gin' in ddl or
        'CONSTRAINT ' in ddl or
        '::text' in ddl or
        'TIMESTAMP WITH TIME ZONE' in ddl or
        'SERIAL' in ddl or
        'BIGSERIAL' in ddl or
        'gin' in ddl.lower() or
        'gist' in ddl.lower() or
        'tsvector' in ddl.lower() or
        'to_tsvector' in ddl.lower() or
        'pg_trgm' in ddl.lower() or
        'btree_gin' in ddl.lower() or
        'btree_gist' in ddl.lower()
        for ddl in [ddl]
    ):
        generated_cases.append({
            "Inputs": {"ddl": ddl},
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