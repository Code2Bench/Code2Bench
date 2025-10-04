from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import json
import os
import atexit
import copy
from urllib.parse import quote

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def convert_goofish_link(url: str) -> str:
    """
    将Goofish商品链接转换为只包含商品ID的手机端格式。
    """
    match_first_link = re.search(r'item\?id=(\d+)', url)
    if match_first_link:
        item_id = match_first_link.group(1)
        bfp_json = f'{{"id":{item_id}}}'
        return f"https://pages.goofish.com/sharexy?loadingVisible=false&bft=item&bfs=idlepc.item&spm=a21ybx.item.0.0&bfp={quote(bfp_json)}"
    return url

# Strategy for generating URLs
def url_strategy():
    # Generate URLs with or without the item?id= pattern
    return st.one_of(
        st.builds(
            lambda item_id: f"https://www.goofish.com/item?id={item_id}",
            st.integers(min_value=1, max_value=999999)
        ),
        st.text(
            alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
            min_size=1,
            max_size=100
        ).map(lambda s: f"https://www.goofish.com/{s}")
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(url=url_strategy())
@example(url="https://www.goofish.com/item?id=123456")
@example(url="https://www.goofish.com/item?id=1")
@example(url="https://www.goofish.com/item?id=999999")
@example(url="https://www.goofish.com/randompath")
@example(url="https://www.goofish.com/")
def test_convert_goofish_link(url: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    url_copy = copy.deepcopy(url)

    # Call func0 to verify input validity
    try:
        expected = convert_goofish_link(url_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "url": url_copy
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