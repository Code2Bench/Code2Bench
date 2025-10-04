from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import List
from xml.sax.saxutils import escape as xml_escape

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _generate_dandan_xml(comments: List[dict]) -> str:
    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<i>',
        '  <chatserver>danmu</chatserver>',
        '  <chatid>0</chatid>',
        '  <mission>0</mission>',
        f'  <maxlimit>{len(comments)}</maxlimit>',
        '  <source>kuyun</source>'
    ]
    for comment in comments:
        content = xml_escape(comment.get('m', ''))
        p_attr_str = comment.get('p', '0,1,25,16777215')
        p_parts = p_attr_str.split(',')

        # 强制修复逻辑：确保 p 属性的格式为 时间,模式,字体大小,颜色,...
        core_parts_end_index = len(p_parts)
        for i, part in enumerate(p_parts):
            if '[' in part and ']' in part:
                core_parts_end_index = i
                break
        core_parts = p_parts[:core_parts_end_index]
        optional_parts = p_parts[core_parts_end_index:]

        # 场景1: 缺少字体大小 (e.g., "1.23,1,16777215")
        if len(core_parts) == 3:
            core_parts.insert(2, '25')
        # 场景2: 字体大小为空或无效 (e.g., "1.23,1,,16777215")
        elif len(core_parts) == 4 and (not core_parts[2] or not core_parts[2].strip().isdigit()):
            core_parts[2] = '25'

        final_p_attr = ','.join(core_parts + optional_parts)
        xml_parts.append(f'  <d p="{final_p_attr}">{content}</d>')
    xml_parts.append('</i>')
    return '\n'.join(xml_parts)

# Strategies for generating inputs
def comment_strategy():
    return st.fixed_dictionaries({
        'm': st.text(min_size=0, max_size=100),
        'p': st.one_of(
            st.just('0,1,25,16777215'),  # Valid default
            st.just('1.23,1,16777215'),  # Missing font size
            st.just('1.23,1,,16777215'),  # Empty font size
            st.just('1.23,1,invalid,16777215'),  # Invalid font size
            st.just('1.23,1,25,16777215,[extra]'),  # With optional parts
            st.just('1.23,1,25,16777215,[extra1],[extra2]')  # Multiple optional parts
        )
    })

def comments_strategy():
    return st.lists(comment_strategy(), min_size=0, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(comments=comments_strategy())
@example(comments=[])
@example(comments=[{'m': 'test', 'p': '0,1,25,16777215'}])
@example(comments=[{'m': 'test', 'p': '1.23,1,16777215'}])
@example(comments=[{'m': 'test', 'p': '1.23,1,,16777215'}])
@example(comments=[{'m': 'test', 'p': '1.23,1,invalid,16777215'}])
@example(comments=[{'m': 'test', 'p': '1.23,1,25,16777215,[extra]'}])
@example(comments=[{'m': 'test', 'p': '1.23,1,25,16777215,[extra1],[extra2]'}])
def test_generate_dandan_xml(comments: List[dict]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    comments_copy = copy.deepcopy(comments)

    # Call func0 to verify input validity
    try:
        expected = _generate_dandan_xml(comments_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "comments": comments_copy
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