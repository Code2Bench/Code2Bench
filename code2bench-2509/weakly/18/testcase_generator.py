from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from xml.sax.saxutils import escape as xml_escape

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _convert_text_danmaku_to_xml(text_content: str) -> str:
    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<i>',
        '  <chatserver>danmu</chatserver>',
        '  <chatid>0</chatid>',
        '  <mission>0</mission>',
        '  <source>misaka</source>'
    ]
    comments = []
    for line in text_content.strip().split('\n'):
        if '|' not in line:
            continue
        params_str, text = line.split('|', 1)
        params = params_str.split(',')
        if len(params) >= 4:
            # 提取关键参数: 时间, 模式, 颜色
            # 格式: 756.103,1,25,16777215,...
            time_sec = params[0]
            mode     = params[1]
            fontsize = params[2]
            color    = params[3]
            p_attr = f"{time_sec},{mode},{fontsize},{color},[custom_text]"
            escaped_text = xml_escape(text.strip())
            comments.append(f'  <d p="{p_attr}">{escaped_text}</d>')
    xml_parts.insert(5, f'  <maxlimit>{len(comments)}</maxlimit>')
    xml_parts.extend(comments)
    xml_parts.append('</i>')
    return '\n'.join(xml_parts)

# Strategy for generating text_content
def text_content_strategy():
    # Generate valid lines with params and text
    valid_line = st.builds(
        lambda time_sec, mode, fontsize, color, text: f"{time_sec},{mode},{fontsize},{color},...|{text}",
        st.floats(min_value=0.0, max_value=1000.0, allow_nan=False, allow_infinity=False),
        st.integers(min_value=0, max_value=10),
        st.integers(min_value=10, max_value=50),
        st.integers(min_value=0, max_value=16777215),
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=100)
    )
    
    # Generate invalid lines (missing '|' or insufficient params)
    invalid_line = st.one_of(
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=100),
        st.builds(
            lambda params: f"{params}|",
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=100)
        )
    )
    
    # Mix valid and invalid lines
    return st.lists(
        st.one_of(valid_line, invalid_line),
        min_size=0, max_size=10
    ).map(lambda lines: '\n'.join(lines))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text_content=text_content_strategy())
@example(text_content="")
@example(text_content="756.103,1,25,16777215,...|Hello, World!")
@example(text_content="100.0,2,30,123456,...|This is a test")
@example(text_content="invalid line\n756.103,1,25,16777215,...|Valid line")
@example(text_content="756.103,1,25,16777215,...|Line 1\n200.0,3,20,654321,...|Line 2")
def test_convert_text_danmaku_to_xml(text_content: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    text_content_copy = copy.deepcopy(text_content)

    # Call func0 to verify input validity
    try:
        expected = _convert_text_danmaku_to_xml(text_content_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "text_content": text_content_copy
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