from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Any, Dict, List
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
def _identify_content_gaps(content_type: Dict[str, Any], writing_style: Dict[str, Any]) -> List[str]:
    gaps = []
    primary_type = content_type.get('primary_type', 'blog')

    if primary_type == 'blog':
        gaps.extend(['Video tutorials', 'Case studies', 'Infographics'])
    elif primary_type == 'video':
        gaps.extend(['Blog posts', 'Whitepapers', 'Webinars'])

    tone = writing_style.get('tone', 'professional')
    if tone == 'professional':
        gaps.append('Personal stories')
    elif tone == 'casual':
        gaps.append('Expert interviews')

    return gaps

# Strategy for generating content_type dictionaries
def content_type_strategy():
    return st.fixed_dictionaries({
        'primary_type': st.one_of([st.just('blog'), st.just('video'), st.text(st.characters(whitelist_categories=('L', 'N')), max_size=10)])
    })

# Strategy for generating writing_style dictionaries
def writing_style_strategy():
    return st.fixed_dictionaries({
        'tone': st.one_of([st.just('professional'), st.just('casual'), st.text(st.characters(whitelist_categories=('L', 'N')), max_size=10)])
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(content_type=content_type_strategy(), writing_style=writing_style_strategy())
@example(content_type={'primary_type': 'blog'}, writing_style={'tone': 'professional'})
@example(content_type={'primary_type': 'video'}, writing_style={'tone': 'casual'})
@example(content_type={'primary_type': 'blog'}, writing_style={'tone': 'casual'})
@example(content_type={'primary_type': 'video'}, writing_style={'tone': 'professional'})
@example(content_type={'primary_type': 'unknown'}, writing_style={'tone': 'unknown'})
def test_identify_content_gaps(content_type: Dict[str, Any], writing_style: Dict[str, Any]):
    global stop_collecting
    if stop_collecting:
        return
    
    content_type_copy = copy.deepcopy(content_type)
    writing_style_copy = copy.deepcopy(writing_style)
    try:
        expected = _identify_content_gaps(content_type_copy, writing_style_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if content_type.get('primary_type') in ['blog', 'video'] or writing_style.get('tone') in ['professional', 'casual']:
        generated_cases.append({
            "Inputs": {"content_type": content_type, "writing_style": writing_style},
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