from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import base64
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
def base64_decode(url_content):  # Base64 转换为 URL 链接内容
    if '-' in url_content:
        url_content = url_content.replace('-', '+')
    if '_' in url_content:
        url_content = url_content.replace('_', '/')
    missing_padding = len(url_content) % 4
    if missing_padding != 0:
        url_content += '=' * (4 - missing_padding)
    try:
        base64_content = base64.b64decode(url_content.encode('utf-8')).decode('utf-8', 'ignore')
        base64_content_format = base64_content
        return base64_content_format
    except UnicodeDecodeError:
        base64_content = base64.b64decode(url_content)
        base64_content_format = base64_content
        return str(base64_content)

# Strategy for generating base64 encoded strings
def base64_strategy():
    # Generate valid base64 characters
    base64_chars = st.characters(
        whitelist_categories=('L', 'N', 'P', 'S'),
        whitelist_characters='-_+/='
    )
    # Generate strings with varying lengths
    return st.text(
        alphabet=base64_chars,
        min_size=0,
        max_size=100
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(url_content=base64_strategy())
@example(url_content="")
@example(url_content="aGVsbG8gd29ybGQ=")  # "hello world"
@example(url_content="aGVsbG8gd29ybGQ")  # "hello world" without padding
@example(url_content="aGVsbG8gd29ybGQ==")  # "hello world" with padding
@example(url_content="aGVsbG8gd29ybGQ===")  # Invalid padding
@example(url_content="aGVsbG8gd29ybGQ=====")  # Invalid padding
@example(url_content="aGVsbG8gd29ybGQ-_")  # With '-' and '_'
def test_base64_decode(url_content: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    url_content_copy = copy.deepcopy(url_content)

    # Call func0 to verify input validity
    try:
        expected = base64_decode(url_content_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "url_content": url_content_copy
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