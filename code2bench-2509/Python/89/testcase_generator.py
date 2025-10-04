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
def longest_common_prefix_between_lists_with_elements(list1, list2):
    """计算两个字符串列表中元素的最长前缀匹配长度
    :param list1:
    :param list2:
    :return:
    """
    max_prefix_length = 0
    max_prefix_elements = ()
    for str1 in list1:
        for str2 in list2:
            prefix_length = 0
            min_len = min(len(str1), len(str2))
            for i in range(min_len):
                if str1[i] == str2[i]:
                    prefix_length += 1
                else:
                    break
            if prefix_length > max_prefix_length:
                max_prefix_length = prefix_length
                max_prefix_elements = (str1, str2)
    return max_prefix_length, max_prefix_elements

# Strategy for generating strings with common prefixes
def string_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20)

# Strategy for generating lists of strings
def list_strategy():
    return st.lists(string_strategy(), min_size=0, max_size=5)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(list1=list_strategy(), list2=list_strategy())
@example(list1=[], list2=[])
@example(list1=["abc"], list2=["abc"])
@example(list1=["abc", "def"], list2=["abc", "ghi"])
@example(list1=["abc", "def"], list2=["abx", "dey"])
@example(list1=["abc", "def"], list2=["xyz", "uvw"])
@example(list1=["abc", "def"], list2=["abcdef", "defghi"])
@example(list1=["abc", "def"], list2=["ab", "de"])
def test_longest_common_prefix_between_lists_with_elements(list1, list2):
    global stop_collecting
    if stop_collecting:
        return
    
    list1_copy = copy.deepcopy(list1)
    list2_copy = copy.deepcopy(list2)
    try:
        expected = longest_common_prefix_between_lists_with_elements(list1_copy, list2_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if len(list1) > 0 and len(list2) > 0:
        generated_cases.append({
            "Inputs": {"list1": list1, "list2": list2},
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