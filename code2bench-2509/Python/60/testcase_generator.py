from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List
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
def parse_topics_string(topics_string: str) -> List[str]:
    if not topics_string:
        return []

    # 分割并清理话题
    topics = [topic.strip() for topic in topics_string.split(",") if topic.strip()]

    # 移除重复话题（保持顺序）
    unique_topics = []
    seen = set()
    for topic in topics:
        if topic not in seen:
            unique_topics.append(topic)
            seen.add(topic)

    return unique_topics

# Strategy for generating topic strings
def topics_string_strategy():
    return st.lists(
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
        min_size=0, max_size=10
    ).map(lambda topics: ",".join(topics))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(topics_string=topics_string_strategy())
@example(topics_string="")
@example(topics_string="topic1")
@example(topics_string="topic1,topic2")
@example(topics_string="topic1,topic1,topic2")
@example(topics_string="topic1, topic2, topic3")
@example(topics_string="topic1,,topic2")
@example(topics_string=" , topic1, topic2 , ")
def test_parse_topics_string(topics_string: str):
    global stop_collecting
    if stop_collecting:
        return

    topics_string_copy = copy.deepcopy(topics_string)
    try:
        expected = parse_topics_string(topics_string_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    generated_cases.append({
        "Inputs": {"topics_string": topics_string},
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