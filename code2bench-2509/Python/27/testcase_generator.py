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
def analyze_content(markdown_content):
    """Analyze the content structure of the markdown."""
    analysis = {}

    # Count different elements
    analysis['lines'] = len(markdown_content.split('\n'))
    analysis['words'] = len(markdown_content.split())
    analysis['headers'] = markdown_content.count('#')
    analysis['lists'] = markdown_content.count('- ') + markdown_content.count('* ')
    analysis['tables'] = markdown_content.count('|')
    analysis['links'] = markdown_content.count('[')

    # Determine content type
    if analysis['tables'] > 10:
        analysis['type'] = 'structured_data'
    elif analysis['headers'] > 5:
        analysis['type'] = 'document'
    elif analysis['lists'] > 5:
        analysis['type'] = 'list_content'
    else:
        analysis['type'] = 'text'

    return analysis

# Strategy for generating markdown content
def markdown_strategy():
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=1,
        max_size=1000
    ).map(lambda s: s.replace('\r', ''))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(markdown_content=markdown_strategy())
@example(markdown_content="# Header\n- List item\n| Table |")
@example(markdown_content="Simple text content")
@example(markdown_content="| Table |\n|-------|\n| Data  |" * 11)
@example(markdown_content="# Header\n## Subheader\n### Subsubheader" * 3)
@example(markdown_content="- List item\n* Another list item" * 6)
@example(markdown_content="[Link](url)")
def test_analyze_content(markdown_content):
    global stop_collecting
    if stop_collecting:
        return
    
    markdown_content_copy = copy.deepcopy(markdown_content)
    try:
        expected = analyze_content(markdown_content_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"markdown_content": markdown_content},
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