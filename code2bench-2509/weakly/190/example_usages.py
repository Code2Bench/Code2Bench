from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import html
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

# Ground truth function
def sanitize_html(text: str) -> str:
    if not text:
        return ""

    # Convert text to string if it's not already
    text = str(text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Handle comparison operators that break MDX
    text = re.sub(r"<(\d+)", r"less than \1", text)
    text = re.sub(r">(\d+)", r"greater than \1", text)
    text = re.sub(r"<=(\d+)", r"less than or equal to \1", text)
    text = re.sub(r">=(\d+)", r"greater than or equal to \1", text)

    # For standalone < and > characters, replace with safer alternatives
    text = re.sub(r"(?<!\w)<(?!\w)", "&lt;", text)
    text = re.sub(r"(?<!\w)>(?!\w)", "&gt;", text)

    # Replace quote types that can break MDX
    text = text.replace("|", "\\|")
    text = re.sub(r"\{([^}]*\s+[^}]*)\}", r"{\1_\2}", text)

    # Handle JSON examples with quotes
    if "{" in text and "}" in text:
        text = re.sub(
            r"(\{[^{}]*\})", lambda m: m.group(0).replace("'", "`").replace('"', "`"), text
        )
        text = re.sub(r"(\{[^{}]+\})", r"`\1`", text)

    # Handle special characters that might trigger MDX parsing
    text = text.replace("$", "\\$")
    text = text.replace("%", "\\%")

    # Some special HTML entities need to be preserved during unescaping
    text = html.unescape(text.replace("&lt;", "_LT_").replace("&gt;", "_GT_"))
    text = text.replace("_LT_", "&lt;").replace("_GT_", "&gt;")

    # Remove any trailing/leading whitespace
    text = text.strip()

    return text

# Strategy for generating text with potential HTML content
def text_strategy():
    # Generate HTML tags
    html_tags = st.one_of(
        st.just("<div>"),
        st.just("<p>"),
        st.just("<a href='#'>"),
        st.just("<img src='image.png'>"),
        st.just("<script>alert('test');</script>")
    )
    
    # Generate comparison operators
    comparison_ops = st.one_of(
        st.just("<4mb"),
        st.just(">10"),
        st.just("<=100"),
        st.just(">=50")
    )
    
    # Generate special characters
    special_chars = st.one_of(
        st.just("$"),
        st.just("%"),
        st.just("|"),
        st.just("{"),
        st.just("}")
    )
    
    # Generate JSON-like strings
    json_like = st.one_of(
        st.just('{"key": "value"}'),
        st.just('{"key": 123}'),
        st.just('{"key": true}')
    )
    
    # Combine all elements into a text string
    return st.lists(
        st.one_of(
            html_tags,
            comparison_ops,
            special_chars,
            json_like,
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20)
        ),
        min_size=0, max_size=10
    ).map(lambda x: ' '.join(x))

# Hypothesis test configuration
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy())
@example(text="")
@example(text="<div>Hello</div>")
@example(text="<4mb")
@example(text=">10")
@example(text="<=100")
@example(text=">=50")
@example(text="|")
@example(text="{}")
@example(text='{"key": "value"}')
@example(text="<script>alert('test');</script>")
def test_sanitize_html(text: str):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return

    # Deep copy input to avoid modification
    text_copy = copy.deepcopy(text)

    # Call func0 to verify input validity
    try:
        expected = sanitize_html(text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Text with HTML tags"
        elif case_count == 1:
            desc = "Text with comparison operators"
        else:
            desc = "Text with special characters"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Empty string"
        elif case_count == 4:
            desc = "Text with JSON-like content"
        elif case_count == 5:
            desc = "Text with script tag"
        elif case_count == 6:
            desc = "Text with mixed content"
        else:
            desc = "Text with standalone special characters"

    # Store case
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "text": text_copy
        },
        "Expected": expected,
        "Usage": None
    })
    case_count += 1
    if case_count >= MAX_CASES:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {sum(len(cases) for cases in generated_cases.values())} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)