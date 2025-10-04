from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
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
def smart_parse(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        json_match = re.search(r'{.*}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        pattern = re.findall(
            r'(\w+)=["\']([^"\']+)["\']|'  # key="value"
            r'(\w+)=([\w.]+)|'  # key=value
            r'(\w+):\s*["\']([^"\']+)["\']|'  # Key: "value"
            r'(\w+):\s*([\w.]+)',  # key: value
            text)

        if pattern:
            parsed_data = {}
            remaining_str = text

            for match in pattern:
                key = next(m for m in [match[0], match[2], match[4], match[6]] if m)
                value = next(m for m in [match[1], match[3], match[5], match[7]] if m)
                parsed_data[key.lower()] = value
                for possible_format in [f'{key}={value}', f'{key}: {value}', f'{key}="{value}"', f'{key}: "{value}"']:
                    remaining_str = remaining_str.replace(possible_format, '')

            remaining_str = remaining_str.strip().strip(',').strip()
            if remaining_str:
                parsed_data['message'] = remaining_str

            return parsed_data

        return {'message': text}

# Strategy for generating text with potential JSON, key-value pairs, or plain text
def text_strategy():
    # Generate JSON-like strings
    json_strategy = st.recursive(
        st.one_of(
            st.none(),
            st.booleans(),
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=10)
        ),
        lambda children: st.lists(children, min_size=1, max_size=3) | st.dictionaries(st.text(min_size=1, max_size=5), children, min_size=1, max_size=3),
        max_leaves=5
    ).map(lambda x: json.dumps(x))

    # Generate key-value pairs
    key_value_strategy = st.lists(
        st.one_of(
            st.tuples(
                st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=5),
                st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
            ).map(lambda x: f'{x[0]}="{x[1]}"'),
            st.tuples(
                st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=5),
                st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
            ).map(lambda x: f'{x[0]}={x[1]}'),
            st.tuples(
                st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=5),
                st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
            ).map(lambda x: f'{x[0]}: "{x[1]}"'),
            st.tuples(
                st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=5),
                st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
            ).map(lambda x: f'{x[0]}: {x[1]}')
        ),
        min_size=0, max_size=5
    ).map(lambda x: ', '.join(x))

    # Generate plain text
    plain_text_strategy = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20)

    # Combine strategies
    return st.one_of(
        json_strategy,
        st.builds(lambda x, y: f"Some text {x} more text {y}", json_strategy, key_value_strategy),
        st.builds(lambda x, y: f"{x} {y}", key_value_strategy, plain_text_strategy),
        plain_text_strategy
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy())
@example(text="")
@example(text="{}")
@example(text='{"key": "value"}')
@example(text='key="value"')
@example(text='key=value')
@example(text='Key: "value"')
@example(text='key: value')
@example(text='Some text key="value" more text')
@example(text='Some text {"key": "value"} more text')
def test_smart_parse(text: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    text_copy = copy.deepcopy(text)

    # Call func0 to verify input validity
    try:
        expected = smart_parse(text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "text": text_copy
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